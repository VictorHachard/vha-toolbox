import html
import re
from dataclasses import dataclass
from hashlib import sha512
from typing import List, Optional, Tuple


# ----------------------------
# Colors
# ----------------------------
def get_hsl_from_seed(seed: str) -> str:
    """
    Generate a deterministic HSL color from a seed (Odoo-like idea).
    """
    hashed = sha512(seed.encode("utf-8")).hexdigest()
    hue = int(hashed[0:2], 16) * 360 / 255
    sat = int(hashed[2:4], 16) * ((70 - 40) / 255) + 40
    lig = 45
    return f"hsl({hue:.0f}, {sat:.0f}%, {lig:.0f}%)"


def _parse_hsl(hsl: str) -> Tuple[float, float, float]:
    m = re.match(r"^\s*hsl\(\s*([0-9.]+)\s*,\s*([0-9.]+)%\s*,\s*([0-9.]+)%\s*\)\s*$", hsl)
    if not m:
        raise ValueError(f"Invalid HSL: {hsl}")
    return float(m.group(1)), float(m.group(2)), float(m.group(3))


def _hsl_to_rgb(h: float, s: float, l: float) -> Tuple[int, int, int]:
    """
    h: 0..360, s/l: 0..100
    """
    h = (h % 360) / 360.0
    s = max(0.0, min(1.0, s / 100.0))
    l = max(0.0, min(1.0, l / 100.0))

    def hue2rgb(p: float, q: float, t: float) -> float:
        if t < 0:
            t += 1
        if t > 1:
            t -= 1
        if t < 1 / 6:
            return p + (q - p) * 6 * t
        if t < 1 / 2:
            return q
        if t < 2 / 3:
            return p + (q - p) * (2 / 3 - t) * 6
        return p

    if s == 0:
        r = g = b = l
    else:
        q = l * (1 + s) if l < 0.5 else l + s - l * s
        p = 2 * l - q
        r = hue2rgb(p, q, h + 1 / 3)
        g = hue2rgb(p, q, h)
        b = hue2rgb(p, q, h - 1 / 3)

    return int(round(r * 255)), int(round(g * 255)), int(round(b * 255))


def _srgb_to_linear(c: float) -> float:
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _relative_luminance(rgb: Tuple[int, int, int]) -> float:
    r, g, b = rgb
    r_lin = _srgb_to_linear(r)
    g_lin = _srgb_to_linear(g)
    b_lin = _srgb_to_linear(b)
    return 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin


def _contrast_ratio(rgb1: Tuple[int, int, int], rgb2: Tuple[int, int, int]) -> float:
    l1 = _relative_luminance(rgb1)
    l2 = _relative_luminance(rgb2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def pick_text_color_for_bg(bg_color: str, prefer_white: bool = True) -> str:
    """
    Picks '#ffffff' or '#111111' based on contrast with bg_color.
    Supports: 'hsl(...)' or '#rrggbb'.
    """
    bg_rgb: Tuple[int, int, int]
    if bg_color.strip().lower().startswith("hsl("):
        h, s, l = _parse_hsl(bg_color)
        bg_rgb = _hsl_to_rgb(h, s, l)
    else:
        m = re.match(r"^\s*#([0-9a-fA-F]{6})\s*$", bg_color)
        if not m:
            raise ValueError(f"Unsupported color format: {bg_color}")
        hx = m.group(1)
        bg_rgb = (int(hx[0:2], 16), int(hx[2:4], 16), int(hx[4:6], 16))

    white = (255, 255, 255)
    dark = (17, 17, 17)

    c_white = _contrast_ratio(bg_rgb, white)
    c_dark = _contrast_ratio(bg_rgb, dark)

    if c_white == c_dark:
        return "#ffffff" if prefer_white else "#111111"
    return "#ffffff" if c_white > c_dark else "#111111"


# ----------------------------
# Text splitting (good defaults)
# ----------------------------
_WORD_RE = re.compile(r"\s+", flags=re.UNICODE)


def split_text_for_svg(
        text: str,
        max_lines: int,
        max_chars_per_line: int,
) -> List[str]:
    """
    Robust splitting:
    - normalize spaces
    - greedily pack words
    - if a single word is too long, hard-split it
    """
    t = (text or "").strip()
    if not t:
        return [""]

    t = _WORD_RE.sub(" ", t)
    words: List[str] = t.split(" ")

    lines: List[str] = []
    cur = ""

    def flush():
        nonlocal cur
        if cur:
            lines.append(cur)
            cur = ""

    def hard_split_long_word(w: str) -> List[str]:
        chunks = []
        for i in range(0, len(w), max_chars_per_line):
            chunks.append(w[i : i + max_chars_per_line])
        return chunks

    for w in words:
        if len(w) > max_chars_per_line:
            # push current line first
            flush()
            # split long word into multiple lines
            for chunk in hard_split_long_word(w):
                lines.append(chunk)
                if len(lines) >= max_lines:
                    return lines[:max_lines]
            continue

        candidate = w if not cur else f"{cur} {w}"
        if len(candidate) <= max_chars_per_line:
            cur = candidate
        else:
            flush()
            cur = w
            if len(lines) >= max_lines:
                return lines[:max_lines]

    flush()
    return lines[:max_lines] if lines else [""]


# ----------------------------
# SVG generator
# ----------------------------
@dataclass(frozen=True)
class SvgTextOptions:
    size: int = 180
    padding: int = 10
    max_lines: int = 4
    max_chars_per_line: int = 16

    font_family: str = "sans-serif"
    font_weight: int = 700

    # If provided: will not be changed
    bg_color: Optional[str] = None

    # If provided: will not be changed
    text_color: Optional[str] = None

    # If True: keep font-size fixed and use textLength condensing.
    # If False: will adapt font-size down if needed.
    fixed_font: bool = True

    # If fixed_font is True, use this font size.
    fixed_font_size: int = 34

    # If fixed_font is False, it will start from this and go down.
    max_font_size: int = 40
    min_font_size: int = 16

    # Extra: show a subtle overlay for readability on some backgrounds
    use_shadow: bool = True


def generate_text_svg(
        text: str,
        size: int = 180,
        *,
        seed: Optional[str] = None,
        bg_color: Optional[str] = None,
        text_color: Optional[str] = None,
        padding: int = 10,
        max_lines: int = 4,
        max_chars_per_line: int = 16,
        fixed_font: bool = True,
        fixed_font_size: int = 34,
        max_font_size: int = 40,
        min_font_size: int = 16,
        font_family: str = "sans-serif",
        font_weight: int = 700,
        use_shadow: bool = True,
) -> str:
    """
    Generate an SVG string with best-effort text placement.

    Args:
        text: displayed text
        size: svg width/height in px (square)
        seed: if bg_color not provided, used to pick deterministic HSL background
        bg_color: optional background color (hsl(...) or #rrggbb)
        text_color: optional text color (#rrggbb). If not provided, chosen by contrast.
        padding: inner padding
        max_lines / max_chars_per_line: splitting rules
        fixed_font: if True, keep font-size fixed and use textLength to fit width
        fixed_font_size: used when fixed_font=True
        max_font_size/min_font_size: used when fixed_font=False
        font_family/font_weight: styling
        use_shadow: adds a subtle shadow for readability

    Returns:
        SVG string (utf-8, xml header included).
    """
    text = (text or "").strip() or "Text"

    if bg_color is None:
        seed_val = seed if seed is not None else text
        bg_color = get_hsl_from_seed(seed_val)

    if text_color is None:
        text_color = pick_text_color_for_bg(bg_color)

    pad = int(padding)
    size = int(size)
    content_w = size - 2 * pad
    content_h = size - 2 * pad

    # Split lines
    lines = split_text_for_svg(text, max_lines=max_lines, max_chars_per_line=max_chars_per_line)
    n = len(lines)

    # Determine font size + line height
    if fixed_font:
        font_size = int(fixed_font_size)
        line_height = int(round(font_size * 1.18))
    else:
        # crude heuristic: start high, reduce until height fits (width handled by textLength anyway)
        font_size = int(max_font_size)
        while font_size > int(min_font_size):
            line_height = int(round(font_size * 1.18))
            if n * line_height <= content_h:
                break
            font_size -= 1
        line_height = int(round(font_size * 1.18))

    # If still too tall, reduce number of lines (keep first lines)
    while n * line_height > content_h and n > 1:
        lines = lines[:-1]
        n = len(lines)

    total_h = n * line_height
    start_y = (size / 2.0) - (total_h / 2.0) + (line_height / 2.0)

    # Optional shadow via filter (cheap, works well)
    defs = ""
    shadow_attr = ""
    if use_shadow:
        defs = (
            "<defs>"
            "<filter id='tshadow' x='-20%' y='-20%' width='140%' height='140%'>"
            "<feDropShadow dx='0' dy='1' stdDeviation='1.2' flood-opacity='0.35'/>"
            "</filter>"
            "</defs>"
        )
        shadow_attr = " filter='url(#tshadow)'"

    # Build <text> nodes
    text_nodes: List[str] = []
    for i, line in enumerate(lines):
        y = start_y + i * line_height
        escaped = html.escape(line)

        # textLength ensures it fits in width without changing font-size.
        # It can compress glyphs slightly (lengthAdjust=spacingAndGlyphs).
        # If line is short, we don't force textLength (prevents weird stretched look).
        force_length = len(line) >= max(6, max_chars_per_line // 2)

        attrs = (
            f"fill='{text_color}' "
            f"font-size='{font_size}' "
            f"font-weight='{int(font_weight)}' "
            "text-anchor='middle' "
            "dominant-baseline='middle' "
            f"font-family='{html.escape(font_family)}' "
            f"x='{size/2:.0f}' y='{y:.0f}'"
        )

        if force_length:
            attrs += f" textLength='{content_w:.0f}' lengthAdjust='spacingAndGlyphs'"

        text_nodes.append(f"<text {attrs}{shadow_attr}>{escaped}</text>")

    svg = (
        "<?xml version='1.0' encoding='UTF-8'?>"
        f"<svg width='{size}' height='{size}' viewBox='0 0 {size} {size}' "
        "xmlns='http://www.w3.org/2000/svg'>"
        f"{defs}"
        f"<rect width='{size}' height='{size}' fill='{bg_color}'/>"
        f"{''.join(text_nodes)}"
        "</svg>"
    )

    return svg
