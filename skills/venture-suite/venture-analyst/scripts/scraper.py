"""
Scrapling wrapper for venture-analyst.
Handles competitor pages, pricing pages, and review sites.
Falls back gracefully on blocked sites.
"""
import re
from typing import Optional


def scrape_competitor(url: str) -> Optional[dict]:
    """
    Scrape a competitor website.
    Tries basic Fetcher first, falls back to StealthyFetcher for Cloudflare.
    """
    try:
        from scrapling import Fetcher
        page = Fetcher(auto_match=False).get(url, timeout=15, stealthy_headers=True)
        if _is_empty(page):
            return _scrape_stealthy(url)
        return _parse_competitor_page(url, page)
    except Exception:
        return _scrape_stealthy(url)


def _scrape_stealthy(url: str) -> Optional[dict]:
    """StealthyFetcher for JS-rendered or Cloudflare-protected sites."""
    try:
        from scrapling import StealthyFetcher
        page = StealthyFetcher(auto_match=False).get(url, timeout=20, network_idle=True)
        if _is_empty(page):
            return None
        return _parse_competitor_page(url, page)
    except Exception:
        return None


def _is_empty(page) -> bool:
    if page is None:
        return True
    try:
        return len(page.get_all_text()) < 100
    except Exception:
        return True


def _parse_competitor_page(url: str, page) -> dict:
    return {
        "url": url,
        "title":       _get_title(page),
        "tagline":     _get_tagline(page),
        "description": _get_meta_description(page),
        "pricing":     _get_pricing(page),
        "features":    _get_features(page),
        "tech_stack":  _get_tech_signals(page),
    }


def _get_title(page) -> str:
    try:
        return page.css("title").first.text.strip()[:120]
    except Exception:
        return ""


def _get_tagline(page) -> str:
    """Extract the main hero headline."""
    selectors = ["h1", "[class*='hero'] h1", "header h1", "[class*='headline']", "[class*='tagline']"]
    for sel in selectors:
        try:
            el = page.css(sel).first
            if el:
                text = el.text.strip()
                if 5 < len(text) < 200:
                    return text
        except Exception:
            pass
    return ""


def _get_meta_description(page) -> str:
    try:
        el = page.css('meta[name="description"]').first
        return (el.attrs.get("content") or "")[:300]
    except Exception:
        return ""


def _get_pricing(page) -> dict:
    """Extract pricing signals from page text."""
    try:
        text = page.get_all_text()
    except Exception:
        return {}

    prices = re.findall(
        r'[\$€£]\s*(\d+(?:[.,]\d+)?)\s*(?:/\s*(?:mo|month|year|yr|user|seat))?',
        text,
        re.IGNORECASE,
    )
    model_keywords = [
        "free", "freemium", "free trial", "per user", "per month", "per year",
        "enterprise", "custom pricing", "contact us", "flat rate",
    ]
    detected_model = [kw for kw in model_keywords if kw.lower() in text.lower()]

    return {
        "prices": prices[:6],
        "model_signals": detected_model[:4],
        "has_free_tier": any(kw in ["free", "freemium", "free trial"] for kw in detected_model),
    }


def _get_features(page) -> list[str]:
    """Extract feature descriptions from bullets and feature sections."""
    features = []
    try:
        for el in page.css("li, [class*='feature'], [class*='benefit']")[:30]:
            try:
                text = el.text.strip()
                if 10 < len(text) < 150 and not text.startswith(("©", "Terms", "Privacy")):
                    features.append(text)
            except Exception:
                pass
    except Exception:
        pass
    return features[:12]


def _get_tech_signals(page) -> list[str]:
    """Detect tech stack from script URLs and meta tags."""
    signals = []
    TECH_PATTERNS = {
        "React":        r"react",
        "Vue":          r"vue\.js|vuejs",
        "Angular":      r"angular",
        "Next.js":      r"_next/",
        "Stripe":       r"js\.stripe\.com",
        "Intercom":     r"intercom",
        "Segment":      r"segment\.com",
        "HubSpot":      r"hubspot",
        "Webflow":      r"webflow",
        "Shopify":      r"shopify",
    }
    try:
        html = str(page)
        for tech, pattern in TECH_PATTERNS.items():
            if re.search(pattern, html, re.IGNORECASE):
                signals.append(tech)
    except Exception:
        pass
    return signals


def scrape_g2_reviews(product_url: str, max_pages: int = 2) -> list[dict]:
    """
    Scrape G2 reviews. Requires StealthyFetcher + Playwright.
    G2 is Cloudflare-protected — basic Fetcher will fail.
    """
    reviews = []
    try:
        from scrapling import StealthyFetcher
        for page_num in range(1, max_pages + 1):
            url = f"{product_url}?page={page_num}"
            page = StealthyFetcher(auto_match=False).get(url, timeout=25, network_idle=True)
            if _is_empty(page):
                break
            for review in page.css("[itemprop='review'], .paper--white, [class*='review-card']"):
                try:
                    reviews.append({
                        "source": "g2",
                        "pros": _safe_text(review, "[class*='pros']"),
                        "cons": _safe_text(review, "[class*='cons']"),
                        "rating": _safe_attr(review, "[itemprop='ratingValue']", "content"),
                        "title": _safe_text(review, "h3, [class*='title']"),
                    })
                except Exception:
                    pass
    except Exception:
        pass
    return reviews


def _safe_text(parent, selector: str) -> str:
    try:
        return parent.css(selector).first.text.strip()[:300]
    except Exception:
        return ""


def _safe_attr(parent, selector: str, attr: str) -> str:
    try:
        return parent.css(selector).first.attrs.get(attr, "")
    except Exception:
        return ""
