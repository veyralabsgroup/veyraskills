"""
web_inspector.py

Extracts SEO data, tech stack, copy signals, CTAs, trust signals,
and performance hints from a public website. Uses Scrapling for
stealth fetching. No API keys required.
"""

import re
import json
from urllib.parse import urlparse, urljoin

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


# -------------------------------------------------------------------
# Fetching
# -------------------------------------------------------------------

def fetch_page(url: str) -> tuple[str, object]:
    """
    Fetch a page and return (html_text, parsed_page).
    Tries StealthyFetcher first, falls back to Fetcher, then requests.
    Returns (raw_html, page_object_or_none).
    """
    if HAS_SCRAPLING:
        try:
            page = StealthyFetcher().fetch(url, headless=True, network_idle=True)
            return page.html_content, page
        except Exception:
            pass
        try:
            page = Fetcher().get(url)
            return page.html_content, page
        except Exception:
            pass

    if HAS_REQUESTS:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; agency-audit/1.0)"
        }
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        return resp.text, None

    raise RuntimeError("No HTTP library available. Install scrapling or requests.")


# -------------------------------------------------------------------
# SEO extraction
# -------------------------------------------------------------------

def extract_seo(html: str, url: str) -> dict:
    """Extract basic SEO elements from raw HTML."""

    def tag_content(pattern, html, group=1):
        m = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
        return m.group(group).strip() if m else None

    title = tag_content(r'<title[^>]*>(.*?)</title>', html)
    meta_desc = tag_content(
        r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html
    ) or tag_content(
        r'<meta\s+content=["\'](.*?)["\']\s+name=["\']description["\']', html
    )
    h1_matches = re.findall(r'<h1[^>]*>(.*?)</h1>', html, re.IGNORECASE | re.DOTALL)
    h1_list = [re.sub(r'<[^>]+>', '', h).strip() for h in h1_matches]

    canonical = tag_content(
        r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']', html
    )
    robots_meta = tag_content(
        r'<meta\s+name=["\']robots["\']\s+content=["\'](.*?)["\']', html
    )

    # Count images and check alt text
    img_tags = re.findall(r'<img[^>]*>', html, re.IGNORECASE)
    imgs_with_alt = sum(1 for img in img_tags if re.search(r'alt=["\'][^"\']+["\']', img, re.IGNORECASE))

    # Check for sitemap and robots.txt references
    has_sitemap_link = bool(re.search(r'sitemap\.xml', html, re.IGNORECASE))

    # Schema markup
    schema_types = re.findall(
        r'"@type"\s*:\s*"([^"]+)"', html, re.IGNORECASE
    )

    return {
        "title": title,
        "title_length": len(title) if title else 0,
        "meta_description": meta_desc,
        "meta_description_length": len(meta_desc) if meta_desc else 0,
        "h1_count": len(h1_list),
        "h1_text": h1_list[0] if h1_list else None,
        "h1_all": h1_list,
        "canonical": canonical,
        "robots_meta": robots_meta,
        "images_total": len(img_tags),
        "images_with_alt": imgs_with_alt,
        "images_missing_alt": len(img_tags) - imgs_with_alt,
        "has_sitemap_link": has_sitemap_link,
        "schema_types": list(set(schema_types)),
    }


# -------------------------------------------------------------------
# Tech stack detection
# -------------------------------------------------------------------

def detect_tech_stack(html: str, url: str) -> dict:
    """Detect CMS, analytics, chat tools from HTML patterns."""

    def contains(pattern):
        return bool(re.search(pattern, html, re.IGNORECASE))

    # CMS detection
    cms = "Unknown"
    if contains(r'wp-content|wp-includes|wordpress'):
        cms = "WordPress"
    elif contains(r'webflow\.com|webflow\.io|\.wf-'):
        cms = "Webflow"
    elif contains(r'shopify\.com|cdn\.shopify|shopify-section'):
        cms = "Shopify"
    elif contains(r'squarespace\.com|squarespace-cdn'):
        cms = "Squarespace"
    elif contains(r'wix\.com|wixsite\.com|_wixCIDX'):
        cms = "Wix"
    elif contains(r'framer\.com|framer-motion'):
        cms = "Framer"
    elif contains(r'ghost\.io|ghost-theme'):
        cms = "Ghost"

    # Analytics
    analytics = []
    if contains(r'google-analytics\.com/analytics|gtag\(|GA_MEASUREMENT_ID|G-[A-Z0-9]+'):
        analytics.append("GA4")
    if contains(r'googletagmanager\.com|GTM-'):
        analytics.append("Google Tag Manager")
    if contains(r'connect\.facebook\.net/[a-z]+/fbevents|fbq\('):
        analytics.append("Meta Pixel")
    if contains(r'hotjar\.com|_hjSettings'):
        analytics.append("Hotjar")
    if contains(r'clarity\.ms|ms\.clarity'):
        analytics.append("Microsoft Clarity")
    if contains(r'segment\.com|analytics\.js'):
        analytics.append("Segment")

    # Chat / support tools
    chat_tools = []
    if contains(r'intercom\.io|intercomSettings'):
        chat_tools.append("Intercom")
    if contains(r'tawk\.to'):
        chat_tools.append("Tawk.to")
    if contains(r'crisp\.chat|window\.\$crisp'):
        chat_tools.append("Crisp")
    if contains(r'drift\.com|window\.drift'):
        chat_tools.append("Drift")
    if contains(r'hubspot\.com/conversations|HubSpot'):
        chat_tools.append("HubSpot Chat")
    if contains(r'tidio\.com|tidioChatCode'):
        chat_tools.append("Tidio")
    if contains(r'livechat\.com|LiveChatWidget'):
        chat_tools.append("LiveChat")
    if contains(r'zendesk\.com|zEWidget'):
        chat_tools.append("Zendesk")

    # Performance signals
    has_lazy_loading = contains(r'loading=["\']lazy["\']')
    has_webp = contains(r'\.webp["\'> ]')
    has_deferred_scripts = contains(r'<script[^>]+(?:defer|async)[^>]*>')
    has_render_blocking_head = bool(
        re.search(r'<head[^>]*>.*?<script(?!\s+(?:defer|async))[^>]*src=', html, re.IGNORECASE | re.DOTALL)
    )

    # HTTPS
    parsed = urlparse(url)
    is_https = parsed.scheme == "https"

    # Cookie / GDPR
    has_cookie_banner = contains(
        r'cookie|cookieconsent|gdpr|rgpd|consentmanager|cookiebot|onetrust'
    )

    return {
        "cms": cms,
        "analytics": analytics,
        "chat_tools": chat_tools,
        "is_https": is_https,
        "has_lazy_loading": has_lazy_loading,
        "has_webp_images": has_webp,
        "has_deferred_scripts": has_deferred_scripts,
        "has_render_blocking_head_scripts": has_render_blocking_head,
        "has_cookie_banner": has_cookie_banner,
    }


# -------------------------------------------------------------------
# Copy and CTA analysis
# -------------------------------------------------------------------

def analyze_copy(html: str) -> dict:
    """Analyze copy quality and CTA presence from HTML."""

    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'\s+', ' ', text).strip().lower()

    # Social proof signals
    social_proof_patterns = [
        r'\b\d+\+?\s*(clients?|customers?|companies|brands|businesses)',
        r'\b\d+\+?\s*(years?)\s+of\s+(experience|expertise)',
        r'trusted\s+by',
        r'(testimonial|review|case\s+study)',
        r'"[^"]{20,100}"',  # Quoted testimonials
    ]
    social_proof_found = [p for p in social_proof_patterns if re.search(p, text, re.IGNORECASE)]

    # Pain-first signals (they address customer problems)
    pain_patterns = [
        r'\b(problem|challenge|struggle|frustrated|difficult|hard|painful)\b',
        r'\b(save\s+time|save\s+money|reduce|eliminate|stop)\b',
        r'\btired\s+of\b',
        r'\bwithout\s+(the\s+)?(hassle|stress|worry)\b',
    ]
    pain_first_count = sum(1 for p in pain_patterns if re.search(p, text, re.IGNORECASE))

    # Feature-first signals (they talk about themselves)
    feature_patterns = [
        r'\bwe\s+(are|have|offer|provide|specialize)\b',
        r'\bour\s+(team|service|solution|platform|approach)\b',
        r'\bstate.of.the.art\b',
        r'\binnovative\b',
        r'\bworld.class\b',
    ]
    feature_first_count = sum(1 for p in feature_patterns if re.search(p, text, re.IGNORECASE))

    is_pain_first = pain_first_count > feature_first_count

    # CTA buttons
    cta_patterns = re.findall(
        r'<(?:a|button)[^>]*>([^<]{2,50})</(?:a|button)>',
        html, re.IGNORECASE
    )
    cta_texts = [re.sub(r'\s+', ' ', c).strip() for c in cta_patterns if len(c.strip()) > 2]
    cta_texts = [c for c in cta_texts if not re.match(r'^(home|about|contact|menu|blog|services?|portfolio)$', c, re.IGNORECASE)][:10]

    # Pricing visibility
    has_pricing = bool(re.search(
        r'\b(pricing|price|cost|plan|€|\$|per\s+month|\/mo|starting\s+at)\b',
        html, re.IGNORECASE
    ))

    # Contact form
    has_form = bool(re.search(r'<form\b', html, re.IGNORECASE))

    # Phone number
    phone_pattern = re.search(
        r'(?:\+34|0034)?\s*[6-9]\d{2}[\s.-]?\d{3}[\s.-]?\d{3}|(?:\+\d{1,3})?\s*\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}',
        html
    )
    has_phone = phone_pattern is not None

    # Trust signals
    trust_patterns = {
        "logos": bool(re.search(r'(client|partner|trusted.by|logo)', html, re.IGNORECASE)),
        "certifications": bool(re.search(r'(certified|certificate|award|accredited)', html, re.IGNORECASE)),
        "team_photos": bool(re.search(r'(our.team|meet.the.team|about.us)', html, re.IGNORECASE)),
        "case_studies": bool(re.search(r'(case.study|success.story|project|portfolio)', html, re.IGNORECASE)),
        "numbers": bool(re.search(r'\b\d{2,}[\+k]?\s*(clients?|customers?|projects?|years?)', html, re.IGNORECASE)),
    }

    return {
        "is_pain_first": is_pain_first,
        "pain_signal_count": pain_first_count,
        "feature_signal_count": feature_first_count,
        "social_proof_signals": len(social_proof_found),
        "social_proof_details": social_proof_found[:3],
        "cta_texts_found": cta_texts,
        "cta_count": len(cta_texts),
        "has_pricing_visible": has_pricing,
        "has_contact_form": has_form,
        "has_phone_number": has_phone,
        "trust_signals": trust_patterns,
        "trust_signal_count": sum(trust_patterns.values()),
    }


# -------------------------------------------------------------------
# Main inspection function
# -------------------------------------------------------------------

def inspect_website(url: str) -> dict:
    """
    Full website inspection. Returns structured audit data.

    Args:
        url: Full URL to inspect (include https://)

    Returns:
        dict with keys: url, seo, tech_stack, copy, summary
    """
    if not url.startswith("http"):
        url = "https://" + url

    html, page = fetch_page(url)

    seo = extract_seo(html, url)
    tech = detect_tech_stack(html, url)
    copy = analyze_copy(html)

    # Build summary flags for quick reference
    critical_issues = []
    quick_wins = []
    important_issues = []

    # Value prop
    if not seo["h1_text"] or len(seo["h1_text"]) < 5:
        critical_issues.append("No clear H1 / value proposition")
    if copy["cta_count"] == 0:
        critical_issues.append("No CTAs detected on page")

    # SEO
    if not seo["title"]:
        important_issues.append("Missing title tag")
    elif seo["title_length"] > 65:
        quick_wins.append("Title tag too long ({} chars) - shorten to under 60".format(seo["title_length"]))

    if not seo["meta_description"]:
        quick_wins.append("Missing meta description - add 120-160 char description")
    elif seo["meta_description_length"] > 165:
        quick_wins.append("Meta description too long ({} chars)".format(seo["meta_description_length"]))

    if seo["h1_count"] == 0:
        important_issues.append("No H1 tag found")
    elif seo["h1_count"] > 1:
        important_issues.append("Multiple H1 tags ({}) - should be exactly one".format(seo["h1_count"]))

    if seo["images_missing_alt"] > 3:
        quick_wins.append("{} images missing alt text".format(seo["images_missing_alt"]))

    # Analytics
    if not tech["analytics"]:
        important_issues.append("No analytics tracking detected")
    elif "Google Tag Manager" not in tech["analytics"]:
        quick_wins.append("No GTM - install for easier tag management")

    if not any("Pixel" in a or "Meta" in a for a in tech["analytics"]):
        important_issues.append("No Meta Pixel detected")

    # Copy
    if copy["social_proof_signals"] == 0:
        important_issues.append("No social proof on homepage")
    if not copy["has_contact_form"]:
        important_issues.append("No contact form detected")

    # Performance
    if not tech["has_lazy_loading"]:
        quick_wins.append("Images not lazy-loaded - add loading='lazy'")
    if not tech["has_webp_images"] and tech["cms"] not in ["Webflow", "Framer"]:
        quick_wins.append("No WebP images detected - convert for faster loads")

    return {
        "url": url,
        "seo": seo,
        "tech_stack": tech,
        "copy": copy,
        "summary": {
            "critical_issues": critical_issues,
            "important_issues": important_issues,
            "quick_wins": quick_wins,
            "cms": tech["cms"],
            "analytics_installed": len(tech["analytics"]) > 0,
            "analytics_tools": tech["analytics"],
            "has_social_proof": copy["social_proof_signals"] > 0,
            "has_cta": copy["cta_count"] > 0,
            "is_https": tech["is_https"],
        }
    }


def format_inspection_output(data: dict) -> str:
    """Format inspect_website() output for Claude to read."""
    seo = data["seo"]
    tech = data["tech_stack"]
    copy = data["copy"]
    summary = data["summary"]

    lines = [
        f"## Web Inspection: {data['url']}",
        "",
        f"### Platform",
        f"CMS: {tech['cms']}",
        f"HTTPS: {'Yes' if tech['is_https'] else 'NO - security issue'}",
        f"Analytics: {', '.join(tech['analytics']) if tech['analytics'] else 'None detected'}",
        f"Chat tools: {', '.join(tech['chat_tools']) if tech['chat_tools'] else 'None'}",
        "",
        f"### SEO Basics",
        f"Title: {'\"' + seo['title'] + '\" (' + str(seo['title_length']) + ' chars)' if seo['title'] else 'MISSING'}",
        f"Meta description: {'Present (' + str(seo['meta_description_length']) + ' chars)' if seo['meta_description'] else 'MISSING'}",
        f"H1: {seo['h1_count']} found - {('\"' + seo['h1_text'] + '\"') if seo['h1_text'] else 'NONE'}",
        f"Images missing alt: {seo['images_missing_alt']} / {seo['images_total']}",
        f"Schema types: {', '.join(seo['schema_types']) if seo['schema_types'] else 'None'}",
        "",
        f"### Copy and Conversion",
        f"Copy tone: {'Pain-first (good)' if copy['is_pain_first'] else 'Feature-first (needs work)'}",
        f"Social proof signals: {copy['social_proof_signals']}",
        f"CTA texts found: {', '.join(copy['cta_texts_found'][:5]) if copy['cta_texts_found'] else 'NONE'}",
        f"Pricing visible: {'Yes' if copy['has_pricing_visible'] else 'No'}",
        f"Contact form: {'Yes' if copy['has_contact_form'] else 'No'}",
        f"Phone number: {'Yes' if copy['has_phone_number'] else 'No'}",
        f"Trust signal count: {copy['trust_signal_count']} / 5",
        "",
        f"### Performance",
        f"Lazy loading: {'Yes' if tech['has_lazy_loading'] else 'No'}",
        f"WebP images: {'Yes' if tech['has_webp_images'] else 'No'}",
        f"Render-blocking scripts: {'Yes - potential issue' if tech['has_render_blocking_head_scripts'] else 'No'}",
        "",
        f"### Issues Summary",
        f"Critical: {len(summary['critical_issues'])}",
    ]

    for issue in summary["critical_issues"]:
        lines.append(f"  - {issue}")

    lines.append(f"Important: {len(summary['important_issues'])}")
    for issue in summary["important_issues"]:
        lines.append(f"  - {issue}")

    lines.append(f"Quick wins: {len(summary['quick_wins'])}")
    for win in summary["quick_wins"]:
        lines.append(f"  - {win}")

    return "\n".join(lines)
