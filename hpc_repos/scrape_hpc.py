"""
One-shot HPC GitHub scraper.
Grabs repos matching HPC queries, filters false positives with word-boundary
matching, scores them with a non-saturating log formula, writes two JSON
files, exits.

Usage:
    export GITHUB_TOKEN=ghp_your_token_here    # optional but recommended
    python scrape_hpc.py
"""

import os
import re
import json
import time
import math
from datetime import datetime, timezone
from pathlib import Path

import requests

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "hpc-scraper",
}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"

API = "https://api.github.com"
MAX_PER_QUERY = 300
OUT_DIR = Path("data")

# --- Queries ---------------------------------------------------------------
NEW_QUERIES = [
    "topic:hpc created:>2025-01-01 stars:>3",
    "topic:hpc created:>2024-06-01 stars:>30",
    "hpc in:name,description created:>2025-01-01 stars:>10",
    "hpc language:C++ created:>2025-01-01 stars:>5",
    "hpc language:Python created:>2025-01-01 stars:>5",
    "hpc language:Rust created:>2024-06-01 stars:>3",
    "cuda created:>2025-06-01 stars:>20",
    "slurm created:>2025-01-01 stars:>5",
]

ACTIVE_QUERIES = [
    "topic:hpc pushed:>2026-06-01 stars:>200",
    "topic:hpc pushed:>2026-08-01 stars:>50",
    "hpc in:name,description pushed:>2026-08-01 stars:>100",
    "cuda pushed:>2026-08-01 stars:>300",
]

# --- False-positive patterns (acronym / word collisions) -------------------
FP_PATTERNS = [
    r"\bHPCA\d*\b",
    r"\bHPCM\b",
    r"\bHPC1\b",
    r"\bHPCwild\b",
    r"\bHuman Performance Capture\b",
    r"\bHuman Mesh Recovery\b",
    r"\bHaskell Program Coverage\b",
    r"\bhpc-coveralls?\b",
    r"\bHellinger PCA\b",
    r"\bHP Cloud\b",
    r"\bHPCloud\b",
    r"\bhippocamp",
    r"\bHPC_manifolds\b",
    r"\bMR24HPC1\b",
]
FP_RE = re.compile("|".join(FP_PATTERNS), re.IGNORECASE)

# --- Topic allowlist (strongest signal — maintainer's own declaration) -----
HPC_TOPICS = {
    "hpc",
    "high-performance-computing",
    "high-performance",
    "supercomputing",
    "exascale",
    "exascale-computing",
    "mpi",
    "openmp",
    "openacc",
    "cuda",
    "opencl",
    "rocm",
    "sycl",
    "hip",
    "kokkos",
    "slurm",
    "parallel-computing",
    "parallel-programming",
    "scientific-computing",
    "distributed-computing",
    "gpu-computing",
    "gpgpu",
    "cfd",
    "fem",
    "finite-elements",
    "linear-algebra",
    "blas",
    "lapack",
    "hdf5",
    "lustre",
    "infiniband",
    "rdma",
    "mpi4py",
}

# --- HPC signal words (word-boundary matched, no ambiguous tokens) ---------
HPC_SIGNALS = [
    # multi-word — always safe
    "high performance computing",
    "high-performance computing",
    "supercomput",
    "exascale",
    "parallel computing",
    "parallel program",
    "distributed comput",
    "gpu comput",
    "scientific comput",
    "numerical comput",
    "job scheduler",
    "workload manager",
    "finite element",
    "amd hip",
    "hip kernel",
    "portable batch system",
    # unambiguous single words
    "mpi",
    "openmp",
    "openacc",
    "cuda",
    "opencl",
    "rocm",
    "sycl",
    "kokkos",
    "blas",
    "lapack",
    "hdf5",
    "adios",
    "lustre",
    "infiniband",
    "rdma",
    "nvshmem",
    "nccl",
    "ucx",
    "slurm",
    "apptainer",
    "singularity",
]

# Precompiled word-boundary regex — critical fix
_SIGNAL_RE = re.compile(
    r"\b(" + "|".join(re.escape(w) for w in HPC_SIGNALS) + r")\b",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------

def gh_get(url, params=None, retries=5):
    for _ in range(retries):
        try:
            r = requests.get(url, headers=HEADERS, params=params, timeout=30)
        except requests.RequestException as e:
            print(f"    network error: {e}, retrying...")
            time.sleep(5)
            continue

        if r.status_code == 403 and "rate limit" in r.text.lower():
            wait = max(
                int(r.headers.get("X-RateLimit-Reset", time.time() + 60))
                - int(time.time()),
                1,
            ) + 2
            print(f"    rate limited, sleeping {wait}s...")
            time.sleep(wait)
            continue
        if r.status_code == 429:
            time.sleep(int(r.headers.get("Retry-After", 60)))
            continue
        if r.status_code == 404:
            return None
        try:
            r.raise_for_status()
        except requests.HTTPError:
            return None
        return r.json()
    return None


def search(query, max_results=MAX_PER_QUERY):
    out = []
    per_page = 100
    for page in range(1, (max_results + per_page - 1) // per_page + 1):
        data = gh_get(f"{API}/search/repositories", params={
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": per_page,
            "page": page,
        })
        if not data or not data.get("items"):
            break
        out.extend(data["items"])
        if len(data["items"]) < per_page:
            break
    return out[:max_results]


# ---------------------------------------------------------------------------
# EXTRACT + FILTER
# ---------------------------------------------------------------------------

def age_days(iso):
    if not iso:
        return 0
    dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return (datetime.now(timezone.utc) - dt).days


def extract(repo):
    lic = (repo.get("license") or {}).get("spdx_id")
    return {
        "name": repo["full_name"],
        "description": repo.get("description"),
        "url": repo["html_url"],
        "stars": repo["stargazers_count"],
        "forks": repo["forks_count"],
        "open_issues": repo.get("open_issues_count"),
        "language": repo.get("language"),
        "topics": repo.get("topics", []),
        "license": lic,
        "has_license": lic not in (None, "NOASSERTION"),
        "archived": repo.get("archived", False),
        "is_fork": repo.get("fork", False),
        "created_at": repo.get("created_at"),
        "pushed_at": repo.get("pushed_at"),
        "age_days": age_days(repo.get("created_at")),
        "days_since_push": age_days(repo.get("pushed_at")),
    }


def is_false_positive(repo):
    """Detect known acronym / word collisions in name + description + topics."""
    text = " ".join(filter(None, [
        repo.get("name"),
        repo.get("description"),
        " ".join(repo.get("topics") or []),
    ]))
    return bool(FP_RE.search(text))


def is_relevant(repo):
    """
    Relevance gate with three tiers:
      1. Explicit HPC topic in the allowlist → accept
      2. 'hpc' as a whole word in name/description → accept
      3. Word-boundary match against HPC_SIGNALS → accept
    Reject everything else.
    """
    if is_false_positive(repo):
        return False

    topics = {t.lower() for t in (repo.get("topics") or [])}

    # Tier 1 — explicit topic
    if topics & HPC_TOPICS:
        return True

    # Tier 2 — 'hpc' as a whole word
    text = " ".join(filter(None, [
        repo.get("name"),
        repo.get("description"),
    ]))
    text_l = text.lower()
    if re.search(r"\bhpc\b", text_l):
        return True

    # Tier 3 — word-boundary signal match
    if _SIGNAL_RE.search(text_l):
        return True
    if _SIGNAL_RE.search(" ".join(topics)):
        return True

    return False


def dedupe(repos):
    seen = {}
    for r in repos:
        key = r["name"].lower()
        if key not in seen or r["stars"] > seen[key]["stars"]:
            seen[key] = r
    return list(seen.values())


# ---------------------------------------------------------------------------
# SCORING  (non-saturating, log-scaled)
# ---------------------------------------------------------------------------

def score(repo):
    stars = repo["stars"]
    age_months = max(repo["age_days"] / 30.0, 0.1)
    velocity = stars / age_months
    days_push = repo["days_since_push"]

    s = 100.0 * math.log1p(stars)
    s += 120.0 * math.log1p(velocity)
    if days_push < 7:
        s += 40
    elif days_push < 30:
        s += 20
    if "hpc" in (repo.get("topics") or []):
        s += 30
    if repo["archived"]:
        s -= 250
    if not repo["has_license"]:
        s -= 10

    return round(s, 1), {
        "stars_per_month": round(velocity, 1),
        "age_months": round(age_months, 1),
        "days_since_push": days_push,
    }


# ---------------------------------------------------------------------------
# PIPELINE
# ---------------------------------------------------------------------------

def collect(queries, label):
    print(f"\n=== {label} ===")
    raw = []
    for q in queries:
        print(f"  q: {q}")
        items = search(q)
        print(f"     -> {len(items)} results")
        raw.extend(extract(r) for r in items)

    print(f"  raw: {len(raw)}")
    raw = dedupe(raw)
    print(f"  after dedupe: {len(raw)}")
    raw = [r for r in raw if is_relevant(r)]
    print(f"  after relevance gate: {len(raw)}")
    return raw


def enrich(repos):
    for r in repos:
        sc, meta = score(r)
        r["score"] = sc
        r["metrics"] = meta
    repos.sort(key=lambda r: r["score"], reverse=True)
    return repos


def save(repos, name):
    OUT_DIR.mkdir(exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = OUT_DIR / f"{name}_{ts}.json"
    path.write_text(
        json.dumps(repos, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"  saved {len(repos)} -> {path}")
    return path


def preview(repos, label, n=15):
    print(f"\n  Top {n} {label}:")
    for r in repos[:n]:
        m = r["metrics"]
        flag = " [archived]" if r["archived"] else ""
        print(f"    {r['score']:>7}  {r['stars']:>6}*  "
              f"{m['stars_per_month']:>6}/mo  {r['name']}{flag}")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    print("HPC one-shot scraper")
    print(f"token: {'yes' if GITHUB_TOKEN else 'NO (10 req/min)'}")

    new_repos = enrich(collect(NEW_QUERIES, "NEW"))
    active_repos = enrich(collect(ACTIVE_QUERIES, "ACTIVE"))

    preview(new_repos, "NEW")
    preview(active_repos, "ACTIVE")

    save(new_repos, "hpc_new")
    save(active_repos, "hpc_active")

    print("\ndone.")


if __name__ == "__main__":
    main()