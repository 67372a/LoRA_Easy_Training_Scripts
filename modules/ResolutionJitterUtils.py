"""Shared helpers for resolution jitter UI fields.

Resolution jitter is configured with three comma-separated numeric lists
(resolutions, batch sizes, weights) stored under flat dataset/subset keys.
"""

RESOLUTION_JITTER_KEYS = (
    "resolution_jitter_resolutions",
    "resolution_jitter_batch_sizes",
    "resolution_jitter_weights",
)


def parse_number_list(text: str, cast=float) -> list:
    """Parse a comma-separated numeric string into a list. Empty text -> empty list."""
    values = []
    for part in text.replace(" ", "").split(","):
        if part == "":
            continue
        values.append(cast(part))
    return values


def format_number_list(values) -> str:
    """Format a numeric list (or None) as a comma-separated string for display."""
    if values is None:
        return ""
    if isinstance(values, (int, float)):
        values = [values]
    return ", ".join(str(v) for v in values)


def jitter_config_is_valid(resolutions: list, batch_sizes: list, weights: list) -> bool:
    """Validate parsed jitter lists: equal non-zero lengths and positive values."""
    if not resolutions or not batch_sizes or not weights:
        return False
    if not (len(resolutions) == len(batch_sizes) == len(weights)):
        return False
    if any(not isinstance(r, int) or isinstance(r, bool) or r <= 0 for r in resolutions):
        return False
    if any(not isinstance(b, int) or isinstance(b, bool) or b < 1 for b in batch_sizes):
        return False
    if any(not isinstance(w, (int, float)) or isinstance(w, bool) or w <= 0 for w in weights):
        return False
    return True
