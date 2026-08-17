"""
Canonical sector_group taxonomy for the VeeRock/ZembiHF signal site.

sector_group is website-facing grouping metadata, not derived from any
per-ticker model script — it's set directly by whichever process writes a
ticker's JSON. Nothing enforced consistency, so casing/naming drifted
("Energy" vs "energy", "Finance" vs "Financials") and each variant became
its own orphan group instead of joining the real one. This module is the
single source of truth other scripts should normalize against.
"""

CANONICAL_SECTOR_GROUPS = [
    "Technology",
    "Consumer Discretionary",
    "Consumer Staples",
    "Industrials",
    "Finance",
    "Healthcare",
    "Utilities",
    "Energy",
    "Basic Resources",
    "Materials",
    "Telecoms/Media",
    "Bonds",
]

# Known bad variants seen in the wild -> canonical value.
_ALIASES = {
    "financials": "Finance",
    "financial": "Finance",
    "utilities": "Utilities",
    "energy": "Energy",
    "materials": "Materials",
    "material": "Materials",
    "telecom": "Telecoms/Media",
    "telecoms": "Telecoms/Media",
    "media": "Telecoms/Media",
    "technology": "Technology",
    "tech": "Technology",
    "industrials": "Industrials",
    "industrial": "Industrials",
    "healthcare": "Healthcare",
    "health care": "Healthcare",
    "consumer discretionary": "Consumer Discretionary",
    "consumer staples": "Consumer Staples",
    "basic resources": "Basic Resources",
    "bonds": "Bonds",
    "bond": "Bonds",
}

_CANONICAL_LOOKUP = {s.lower(): s for s in CANONICAL_SECTOR_GROUPS}


def normalize_sector_group(value: str) -> tuple[str | None, bool]:
    """
    Returns (normalized_value, was_changed).
    normalized_value is None if the input doesn't match any canonical
    value or known alias, even case-insensitively — caller should treat
    that as a hard validation failure, not silently pass it through.
    """
    if value is None:
        return None, False
    stripped = value.strip()
    if stripped in CANONICAL_SECTOR_GROUPS:
        return stripped, False
    key = stripped.lower()
    if key in _CANONICAL_LOOKUP:
        return _CANONICAL_LOOKUP[key], True
    if key in _ALIASES:
        return _ALIASES[key], True
    return None, False
