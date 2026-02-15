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


if __name__ == "__main__":
    unittest.main()
