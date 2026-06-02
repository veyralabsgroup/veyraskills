"""
competitor_finder.py

Finds competitors for a given company/URL and extracts basic
positioning signals. Uses ddgs for search, Scrapling for scraping.
No API keys required.
"""

import re
from urllib.parse import urlparse

try:
    from ddgs import DDGS
    HAS_DDGS = True
except ImportError:
    HAS_DDGS = False

try:
    from scrapling import Fetcher, StealthyFetcher
    HAS_SCRAPLING = True
except ImportError:
    HAS_SCRAPLING = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


# -------------------------------------------------------------------
# Competitor discovery
# -------------------------------------------------------------------

def find_competitors(company_name: str, industry: str = "", url: str = "", limit: int = 5) -> list[str]:
    """
    Find competitor URLs for a company.

    Args:
        company_name: Name of the company being audited
        industry: Industry or service type (optional, improves results)
        url: Company URL (used to extract domain for exclusion)
        limit: Max number of competitors to return

    Returns:
        List of competitor URLs
    """
    if not HAS_DDGS:
        return []

    own_domain = ""
    if url:
        parsed = urlparse(url if url.startswith("http") else "https://" + url)
        own_domain = parsed.netloc.replace("www.", "")

    queries = []
    if industry:
        queries.append(f"{industry} alternatives to {company_name}")
        queries.append(f"best {industry} companies like {company_name}")
    queries.append(f"{company_name} competitors")
    queries.append(f"alternatives to {company_name}")

    found_urls = []
    seen_domains = {own_domain} if own_domain else set()

    with DDGS() as ddgs:
        for query in queries:
            if len(found_urls) >= limit:
                break
            try:
                results = ddgs.text(query, max_results=8)
                for r in (results or []):
                    href = r.get("href", "")
                    if not href:
                        continue
                    parsed = urlparse(href)
                    domain = parsed.netloc.replace("www.", "")
                    # Skip directories, review sites, news
                    if any(skip in domain for skip in [
                        "wikipedia", "linkedin", "facebook", "instagram",
                        "twitter", "x.com", "yelp", "trustpilot", "capterra",
                        "g2.com", "glassdoor", "reddit", "youtube",
                        "medium", "forbes", "techcrunch",
                    ]):
                        continue
                    if domain not in seen_domains:
                        seen_domains.add(domain)
                        found_urls.append(href)
                    if len(found_urls) >= limit:
                        break
            except Exception:
                continue

    return found_urls[:limit]


# -------------------------------------------------------------------
# Competitor page scraping
# -------------------------------------------------------------------

def _fetch_html(url: str) -> str:
    """Fetch HTML with best available method."""
    if HAS_SCRAPLING:
        try:
            page = Fetcher().get(url, timeout=10)
            return page.html_content
        except Exception:
            pass
    if HAS_REQUESTS:
        try:
            headers = {"User-Agent": "Mozilla/5.0 (compatible; agency-audit/1.0)"}
            resp = requests.get(url, headers=headers, timeout=10)
            return resp.text
        except Exception:
            pass
    return ""


def _clean_text(html_fragment: str) -> str:
    """Strip HTML tags and normalize whitespace."""
    text = re.sub(r'<[^>]+>', ' ', html_fragment)
    return re.sub(r'\s+', ' ', text).strip()


def scrape_competitor_signals(url: str) -> dict:
    """
    Extract positioning signals from a competitor URL.

    Returns dict with: url, headline, value_prop, cta_text,
    has_social_proof, has_pricing, has_case_studies, analytics, cms
    """
    html = _fetch_html(url)
    if not html:
        return {"url": url, "error": "Could not fetch page"}

    # Headline (H1)
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.IGNORECASE | re.DOTALL)
    headline = _clean_text(h1_match.group(1)) if h1_match else None

    # Sub-headline (first H2 or subtitle paragraph)
    h2_match = re.search(r'<h2[^>]*>(.*?)</h2>', html, re.IGNORECASE | re.DOTALL)
    sub_headline = _clean_text(h2_match.group(1)) if h2_match else None

    # Primary CTA
    cta_matches = re.findall(
        r'<(?:a|button)[^>]*class=["\'][^"\']*(?:btn|button|cta)[^"\']*["\'][^>]*>(.*?)</(?:a|button)>',
        html, re.IGNORECASE | re.DOTALL
    )
    cta_texts = [_clean_text(c) for c in cta_matches if len(_clean_text(c)) > 2][:3]

    # Social proof
    has_testimonials = bool(re.search(r'testimonial|review|"[^"]{20,100}"', html, re.IGNORECASE))
    has_client_logos = bool(re.search(r'(trusted.by|our.clients?|partners?|client.logo)', html, re.IGNORECASE))
    has_numbers = bool(re.search(r'\b\d{2,}[\+k]?\s*(clients?|customers?|projects?|brands?)', html, re.IGNORECASE))
    has_case_studies = bool(re.search(r'(case.stud|success.stor|our.work|portfolio)', html, re.IGNORECASE))

    social_proof_count = sum([has_testimonials, has_client_logos, has_numbers, has_case_studies])

    # Pricing
    has_pricing = bool(re.search(
        r'\b(pricing|price|cost|plan|€|\$|per\s+month|\/mo|starting\s+at)\b',
        html, re.IGNORECASE
    ))

    # Analytics (quick check)
    analytics = []
    if re.search(r'gtag\(|G-[A-Z0-9]+|google-analytics', html, re.IGNORECASE):
        analytics.append("GA4")
    if re.search(r'GTM-', html):
        analytics.append("GTM")
    if re.search(r'fbq\(|connect\.facebook\.net', html, re.IGNORECASE):
        analytics.append("Meta Pixel")

    # CMS
    cms = "Unknown"
    if re.search(r'wp-content|wp-includes', html, re.IGNORECASE):
        cms = "WordPress"
    elif re.search(r'webflow\.com', html, re.IGNORECASE):
        cms = "Webflow"
    elif re.search(r'cdn\.shopify', html, re.IGNORECASE):
        cms = "Shopify"
    elif re.search(r'squarespace\.com', html, re.IGNORECASE):
        cms = "Squarespace"
    elif re.search(r'wix\.com|wixsite', html, re.IGNORECASE):
        cms = "Wix"

    # Pain-first vs feature-first
    text_lower = html.lower()
    pain_signals = sum(1 for p in [
        r'tired of', r'frustrated', r'struggling', r'save time', r'stop wasting',
    ] if re.search(p, text_lower))
    is_pain_first = pain_signals > 0

    return {
        "url": url,
        "headline": headline,
        "sub_headline": sub_headline,
        "cta_texts": cta_texts,
        "has_social_proof": social_proof_count > 0,
        "social_proof_count": social_proof_count,
        "has_pricing": has_pricing,
        "has_case_studies": has_case_studies,
        "has_client_logos": has_client_logos,
        "has_testimonials": has_testimonials,
        "is_pain_first": is_pain_first,
        "cms": cms,
        "analytics": analytics,
    }


# -------------------------------------------------------------------
# Comparison table
# -------------------------------------------------------------------

def compare_positioning(target_url: str, competitor_urls: list[str]) -> dict:
    """
    Scrape target + competitors, return structured comparison.

    Args:
        target_url: The company being audited
        competitor_urls: List of competitor URLs

    Returns:
        dict with target, competitors, gaps, advantages
    """
    target_data = scrape_competitor_signals(target_url)
    competitor_data = []

    for url in competitor_urls[:4]:
        try:
            data = scrape_competitor_signals(url)
            competitor_data.append(data)
        except Exception:
            competitor_data.append({"url": url, "error": "scraping failed"})

    # Calculate gaps (things competitors have that target lacks)
    gaps = []
    if not target_data.get("has_social_proof"):
        comps_with_proof = sum(1 for c in competitor_data if c.get("has_social_proof"))
        if comps_with_proof > 0:
            gaps.append(f"Social proof: {comps_with_proof}/{len(competitor_data)} competitors have it, target does not")

    if not target_data.get("has_pricing"):
        comps_with_pricing = sum(1 for c in competitor_data if c.get("has_pricing"))
        if comps_with_pricing > 0:
            gaps.append(f"Pricing visibility: {comps_with_pricing}/{len(competitor_data)} competitors show pricing, target does not")

    if not target_data.get("has_case_studies"):
        comps_with_cases = sum(1 for c in competitor_data if c.get("has_case_studies"))
        if comps_with_cases > 0:
            gaps.append(f"Case studies: {comps_with_cases}/{len(competitor_data)} competitors have case studies, target does not")

    if not target_data.get("is_pain_first"):
        comps_pain_first = sum(1 for c in competitor_data if c.get("is_pain_first"))
        if comps_pain_first > 1:
            gaps.append(f"Pain-first messaging: {comps_pain_first} competitors lead with customer problems, target does not")

    # Calculate advantages (things target has that competitors lack)
    advantages = []
    if target_data.get("has_pricing"):
        comps_without = sum(1 for c in competitor_data if not c.get("has_pricing"))
        if comps_without > 1:
            advantages.append(f"Pricing transparency: target shows pricing while {comps_without} competitors hide it")

    if target_data.get("has_case_studies"):
        comps_without = sum(1 for c in competitor_data if not c.get("has_case_studies"))
        if comps_without > 1:
            advantages.append(f"Case studies present while {comps_without} competitors lack them")

    return {
        "target": target_data,
        "competitors": competitor_data,
        "gaps": gaps,
        "advantages": advantages,
    }


def format_comparison_output(comparison: dict) -> str:
    """Format comparison data as a readable table for Claude."""
    target = comparison["target"]
    competitors = comparison["competitors"]

    all_sites = [target] + competitors
    lines = [
        "## Competitor Comparison",
        "",
        "| Signal | " + " | ".join(
            [urlparse(s.get("url", "")).netloc.replace("www.", "") for s in all_sites]
        ) + " |",
        "|--------|" + "|".join(["------" for _ in all_sites]) + "|",
    ]

    def yn(val):
        return "Y" if val else "N"

    signals = [
        ("Clear H1", lambda s: bool(s.get("headline") and len(s.get("headline", "")) > 5)),
        ("Social proof", lambda s: s.get("has_social_proof", False)),
        ("Case studies", lambda s: s.get("has_case_studies", False)),
        ("Pricing visible", lambda s: s.get("has_pricing", False)),
        ("Pain-first copy", lambda s: s.get("is_pain_first", False)),
        ("Client logos", lambda s: s.get("has_client_logos", False)),
        ("Analytics", lambda s: len(s.get("analytics", [])) > 0),
    ]

    for label, fn in signals:
        row = f"| {label} |"
        for site in all_sites:
            row += f" {yn(fn(site))} |"
        lines.append(row)

    lines.extend(["", "### Gaps (target lacks these vs competitors):"])
    for g in comparison["gaps"] or ["None identified"]:
        lines.append(f"- {g}")

    lines.extend(["", "### Advantages (target has, competitors lack):"])
    for a in comparison["advantages"] or ["None identified"]:
        lines.append(f"- {a}")

    lines.extend(["", "### Competitor Headlines:"])
    for c in competitors:
        domain = urlparse(c.get("url", "")).netloc.replace("www.", "")
        headline = c.get("headline", "N/A")
        lines.append(f"- {domain}: \"{headline}\"")

    return "\n".join(lines)
