"""
Level 2 auto-detection.
Silently detects available enhancements. Never asks the user for config.
"""
import os
import subprocess
import time
import requests


def detect_level() -> dict:
    """
    Detect what's available. Returns a capability map.
    Called once at session start — results cached for the session.
    """
    return {
        "docker":          _has_docker(),
        "searxng":         _has_searxng(),
        "veyrascrape_mcp": _has_env("VEYRASCRAPE_API_KEY"),
        "github_token":    _has_env("GITHUB_TOKEN"),
        "exa_key":         _has_env("EXA_API_KEY"),
        "tavily_key":      _has_env("TAVILY_API_KEY"),
        "groq_key":        _has_env("GROQ_API_KEY"),
    }


def _has_env(key: str) -> bool:
    val = os.environ.get(key, "").strip()
    return bool(val)


def _has_docker() -> bool:
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=4,
        )
        return result.returncode == 0
    except Exception:
        return False


def _has_searxng(ports: list[int] = None) -> bool:
    if ports is None:
        ports = [8080, 8888, 4000]
    for port in ports:
        try:
            r = requests.get(
                f"http://localhost:{port}/search",
                params={"q": "test", "format": "json"},
                timeout=2,
            )
            if r.status_code == 200:
                return True
        except Exception:
            pass
    return False


def ensure_searxng() -> dict:
    """
    Launch SearXNG via Docker if available and not already running.
    Returns status dict.
    """
    if _has_searxng():
        return {"available": True, "url": "http://localhost:8080", "launched": False}

    if not _has_docker():
        return {"available": False, "reason": "docker_not_found"}

    try:
        subprocess.run(
            [
                "docker", "run", "-d",
                "--name", "venture-searxng",
                "-p", "8080:8080",
                "searxng/searxng",
            ],
            capture_output=True,
            timeout=45,
        )
        # give it time to start
        for _ in range(6):
            time.sleep(2)
            if _has_searxng():
                return {"available": True, "url": "http://localhost:8080", "launched": True}
        return {"available": False, "reason": "searxng_start_timeout"}
    except Exception as e:
        return {"available": False, "reason": str(e)}


def search_searxng(query: str, url: str = "http://localhost:8080", limit: int = 10) -> list[dict]:
    """Search via local SearXNG instance."""
    try:
        r = requests.get(
            f"{url}/search",
            params={"q": query, "format": "json", "pageno": 1},
            timeout=10,
        )
        results = r.json().get("results", [])[:limit]
        return [
            {
                "source": "searxng",
                "title": res.get("title", ""),
                "url": res.get("url", ""),
                "text": res.get("content", ""),
                "engine": res.get("engine", ""),
            }
            for res in results
        ]
    except Exception:
        return []


def search_with_exa(query: str, api_key: str, limit: int = 10) -> list[dict]:
    """Semantic search via Exa API (optional Level 3 enhancement)."""
    try:
        import exa_py
        exa = exa_py.Exa(api_key=api_key)
        results = exa.search(query, num_results=limit, use_autoprompt=True)
        return [
            {
                "source": "exa",
                "title": r.title or "",
                "url": r.url,
                "text": r.text or "",
            }
            for r in results.results
        ]
    except Exception:
        return []


def best_search(query: str, env: dict, limit: int = 10) -> list[dict]:
    """
    Use the best available search method based on detected environment.
    Priority: Exa > SearXNG > Tavily > ddgs
    """
    # Level 3: Exa
    if env.get("exa_key"):
        results = search_with_exa(query, os.environ["EXA_API_KEY"], limit)
        if results:
            return results

    # Level 2: SearXNG
    if env.get("searxng"):
        results = search_searxng(query, limit=limit)
        if results:
            return results

    # Level 2: Tavily
    if env.get("tavily_key"):
        try:
            from tavily import TavilyClient
            client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
            response = client.search(query, max_results=limit)
            return [
                {
                    "source": "tavily",
                    "title": r.get("title", ""),
                    "url": r.get("url", ""),
                    "text": r.get("content", ""),
                }
                for r in response.get("results", [])
            ]
        except Exception:
            pass

    # Level 1: ddgs (always available)
    from scripts.sources import search_web
    return search_web(query, limit)
