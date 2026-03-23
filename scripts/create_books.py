"""Utility script to seed the DevOps Book API with sample books."""

import argparse
import json
from pathlib import Path
from typing import Iterable, List, Optional
from urllib import error, request

SAMPLE_BOOKS = [
    {"id": 1, "title": "DevOps Handbook", "author": "Gene Kim", "published_year": 2016},
    {"id": 2, "title": "Site Reliability Engineering", "author": "Betsy Beyer", "published_year": 2016},
    {"id": 3, "title": "Accelerate", "author": "Nicole Forsgren", "published_year": 2018},
    {"id": 4, "title": "Team Topologies", "author": "Matthew Skelton", "published_year": 2019},
]


def load_books(path: Optional[Path]) -> List[dict]:
    if not path:
        return SAMPLE_BOOKS
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
        if not isinstance(data, list):
            raise ValueError("Expected a JSON list of book objects")
        return data


def post_book(base_url: str, payload: dict) -> tuple[int, str]:
    url = base_url.rstrip("/") + "/books/"
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with request.urlopen(req) as resp:
            body = resp.read().decode("utf-8")
            return resp.status, body
    except error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8")
    except error.URLError as exc:
        raise SystemExit(f"Failed to reach API at {url}: {exc.reason}") from exc


def seed_books(base_url: str, books: Iterable[dict]) -> None:
    payloads = list(books)
    print(f"Seeding {len(payloads)} books against {base_url}...")
    for payload in payloads:
        status, body = post_book(base_url, payload)
        title = payload.get("title", payload.get("id"))
        if status == 200:
            print(f"[OK] Created '{title}'")
        elif status == 400:
            print(f"[WARN] Skipped '{title}' (already exists)")
        else:
            print(f"[ERR] Failed to create '{title}' (status {status}): {body}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Seed the DevOps Book API with sample data.")
    parser.add_argument(
        "--base-url",
        default="http://localhost:8000",
        help="FastAPI base URL (default: http://localhost:8000)",
    )
    parser.add_argument(
        "--books-file",
        type=Path,
        help="Optional path to a JSON file containing an array of book objects.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    books = load_books(args.books_file)
    seed_books(args.base_url, books)


if __name__ == "__main__":
    main()
# *** End Patch