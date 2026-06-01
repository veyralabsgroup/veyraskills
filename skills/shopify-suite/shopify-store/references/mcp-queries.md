# MCP Queries — shopify-store Reference

Ready-to-use GraphQL queries for Mode A (shopify-mcp connected).
All queries use the Admin API via the shopify-mcp `graphql` tool.

---

## Products

### Get all products with SEO fields
```graphql
query GetProducts($cursor: String) {
  products(first: 250, after: $cursor) {
    pageInfo { hasNextPage endCursor }
    nodes {
      id
      title
      handle
      status
      descriptionHtml
      seo { title description }
      images(first: 5) {
        nodes { id url altText }
      }
      variants(first: 100) {
        nodes { id title sku price availableForSale }
      }
    }
  }
}
```

### Products missing SEO data
```graphql
query ProductsSEOAudit {
  products(first: 250, query: "status:active") {
    nodes {
      id
      title
      seo { title description }
      images(first: 1) {
        nodes { altText }
      }
    }
  }
}
```

---

## Collections

### Full collection structure
```graphql
query GetCollections {
  collections(first: 100) {
    nodes {
      id
      title
      handle
      sortOrder
      productsCount { count }
      seo { title description }
      image { altText url }
      ruleSet {
        rules { column relation condition }
      }
    }
  }
}
```

---

## Navigation (Menus)

```graphql
query GetMenus {
  menus(first: 10) {
    nodes {
      id
      title
      handle
      items {
        id
        title
        url
        type
        items {
          id
          title
          url
          type
        }
      }
    }
  }
}
```

---

## Orders (last 90 days)

```graphql
query GetOrders {
  orders(first: 250, query: "created_at:>2025-01-01") {
    nodes {
      id
      totalPriceSet { shopMoney { amount currencyCode } }
      lineItems(first: 10) {
        nodes { quantity title sku }
      }
      customer { id email numberOfOrders }
      createdAt
      cancelledAt
      financialStatus
      fulfillmentStatus
    }
  }
}
```

---

## Metafields

### Get product metafields
```graphql
query GetProductMetafields($id: ID!) {
  product(id: $id) {
    metafields(first: 20) {
      nodes {
        namespace
        key
        value
        type
      }
    }
  }
}
```

### Set SEO metafield
```graphql
mutation SetMetafield($metafields: [MetafieldsSetInput!]!) {
  metafieldsSet(metafields: $metafields) {
    metafields { key value }
    userErrors { field message }
  }
}
```
Variables:
```json
{
  "metafields": [{
    "ownerId": "gid://shopify/Product/123",
    "namespace": "seo",
    "key": "description",
    "value": "Your SEO description here",
    "type": "single_line_text_field"
  }]
}
```

---

## Installed Apps (via App Installations)

```graphql
query GetInstalledApps {
  appInstallations(first: 50) {
    nodes {
      app {
        title
        handle
        developerName
        pricingSummary
      }
      launchUrl
      uninstallUrl
    }
  }
}
```

---

## Shopify Analytics (basic)

```graphql
query GetShopInfo {
  shop {
    name
    myshopifyDomain
    plan { displayName partnerDevelopment }
    currencyCode
    timezoneAbbreviation
    ianaTimezone
  }
}
```

For revenue/conversion analytics, use the Reports API:
```graphql
query GetReports {
  reports(first: 10, query: "report_type:custom") {
    nodes {
      id
      name
      category
      shopifyQL
    }
  }
}
```
