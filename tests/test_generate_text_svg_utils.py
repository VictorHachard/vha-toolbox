import re
import unittest

from vha_toolbox.generate_text_svg import get_hsl_from_seed, pick_text_color_for_bg, split_text_for_svg


class GetHslFromSeedTestCase(unittest.TestCase):
    def test_deterministic(self):
        self.assertEqual(get_hsl_from_seed("hello"), get_hsl_from_seed("hello"))

    def test_different_seeds_give_different_colors(self):
        self.assertNotEqual(get_hsl_from_seed("hello"), get_hsl_from_seed("world"))

    def test_output_format(self):
        result = get_hsl_from_seed("test")
        self.assertRegex(result, r"^hsl\(\d+, \d+%, 45%\)$")

    def test_lightness_always_45(self):
        for seed in ["a", "abc", "long seed value", "123"]:
            self.assertIn("45%)", get_hsl_from_seed(seed))

    def test_empty_seed_raises(self):
        with self.assertRaises(ValueError):
            get_hsl_from_seed("")

    def test_non_string_raises(self):
        with self.assertRaises((ValueError, AttributeError)):
            get_hsl_from_seed(123)


class PickTextColorForBgTestCase(unittest.TestCase):
    def test_black_bg_returns_white(self):
        self.assertEqual(pick_text_color_for_bg("#000000"), "#ffffff")

    def test_white_bg_returns_dark(self):
        self.assertEqual(pick_text_color_for_bg("#ffffff"), "#111111")

    def test_dark_gray_returns_white(self):
        self.assertEqual(pick_text_color_for_bg("#333333"), "#ffffff")

    def test_light_gray_returns_dark(self):
        self.assertEqual(pick_text_color_for_bg("#cccccc"), "#111111")

    def test_hsl_black_returns_white(self):
        self.assertEqual(pick_text_color_for_bg("hsl(0, 0%, 0%)"), "#ffffff")

    def test_hsl_white_returns_dark(self):
        self.assertEqual(pick_text_color_for_bg("hsl(0, 0%, 100%)"), "#111111")

    def test_hsl_dark_returns_white(self):
        self.assertEqual(pick_text_color_for_bg("hsl(200, 80%, 20%)"), "#ffffff")

    def test_hsl_light_returns_dark(self):
        self.assertEqual(pick_text_color_for_bg("hsl(200, 80%, 85%)"), "#111111")

    def test_invalid_color_raises(self):
        with self.assertRaises(ValueError):
            pick_text_color_for_bg("red")

    def test_invalid_rgb_raises(self):
        with self.assertRaises(ValueError):
            pick_text_color_for_bg("rgb(0, 0, 0)")

    def test_returns_one_of_two_valid_colors(self):
        result = pick_text_color_for_bg("#888888")
        self.assertIn(result, ("#ffffff", "#111111"))


class SplitTextForSvgTestCase(unittest.TestCase):
    def test_short_text_stays_one_line(self):
        self.assertEqual(split_text_for_svg("Hello", 4, 16), ["Hello"])

    def test_text_wraps_at_max_chars(self):
        result = split_text_for_svg("Hello World", 4, 6)
        self.assertEqual(result, ["Hello", "World"])

    def test_respects_max_lines(self):
        result = split_text_for_svg("one two three four five", 2, 10)
        self.assertEqual(len(result), 2)

    def test_hard_splits_long_word(self):
        result = split_text_for_svg("ABCDEFGH", 4, 4)
        self.assertEqual(result, ["ABCD", "EFGH"])

    def test_long_word_capped_by_max_lines(self):
        result = split_text_for_svg("SUPERCALIFRAGILISTIC", 4, 5)
        self.assertEqual(result, ["SUPER", "CALIF", "RAGIL", "ISTIC"])

    def test_empty_text_returns_one_empty_string(self):
        self.assertEqual(split_text_for_svg("", 4, 16), [""])

    def test_whitespace_only_returns_one_empty_string(self):
        self.assertEqual(split_text_for_svg("   ", 4, 16), [""])

    def test_multiple_spaces_treated_as_single_space(self):
        result = split_text_for_svg("hello   world", 4, 16)
        self.assertEqual(result, ["hello world"])

    def test_words_packed_greedily_on_same_line(self):
        # "one two" = 7 chars ≤ 10, so they share a line
        result = split_text_for_svg("one two three", 4, 10)
        self.assertEqual(result[0], "one two")

    def test_multiline_result_count(self):
        result = split_text_for_svg("a b c d e f g h", 4, 3)
        self.assertLessEqual(len(result), 4)


if __name__ == '__main__':
    unittest.main()
