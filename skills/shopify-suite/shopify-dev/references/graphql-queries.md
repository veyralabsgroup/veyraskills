# GraphQL Queries — shopify-dev Reference

Ready-to-use queries for Storefront API and Admin API.
Check API version in your app config before using — Shopify deprecates quarterly.

---

## Storefront API

Use for: public-facing data, headless storefronts, Hydrogen.
Auth: public Storefront API token (safe for frontend).

### Products

```graphql
query GetProduct($handle: String!) {
  product(handle: $handle) {
    id
    title
    handle
    description
    descriptionHtml
    vendor
    productType
    tags
    priceRange {
      minVariantPrice { amount currencyCode }
      maxVariantPrice { amount currencyCode }
    }
    compareAtPriceRange {
      minVariantPrice { amount currencyCode }
    }
    featuredImage { url altText width height }
    images(first: 20) {
      nodes { id url altText width height }
    }
    variants(first: 100) {
      nodes {
        id
        title
        availableForSale
        quantityAvailable
        price { amount currencyCode }
        compareAtPrice { amount currencyCode }
        selectedOptions { name value }
        image { url altText }
      }
    }
    seo { title description }
  }
}
```

### Collections

```graphql
query GetCollection($handle: String!, $cursor: String) {
  collection(handle: $handle) {
    id
    title
    handle
    description
    image { url altText }
    products(first: 24, after: $cursor, sortKey: BEST_SELLING) {
      pageInfo { hasNextPage endCursor }
      nodes {
        id
        title
        handle
        featuredImage { url altText }
        priceRange {
          minVariantPrice { amount currencyCode }
        }
        availableForSale
      }
    }
  }
}
```

### Cart

```graphql
mutation CartCreate($lines: [CartLineInput!], $buyerIdentity: CartBuyerIdentityInput) {
  cartCreate(input: { lines: $lines, buyerIdentity: $buyerIdentity }) {
    cart {
      id
      checkoutUrl
      totalQuantity
      cost {
        totalAmount { amount currencyCode }
        subtotalAmount { amount currencyCode }
      }
      lines(first: 100) {
        nodes {
          id
          quantity
          merchandise {
            ... on ProductVariant {
              id
              title
              price { amount currencyCode }
              product { title handle featuredImage { url } }
            }
          }
        }
      }
    }
    userErrors { field message }
  }
}
```

```graphql
mutation CartLinesAdd($cartId: ID!, $lines: [CartLineInput!]!) {
  cartLinesAdd(cartId: $cartId, lines: $lines) {
    cart { id totalQuantity cost { totalAmount { amount currencyCode } } }
    userErrors { field message }
  }
}
```

```graphql
mutation CartLinesUpdate($cartId: ID!, $lines: [CartLineUpdateInput!]!) {
  cartLinesUpdate(cartId: $cartId, lines: $lines) {
    cart { id totalQuantity }
    userErrors { field message }
  }
}
```

### Search (Predictive)

```graphql
query PredictiveSearch($query: String!) {
  predictiveSearch(query: $query, limit: 5) {
    products {
      id
      title
      handle
      featuredImage { url altText }
      priceRange { minVariantPrice { amount currencyCode } }
    }
    collections { id title handle }
    pages { id title handle }
  }
}
```

### Customer

```graphql
query GetCustomer($customerAccessToken: String!) {
  customer(customerAccessToken: $customerAccessToken) {
    id
    firstName
    lastName
    email
    orders(first: 10, sortKey: PROCESSED_AT, reverse: true) {
      nodes {
        id
        orderNumber
        processedAt
        financialStatus
        fulfillmentStatus
        totalPrice { amount currencyCode }
        lineItems(first: 5) {
          nodes {
            title
            quantity
            variant { image { url } price { amount currencyCode } }
          }
        }
      }
    }
  }
}
```

---

## Admin API

Use for: app backends, webhooks, bulk operations.
Auth: Admin API access token (server-side only, never expose to client).

### Product Create

```graphql
mutation ProductCreate($input: ProductInput!) {
  productCreate(input: $input) {
    product {
      id
      title
      handle
      status
    }
    userErrors { field message }
  }
}
```

Variables:
```json
{
  "input": {
    "title": "Product Title",
    "descriptionHtml": "<p>Description</p>",
    "vendor": "Brand Name",
    "productType": "Category",
    "status": "DRAFT",
    "variants": [
      {
        "price": "29.99",
        "sku": "SKU-001",
        "inventoryQuantities": [{
          "availableQuantity": 100,
          "locationId": "gid://shopify/Location/YOUR_LOCATION_ID"
        }]
      }
    ]
  }
}
```

### Metafields Set (bulk)

```graphql
mutation MetafieldsSet($metafields: [MetafieldsSetInput!]!) {
  metafieldsSet(metafields: $metafields) {
    metafields { key value namespace }
    userErrors { field message }
  }
}
```

### Bulk Operations (for large datasets)

```graphql
mutation BulkOperationRunQuery($query: String!) {
  bulkOperationRunQuery(query: $query) {
    bulkOperation { id status }
    userErrors { field message }
  }
}
```

Poll for completion:
```graphql
query BulkOperationStatus {
  currentBulkOperation {
    id
    status
    errorCode
    objectCount
    fileSize
    url
    partialDataUrl
  }
}
```

---

## Common Patterns

### Cursor-based pagination

```typescript
async function fetchAllProducts(storefront) {
  let allProducts = [];
  let cursor = null;
  let hasNextPage = true;

  while (hasNextPage) {
    const { products } = await storefront.query(PRODUCTS_QUERY, {
      variables: { cursor },
    });
    allProducts.push(...products.nodes);
    hasNextPage = products.pageInfo.hasNextPage;
    cursor = products.pageInfo.endCursor;
  }

  return allProducts;
}
```

### Error handling for mutations

```typescript
const { data } = await admin.graphql(MUTATION, { variables });

if (data.productCreate.userErrors.length > 0) {
  throw new Error(
    data.productCreate.userErrors.map(e => `${e.field}: ${e.message}`).join(', ')
  );
}
```
