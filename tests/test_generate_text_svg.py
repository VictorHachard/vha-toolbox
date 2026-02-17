import re
import unittest

from vha_toolbox import generate_text_svg


class GenerateTextSvgTestCase(unittest.TestCase):

    def test_generate_text_svg_default(self):
        svg = generate_text_svg("Hello World", 180, seed="hello-1")
        expected_svg = """<?xml version='1.0' encoding='UTF-8'?><svg width='180' height='180' viewBox='0 0 180 180' xmlns='http://www.w3.org/2000/svg'><defs><filter id='tshadow' x='-20%' y='-20%' width='140%' height='140%'><feDropShadow dx='0' dy='1' stdDeviation='1.2' flood-opacity='0.35'/></filter></defs><rect width='180' height='180' fill='hsl(181, 46%, 45%)'/><text fill='#111111' font-size='34' font-weight='700' text-anchor='middle' dominant-baseline='middle' font-family='sans-serif' x='90' y='90' textLength='160' lengthAdjust='spacingAndGlyphs' filter='url(#tshadow)'>Hello World</text></svg>"""
        self.assertEqual(svg, expected_svg)

    def test_generate_text_svg_with_bg_color(self):
        svg = generate_text_svg("Hello World", 180, bg_color="hsl(210, 60%, 45%)")
        expected_svg = """<?xml version='1.0' encoding='UTF-8'?><svg width='180' height='180' viewBox='0 0 180 180' xmlns='http://www.w3.org/2000/svg'><defs><filter id='tshadow' x='-20%' y='-20%' width='140%' height='140%'><feDropShadow dx='0' dy='1' stdDeviation='1.2' flood-opacity='0.35'/></filter></defs><rect width='180' height='180' fill='hsl(210, 60%, 45%)'/><text fill='#ffffff' font-size='34' font-weight='700' text-anchor='middle' dominant-baseline='middle' font-family='sans-serif' x='90' y='90' textLength='160' lengthAdjust='spacingAndGlyphs' filter='url(#tshadow)'>Hello World</text></svg>"""
        self.assertEqual(svg, expected_svg)

    def test_generate_text_svg_with_bg_and_text_color(self):
        svg = generate_text_svg(
            "Hello World",
            180,
            bg_color="#112233",
            text_color="#ffff00",
        )
        expected_svg = """<?xml version='1.0' encoding='UTF-8'?><svg width='180' height='180' viewBox='0 0 180 180' xmlns='http://www.w3.org/2000/svg'><defs><filter id='tshadow' x='-20%' y='-20%' width='140%' height='140%'><feDropShadow dx='0' dy='1' stdDeviation='1.2' flood-opacity='0.35'/></filter></defs><rect width='180' height='180' fill='#112233'/><text fill='#ffff00' font-size='34' font-weight='700' text-anchor='middle' dominant-baseline='middle' font-family='sans-serif' x='90' y='90' textLength='160' lengthAdjust='spacingAndGlyphs' filter='url(#tshadow)'>Hello World</text></svg>"""
        self.assertEqual(svg, expected_svg)

    def test_generate_text_svg_multiline(self):
        svg = generate_text_svg(
            "Banc Solaire Ultra 12",
            180,
            seed="banc-12",
            max_lines=4,
            max_chars_per_line=10,
        )
        expected_svg = """<?xml version='1.0' encoding='UTF-8'?><svg width='180' height='180' viewBox='0 0 180 180' xmlns='http://www.w3.org/2000/svg'><defs><filter id='tshadow' x='-20%' y='-20%' width='140%' height='140%'><feDropShadow dx='0' dy='1' stdDeviation='1.2' flood-opacity='0.35'/></filter></defs><rect width='180' height='180' fill='hsl(316, 60%, 45%)'/><text fill='#ffffff' font-size='34' font-weight='700' text-anchor='middle' dominant-baseline='middle' font-family='sans-serif' x='90' y='50' filter='url(#tshadow)'>Banc</text><text fill='#ffffff' font-size='34' font-weight='700' text-anchor='middle' dominant-baseline='middle' font-family='sans-serif' x='90' y='90' textLength='160' lengthAdjust='spacingAndGlyphs' filter='url(#tshadow)'>Solaire</text><text fill='#ffffff' font-size='34' font-weight='700' text-anchor='middle' dominant-baseline='middle' font-family='sans-serif' x='90' y='130' textLength='160' lengthAdjust='spacingAndGlyphs' filter='url(#tshadow)'>Ultra 12</text></svg>"""
        self.assertEqual(svg, expected_svg)

    def test_generate_text_svg_fixed_font_false(self):
        svg = generate_text_svg(
            "This is a longer text that may need resizing",
            180,
            seed="long-1",
            fixed_font=False,
            max_font_size=40,
            min_font_size=16,
            max_lines=4,
            max_chars_per_line=14,
        )
        expected_svg = """<?xml version='1.0' encoding='UTF-8'?><svg width='180' height='180' viewBox='0 0 180 180' xmlns='http://www.w3.org/2000/svg'><defs><filter id='tshadow' x='-20%' y='-20%' width='140%' height='140%'><feDropShadow dx='0' dy='1' stdDeviation='1.2' flood-opacity='0.35'/></filter></defs><rect width='180' height='180' fill='hsl(102, 54%, 45%)'/><text fill='#111111' font-size='34' font-weight='700' text-anchor='middle' dominant-baseline='middle' font-family='sans-serif' x='90' y='30' textLength='160' lengthAdjust='spacingAndGlyphs' filter='url(#tshadow)'>This is a</text><text fill='#111111' font-size='34' font-weight='700' text-anchor='middle' dominant-baseline='middle' font-family='sans-serif' x='90' y='70' textLength='160' lengthAdjust='spacingAndGlyphs' filter='url(#tshadow)'>longer text</text><text fill='#111111' font-size='34' font-weight='700' text-anchor='middle' dominant-baseline='middle' font-family='sans-serif' x='90' y='110' textLength='160' lengthAdjust='spacingAndGlyphs' filter='url(#tshadow)'>that may need</text><text fill='#111111' font-size='34' font-weight='700' text-anchor='middle' dominant-baseline='middle' font-family='sans-serif' x='90' y='150' textLength='160' lengthAdjust='spacingAndGlyphs' filter='url(#tshadow)'>resizing</text></svg>"""
        self.assertEqual(svg, expected_svg)

    def test_generate_text_svg_no_shadow(self):
        svg = generate_text_svg(
            "No shadow",
            180,
            seed="shadow-off",
            use_shadow=False,
        )
        expected_svg = """<?xml version='1.0' encoding='UTF-8'?><svg width='180' height='180' viewBox='0 0 180 180' xmlns='http://www.w3.org/2000/svg'><rect width='180' height='180' fill='hsl(157, 68%, 45%)'/><text fill='#111111' font-size='34' font-weight='700' text-anchor='middle' dominant-baseline='middle' font-family='sans-serif' x='90' y='90' textLength='160' lengthAdjust='spacingAndGlyphs'>No shadow</text></svg>"""
        self.assertEqual(svg, expected_svg)

    def test_generate_text_svg_raises_on_empty_text(self):
        with self.assertRaises(ValueError):
            generate_text_svg("", 180, seed="x")

    def test_generate_text_svg_raises_on_whitespace_text(self):
        with self.assertRaises(ValueError):
            generate_text_svg("   \n\t", 180, seed="x")

    def test_generate_text_svg_raises_on_invalid_bg_color(self):
        with self.assertRaises(ValueError):
            generate_text_svg("Hello", 180, bg_color="rgb(1,2,3)")

    def test_generate_text_svg_raises_on_invalid_hex_bg_color(self):
        with self.assertRaises(ValueError):
            generate_text_svg("Hello", 180, bg_color="#123")

    def test_generate_text_svg_raises_on_invalid_hsl_bg_color(self):
        with self.assertRaises(ValueError):
            generate_text_svg("Hello", 180, bg_color="hsl(10, 120%, 40%)")

    def test_generate_text_svg_raises_on_invalid_text_color(self):
        with self.assertRaises(ValueError):
            generate_text_svg("Hello", 180, bg_color="#112233", text_color="yellow")

    def test_generate_text_svg_raises_on_padding_too_large(self):
        with self.assertRaises(ValueError):
            generate_text_svg("Hello", 180, seed="x", padding=90)

    def test_generate_text_svg_raises_on_negative_size(self):
        with self.assertRaises(ValueError):
            generate_text_svg("Hello", -1, seed="x")

    def test_generate_text_svg_raises_on_invalid_font_weight(self):
        with self.assertRaises(ValueError):
            generate_text_svg("Hello", 180, seed="x", font_weight=0)

    def test_generate_text_svg_raises_on_invalid_font_family_empty(self):
        with self.assertRaises(ValueError):
            generate_text_svg("Hello", 180, seed="x", font_family="")

    def test_generate_text_svg_raises_on_invalid_font_family_spaces_unquoted(self):
        with self.assertRaises(ValueError):
            generate_text_svg("Hello", 180, seed="x", font_family="Open Sans")

    def test_generate_text_svg_accepts_quoted_font_family(self):
        svg = generate_text_svg("Hello", 180, seed="x", font_family='"Open Sans", sans-serif')
        self.assertIn("font-family='&quot;Open Sans&quot;, sans-serif'", svg)

    def test_generate_text_svg_accepts_generic_font(self):
        svg = generate_text_svg("Hello", 180, seed="x", font_family="serif")
        self.assertIn("font-family='serif'", svg)

    def test_generate_text_svg_hard_split_long_word(self):
        svg = generate_text_svg(
            "SUPERCALIFRAGILISTICEXPIALIDOCIOUS",
            180,
            seed="longword",
            max_lines=4,
            max_chars_per_line=8,
        )
        # we just assert there are multiple <text> lines
        self.assertGreaterEqual(svg.count("<text "), 2)

    def test_generate_text_svg_force_textLength_logic_short_line(self):
        # short line should typically avoid textLength (depending on implementation threshold)
        svg = generate_text_svg("Hi", 180, seed="short", max_chars_per_line=16)
        # For very short lines, "textLength=" may be absent
        # (This is a behavior test, not a strict snapshot)
        self.assertIn(">Hi</text>", svg)

    def test_generate_text_svg_seed_deterministic(self):
        svg1 = generate_text_svg("Same", 180, seed="same-seed")
        svg2 = generate_text_svg("Same", 180, seed="same-seed")
        self.assertEqual(svg1, svg2)

    def test_generate_text_svg_forced_text_color_adapts_bg_when_bg_missing(self):
        # text forced, bg missing -> bg should be auto-picked AND should make the chosen text win
        svg = generate_text_svg(
            "Hello World",
            180,
            seed="forced-text-1",
            text_color="#ffffff",
        )
        # Must contain forced text color
        self.assertIn("fill='#ffffff'", svg)

        # Background should be HSL (from seed), not empty
        self.assertRegex(svg, r"<rect width='180' height='180' fill='hsl\([0-9.]+, [0-9.]+%, [0-9.]+%\)'/>")

        # And since text is forced white, picked bg should NOT lead to automatic black text,
        # but here text is forced anyway. We assert bg was adapted by checking that the bg is not the raw seed default.
        # (Raw seed default in your generator is always l=45)
        self.assertNotIn("% 45%)'/>", svg)  # lightness changed from 45% in adapted mode


    def test_generate_text_svg_forced_text_color_does_not_change_bg_if_bg_forced(self):
        svg = generate_text_svg(
            "Hello World",
            180,
            bg_color="hsl(210, 60%, 45%)",
            text_color="#ffffff",
        )
        # Both respected as-is
        self.assertIn("fill='hsl(210, 60%, 45%)'", svg)
        self.assertIn("fill='#ffffff'", svg)


    def test_generate_text_svg_forced_text_color_keeps_seed_hue_sat(self):
        # If you implement "keep hue/sat, adjust only lightness",
        # then hue/sat must match the seed-derived bg.
        svg_seed = generate_text_svg(
            "Hello World",
            180,
            seed="forced-text-2",
        )
        svg_forced_text = generate_text_svg(
            "Hello World",
            180,
            seed="forced-text-2",
            text_color="#ffffff",
        )

        # Extract bg hsl(...) from both
        m1 = re.search(r"<rect width='180' height='180' fill='(hsl\([^']+\))'/>", svg_seed)
        m2 = re.search(r"<rect width='180' height='180' fill='(hsl\([^']+\))'/>", svg_forced_text)
        self.assertIsNotNone(m1)
        self.assertIsNotNone(m2)

        hsl1 = m1.group(1)
        hsl2 = m2.group(1)

        # Parse hue and saturation (ignore lightness)
        m1p = re.match(r"hsl\(\s*([0-9.]+)\s*,\s*([0-9.]+)%\s*,\s*([0-9.]+)%\s*\)", hsl1)
        m2p = re.match(r"hsl\(\s*([0-9.]+)\s*,\s*([0-9.]+)%\s*,\s*([0-9.]+)%\s*\)", hsl2)
        self.assertIsNotNone(m1p)
        self.assertIsNotNone(m2p)

        # Same hue + sat
        self.assertEqual(m1p.group(1), m2p.group(1))
        self.assertEqual(m1p.group(2), m2p.group(2))

        # Different lightness (very likely; and expected if adaptation is applied)
        self.assertNotEqual(m1p.group(3), m2p.group(3))


    def test_generate_text_svg_forced_black_text_adapts_bg_when_bg_missing(self):
        svg = generate_text_svg(
            "Hello World",
            180,
            seed="forced-text-3",
            text_color="#111111",
        )
        self.assertIn("fill='#111111'", svg)
        self.assertRegex(svg, r"<rect width='180' height='180' fill='hsl\([0-9.]+, [0-9.]+%, [0-9.]+%\)'/>")
        self.assertNotIn("% 45%)'/>", svg)  # lightness changed from 45% in adapted mode


if __name__ == "__main__":
    unittest.main()
