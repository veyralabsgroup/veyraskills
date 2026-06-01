Activate the shopify-store skill. Task: $ARGUMENTS

Start with mode detection: attempt list_products via shopify-mcp. If MCP responds, run the full Mode A audit pipeline. If not available, switch to Mode B (public extraction via Scrapling). Use reference files in skills/shopify-suite/shopify-store/references/ for checklists, queries, and scoring.
