# Review: `dicipler-pixel/coboundary-k3-lean`, branch `palomar-package`

Reviewed commit `0bacf284223282206d445949f0a41faa7b944f8a` (branch head), 24 November 2026.
Independent checkout, independent toolchain. **No files in that repository were modified, nothing
was pushed to `palomar-package` or `main`, and no pull request was opened** (the platform's GitHub
connector is scoped to `emergent-transport-lean`, so it cannot reach this repository; and the
brief was to report as a comment rather than as edits). The one local experiment described in §1
was made in a scratch clone and reverted; the tree was verified clean afterwards.

Claim reviewed: `h1(K_k) = k/3` for every `k >= 3` (`CoboundaryK3.h1_eq_all`), against
Section 1 and Theorem 8 of DOI 10.5281/zenodo.23245792 (v7, 8 October 2026).

---

## 1. Does `scripts/verify-comparator.sh` pass on the branch head?

**Yes.** `Your solution is okay!`

Setup: the local toolchain is `leanprover/lean4:v4.35.0` (`/opt/lean.4.35.0-56a005855ea1`), which
bundles `lake`, `leanexport`, `leanchecker`, `nanoda_bin` and `con-ron` — the five the script
requires. Mathlib was built from the pinned `lake-manifest.json` rev
(`56a005855ea1…`, `v4.35.0`) into a writable `.lake/packages`. `bwrap` present.

    lake build            -> Build completed successfully (2001 jobs)
    ./scripts/verify-comparator.sh
      Build completed successfully (1998 jobs)      # replay
      con-ron: accepted 13592 declarations (--verified)
      nanoda kernel accepts the solution
      Lean default kernel accepts the solution
      Your solution is okay!

Axiom audit, run separately:

    CoboundaryK3.h1_eq_all            -> [propext, Classical.choice, Quot.sound]
    CoboundaryK3.gaugeDist_mul_le     -> [propext, Classical.choice, Quot.sound]
    CoboundaryK3.gaugeDist_eq_zero_iff-> [propext, Classical.choice, Quot.sound]

exactly the `permitted_axioms` in `comparator.json`, with no `sorryAx` and no `native_decide`
in the library or `Solution` (`sorry` appears only in `Challenge.lean`, as intended).

**One adversarial test worth reporting.** `comparator.json` has `definition_names: []`, which
might suggest that only the three theorem *statements* are compared and that the definitions
floating beneath them are unpinned. I checked: tampering with `Challenge.lean` alone, multiplying
`defect` by 2, makes Comparator fail with

    error: Const does not match between challenge and target 'CoboundaryK3.defect'

so definitions are matched even when not listed. Reverted; clean run reproduces "okay". This is
the single most reassuring thing in the repository.

Also verified independently, outside Lean: exhaustive enumeration for `k = 3` and `k = 4` over
all `Sym(3)`-valued cochains and all gauges gives `min N/D = 1` and `4/3` respectively.

## 2. `Challenge.lean` against Section 1 and Theorem 8

**Definitions.** `moved`, `edges`, `triangles`, `val`, `defect`, `cost`, `gaugeDist`, `h1` all
match the paper's Section 1 in the counting convention: `N` is the total moved-point triangle
defect, `D` the minimum over `Sym(3)` gauges of the moved-point edge cost, and
`h1 = inf N/D` over non-coboundaries. The paper's own identity
`h1^count = (|T|/|E|)·h1^norm` with `|T|/|E| = (k−2)/3` gives exactly `N/D`, so the Lean's `h1`
is the paper's `h1^count` — not a rescaled variant.

**One convention drift, harmless but undocumented.** The paper's coboundary is
`δβ(u,v) = β(u)^{-1}β(v)` and its edge distance is `d_H(α(u,v), δβ(u,v))`; the Lean's edge term
is `moved((β u)⁻¹ * α u v * β v)`. These differ per edge — for 36 of the 216 triples
`(α, β_u, β_v)` the two moved-counts disagree (0 versus 3). They agree after the bijection
`β ↦ β^{-1}`: I verified `cost_lean(β) = cost_paper(β^{-1})` for every gauge on 50 random
`K_4` cochains, so the gauge minimum, the coboundary set, and hence `h1` are identical. The
docstring asserting the Lean's `gaugeDist` *is* "the paper's `D` (Section 1)" is therefore true
of the minimum and not of the summand. Worth one sentence in the docstring; no mathematical
consequence.

**Hypotheses.** None hidden. `h1_eq_all` carries `3 ≤ k` explicitly; `h1_eq_k_div_three_ge_four`
carries `4 ≤ k`, matching Theorem 8. `k_div_three_le_h1` takes the existence of a non-coboundary
as an explicit hypothesis and every call site discharges it with a concrete witness.

**Vacuity.** None. `h1` is an `sInf`, so on an empty index set it would be `0` by Mathlib's
convention; the docstring says so, `gaugeDist_eq_zero_iff` identifies the index set with the
non-coboundaries, and each `h1 = k/3` result is proved with a witness in hand, so the set is
nonempty wherever a claim is made. Nothing is claimed for `k ≤ 2`.

**Scope versus the paper.** The Lean proves the `Sym(3)`-valued, same-degree, counting-convention
statement. The paper's Theorem 8 additionally gives `h1^norm = k/(k−2)`, permutation coefficients
of every degree, and Proposition 10's cross-degree convention; none of those is formalized. This
is stated in `fidelity.divergences` and `status.scope`, so it is disclosed rather than hidden —
but see objection 1 in §5.

**A strengthening, and it is true.** The Lean proves `k ≥ 3` where the paper states `k ≥ 4`. I
checked the extra case independently: exhaustive enumeration at `k = 3` gives `min N/D = 1 = 3/3`.
The extension is sound, not a slip, and `fidelity.divergences` flags it as a difference rather
than presenting it as the paper's own claim.

## 3. `formalization.yaml` against Palomar policy

I ran Palomar's own validator (`PalomarSubmission/scripts/submission_contract.py`,
`load_formalization_metadata`) on the file:

    VALID: metadata accepted

Classification codes checked against the registry snapshots: `math.CO`, `math.GR` present in
`arxiv-categories.json`; `05E45`, `55U10`, `20B30` present in `msc2020-codes.json`. Field sizes
within limits. `project.authors` and `project.responsible_maintainers` are human only.
`review.status: self-assessed` is an accepted upstream value and its note is honest
("no human mathematician other than the author has reviewed the paper or the statements").

Three findings, none of which blocks intake today:

**(a) `sources[].type` uses values the written contract does not allow.** `CONTRIBUTING.md` §3.2
says "when a source has a `type`, it must be `paper`, `book`, `web discussion`, `folklore`,
`original-proof`, or `other`". The file uses `type: "preprint"` (paper) and `type: "article"`
(Chapman–Lubotzky, Kozlov). The *code* does not enforce that enum —
`_optional_text(item.get("type"), …, maximum=200)` accepts any string — which is why the
validator passes. This is a mismatch between the prose contract and the implementation, and it
is a live risk: if the implementation is tightened to the documented enum, the submission fails.
Smallest fix: `preprint` → `paper`; both `article` → `paper`. Nothing else changes, since the
`note` and `location` fields already carry the bibliographic detail.

**(b) `AI_USE.md` line 3 describes "the physics behind this library".** This is a leftover from
the sibling transport-geometry repository; there is no physics in a coboundary-expansion
project. `formalization.yaml`'s automation account is correct, so the two do not contradict each
other — but a reviewer reading `AI_USE.md` will notice, and it is the kind of copy error that
makes a reader doubt the rest. Smallest fix: delete "and the physics".

**(c) `comparator.json` carries `enable_nanoda: true`, which Palomar ignores.** The repository's
own `verify-comparator.sh` strips it before running precisely because it is not a submitter
field. Harmless, but dead configuration that invites the reader to think it does something.
Smallest fix: delete the key.

## 4. Licence

**Accepted, with no change needed.** `PalomarSubmission/scripts/verify_submission.py` selects root
licence files with

    ^(?:licen[cs]e|copying|unlicense|ofl)(?:\.(?:md|markdown|txt))?$      (IGNORECASE)

Against the repository root: `LICENSE` matches; `LICENSE-CC-BY-4.0.md` does **not** match, and
neither does `LICENSING.md`. So `repository_license_file` finds exactly one conventional licence
file and does not raise the "multiple licence files" error. `LICENSE` is the standard MIT text
("MIT License / Copyright (c) 2026 Jeromie Beasley / Permission is hereby granted…"), which
Licensee identifies as `MIT` at its 98% threshold, and `formalization.yaml` declares
`project.license: "MIT"`. Identical, unambiguous, matching.

So the dual-licensing is invisible to the detector *because of how the second file is named*. That
is worth knowing: renaming `LICENSE-CC-BY-4.0.md` to `LICENSE.md`, or `LICENSING.md` to
`LICENCE.txt`, would immediately fail mechanical verification with "must contain exactly one
conventional licence file". The current arrangement is correct and should be left alone; the risk
is a future tidy-up.

One editorial note rather than a mechanical one: `project.license: MIT` declares the licence of
the whole submitted snapshot, while `LICENSING.md` and `README.md` tell a reader the prose is
CC BY 4.0. That is a real dual licence and Palomar records only the detected one. It is not a
failure, but a reviewer may ask for a sentence in `formalization.yaml` making clear that the
submitted snapshot is MIT for the files it contains, with CC BY 4.0 reserved to prose outside the
formalization.

## 5. The three strongest objections a Palomar reviewer could raise

**Objection 1 — "The title claims more than the artifact proves."** `project.name` reads "The
permutation coboundary constant of the complete complex is k/3", unqualified. The paper's Theorem
8 gives two normalisations, every permutation degree, and a cross-degree extension; the Lean gives
one normalisation, `Sym(3)`, same degree. *What answers it:* `project.description` opens by
specifying `Sym(3)` coefficients and the counting convention, `status.scope` enumerates exactly
what is and is not formalized, and `fidelity.divergences` names the normalised and cross-degree
conventions as not formalized. The disclosure is complete and prominent — but the *name* is the
string the registry shows in a list, and it is the one place the qualifier is missing. I would
expect a reviewer to ask for "in the counting convention with Sym(3) coefficients" in the name.

**Objection 2 — "Is `h1` doing any work, or is it a definition that could be satisfied by
anything?"** It is an `sInf` over a possibly empty set of ratios, so on its face it is a
definition with a degenerate case. *What answers it:* the docstring names the empty-set
convention; `gaugeDist_eq_zero_iff` proves that `0 < gaugeDist α` is exactly "α is not a
coboundary", which is the paper's index set; every value theorem is proved from a concrete
witness, so no claim rests on the empty case; and `k_div_three_le_h1` isolates the nonemptiness as
an explicit hypothesis rather than smuggling it in. An independent exhaustive computation at
`k = 3, 4` reproduces the values. This objection is fully answered.

**Objection 3 — "The gauge convention is not the paper's."** The Lean's edge term is
`β_u^{-1} α β_v`; the paper's is `d_H(α, β_u^{-1}β_v)`. They differ on individual gauges (36 of
216 triples). *What answers it:* they are related by the gauge bijection `β ↦ β^{-1}`, so the
minimum — which is what `h1` uses — is unchanged, and the coboundary sets coincide. The theorem is
therefore about the paper's constant. But nothing in the repository says so: the docstrings assert
identity with Section 1's `D` without noting the inversion. This is the one finding I would want
fixed before submission, and the fix is a sentence, not a proof.

## Summary

| item | verdict |
| :--- | :--- |
| 1. comparator on branch head | **passes**, three kernels, permitted axioms only |
| 2. `Challenge.lean` vs Section 1 / Thm 8 | faithful; one undocumented but harmless `β ↦ β^{-1}` drift; `k ≥ 3` extension verified true |
| 3. `formalization.yaml` | mechanically valid; fix `type: preprint/article` → `paper`; `AI_USE.md` "physics" leftover; dead `enable_nanoda` |
| 4. licence | **accepted as exactly one, MIT**; no change; do not rename the CC file |
| 5. research interest | scope disclosure and non-vacuity are strong; the gauge convention needs one sentence |

The mathematical core is genuinely substantial and the packaging is unusually careful: the
staircase seeds, the parity retraction, the replication lemma and the decomposition of every
`k ≥ 3` are a real proof, not an enumeration, and the enumeration only supplies `k ≤ 8`. Nothing I
found changes a mathematical claim. Everything I would change is documentation.
