# App Architecture — shopify-dev Reference

Decisions and patterns for Shopify app structure, auth, billing, and production readiness.

---

## Tech Stack (2025+)

Shopify's recommended stack for new apps:

| Layer | Tech |
|-------|------|
| Framework | Remix (replaces Express) |
| UI | Polaris + App Bridge |
| ORM | Prisma (SQLite dev, Postgres prod) |
| Auth | OAuth client credentials (Dev Dashboard) |
| Hosting | Fly.io, Railway, Vercel, Render |
| Extensions | Checkout UI, Admin UI, Web Pixel |

---

## Project Structure

```
my-shopify-app/
├── app/
│   ├── routes/
│   │   ├── app._index.tsx       ← main embedded page
│   │   ├── app.products.tsx     ← products feature page
│   │   ├── app.settings.tsx     ← settings
│   │   ├── webhooks.tsx         ← webhook receiver
│   │   └── auth.$.tsx           ← Shopify OAuth flow (auto-generated)
│   ├── shopify.server.ts        ← auth config, API client
│   ├── db.server.ts             ← Prisma client singleton
│   └── root.tsx                 ← App wrapper with AppProvider
├── extensions/
│   └── checkout-ui/             ← checkout extension (if any)
├── prisma/
│   ├── schema.prisma
│   └── migrations/
├── .env                         ← never commit
├── shopify.app.toml             ← app config for CLI
└── remix.config.js
```

---

## Authentication

### How it works (OAuth client credentials, 2025+)

1. Merchant installs app from App Store / Dev Dashboard
2. Shopify redirects to your `/auth` route with shop domain
3. Your app redirects to Shopify OAuth screen
4. Merchant approves — Shopify redirects back with authorization code
5. Your app exchanges code for session token
6. Session stored in DB (per-shop)

All this is handled by `@shopify/shopify-app-remix` — you don't implement it manually.

### shopify.server.ts pattern

```typescript
import "@shopify/shopify-app-remix/adapters/node";
import {
  AppDistribution,
  shopifyApp,
  LATEST_API_VERSION,
} from "@shopify/shopify-app-remix/server";
import { PrismaSessionStorage } from "@shopify/shopify-app-session-storage-prisma";
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

const shopify = shopifyApp({
  apiKey: process.env.SHOPIFY_API_KEY,
  apiSecretKey: process.env.SHOPIFY_API_SECRET || "",
  apiVersion: LATEST_API_VERSION,
  scopes: process.env.SCOPES?.split(","),
  appUrl: process.env.SHOPIFY_APP_URL || "",
  authPathPrefix: "/auth",
  sessionStorage: new PrismaSessionStorage(prisma),
  distribution: AppDistribution.AppStore,
});

export default shopify;
export const apiVersion = LATEST_API_VERSION;
export const addDocumentResponseHeaders = shopify.addDocumentResponseHeaders;
export const authenticate = shopify.authenticate;
export const unauthenticated = shopify.unauthenticated;
export const login = shopify.login;
export const registerWebhooks = shopify.registerWebhooks;
export const sessionStorage = shopify.sessionStorage;
```

### Using auth in routes

```typescript
// Embedded page (inside Shopify admin)
export const loader = async ({ request }) => {
  const { admin, session } = await authenticate.admin(request);
  // admin.graphql() for API calls
  // session.shop = "store-name.myshopify.com"
};

// Webhook (not embedded — different auth method)
export const action = async ({ request }) => {
  const { shop, topic, payload } = await authenticate.webhook(request);
};

// Public (no auth — for storefront-facing APIs)
export const loader = async ({ request }) => {
  const { storefront } = await unauthenticated.storefront("store.myshopify.com");
};
```

---

## Database

### Prisma schema for session storage

```prisma
model Session {
  id          String    @id
  shop        String
  state       String
  isOnline    Boolean   @default(false)
  scope       String?
  expires     DateTime?
  accessToken String
  userId      BigInt?
  firstName   String?
  lastName    String?
  email       String?
  accountOwner Boolean  @default(false)
  locale      String?
  collaborator Boolean? @default(false)
  emailVerified Boolean? @default(false)
}
```

### App data example (products table)

```prisma
model ProductSetting {
  id          String  @id @default(uuid())
  shop        String
  productId   String
  badgeText   String?
  isHidden    Boolean @default(false)
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt

  @@unique([shop, productId])
}
```

### Dev vs prod DB

- Dev: SQLite (zero setup, file-based)
- Prod: Postgres (Railway, Supabase, PlanetScale)

Switch in `prisma/schema.prisma`:
```prisma
datasource db {
  provider = "postgresql"  // "sqlite" for dev
  url      = env("DATABASE_URL")
}
```

---

## Billing

Shopify billing API requires app to charge via Shopify (mandatory for App Store apps).

### Create a subscription

```typescript
export const loader = async ({ request }) => {
  const { billing } = await authenticate.admin(request);

  const { hasActivePayment, appSubscriptions } = await billing.check({
    plans: ["Basic Plan"],
    isTest: process.env.NODE_ENV !== "production",
  });

  if (!hasActivePayment) {
    await billing.request({
      plan: "Basic Plan",
      isTest: process.env.NODE_ENV !== "production",
      returnUrl: `${process.env.SHOPIFY_APP_URL}/app`,
    });
  }
};
```

### Define plans in shopify.server.ts

```typescript
const shopify = shopifyApp({
  // ...existing config...
  billing: {
    "Basic Plan": {
      amount: 9.99,
      currencyCode: "USD",
      interval: BillingInterval.Monthly,
    },
    "Pro Plan": {
      amount: 29.99,
      currencyCode: "USD",
      interval: BillingInterval.Monthly,
    },
  },
});
```

### Check subscription status in any route

```typescript
const { billing } = await authenticate.admin(request);
const { hasActivePayment } = await billing.check({ plans: ["Pro Plan"] });

if (!hasActivePayment) {
  return redirect("/app/upgrade");
}
```

---

## Webhooks

### Register in shopify.app.toml

```toml
[[webhooks.subscriptions]]
topics = ["products/update", "products/delete"]
uri = "/webhooks"

[[webhooks.subscriptions]]
topics = ["app/uninstalled"]
uri = "/webhooks"
```

Or register programmatically:

```typescript
// root.tsx or entry point
import { registerWebhooks } from "./shopify.server";

export const action = async ({ request }) => {
  const { topic, shop } = await authenticate.webhook(request);
  await registerWebhooks({ session });
};
```

### Webhook handler

```typescript
// app/routes/webhooks.tsx
export const action = async ({ request }) => {
  const { topic, shop, session, admin, payload } =
    await authenticate.webhook(request);

  if (!admin && topic !== "APP_UNINSTALLED") {
    throw new Response();
  }

  switch (topic) {
    case "APP_UNINSTALLED":
      if (session) {
        await db.session.deleteMany({ where: { shop } });
      }
      break;

    case "PRODUCTS_UPDATE":
      await syncProduct(shop, payload);
      break;

    default:
      throw new Response("Unhandled webhook topic", { status: 404 });
  }

  return new Response();
};
```

---

## Production Checklist

Before submitting to App Store:

- [ ] `LATEST_API_VERSION` set and updated quarterly
- [ ] Webhooks registered for `APP_UNINSTALLED`, `CUSTOMERS_DATA_REQUEST`, `CUSTOMERS_REDACT`, `SHOP_REDACT` (GDPR — mandatory)
- [ ] Billing implemented if charging merchants
- [ ] Session storage uses Postgres (not SQLite)
- [ ] All Admin API calls handle `userErrors`
- [ ] Rate limit handling: retry on 429 with exponential backoff
- [ ] App URL set in `.env` and `shopify.app.toml`
- [ ] Polaris `AppProvider` wraps entire app with i18n translations
- [ ] No API keys or secrets in client-side code
- [ ] App passes Shopify's built-in review checklist (run `shopify app build` and check output)

---

## Rate Limits

Shopify Admin GraphQL: 1000 points/second per store.

Query cost: each field costs 1 point; connections multiply by requested count.
`products(first: 250)` = ~250 points. `products.variants.metafields` = ~250 × 250.

```typescript
// Check cost in response headers
const response = await admin.graphql(QUERY);
const headers = response.headers;
// X-Shopify-Shop-Api-Call-Limit: used/max
```

For bulk operations (catalog exports, large migrations), use `bulkOperationRunQuery` — no rate limits.
