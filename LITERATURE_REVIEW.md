# Systematic literature review — open questions on the state of the art

This document records a systematic search of the mathematical literature against
the unresolved bibliographic questions raised by the internal peer review
(`REVIEW.md`) and by the manuscript's own Discussion (`paper/main.tex`). It is a
working research document, kept in English only (unlike `REPORT.md` /
`RELATORIO.md`, which are the bilingual publishable report).

**Search conducted:** 12–13 July 2026 (Q1–Q3); 17 July 2026 (Q4).
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
| Q4 | The **variable-depth** no-go (added 2026-07-17): is the all-ones-telescoping / single-block-expansion obstruction for variable-depth stopping-rule potentials — no bounded correction `w(n)` makes `log₂n + w(n)` block-descend under any adapted rule stopping `1^s`, nor under any rule with unbounded `Γ_σ` — stated anywhere (Wirsching; Kohl / RCWA; Terras–Garner coefficient stopping time thread; Tao's stopping-time setup)? | Thms `thm:stopping`, `thm:expansion`, `thm:characterize`, Remark `rem:boundary` |

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
| Q4 | `Collatz stopping time bounded potential no-go prefix code parity word telescoping` | web + arXiv | ~20 | 0 |
| Q4 | `"coefficient stopping time" Terras conjecture survey` | web + arXiv | ~10 | 1 (Garner 1981) |
| Q4 | `Collatz Lyapunov / potential stopping time nonexistence bounded correction (2024–2026)` | web + arXiv | ~10 (non-refereed "proofs" excluded) | 0 |
| Q4 | `Wirsching 3n+1 monograph Lyapunov potential descent nonexistence` | web (monograph scope) | ~10 | 0 |
| Q4 | `Collatz Mersenne 2^k−1 unbounded growth nonexistence bounded weight` | web + arXiv | ~10 | 0 |

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

**Verdict: known, and the match is now confirmed *exact* (verified against the
Evans–Matsen full text, 2026-07-17, under Tier 2 G6; re-verified 2026-07-17
against arXiv:1005.1699 eq. (5) and arXiv:1304.5219 / Kloeckner Mathematika
2015). Lemma 5.5 is the specialization to ℤ/pᵏℤ of Evans–Matsen equation (5).
Keep the self-contained proof; attribution tightened to cite the exact
equation. G6 closed.**

**Exactness check (G6).** Evans–Matsen (2012), §2, eq. (5): for a metric tree
`T` with length measure `λ`, `W₁(P,Q) = ∫_T |P(τ(y)) − Q(τ(y))| λ(dy)`, where
`τ(y)` is the subtree below `y` — a sum over edges of (edge length)·(TV
discrepancy of the two subtree masses). Their eq. (1) is the point-mass
(weighted-UniFrac) special case. The manuscript's `(ℤ/pᵏℤ, p-adic
ultrametric)` is exactly the leaf metric of a rooted `p`-ary tree of depth `k`:
the edge from level `ℓ−1` to `ℓ` has length `p^{−(ℓ−1)} − p^{−ℓ}`, its subtree
is a congruence cell mod `p^ℓ`, and `2m_ℓ` is the aggregate discrepancy across
those cells — so `lem:w1formula` is eq. (5) evaluated on that tree, not merely
a related ultrametric-transport result. Kloeckner (2015) is the correct
*framework* reference (W₁ as an affine isometry onto a convex subset of `ℓ¹`
for compact ultrametric spaces; Theorem 1.1 / §3 gives the ℓ¹ coordinates via
masses of balls, which is the continuous-ultrametric parent of the finite-tree
formula), but Evans–Matsen is the source of the exact closed form. Manuscript
updated accordingly (the paragraph preceding `lem:w1formula` now cites
`[evansmatsen2012, eq. (5)]` explicitly, and the two-line self-contained proof
is retained so the lemma has no external dependency for reproducibility).

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

### Q4 — Priority of the variable-depth no-go (search of 2026-07-17)

**Verdict: no prior statement located. The ingredients are folklore; the
packaging as a nonexistence theorem — and the adapted-rule characterization by
expansion rate — was not found anywhere. Closest engaged relative: the
Terras–Garner coefficient stopping time conjecture, which the manuscript
already identifies as the exact boundary of the no-go. Hedge as for Q1: a
documented negative search, not a proof of absence.**

What the search established:

- **Both mechanical ingredients are classical.** (i) The all-ones ascent — the
  class `−1 mod 2^ℓ` (Mersenne seeds `2^ℓ − 1`) rises for `ℓ` consecutive
  accelerated steps — is Terras (1976) / Everett (1977) folklore, exactly as in
  Q1. (ii) Unbounded single-block growth of the untruncated Syracuse step on
  Mersenne seeds (`S(2^ℓ−1) = (3^ℓ−1)/2`) is elementary and appears throughout
  the stopping-time literature. What was **not found** is either ingredient
  *stated as a nonexistence theorem* for the class `V(n) = log₂n + w(n)`, `w`
  bounded, under adapted (prefix-code) stopping rules — i.e., nothing resembling
  `thm:stopping` (telescoping along all-ones chains defeats every bounded
  correction for every rule stopping `1^s`), `thm:expansion` (the
  single-block criterion `limsup Γ_σ = ∞`, adaptedness not required), or the
  characterization `thm:characterize` (obstruction ⟺ expansion rate
  `E(S) = ∞` for the single-block filter, plus the all-ones/cycle filter for
  finite maximal prefix codes).
- **The stopping-time literature runs orthogonally.** Winkler (arXiv:1504.00212)
  and the related work on residue classes with equal stopping time enumerate
  and structure the classes `mod 2^σ`; they contain no potential/no-go
  statement. Wirsching's monograph (LNM 1681, 1998) develops predecessor-set
  and measure-theoretic machinery, not descent certificates; no Lyapunov
  nonexistence statement is in its scope.
- **The engaged boundary object is Terras–Garner.** The coefficient stopping
  time conjecture (`σ(n) = τ(n)`; equivalently, descent with `w ≡ 0` at the
  coefficient stopping time) is stated in Terras (1976) and **Garner (1981)**,
  and Lagarias (1985, §"coefficient stopping time") proves its truth would
  imply the nonexistence of nontrivial cycles (verified against the survey
  text, node5 of the online edition). This confirms the manuscript's Remark
  `rem:boundary`: the surviving non-expansive prototype is precisely an open
  conjecture, so neither filter can be strengthened to cover it without
  deciding an open problem. Garner (1981) was previously uncited — it should be
  added alongside Terras in `rem:boundary` and Definition `def:adapted`.
- **Kohl / RCWA (re-checked under Q4 lens).** Kohl (2008) remains a no-go about
  conjugating permutations in the RCWA category; nothing in the RCWA line
  treats data-dependent stopping schedules or bounded additive corrections.
- **Tao's setup is variable-depth but almost-all.** Tao (2022) works with
  data-dependent stopping times (Syracuse random variables, `n^{1/2}`-type
  weights) in a probabilistic framework; his results are density statements,
  not pointwise descent certificates, and contain no nonexistence theorem for
  potential classes. The manuscript already positions itself below Tao.
- **The contaminating literature again runs the opposite way** (non-refereed
  "strictly decreasing functional" proofs, several 2024–2026); as in Q1, they
  assert existence for classes the manuscript refutes, none in a reputable
  venue, and none engages adapted stopping rules.

**Consequence.** The variable-depth theorems can be presented as new *as
packaging*, with the same hedged posture as Q1: state that a documented search
located no prior formulation, claim no absolute priority, and keep the
falsifiable request-for-pointer framing. Edits: (1) add `garner1981` to
`references.bib` (verified: L. E. Garner, *On the Collatz 3n+1 algorithm*,
Proc. Amer. Math. Soc. **82** (1981), no. 1, 19–22,
doi:10.1090/S0002-9939-1981-0603593-2) and cite it with Terras for the
coefficient stopping time conjecture; (2) add a "relation to the literature"
remark for Section `sec:stopping` mirroring `rem:originality`; (3) soften the
abstract's "previously thought to escape" (no documented prior belief exists —
the phrase referred to an earlier version of this work) to a neutral
formulation.

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

Applied in the Q4 session (2026-07-17): `garner1981` added to
`paper/references.bib`; Garner cited in Definition `def:adapted` and Remark
`rem:boundary`; new Remark `rem:stoppingoriginality` (relation of the
variable-depth theorems to the literature) added to Section `sec:stopping`;
abstract's "previously thought to escape" softened.

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
- Garner, L. E. (1981). On the Collatz 3n+1 algorithm. *Proc. Amer. Math.
  Soc.* **82**(1), 19–22. doi:10.1090/S0002-9939-1981-0603593-2.

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
