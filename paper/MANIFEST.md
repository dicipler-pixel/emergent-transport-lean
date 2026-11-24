# Manifest — Gaps and Totals

Pins the artefacts this draft rests on.

| file | sha256 (first 16) | bytes |
| :--- | :--- | ---: |
| `paper/main.pdf` | `8f85f1286a4d5065` | 550684 |
| `paper/main.tex` | `e807eed3379762b2` | 1901 |
| `paper/fig_sheets.pdf` | `9a62541d794267f5` | 22858 |
| `EmergentTransport/GapsAndTotals.lean` | `a8b3861623a89b7d` | 10962 |
| `EmergentTransport/Basic.lean` | `9f76d54d49a8ff1e` | 8288 |
| `scripts/gates/g01_shape_spectrum.py` | `5e003af9590efa73` | 9377 |
| `scripts/gates/g02_gap_hierarchy.py` | `6d0f50d2151bf8b9` | 5466 |
| `scripts/gates/g03_mass_breaking.py` | `a411e7e5230f6427` | 9797 |
| `scripts/gates/g04_projector_constant.py` | `a55b668d706d83df` | 5930 |
| `scripts/gates/g05_tan_theta.py` | `15f46e391fd6945b` | 5303 |
| `scripts/gates/g06_projector_tan2.py` | `f21b21b36367075f` | 8056 |
| `scripts/gates/make_fig_sheets.py` | `5d739784747ee5f3` | 2049 |
| `scripts/verify.py` | `237b8ed7bfd1be48` | 7950 |
| `notes/04_PI_OVER_2.md` | `2317be9b0ebd1d28` | 9239 |
| `notes/05_TAN_THETA.md` | `02a192b82072922f` | 5305 |
| `notes/06_CONVEX_HULL.md` | `d2e50cd2b2392bde` | 4584 |
| `notes/07_TWO_MAPS.md` | `ee924697655b122b` | 4481 |

## Gate state

* `g01_shape_spectrum`: 20 assertions, passed = True
* `g02_gap_hierarchy`: 13 assertions, passed = True
* `g03_mass_breaking`: 20 assertions, passed = True
* `g04_projector_constant`: 10 assertions, passed = True
* `g05_tan_theta`: 4 assertions, passed = True
* `g06_projector_tan2`: 12 assertions, passed = True

* total: 79 gate assertions

## Verification

`python3 scripts/verify.py --direct` → 29 theorems, axioms `{propext, Classical.choice,
Quot.sound}`, 6 false controls rejected (re-run from a clean clone of
`openmath/gaps-and-totals` at 9aaedaf).
