import html
import re
from dataclasses import dataclass
from hashlib import sha512
from typing import List, Optional, Tuple


# ----------------------------
# Validators
# ----------------------------
_HEX_COLOR_RE = re.compile(r"^\s*#([0-9a-fA-F]{6})\s*$")
_HSL_RE = re.compile(
    r"^\s*hsl\(\s*([0-9.]+)\s*,\s*([0-9.]+)%\s*,\s*([0-9.]+)%\s*\)\s*$"
)
_CSS_IDENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*$")


def _is_finite_number(x) -> bool:
    try:
        return x == x and x not in (float("inf"), float("-inf"))
    except Exception:
        return False


def _validate_positive_int(name: str, value: int, min_value: int = 1) -> int:
    if not isinstance(value, int):
        raise ValueError(f"{name} must be an int, got {type(value).__name__}")
    if value < min_value:
        raise ValueError(f"{name} must be >= {min_value}, got {value}")
    return value


def _validate_positive_number(name: str, value: float, min_value: float = 0.0) -> float:
    if not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a number, got {type(value).__name__}")
    if not _is_finite_number(float(value)):
        raise ValueError(f"{name} must be finite, got {value}")
    if float(value) < min_value:
        raise ValueError(f"{name} must be >= {min_value}, got {value}")
    return float(value)


def _validate_color(name: str, color: str) -> str:
    if not isinstance(color, str) or not color.strip():
        raise ValueError(f"{name} must be a non-empty string")
    c = color.strip()

    if _HEX_COLOR_RE.match(c):
        return c.lower()

    m = _HSL_RE.match(c.lower())
    if m:
        h = float(m.group(1))
        s = float(m.group(2))
        l = float(m.group(3))

        if not (_is_finite_number(h) and _is_finite_number(s) and _is_finite_number(l)):
            raise ValueError(f"{name} contains non-finite numbers: {color}")

        if s < 0 or s > 100:
            raise ValueError(f"{name} saturation must be in [0,100], got {s}")
        if l < 0 or l > 100:
            raise ValueError(f"{name} lightness must be in [0,100], got {l}")
        # Hue can wrap (CSS allows any number), so we accept any finite hue.
        return f"hsl({h:.0f}, {s:.0f}%, {l:.0f}%)"

    raise ValueError(f"{name} must be '#rrggbb' or 'hsl(h, s%, l%)', got: {color}")


# Minimal “font-family exists” checker.
# In CSS/SVG, you cannot reliably check system fonts at runtime without a renderer.
# So we enforce: either a generic family or a syntactically valid list.
_GENERIC_FONTS = {"serif", "sans-serif", "monospace", "cursive", "fantasy", "system-ui"}


def _validate_font_family(font_family: str) -> str:
    if not isinstance(font_family, str) or not font_family.strip():
        raise ValueError("font_family must be a non-empty string")

    ff = font_family.strip()

    # Allow comma-separated list: e.g. "Inter, sans-serif"
    parts = [p.strip() for p in ff.split(",") if p.strip()]
    if not parts:
        raise ValueError("font_family must contain at least one font name")

    for p in parts:
        pl = p.lower()
        if pl in _GENERIC_FONTS:
            continue

        # Allow quoted font names: "Open Sans"
        if (p.startswith('"') and p.endswith('"')) or (p.startswith("'") and p.endswith("'")):
            inner = p[1:-1].strip()
            if not inner:
                raise ValueError(f"Invalid quoted font name in font_family: {p}")
            continue

        # Unquoted font: must be a CSS identifier (no spaces).
        if not _CSS_IDENT_RE.match(p):
            raise ValueError(
                f"Invalid font name '{p}'. Use quotes for spaces, e.g. \"Open Sans\"."
            )

    return ff


def _validate_font_weight(font_weight: int) -> int:
    if not isinstance(font_weight, int):
        raise ValueError(f"font_weight must be int, got {type(font_weight).__name__}")
    if font_weight < 1 or font_weight > 1000:
        raise ValueError(f"font_weight must be in [1,1000], got {font_weight}")
    return font_weight


# ----------------------------
# Colors
# ----------------------------
def get_hsl_from_seed(seed: str) -> str:
    """
    Generate a deterministic HSL color from a seed (Odoo-like idea).
    """
    if not isinstance(seed, str) or not seed:
        raise ValueError("seed must be a non-empty string")
    hashed = sha512(seed.encode("utf-8")).hexdigest()
    hue = int(hashed[0:2], 16) * 360 / 255
    sat = int(hashed[2:4], 16) * ((70 - 40) / 255) + 40
    lig = 45
    return f"hsl({hue:.0f}, {sat:.0f}%, {lig:.0f}%)"


def _parse_hsl(hsl: str) -> Tuple[float, float, float]:
    m = _HSL_RE.match(hsl)
    if not m:
        raise ValueError(f"Invalid HSL: {hsl}")
    return float(m.group(1)), float(m.group(2)), float(m.group(3))


def _hsl_to_rgb(h: float, s: float, l: float) -> Tuple[int, int, int]:
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
    bg_color = _validate_color("bg_color", bg_color)

    bg_rgb: Tuple[int, int, int]
    if bg_color.lower().startswith("hsl("):
        h, s, l = _parse_hsl(bg_color.lower())
        bg_rgb = _hsl_to_rgb(h, s, l)
    else:
        m = _HEX_COLOR_RE.match(bg_color)
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
# Text splitting
# ----------------------------
_WORD_RE = re.compile(r"\s+", flags=re.UNICODE)


def split_text_for_svg(text: str, max_lines: int, max_chars_per_line: int) -> List[str]:
    _validate_positive_int("max_lines", int(max_lines), 1)
    _validate_positive_int("max_chars_per_line", int(max_chars_per_line), 1)

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
        return [w[i:i + max_chars_per_line] for i in range(0, len(w), max_chars_per_line)]

    for w in words:
        if len(w) > max_chars_per_line:
            flush()
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
    bg_color: Optional[str] = None
    text_color: Optional[str] = None
    fixed_font: bool = True
    fixed_font_size: int = 34
    max_font_size: int = 40
    min_font_size: int = 16
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
        max_lines: splitting rule (maximum number of lines)
        max_chars_per_line: splitting rule (maximum characters per line)
        fixed_font: if True, keep font-size fixed and use textLength to fit width
        fixed_font_size: used when fixed_font=True
        max_font_size: used when fixed_font=False (starting font size)
        min_font_size: used when fixed_font=False (minimum font size)
        font_family: font family (CSS/SVG font-family)
        font_weight: font weight
        use_shadow: adds a subtle shadow for readability

    Returns:
        SVG string (utf-8, xml header included).

    Examples:
        >>> svg = generate_text_svg("Hello World", size=180)
        >>> print(svg)  # SVG string with "Hello World" centered

        >>> svg = generate_text_svg("This is a longer text that should wrap into multiple lines", size=180, max_lines=3, max_chars_per_line=20)
        >>> print(svg)  # SVG string with wrapped text

        >>> svg = generate_text_svg("Short", size=180, bg_color="#ff0000", text_color="#00ff00")
        >>> print(svg)  # SVG string with red background and green text

    Raises:
        ValueError: if text is empty or if color formats are invalid.
        ValueError: if the seed is empty or not a string.
        ValueError: if a parameter expected to be an integer is not an integer.
        ValueError: if an integer parameter is lower than the allowed minimum value.
        ValueError: if a parameter expected to be a number is not numeric.
        ValueError: if a numeric parameter is not finite (NaN or infinite).
        ValueError: if a color value is empty or not a string.
        ValueError: if a color format is invalid (not #rrggbb or hsl(h, s%, l%)).
        ValueError: if HSL saturation is outside the range 0–100.
        ValueError: if HSL lightness is outside the range 0–100.
        ValueError: if the font family is empty or not a valid CSS font-family definition.
        ValueError: if a font name is invalid or contains spaces without quotes.
        ValueError: if the font weight is not an integer.
        ValueError: if the font weight is outside the range 1–1000.
        ValueError: if the input text is empty after trimming.
        ValueError: if padding is too large compared to the SVG size.
        ValueError: if the text color is provided but is not a valid hexadecimal color.
        ValueError: if no background color is provided and the seed is missing or invalid.
    """
    text = (text or "").strip()
    if not text:
        raise ValueError("Text must be non-empty")

    size = _validate_positive_int("size", int(size), 1)
    padding = _validate_positive_int("padding", int(padding), 0)
    max_lines = _validate_positive_int("max_lines", int(max_lines), 1)
    max_chars_per_line = _validate_positive_int("max_chars_per_line", int(max_chars_per_line), 1)
    font_weight = _validate_font_weight(font_weight)
    font_family = _validate_font_family(font_family)

    if padding * 2 >= size:
        raise ValueError(f"padding too large: padding*2 ({padding*2}) must be < size ({size})")

    if bg_color is not None:
        bg_color = _validate_color("bg_color", bg_color)

    if text_color is not None:
        text_color = _validate_color("text_color", text_color)
        # enforce hex-only for text color if you want; comment this out if you want HSL for text too
        if not _HEX_COLOR_RE.match(text_color):
            raise ValueError("text_color must be '#rrggbb' (hex)")

    if bg_color is None:
        seed_val = seed if seed is not None else text
        if not isinstance(seed_val, str) or not seed_val:
            raise ValueError("seed must be a non-empty string when bg_color is not provided")
        bg_color = get_hsl_from_seed(seed_val)

    if text_color is None:
        text_color = pick_text_color_for_bg(bg_color)

    content_w = size - 2 * padding
    content_h = size - 2 * padding

    lines = split_text_for_svg(text, max_lines=max_lines, max_chars_per_line=max_chars_per_line)
    n = len(lines)

    if fixed_font:
        fixed_font_size = _validate_positive_int("fixed_font_size", int(fixed_font_size), 1)
        font_size = fixed_font_size
        line_height = int(round(font_size * 1.18))
    else:
        max_font_size = _validate_positive_int("max_font_size", int(max_font_size), 1)
        min_font_size = _validate_positive_int("min_font_size", int(min_font_size), 1)
        if min_font_size > max_font_size:
            raise ValueError("min_font_size must be <= max_font_size")

        font_size = max_font_size
        while font_size > min_font_size:
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
            f"font-weight='{font_weight}' "
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
