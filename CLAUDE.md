# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`vha-toolbox` is a personal Python utility package published to PyPI. It supports Python 3.9–3.14. Dependencies: `Unidecode` and `Pillow`.

## Commands

**Install for development:**
```bash
pip install .
pip install pytest Pillow
```

**Run all tests:**
```bash
pytest tests/test*
```

**Run a single test file:**
```bash
pytest tests/test_generate_text_svg.py
```

**Build for PyPI:**
```bash
python -m build
```

Publishing to PyPI is done manually via the `pypi-publish` GitHub Actions workflow (requires `PYPI_API_TOKEN` secret). Version is set in `setup.py`.

## Architecture

All public functions are re-exported from `vha_toolbox/__init__.py` via star imports (except `generate_text_svg`, which is imported explicitly). Adding a new module requires adding an import line to `__init__.py` and adding it to the `packages` list is not needed (single-package: `vha_toolbox`).

### Module overview

| Module | Purpose |
|---|---|
| `string_manipulation.py` | `truncate_with_ellipsis`, `replace_multiple_substrings`, `anonymize_sentence`, `text_to_html`, `seconds_to_humantime` |
| `generate_text_svg.py` | SVG avatar/thumbnail generator with color utilities (`get_hsl_from_seed`, `pick_text_color_for_bg`, `split_text_for_svg`, `generate_text_svg`) |
| `image_crop_utils.py` | `crop_to_square` (requires Pillow) |
| `data_manipulation.py` | `sort_dict_by_list` |
| `date_utils.py` | Date helpers |
| `ean.py` / `isbn.py` | EAN/ISBN barcode validation |
| `excel_column_conversion.py` | Excel column letter↔number conversion |
| `file_hash_utils.py` | File hashing |
| `format_size.py` | Human-readable file size formatting |
| `frame_ratio_utils.py` | Aspect ratio utilities |
| `highlight_text.py` | Text highlighting |
| `magnet_link.py` | Magnet link parsing/generation |
| `sql_helper.py` | SQL query helpers |
| `table_generator.py` | ASCII/text table generation |

### `generate_text_svg.py` internals

This is the most complex module. It is structured in layers:
1. **Validators** (`_validate_*`) — strict input validation raising `ValueError`
2. **Color helpers** — HSL↔RGB conversion, contrast ratio (WCAG), `get_hsl_from_seed` (SHA-512-based deterministic hue), `pick_text_color_for_bg`, `_best_bg_for_forced_text`
3. **Text splitting** — `split_text_for_svg` word-wraps text with hard-split for long words
4. **SVG generation** — `generate_text_svg` assembles the final SVG string; `SvgTextOptions` dataclass documents defaults

Colors must be `#rrggbb` or `hsl(h, s%, l%)`. `text_color` must be hex only. Background can be auto-derived from a `seed` string.

### Testing conventions

Each module has a corresponding test file in `tests/`. Tests use `unittest.TestCase`. Snapshot tests compare exact SVG strings; functional tests check `ValueError` raises for invalid inputs.
