"""
Level 1 data sources for venture-analyst.
Zero API keys required. Works immediately after install.
"""
import time
import requests
from typing import Optional

REDDIT_UA = "venture-analyst/1.0 (open-source research tool; github.com/veyralabsgroup/veyraskills)"


# ── HN Algolia (no auth, 10k req/hour) ────────────────────────────────────────

def search_hn(query: str, limit: int = 20) -> list[dict]:
    """Search Hacker News via Algolia API. Best zero-key source."""
    url = "https://hn.algolia.com/api/v1/search"
    params = {
        "query": query,
        "hitsPerPage": limit,
        "tags": "(story,ask_hn,show_hn)",
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        hits = r.json().get("hits", [])
        return [
            {
                "source": "hackernews",
                "title": h.get("title") or (h.get("story_text", "")[:80] + "..."),
                "url": h.get("url") or f"https://news.ycombinator.com/item?id={h.get('objectID')}",
                "points": h.get("points", 0),
                "comments": h.get("num_comments", 0),
                "text": (h.get("story_text") or "")[:400],
                "author": h.get("author", ""),
                "date": h.get("created_at", "")[:10],
            }
            for h in hits
        ]
    except Exception:
        return []


def search_hn_comments(query: str, min_points: int = 5, limit: int = 30) -> list[dict]:
    """Search HN comments — great for finding raw pain and opinions."""
    url = "https://hn.algolia.com/api/v1/search"
    params = {
        "query": query,
        "hitsPerPage": limit,
        "tags": "comment",
        "numericFilters": f"points>{min_points}",
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        hits = r.json().get("hits", [])
        return [
            {
                "source": "hackernews_comment",
                "text": (h.get("comment_text") or "")[:500],
                "url": f"https://news.ycombinator.com/item?id={h.get('objectID')}",
                "points": h.get("points", 0),
                "author": h.get("author", ""),
            }
            for h in hits if h.get("comment_text")
        ]
    except Exception:
        return []


# ── Reddit (no auth, custom UA required) ──────────────────────────────────────

def search_reddit(
    query: str,
    subreddits: Optional[list[str]] = None,
    limit: int = 25,
    timeframe: str = "year",
) -> list[dict]:
    """Search Reddit via public .json endpoint. Custom UA avoids 429s."""
    results = []
    headers = {"User-Agent": REDDIT_UA}

    if subreddits:
        per_sub = max(5, limit // len(subreddits[:4]))
        for sub in subreddits[:4]:
            url = f"https://www.reddit.com/r/{sub}/search.json"
            params = {"q": query, "sort": "top", "limit": per_sub, "t": timeframe, "restrict_sr": 1}
            _reddit_fetch(url, params, headers, results)
            time.sleep(1.2)
    else:
        url = "https://www.reddit.com/search.json"
        params = {"q": query, "sort": "relevance", "limit": limit, "t": timeframe}
        _reddit_fetch(url, params, headers, results)

    return results


def _reddit_fetch(url: str, params: dict, headers: dict, results: list) -> None:
    try:
        r = requests.get(url, params=params, headers=headers, timeout=12)
        if r.status_code == 200:
            for post in r.json().get("data", {}).get("children", []):
                d = post.get("data", {})
                results.append({
                    "source": "reddit",
                    "title": d.get("title", ""),
                    "url": f"https://reddit.com{d.get('permalink', '')}",
                    "upvotes": d.get("score", 0),
                    "comments": d.get("num_comments", 0),
                    "text": (d.get("selftext") or "")[:500],
                    "subreddit": d.get("subreddit", ""),
                })
    except Exception:
        pass


# ── GitHub Issues (no auth, 60 req/hour) ──────────────────────────────────────

def search_github_issues(
    query: str,
    limit: int = 20,
    token: Optional[str] = None,
) -> list[dict]:
    """
    Search GitHub issues for pain points and feature requests.
    Unauthenticated: 60 req/hour (enough for a single analysis).
    With GITHUB_TOKEN: 5,000 req/hour.
    """
    url = "https://api.github.com/search/issues"
    params = {
        "q": f"{query} type:issue",
        "sort": "reactions",
        "order": "desc",
        "per_page": min(limit, 30),
    }
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    try:
        r = requests.get(url, params=params, headers=headers, timeout=12)
        if r.status_code != 200:
            return []
        return [
            {
                "source": "github",
                "title": i.get("title", ""),
                "url": i.get("html_url", ""),
                "reactions": i.get("reactions", {}).get("total_count", 0),
                "comments": i.get("comments", 0),
                "text": (i.get("body") or "")[:400],
                "repo": i.get("repository_url", "").split("/")[-1],
                "state": i.get("state", ""),
            }
            for i in r.json().get("items", [])
        ]
    except Exception:
        return []


def search_github_repos(
    query: str,
    limit: int = 10,
    token: Optional[str] = None,
) -> list[dict]:
    """Find existing repos/tools in the space."""
    url = "https://api.github.com/search/repositories"
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": min(limit, 20),
    }
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    try:
        r = requests.get(url, params=params, headers=headers, timeout=12)
        if r.status_code != 200:
            return []
        return [
            {
                "source": "github_repo",
                "name": repo.get("full_name", ""),
                "url": repo.get("html_url", ""),
                "stars": repo.get("stargazers_count", 0),
                "description": repo.get("description", ""),
                "language": repo.get("language", ""),
                "updated": repo.get("updated_at", "")[:10],
            }
            for repo in r.json().get("items", [])
        ]
    except Exception:
        return []


# ── Web search (ddgs, no key) ──────────────────────────────────────────────────

def search_web(query: str, limit: int = 10) -> list[dict]:
    """Web search via ddgs. No API key. May rate-limit on heavy use."""
    try:
        from ddgs import DDGS
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=limit):
                results.append({
                    "source": "web",
                    "title": r.get("title", ""),
                    "url": r.get("href", ""),
                    "text": r.get("body", ""),
                })
        return results
    except Exception:
        return []


# ── Google Trends (no key) ─────────────────────────────────────────────────────

def get_trends(keyword: str) -> dict:
    """Google Trends via trendspyg. Fragile but free."""
    try:
        from trendspyg import TrendReq
        pytrends = TrendReq(hl="en-US", tz=360)
        pytrends.build_payload([keyword], timeframe="today 12-m")
        data = pytrends.interest_over_time()
        if data.empty:
            return {"trend": "no_data", "avg_interest": 0}

        avg = float(data[keyword].mean())
        recent = float(data[keyword].iloc[-8:].mean())
        if recent > avg * 1.25:
            trend = "rising"
        elif recent < avg * 0.75:
            trend = "declining"
        else:
            trend = "stable"

        related = {}
        try:
            related_data = pytrends.related_queries()
            top = related_data.get(keyword, {}).get("top")
            if top is not None and not top.empty:
                related = {row["query"]: row["value"] for _, row in top.head(5).iterrows()}
        except Exception:
            pass

        return {
            "trend": trend,
            "avg_interest": round(avg, 1),
            "recent_interest": round(recent, 1),
            "related_queries": related,
        }
    except Exception:
        return {"trend": "unavailable", "avg_interest": 0}


# ── Evidence Score ─────────────────────────────────────────────────────────────

def calculate_evidence_score(results: dict) -> dict:
    """
    Score the evidence quality collected across all sources.
    Returns score 0-100 + breakdown per source.
    """
    reddit = results.get("reddit", [])
    hn = results.get("hackernews", []) + results.get("hackernews_comment", [])
    github = results.get("github", [])
    competitors = results.get("competitors", [])
    trends = results.get("trends", {})

    # Weighted scoring
    reddit_pts  = min(len(reddit) * 1.5, 25)
    hn_pts      = min(len(hn) * 2.5, 25)
    github_pts  = min(len(github) * 2, 20)
    comp_pts    = min(len(competitors) * 3, 20)
    trend_pts   = 10 if trends.get("trend") not in ("unavailable", "no_data") else 0

    score = int(reddit_pts + hn_pts + github_pts + comp_pts + trend_pts)

    return {
        "evidence_score": min(score, 100),
        "breakdown": {
            "reddit_mentions": len(reddit),
            "hn_discussions": len(hn),
            "github_issues": len(github),
            "competitors_found": len(competitors),
            "trend_data": trends.get("trend", "unavailable"),
        },
    }
