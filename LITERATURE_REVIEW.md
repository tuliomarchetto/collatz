# Systematic literature review — open questions on the state of the art

This document records a systematic search of the mathematical literature against
the three unresolved bibliographic questions raised by the internal peer review
(`REVIEW.md`) and by the manuscript's own Discussion (`paper/main.tex`). It is a
working research document, kept in English only (unlike `REPORT.md` /
`RELATORIO.md`, which are the bilingual publishable report).

**Search conducted:** 12–13 July 2026.
**Searcher's access:** USP institutional network (IP-based access to Scopus, Web
of Science, MathSciNet, SpringerLink, Cambridge Core, Oxford Academic, AMS).

---

## 1. Purpose and scope

Three questions, each tied to a specific claim in the manuscript.

| # | Question | Manuscript locus |
|---|----------|------------------|
| Q1 | Is the nonexistence theorem "no `V(n) = log₂n + w(n mod 2ʲ)` is strictly decreasing on the positive odd integers under `T`", with its robustness corollary, stated explicitly anywhere in the 3x+1 literature? | Thm 3.2 (`thm:main`), Cor 3.5 (`cor:robust`), Remark `rem:originality` |
| Q2 | Are the ℤ₃ Dobrushin–Wasserstein contraction (τ ≤ 1/3, exactness open) and the ℤ₂ finite-time Haar averaging already stated? How do they relate to the known Markov / transfer-operator / p-adic-ergodic theory? | Thms 4.3 & 4.5 (`thm:z3`, `thm:z2`), Remark `rem:tauk`, Discussion "Wasserstein contraction and prior theory" |
| Q3 | The closed-form `W₁` on ℤ/pᵏℤ with the p-adic ultrametric (Lemma 5.5) — is this known in the optimal-transport literature, and what is the correct citation? | Lemma 5.5 (`lem:w1formula`) |

Out of scope by decision: updating cycle-exclusion bounds beyond Hercher 2023
(the manuscript already cites Hercher 2023 and flags the supersession).

---

## 2. Methodology

**Inclusion criterion.** A work is *retained* only if (a) it is a peer-reviewed
paper, a recognized monograph, or a preprint by an established author on a
reputable server (arXiv), and (b) its bibliographic record (author, title,
venue, year, DOI/arXiv id) was confirmed on the publisher page, arXiv, zbMATH,
or Crossref. No citation was entered from memory. Crossref was used as the
authoritative source for every DOI recorded below.

**Exclusion criterion.** The 3x+1 literature is heavily contaminated by
low-quality "proofs of the Collatz conjecture" — self-published PDFs on viXra,
academia.edu, ResearchGate, and predatory journals, many of which invoke a
"Lyapunov function" or "entropy potential" that strictly decreases. These were
*excluded* from the retained set: none is peer-reviewed in a reputable venue,
and every one asserts the *opposite* of Q1 (existence of a global decreasing
certificate) rather than the manuscript's *nonexistence* result for a specific
class. Their prevalence is itself a finding (see Q1).

**Sources searched.**

- **Lagarias's annotated bibliographies of the 3x+1 problem**, Parts I and II
  (arXiv `math/0309224`, updated Jan 2011; arXiv `math/0608208`, updated Jan
  2012) — the authoritative ~300-item annotated survey. Downloaded the LaTeX
  sources and grepped the full text for `Lyapunov`, `potential`, `monotone`,
  `decreasing`, `descent`, `drift`, `weight`, `residue`.
- **arXiv** full-text search (`Collatz Lyapunov`, `"3x+1" Lyapunov`, and the Q2
  / Q3 strings below).
- **Crossref** bibliographic API — DOI and venue confirmation for every retained
  work.
- **zbMATH Open** and **Google Scholar / general web** — forward citation
  chasing from Terras 1976, Everett 1977, Tao 2022, and Kohl 2008.
- Publisher pages (Cambridge Core, Oxford Academic, AMS, AIMS, World
  Scientific) for exact volume/issue/page confirmation.

**Search-string log.**

| Q | String | Source | Screened | Retained |
|---|--------|--------|----------|----------|
| Q1 | `Lyapunov`, `potential function`, `monotone`, `decreasing`, `descent`, `drift` | Lagarias bib. I + II (full text) | ~10 keyword hits | 1 (Kohl 2008) |
| Q1 | `Collatz Lyapunov` | arXiv | 1 (unrelated: gene-regulatory networks) | 0 |
| Q1 | `"3x+1" Lyapunov` | arXiv | 0 | 0 |
| Q1 | `Collatz Lyapunov nonexistence / no monotone potential` | web | ~8 (all non-refereed "proofs") | 0 |
| Q2 | `Collatz Syracuse 2-adic ergodic Bernoulli`, `p-adic shift measure-preserving` | web + arXiv | ~9 | 2 (KLPS 2009, 2011) |
| Q2 | `Tao Syracuse random variables total variation mixing 3-adic` | web + arXiv | confirmed Tao 2022 (already cited) | 0 new |
| Q3 | `Wasserstein ultrametric closed form Kloeckner` | web + arXiv | ~9 | 1 (Kloeckner 2015) |
| Q3 | `Kantorovich Wasserstein tree metric closed form Evans Matsen` | web + arXiv | ~9 | 1 (Evans–Matsen 2012) |

---

## 3. Findings

### Q1 — Priority of the modular-Lyapunov no-go

**Verdict: no prior explicit statement located. The systematic search supports
(does not prove) the manuscript's framing that the ℤ₊ formulation is not stated
explicitly in the literature. The closest reputable relative is Kohl (2008).**

What the search established:

- **The underlying phenomenon is folklore, exactly as the manuscript says.**
  The fact that the residue class `−1 mod 2ᵏ` rises for `k` consecutive
  accelerated steps (e.g. `n = 2ᵏ − 1`) traces to the stopping-time analyses of
  Terras (1976) and Everett (1977), both already cited. No descent argument
  reading only a fixed finite dyadic residue can be uniform — this is understood
  but, in the sources examined, stated as a heuristic, never as a *nonexistence
  theorem* for the additive class `V(n) = log₂n + w(n mod 2ʲ)`.
- **Neither Lagarias bibliography contains the words "Lyapunov", "potential
  function", or "descent" in connection with such a no-go.** The only structural
  matches for "monotone/decreasing function" are (i) Wu (1995), on monotonicity
  of coalescence numbers (unrelated), and (ii) the RCWA line of Stefan Kohl.
- **Closest reputable relative — Kohl (2008), "On conjugates of Collatz-type
  mappings".** Kohl proves a genuine *no-go about the conjugating structure*: if
  a residue-class-wise affine (RCWA) map `f` is "almost contracting" and some
  iterate decreases almost all integers, then the permutation `σ` that
  witnesses the almost-contracting property *cannot itself be RCWA*. This is a
  nonexistence result about a *conjugacy* in the RCWA category, adjacent in
  spirit to the manuscript's obstruction but about a different object (a
  conjugating permutation, not an additive `log + modular` potential). It is
  worth citing precisely to delimit what is and is not new.
- **The contaminating literature runs the opposite way.** Numerous
  non-refereed manuscripts claim to *prove* Collatz via a strictly decreasing
  Lyapunov / entropy functional. None is peer-reviewed in a reputable venue, and
  each asserts the existence the manuscript rules out for its class. They do not
  bear on Q1 except as evidence that the *nonexistence* direction is
  under-served in print — which is consistent with the manuscript's claim.

**Consequence.** The manuscript's careful non-claim of priority is correct and
can now be stated as the outcome of a *documented* systematic search rather than
a to-do. Add Kohl (2008) as the closest reputable relative and cite it in
`rem:originality`, the report's "Note on the Literature", and the extraction
notes' "Relation to the literature". The notes' motivating **question** should
be retained but reframed: the search has been performed and did not find it, so
the question becomes a request for a pointer to any source the search missed.

### Q2 — Wasserstein / mixing state of the art

**Verdict: the ingredients are classical and the strong form of the ℤ₃ result is
Tao (2022); the exact Dobrushin–Wasserstein *coefficient packaging* was not
found stated elsewhere, and τ(P) = 1/3 exactness remains open. No contradiction
with the manuscript; it strengthens Remark `rem:tauk` and the "prior theory"
paragraph.**

- **ℤ₃ side.** The manuscript's τ(Pₖ) ≤ 1/3 is an elementary consequence of
  `|3|₃ = 1/3` and synchronous coupling. The *strong* statement about fine-scale
  mixing of the Syracuse distribution modulo 3ᵏ is **Tao (2022)** (already
  cited): he proves total-variation equidistribution of the Syracuse random
  variables via decay of their characteristic function — a far deeper result
  than a contraction coefficient. The manuscript already positions itself below
  Tao; this is confirmed. No source was found stating the *exact*
  Dobrushin–Wasserstein coefficient for the ℤ₃ Syracuse chain, nor resolving
  whether the τ = 1/3 upper bound is attained in the supremum over ℤ₃ (the open
  question of Remark `rem:tauk`). The finite exact values τ₂ = 5/21, τ₃ =
  455/1387, τ₄ ≈ 0.33333206 are reproduced by the accompanying code and remain
  the only concrete data on the question.
- **ℤ₂ side.** The finite-time Haar-averaging / Bernoulli-shift reading of the
  2-adic Collatz map is classical: the 2-adic conjugacy to the shift is
  Bernstein–Lagarias (1996, already cited), and the general framework of
  measure-preserving / Bernoulli transformations on ℤₚ is
  **Kingsbery–Levin–Preygel–Silva (2009, TAMS)** and its sequel **(2011, DCDS)**
  "Dynamics of the p-adic shift and applications". The manuscript's Theorem 4.5
  is a Wasserstein re-reading of this well-established structure, correctly
  framed as such.

**Consequence.** Add the two Kingsbery–Levin–Preygel–Silva references as the
standard citation for p-adic Bernoulli/shift dynamics, in the "prior theory"
paragraph of the Discussion and the ℤ₂ theorem context. Keep Remark `rem:tauk`'s
open-question framing; it is genuinely open. No numeric claim changes.

### Q3 — Closed-form W₁ on ultrametric quotients

**Verdict: known. Lemma 5.5 is a special case of the closed-form Wasserstein-1
distance on trees / ultrametric spaces. Keep the proof; add the attribution.**

- **Evans & Matsen (2012)**, "The phylogenetic Kantorovich–Rubinstein metric for
  environmental sequence samples", J. R. Stat. Soc. Ser. B **74**(3), 569–592 —
  the standard closed-form `W₁` (Kantorovich–Rubinstein) distance on a finite
  metric tree, as a sum over edges of the total-variation discrepancy of the two
  sides of the edge. Since (ℤ/pᵏℤ, p-adic ultrametric) is exactly the metric of
  a rooted `p`-ary tree of depth `k`, the manuscript's Lemma 5.5 telescoping
  formula is the Evans–Matsen edge formula specialized to that tree.
- **Kloeckner (2015)**, "A geometric study of Wasserstein spaces: ultrametrics",
  Mathematika **61**(1), 162–178 — the systematic study of Wasserstein spaces
  over compact ultrametric spaces, giving the reformulation of the distance
  specific to the ultrametric case (affine isometry to a convex subset of ℓ¹).
  This is the natural reference for the ultrametric optimal-transport framework
  the lemma lives in.

**Consequence.** Add a one-line remark to Lemma 5.5 attributing the closed form
to the tree/ultrametric optimal-transport literature (Evans–Matsen 2012;
Kloeckner 2015), noting the lemma is the specialization to ℤ/pᵏℤ. The lemma's
self-contained proof stays (it is short and keeps the paper reproducible).

---

## 4. Consequences for the manuscript (edit list)

Applied in the same session as this review:

1. **`paper/references.bib`** — five new verified entries:
   `kohl2008` (Q1), `kingsberyetal2009` + `kingsberyetal2011` (Q2),
   `kloeckner2015` + `evansmatsen2012` (Q3).
2. **`paper/main.tex`**
   - `rem:originality` (§3): note the systematic search; cite Kohl (2008) as the
     closest reputable relative and RCWA no-go.
   - `rem:tauk` (§4): unchanged in substance; τ = 1/3 exactness stays open (Q2
     confirmed nothing supersedes it).
   - `thm:z2` context / Discussion "prior theory": cite Kingsbery–Levin–Preygel–
     Silva (2009, 2011) for the p-adic Bernoulli/shift structure.
   - `lem:w1formula` (§5): add Evans–Matsen (2012) and Kloeckner (2015)
     attribution.
3. **`REPORT.md` + `RELATORIO.md`** — mirror the same substantive additions in
   both languages (same turn): the "Note on the Literature" gains Kohl (2008) and
   the "systematic search" phrasing; the Wasserstein section gains the
   prior-theory citations; the exact-W₁ description gains the OT attribution.
4. **`note/lyapunov-obstruction-en.tex` + `note/nota-obstrucao-lyapunov-pt.tex`**
   — the "Relation to the literature" section reframes the priority question as
   the outcome of a documented search and cites Kohl (2008) as the closest
   relative (both languages, same turn).

**Bibliographic records (all DOIs confirmed via Crossref):**

- Kohl, S. (2008). On conjugates of Collatz-type mappings. *Int. J. Number
  Theory* **4**(1), 117–120. doi:10.1142/S1793042108001237.
- Kingsbery, J., Levin, A., Preygel, A., Silva, C. E. (2009). On
  measure-preserving 𝒞¹ transformations of compact-open subsets of
  non-archimedean local fields. *Trans. Amer. Math. Soc.* **361**, 61–85.
  doi:10.1090/S0002-9947-08-04686-2. arXiv:0710.5562.
- Kingsbery, J., Levin, A., Preygel, A., Silva, C. E. (2011). Dynamics of the
  p-adic shift and applications. *Discrete Contin. Dyn. Syst.* **30**(1),
  209–218. doi:10.3934/dcds.2011.30.209. arXiv:0903.4226.
- Kloeckner, B. (2015). A geometric study of Wasserstein spaces: ultrametrics.
  *Mathematika* **61**(1), 162–178. doi:10.1112/S0025579314000059.
  arXiv:1304.5219.
- Evans, S. N., Matsen, F. A. (2012). The phylogenetic Kantorovich–Rubinstein
  metric for environmental sequence samples. *J. R. Stat. Soc. Ser. B* **74**(3),
  569–592. doi:10.1111/j.1467-9868.2011.01018.x. arXiv:1005.1699.

## 5. Limitations of this review

- **MathSciNet / zbMATH deep review text** was not exhaustively mined; the
  searches above relied on Lagarias's annotated bibliographies (which curate the
  3x+1 corpus through ~2012), arXiv full text, Crossref, and forward citation
  chasing. A negative result on Q1 is therefore *strong but not a proof of
  absence*; the reframed question in the extraction notes remains the honest
  posture.
- Q1's negative finding concerns the *specific additive class* `log₂n + w(n mod
  2ʲ)`. Adjacent no-go results about other certificate classes (e.g. Kohl's RCWA
  conjugacy result) exist and are now cited; a result phrased differently but
  logically equivalent could in principle exist under terminology the search did
  not cover.
