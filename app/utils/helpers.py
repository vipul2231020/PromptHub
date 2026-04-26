from typing import List, Optional
import re


def clean_text(text: str) -> str:
    """Remove extra whitespace and normalize text."""
    return re.sub(r'\s+', ' ', text.strip())


def truncate_text(text: str, max_length: int = 200) -> str:
    """Truncate text to max_length with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def parse_tags(tags_input: str) -> List[str]:
    """Parse comma-separated tags string to list."""
    if not tags_input:
        return []
    return [tag.strip().lower() for tag in tags_input.split(",") if tag.strip()]


def build_pagination_response(
    data: list,
    total: int,
    skip: int,
    limit: int,
) -> dict:
    """Build standardized pagination response."""
    return {
        "data": data,
        "total": total,
        "skip": skip,
        "limit": limit,
        "has_more": (skip + limit) < total,
    }
