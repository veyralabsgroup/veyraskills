"""
ad_library.py

Scrapes Meta Ad Library (public, no login required) to extract
active ads for a given brand or search term.
"""

import re
import json
from urllib.parse import quote

try:
    from scrapling import StealthyFetcher, Fetcher
    HAS_SCRAPLING = True
except ImportError:
    HAS_SCRAPLING = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


AD_LIBRARY_URL = "https://www.facebook.com/ads/library/"


def build_library_url(search_term: str, country: str = "ES", active_only: bool = True) -> str:
    """Build a Meta Ad Library search URL."""
    params = {
        "active_status": "active" if active_only else "all",
        "ad_type": "all",
        "country": country,
        "search_terms": search_term,
        "media_type": "all",
    }
    query = "&".join(f"{k}={quote(str(v))}" for k, v in params.items())
    return f"{AD_LIBRARY_URL}?{query}"


def scrape_meta_ads(brand_name: str, country: str = "ES", limit: int = 20) -> list[dict]:
    """
    Attempt to scrape Meta Ad Library for a brand.

    Note: Meta Ad Library is a JavaScript-heavy SPA. StealthyFetcher
    with headless=True and network_idle=True is needed to get rendered
    content. Without Scrapling with stealth mode, this returns empty.

    Falls back to returning the URL and instructions for manual review
    if scraping fails.

    Args:
        brand_name: Brand or company name to search
        country: ISO country code (ES, US, GB, etc.)
        limit: Max ads to return

    Returns:
        List of ad dicts, or list with single "manual_review" entry
    """
    url = build_library_url(brand_name, country)

    if HAS_SCRAPLING:
        try:
            page = StealthyFetcher().fetch(
                url,
                headless=True,
                network_idle=True,
                wait=3000,
            )
            ads = _parse_library_page(page.html_content, brand_name)
            if ads:
                return ads[:limit]
        except Exception:
            pass

    # Fallback: return URL + instructions for manual copy-paste
    return [{
        "type": "manual_review",
        "url": url,
        "instructions": (
            f"Meta Ad Library requires JavaScript rendering. "
            f"Open this URL in a browser and paste the ad copy here for analysis: {url}"
        ),
        "brand": brand_name,
    }]


def _parse_library_page(html: str, brand_name: str) -> list[dict]:
    """Extract ad data from rendered Meta Ad Library HTML."""
    ads = []

    # Meta Ad Library renders as React - look for data in script tags or rendered text
    # The library renders ad cards with specific aria-labels and data attributes

    # Try to find ad cards (rendered HTML pattern)
    ad_card_pattern = re.compile(
        r'<div[^>]*data-testid=["\']ad-card["\'][^>]*>(.*?)</div>\s*</div>\s*</div>',
        re.DOTALL | re.IGNORECASE
    )
    cards = ad_card_pattern.findall(html)

    for card in cards:
        ad = _extract_ad_from_card(card)
        if ad:
            ads.append(ad)

    # Fallback: extract any substantial text blocks that look like ad copy
    if not ads:
        ads = _extract_ad_text_blocks(html, brand_name)

    return ads


def _extract_ad_from_card(card_html: str) -> dict | None:
    """Extract ad data from a single ad card HTML block."""
    clean = lambda h: re.sub(r'<[^>]+>', ' ', h).strip()
    clean_ws = lambda t: re.sub(r'\s+', ' ', t).strip()

    # Ad body text (primary copy)
    body_match = re.search(
        r'<div[^>]*class=["\'][^"\']*_body[^"\']*["\'][^>]*>(.*?)</div>',
        card_html, re.IGNORECASE | re.DOTALL
    )
    body = clean_ws(clean(body_match.group(1))) if body_match else None

    # CTA button
    cta_match = re.search(
        r'<a[^>]*role=["\']button["\'][^>]*>(.*?)</a>',
        card_html, re.IGNORECASE | re.DOTALL
    )
    cta = clean_ws(clean(cta_match.group(1))) if cta_match else None

    # Start date
    date_match = re.search(
        r'(Started running|Began running)[^<]*<[^>]*>([^<]+)</[^>]*>',
        card_html, re.IGNORECASE
    )
    start_date = clean_ws(date_match.group(2)) if date_match else None

    if not body or len(body) < 10:
        return None

    return {
        "body": body[:500],
        "cta": cta,
        "start_date": start_date,
        "media_type": "image" if re.search(r'<img', card_html, re.IGNORECASE) else
                      "video" if re.search(r'<video', card_html, re.IGNORECASE) else "unknown",
    }


def _extract_ad_text_blocks(html: str, brand_name: str) -> list[dict]:
    """Fallback: extract text blocks from rendered page that look like ad copy."""
    clean_html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    clean_html = re.sub(r'<style[^>]*>.*?</style>', '', clean_html, flags=re.DOTALL)

    text = re.sub(r'<[^>]+>', ' ', clean_html)
    text = re.sub(r'\s+', ' ', text).strip()

    # Find sentences that look like ad copy (longer blocks, not nav/UI text)
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if len(s.strip()) > 40]

    # Deduplicate
    seen = set()
    unique = []
    for s in sentences:
        if s not in seen:
            seen.add(s)
            unique.append(s)

    if not unique:
        return []

    # Group into rough "ads" (every 3-4 sentences)
    ads = []
    for i in range(0, min(len(unique), 30), 4):
        body = " ".join(unique[i:i+4])
        if len(body) > 50:
            ads.append({
                "body": body[:500],
                "cta": None,
                "start_date": None,
                "media_type": "unknown",
                "note": "Extracted from page text - manual verification recommended",
            })

    return ads


def format_ads_for_analysis(ads: list[dict], brand_name: str) -> str:
    """Format scraped ads as readable text for Claude to analyze."""
    if not ads:
        return f"No ads found for {brand_name}."

    if ads[0].get("type") == "manual_review":
        return (
            f"Meta Ad Library requires a browser to render.\n"
            f"Open this URL and paste the ad copy for analysis:\n"
            f"{ads[0]['url']}\n\n"
            f"Or describe the ads you see and the analysis will continue from there."
        )

    lines = [f"## Ads found for: {brand_name}", f"Total: {len(ads)} ads", ""]

    for i, ad in enumerate(ads, 1):
        lines.append(f"### Ad {i}")
        if ad.get("start_date"):
            lines.append(f"Running since: {ad['start_date']}")
        lines.append(f"Media type: {ad.get('media_type', 'unknown')}")
        if ad.get("cta"):
            lines.append(f"CTA button: {ad['cta']}")
        lines.append(f"Copy:\n{ad['body']}")
        if ad.get("note"):
            lines.append(f"Note: {ad['note']}")
        lines.append("")

    return "\n".join(lines)
