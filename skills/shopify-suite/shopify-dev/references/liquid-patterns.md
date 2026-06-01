# Liquid Patterns — shopify-dev Reference

Common Liquid patterns, filters, and gotchas for Shopify theme development.

---

## Objects

### Global objects (available everywhere)

| Object | What it is |
|--------|-----------|
| `shop` | Store settings, name, currency, policies |
| `cart` | Current cart (items, total, count) |
| `customer` | Logged-in customer (nil if guest) |
| `request` | Current request info (page_type, host) |
| `settings` | Theme settings from settings_data.json |
| `content_for_header` | Required in `<head>` — Shopify scripts injection |
| `content_for_layout` | Required in layout — renders template content |

### Template-specific objects

| Template | Objects available |
|----------|------------------|
| product | `product`, `current_variant` |
| collection | `collection`, `current_tags`, `current_vendor` |
| article | `article`, `blog` |
| page | `page` |
| cart | `cart` |
| order (customer) | `order` |

---

## Filters

### String filters

```liquid
{{ product.title | upcase }}
{{ product.title | downcase }}
{{ product.title | capitalize }}
{{ product.description | strip_html }}
{{ product.description | truncate: 150 }}
{{ product.description | truncate_words: 30 }}
{{ "  padded  " | strip }}
{{ product.handle | replace: "-", " " }}
```

### Number and money filters

```liquid
{{ product.price | money }}                 → "€29,99"
{{ product.price | money_without_currency }} → "29,99"
{{ product.price | money_with_currency }}    → "29,99 EUR"
{{ product.price | divided_by: 100.0 }}      → raw float
{{ 1.5 | round }}                            → 2
{{ 1.5 | floor }}                            → 1
{{ 1.5 | ceil }}                             → 2
```

Note: Shopify stores prices in cents. `product.price` = 2999 = €29.99. Always use `| money` for display.

### URL filters

```liquid
{{ product.featured_image | img_url: '800x' }}
{{ product.featured_image | img_url: '800x600', crop: 'center' }}
{{ product.featured_image | image_url: width: 800 }}  ← new Liquid syntax
{{ 'theme.css' | asset_url }}
{{ 'custom.js' | asset_url | script_tag }}
{{ product.url | within: collection }}  ← collection-scoped URL
```

### Array filters

```liquid
{{ product.tags | join: ", " }}
{{ collection.products | size }}
{{ product.images | first }}
{{ product.images | last }}
{{ product.variants | map: "title" | join: ", " }}
{{ collection.products | where: "available", true }}
{{ collection.products | sort: "price" }}
{{ collection.products | reverse }}
```

### Date filters

```liquid
{{ article.created_at | date: "%B %d, %Y" }}   → "January 15, 2025"
{{ article.created_at | date: "%Y-%m-%d" }}     → "2025-01-15"
{{ "now" | date: "%s" | plus: 0 }}              → Unix timestamp
```

---

## Tags

### Conditionals

```liquid
{% if customer %}
  Hello, {{ customer.first_name }}
{% elsif request.page_type == "product" %}
  Product page
{% else %}
  Guest
{% endif %}

{% unless product.available %}
  Sold out
{% endunless %}

{% case product.type %}
  {% when "Shirt" %}
    ...
  {% when "Pants", "Trousers" %}
    ...
  {% else %}
    ...
{% endcase %}
```

### Loops

```liquid
{% for product in collection.products %}
  {{ product.title }}
{% endfor %}

{% for i in (1..5) %}
  {{ i }}
{% endfor %}

{% for tag in product.tags limit: 3 offset: 1 %}
  {{ tag }}
{% endfor %}

{% for product in collection.products %}
  {% if forloop.first %}First{% endif %}
  {% if forloop.last %}Last{% endif %}
  {{ forloop.index }}  ← 1-based
  {{ forloop.index0 }} ← 0-based
{% endfor %}
```

### Content inclusion

```liquid
{% render 'card-product', product: product %}
{% render 'icon', name: 'cart' %}

{% section 'header' %}

{% include 'snippet' %}   ← deprecated, use render
```

`render` is sandboxed — parent variables not accessible unless passed explicitly.

### Pagination

```liquid
{% paginate collection.products by 24 %}
  {% for product in collection.products %}
    ...
  {% endfor %}

  {{ paginate | default_pagination }}
{% endpaginate %}
```

Custom pagination:
```liquid
{% paginate collection.products by 24 %}
  {% if paginate.previous %}
    <a href="{{ paginate.previous.url }}">Previous</a>
  {% endif %}

  {% for part in paginate.parts %}
    {% if part.is_link %}
      <a href="{{ part.url }}">{{ part.title }}</a>
    {% else %}
      <span>{{ part.title }}</span>
    {% endif %}
  {% endfor %}

  {% if paginate.next %}
    <a href="{{ paginate.next.url }}">Next</a>
  {% endif %}
{% endpaginate %}
```

---

## Gotchas

### Blank vs nil vs false

```liquid
{% if product.metafields.custom.badge %}  ← true if value exists AND not empty
{% if product.metafields.custom.badge != blank %}  ← safer
{% if product.metafields.custom.badge == nil %}  ← only nil check
```

### Price display edge case

Always check for variant availability before displaying compare_at_price:
```liquid
{% if product.compare_at_price_max > product.price_min %}
  <s>{{ product.compare_at_price_max | money }}</s>
{% endif %}
```

### render scope

```liquid
{% render 'card', product: product %}
```

Inside `card.liquid`, only `product` is accessible — not `collection`, `shop`, `settings`, etc. Pass each required variable explicitly.

`settings` is an exception — globally accessible in rendered snippets.

### Forloop and break

Liquid has no `break` in for loops. Use `limit` to cap iterations, or build logic with conditionals and `continue`:

```liquid
{% for product in collection.products limit: 10 %}
  {% if product.available == false %}{% continue %}{% endif %}
  {{ product.title }}
{% endfor %}
```

### Section settings output in JS

```liquid
<script>
  const threshold = {{ section.settings.countdown_hours | times: 3600 }};
  const color = {{ section.settings.text_color | json }};
</script>
```

`| json` escapes strings correctly. Never interpolate raw strings into JS.

### Metafield access

```liquid
{{ product.metafields.custom.size_guide }}
{{ product.metafields["reviews"]["rating"] }}

{% assign guide = product.metafields.custom.size_guide %}
{% if guide %}
  {{ guide.value }}
{% endif %}
```

Metafield types in Liquid: `value` for single values, `.value.items` for list types.

### Translation (i18n)

```liquid
{{ 'products.product.add_to_cart' | t }}
{{ 'cart.items_count' | t: count: cart.item_count }}
```

Keys defined in `locales/en.default.json`. Always use `| t` for user-facing strings.

---

## Liquid Anti-Patterns

**Using `include` instead of `render`:** `include` shares scope (can read parent variables), which creates hidden coupling. Use `render`.

**Doing math with price in Liquid:** `product.price | times: 1.21` for VAT display — Liquid math on integers (cents) then format. Don't format first, then calculate.

**Nested loops for lookups:** O(n²) in Liquid. Build a hash map instead:
```liquid
{% assign variant_map = "" %}
{% for variant in product.variants %}
  {% assign variant_map = variant_map | append: variant.id | append: ":" | append: variant.title | append: "," %}
{% endfor %}
```
Or pass data to JS and handle there.

**Long conditional chains in Liquid:** Move logic to a snippet with `render`, or handle in JS.
