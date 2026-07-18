# Systematic literature review — Collatz Lab corpus

Working research document (English only). Complements the bilingual
publishable report (`REPORT.md` / `RELATORIO.md`) and the formal manuscript
(`paper/main.tex`). It records (i) the bibliographic corpus the project
depends on, organized by mathematical theme, and (ii) the priority searches
(Q1–Q4) that justify the manuscript's originality hedges.

**Search windows.** 12–13 July 2026 (Q1–Q3); 17 July 2026 (Q4, G6
re-verification); **18 July 2026 (systematic reorganization + DOI audit
under USP institutional access).**

**Access.** USP institutional network: Crossref API, arXiv, zbMATH Open,
publisher platforms (Cambridge Core, SpringerLink, AMS, AIMS, Oxford,
Waterloo JIS). Every retained DOI below was checked against Crossref or the
publisher page in this window, except as noted.

---

## 0. How to use this document

| Section | Purpose |
|---------|---------|
| §1 Purpose and scope | What questions the review answers |
| §2 Methodology | Inclusion / exclusion / sources |
| **§3 Thematic bibliography** | **All papers needed by the project, by domain** |
| §4 Priority questions Q1–Q4 | Originality / positioning verdicts |
| §5 Mapping to the manuscript | Which claim cites what |
| §6 Limitations | What this review does *not* prove |

Items already in `paper/references.bib` are marked **`[bib]`**. Items useful
for the laboratory / Tier-3 G11 but not (yet) cited in the manuscript are
marked **`[adjacent]`**. Optional formalization pointers are **`[formal]`**.

---

## 1. Purpose and scope

### 1.1 Bibliographic questions (priority searches)

| # | Question | Manuscript locus |
|---|----------|------------------|
| Q1 | Is the nonexistence theorem “no \(V(n)=\log_2 n+w(n\bmod 2^j)\) is strictly decreasing on positive odds under \(T\)”, with its robustness corollary, stated explicitly in the 3x+1 literature? | `thm:main`, `cor:robust`, `rem:originality` |
| Q2 | Are the \(\mathbb{Z}_3\) Dobrushin–Wasserstein contraction and the \(\mathbb{Z}_2\) finite-time Haar averaging already stated? Relation to Markov / transfer / p-adic ergodic theory? | `thm:z3`, `thm:tausharp`, `thm:z2`, Discussion |
| Q3 | Is the closed-form \(W_1\) on \(\mathbb{Z}/p^k\mathbb{Z}\) with the p-adic ultrametric known in optimal transport? Correct citation? | `lem:w1formula` |
| Q4 | Is the variable-depth no-go (all-ones telescoping / single-block expansion / exact boundary \(\Lambda\)) stated anywhere? | `thm:stopping`, `thm:expansion`, `thm:characterize`, `thm:exactboundary` |

### 1.2 Thematic scope (full corpus)

Beyond Q1–Q4, the project needs a **working map of the literature** in every
domain it touches:

1. Surveys and annotated bibliographies  
2. Stopping times and almost-all results (Terras → Tao)  
3. Cycles and Diophantine exclusion  
4. 2-adic structure and conjugacy  
5. Modular Markov chains (Matthews–Watts line)  
6. Lyapunov / RCWA / obstruction relatives  
7. Transfer operators, Wasserstein, ultrametric OT  
8. Computational verification  
9. Formalization frontier (Lean / ccchallenge) — pointer only  

Out of scope as *claimed results*: improving Hercher's cycle bound;
proving almost-all statements beyond Tao; non-refereed “proofs of Collatz”.

---

## 2. Methodology

**Inclusion.** Peer-reviewed paper, recognized monograph, or arXiv preprint
by an established author, with bibliographic record confirmed on publisher
page / arXiv / zbMATH / Crossref. No citation from memory alone.

**Exclusion.** viXra / academia.edu / ResearchGate / predatory-journal
“proofs of Collatz” that assert a global decreasing Lyapunov/entropy
functional. They assert the *opposite* of Q1 and are not retained, except as
a contamination note.

**Primary sources searched.**

- Lagarias annotated bibliographies: arXiv `math/0309224` (1963–1999, v13 Jan
  2011); arXiv `math/0608208` (2000–2009). Full-text greps for Lyapunov /
  potential / monotone / descent / stopping / Wasserstein / conjugacy.
- arXiv full text (math.NT, math.DS, math.PR).
- Crossref bibliographic + content negotiation APIs (DOI audit, 18 Jul 2026).
- Forward citation chasing from Terras 1976, Everett 1977, Tao 2022, Kohl
  2008, Barina 2025.
- Publisher pages for volume / issue / pages.

**Search-string log (priority questions).**

| Q | String | Source | Screened | Retained |
|---|--------|--------|----------|----------|
| Q1 | Lyapunov / potential / monotone / descent in Lagarias bib. | Lagarias I+II | ~10 hits | 1 (Kohl 2008) |
| Q1 | `Collatz Lyapunov`, `"3x+1" Lyapunov` | arXiv | 1 unrelated | 0 |
| Q2 | Collatz Syracuse 2-adic ergodic / p-adic shift | web+arXiv | ~9 | 2 (KLPS 2009, 2011) |
| Q3 | Wasserstein ultrametric Kloeckner; Kantorovich tree Evans Matsen | web+arXiv | ~18 | 2 |
| Q4 | stopping time bounded potential no-go / coefficient stopping Garner | web+arXiv | ~40 | 1 (Garner 1981) |

---

## 3. Thematic bibliography

Every entry: short role in *this* project, then full citation with DOI/arXiv
when confirmed. Order within each domain is roughly chronological.

### 3.A Surveys and annotated bibliographies

| Tag | Role for this project |
|-----|------------------------|
| **`[bib]` Lagarias 1985** | Canonical short survey; coefficient stopping time and its cycle implication |
| **`[bib]` Lagarias 2010** | Edited volume (Ultimate Challenge); handbook entry point |
| **`[adjacent]` Lagarias bib. I** | Authoritative ~annotated corpus 1963–1999; primary Q1 search surface |
| **`[adjacent]` Lagarias bib. II** | Corpus 2000–2009 |

1. **`[bib]` Lagarias, J. C. (1985).** The \(3x+1\) problem and its
   generalizations. *Amer. Math. Monthly* **92**(1), 3–23.
   doi:[10.1080/00029890.1985.11971528](https://doi.org/10.1080/00029890.1985.11971528).

2. **`[bib]` Lagarias, J. C., ed. (2010).** *The Ultimate Challenge: The
   \(3x+1\) Problem.* AMS, Providence, RI. ISBN 978-0-8218-4940-8.

3. **`[adjacent]` Lagarias, J. C. (2011 update).** The \(3x+1\) problem: an
   annotated bibliography (1963–1999). arXiv:[math/0309224](https://arxiv.org/abs/math/0309224).

4. **`[adjacent]` Lagarias, J. C. (2012 update).** The \(3x+1\) problem: an
   annotated bibliography, II (2000–2009). arXiv:[math/0608208](https://arxiv.org/abs/math/0608208).

### 3.B Stopping times and almost-all results

The field's **positive** frontier (Tier 3 G11). Natural density up through
Korec; logarithmic density in Tao.

| Tag | Role |
|-----|------|
| **`[bib]` Terras 1976** | Finite stopping time for almost all \(n\) (natural density); parity bijection seeds |
| **`[bib]` Everett 1977** | Independent almost-all finite stopping / iteration analysis |
| **`[adjacent]` Allouche 1978/79** | \(\mathrm{Col}_{\min}(N)<N^\theta\) a.e., \(\theta>\tfrac32-\log_2 3\approx 0.869\) |
| **`[adjacent]` Korec 1994** | Same with \(\theta>\log 3/\log 4\approx 0.7924\) |
| **`[bib]` Tao 2022** | \(\mathrm{Col}_{\min}(N)\le f(N)\) a.e. (log-density) for every \(f\to\infty\) |
| **`[bib]` Garner 1981** | Coefficient stopping time conjecture (with Terras) |

5. **`[bib]` Terras, R. (1976).** A stopping time problem on the positive
   integers. *Acta Arith.* **30**(3), 241–252.
   doi:[10.4064/aa-30-3-241-252](https://doi.org/10.4064/aa-30-3-241-252).
   **Crossref verified 2026-07-18.**

6. **`[bib]` Everett, C. J. (1977).** Iteration of the number-theoretic
   function \(f(2n)=n\), \(f(2n+1)=3n+2\). *Adv. Math.* **25**(1), 42–45.
   doi:[10.1016/0001-8708(77)90087-1](https://doi.org/10.1016/0001-8708(77)90087-1).

7. **`[adjacent]` Allouche, J.-P. (1978–1979).** Sur la conjecture de
   “Syracuse–Kakutani–Collatz”. *Séminaire de Théorie des Nombres de Bordeaux*,
   Exp. No. 9. (As cited by Tao 2022 and Lagarias surveys; not in Crossref as
   a journal article.)

8. **`[adjacent]` Korec, I. (1994).** A density estimate for the \(3x+1\)
   problem. *Math. Slovaca* **44**(1), 85–89. (Standard citation in Tao 2022
   for the \(\log 3/\log 4\) threshold; Math. Slovaca pre-Crossref era —
   record taken from secondary citation chain, not re-DOI'd.)

9. **`[bib]` Garner, L. E. (1981).** On the Collatz \(3n+1\) algorithm.
   *Proc. Amer. Math. Soc.* **82**(1), 19–22.
   doi:[10.1090/S0002-9939-1981-0603593-2](https://doi.org/10.1090/S0002-9939-1981-0603593-2).
   **Crossref verified 2026-07-18.**

10. **`[bib]` Tao, T. (2022).** Almost all orbits of the Collatz map attain
    almost bounded values. *Forum Math. Pi* **10**, e12.
    doi:[10.1017/fmp.2022.8](https://doi.org/10.1017/fmp.2022.8);
    arXiv:[1909.03562](https://arxiv.org/abs/1909.03562).
    **Crossref verified 2026-07-18.**

**Density ladder (for G11 / `collatz/density.py`).**

| Result | Notion of “almost all” | Bound |
|--------|------------------------|-------|
| Terras 1976 / Everett 1977 | natural density | finite stopping time / \(\mathrm{Col}_{\min}<N\) |
| Allouche 1978/79 | natural density | \(\mathrm{Col}_{\min}<N^\theta\), \(\theta>0.869\) |
| Korec 1994 | natural density | \(\theta>\log 3/\log 4\approx 0.7924\) |
| **Tao 2022** | **logarithmic density** | \(\mathrm{Col}_{\min}\le f(N)\) for every \(f\to\infty\) |

### 3.C Cycles and Diophantine exclusion

| Tag | Role |
|-----|------|
| **`[bib]` Eliahou 1993** | Diophantine lower bounds on nontrivial cycle length |
| **`[bib]` Simons–de Weger 2005** | \(m\)-cycle theory + computation |
| **`[bib]` Hercher 2023** | No \(m\)-cycles for \(m\le 91\) (current combinatorial record) |
| **`[bib]` Khinchin 1964** | Continued-fraction background for certified convergents |

11. **`[bib]` Eliahou, S. (1993).** The \(3x+1\) problem: new lower bounds on
    nontrivial cycle lengths. *Discrete Math.* **118**(1–3), 45–56.
    doi:[10.1016/0012-365X(93)90052-U](https://doi.org/10.1016/0012-365X(93)90052-U).
    **Crossref verified 2026-07-18.**

12. **`[bib]` Simons, J. and de Weger, B. (2005).** Theoretical and
    computational bounds for \(m\)-cycles of the \(3n+1\) problem. *Acta
    Arith.* **117**(1), 51–70.
    doi:[10.4064/aa117-1-3](https://doi.org/10.4064/aa117-1-3).
    **Crossref verified 2026-07-18.**

13. **`[bib]` Hercher, C. (2023).** There are no Collatz \(m\)-cycles with
    \(m\le 91\). *J. Integer Sequences* **26**(3), Article 23.3.5.
    arXiv:[2201.00406](https://arxiv.org/abs/2201.00406);
    journal:[JIS](https://cs.uwaterloo.ca/journals/JIS/VOL26/Hercher/hercher5.html).

14. **`[bib]` Khinchin, A. Ya. (1964).** *Continued Fractions.* Univ. of
    Chicago Press (Dover reprint 1997).

### 3.D 2-adic structure and conjugacy

| Tag | Role |
|-----|------|
| **`[bib]` Terras 1976** | Parity vector bijection on \(\mathbb{Z}/2^k\mathbb{Z}\) |
| **`[bib]` Bernstein–Lagarias 1996** | \(3x+1\) conjugacy map on \(\mathbb{Z}_2\) |
| **`[bib]` Kingsbery–Levin–Preygel–Silva 2009, 2011** | Measure-preserving / Bernoulli \(p\)-adic shifts |

15. **`[bib]` Bernstein, D. J. and Lagarias, J. C. (1996).** The \(3x+1\)
    conjugacy map. *Canad. J. Math.* **48**(6), 1154–1169.
    doi:[10.4153/cjm-1996-060-x](https://doi.org/10.4153/cjm-1996-060-x)
    (note: Crossref normalizes the suffix as `-x`; older `-6` redirects).
    **Crossref verified 2026-07-18.**

16. **`[bib]` Kingsbery, J., Levin, A., Preygel, A., Silva, C. E. (2009).**
    On measure-preserving \(\mathcal{C}^1\) transformations of compact-open
    subsets of non-archimedean local fields. *Trans. Amer. Math. Soc.*
    **361**(1), 61–85.
    doi:[10.1090/S0002-9947-08-04686-2](https://doi.org/10.1090/S0002-9947-08-04686-2);
    arXiv:[0710.5562](https://arxiv.org/abs/0710.5562).

17. **`[bib]` Kingsbery, J., Levin, A., Preygel, A., Silva, C. E. (2011).**
    Dynamics of the \(p\)-adic shift and applications. *Discrete Contin. Dyn.
    Syst.* **30**(1), 209–218.
    doi:[10.3934/dcds.2011.30.209](https://doi.org/10.3934/dcds.2011.30.209);
    arXiv:[0903.4226](https://arxiv.org/abs/0903.4226).

### 3.E Modular Markov chains and statistical models

| Tag | Role |
|-----|------|
| **`[bib]` Matthews–Watts 1984, 1985** | Induced chains mod \(3^k\); non-uniform stationary vectors |
| **`[bib]` Sinai 2003** | Statistical \((3x+1)\) model |
| **`[bib]` Kontorovich–Sinai 2007** | Structure theorem for \((3x+1)\) |
| **`[bib]` Krasikov–Lagarias 2003** | Density bounds via difference inequalities; inverse-tree lower bounds |

18. **`[bib]` Matthews, K. R. and Watts, A. M. (1984).** A generalization of
    Hasse's generalization of the Syracuse algorithm. *Acta Arith.* **43**(2),
    167–175.

19. **`[bib]` Matthews, K. R. and Watts, A. M. (1985).** A Markov approach to
    the generalized Syracuse algorithm. *Acta Arith.* **45**(1), 29–42.
    doi:[10.4064/aa-45-1-29-42](https://doi.org/10.4064/aa-45-1-29-42).
    **Crossref verified 2026-07-18.**

20. **`[bib]` Sinai, Y. G. (2003).** Statistical \((3x+1)\) problem.
    *Comm. Pure Appl. Math.* **56**(7), 1016–1028.
    doi:[10.1002/cpa.10084](https://doi.org/10.1002/cpa.10084)
    (**corrected 2026-07-18**: older bib entry used `…10082`, which Crossref
    resolves to an unrelated paper; the Sinai article is `…10084`).

21. **`[bib]` Kontorovich, A. V. and Sinai, Y. G. (2007).** Structure theorem
    for \((3x+1)\) problem. *C. R. Math. Acad. Sci. Paris* **345**(8), 421–426.
    doi:[10.1016/j.crma.2007.09.006](https://doi.org/10.1016/j.crma.2007.09.006).

22. **`[bib]` Krasikov, I. and Lagarias, J. C. (2003).** Bounds for the
    \(3x+1\) problem using difference inequalities. *Acta Arith.* **109**(3),
    237–258.
    doi:[10.4064/aa109-3-4](https://doi.org/10.4064/aa109-3-4).
    **Crossref verified 2026-07-18.**

23. **`[bib]` Wirsching, G. J. (1998).** *The Dynamical System Generated by
    the \(3n+1\) Function.* Lecture Notes in Math. **1681**, Springer.
    doi:[10.1007/BFb0095985](https://doi.org/10.1007/BFb0095985).
    **Crossref verified 2026-07-18.** Predecessor-set and measure-theoretic
    monograph; no Lyapunov nonexistence statement (Q4).

### 3.F Lyapunov, RCWA, and obstruction relatives

| Tag | Role |
|-----|------|
| **`[bib]` Kohl 2008** | Closest reputable *no-go* relative (RCWA conjugacy, not additive potential) |
| **`[bib]` Karp 1978** | Maximum mean cycle algorithm for the residue-graph certificate |

24. **`[bib]` Kohl, S. (2008).** On conjugates of Collatz-type mappings.
    *Int. J. Number Theory* **4**(1), 117–120.
    doi:[10.1142/S1793042108001237](https://doi.org/10.1142/S1793042108001237).
    **Crossref verified 2026-07-18.**

25. **`[bib]` Karp, R. M. (1978).** A characterization of the minimum cycle
    mean in a digraph. *Discrete Math.* **23**(3), 309–311.
    doi:[10.1016/0012-365X(78)90011-0](https://doi.org/10.1016/0012-365X(78)90011-0)
    (Crossref also indexes a closely related 23(1) page range for the same
    article family; the manuscript's 23(3):309–311 matches the standard
    MathSciNet record).

**Contamination note (not retained).** Non-refereed manuscripts claiming a
strictly decreasing global Lyapunov/entropy functional for Collatz are
abundant (viXra, ResearchGate, predatory venues, several 2024–2026). They
assert *existence* for classes this project *rules out*. None is peer-reviewed
in a reputable venue; none is cited.

### 3.G Transfer operators, Wasserstein, ultrametric optimal transport

| Tag | Role |
|-----|------|
| **`[bib]` Villani 2009** | Standard OT reference |
| **`[bib]` Evans–Matsen 2012** | Exact \(W_1\) on metric trees, eq. (5) = `lem:w1formula` |
| **`[bib]` Kloeckner 2015** | Ultrametric Wasserstein framework (\(\ell^1\) isometry) |
| **`[bib]` Tao 2022** | Syracuse random variables; TV equidistribution (stronger than \(\tau\)) |

26. **`[bib]` Villani, C. (2009).** *Optimal Transport: Old and New.*
    Grundlehren **338**, Springer.
    doi:[10.1007/978-3-540-71050-9](https://doi.org/10.1007/978-3-540-71050-9).

27. **`[bib]` Evans, S. N. and Matsen, F. A. (2012).** The phylogenetic
    Kantorovich–Rubinstein metric for environmental sequence samples.
    *J. R. Stat. Soc. Ser. B* **74**(3), 569–592.
    doi:[10.1111/j.1467-9868.2011.01018.x](https://doi.org/10.1111/j.1467-9868.2011.01018.x);
    arXiv:[1005.1699](https://arxiv.org/abs/1005.1699).
    **Crossref + full-text eq. (5) verified 2026-07-17/18.**

28. **`[bib]` Kloeckner, B. R. (2015).** A geometric study of Wasserstein
    spaces: ultrametrics. *Mathematika* **61**(1), 162–178.
    doi:[10.1112/S0025579314000059](https://doi.org/10.1112/S0025579314000059);
    arXiv:[1304.5219](https://arxiv.org/abs/1304.5219).
    **Crossref verified 2026-07-18** (Crossref lists year 2014 for online;
    print year 2015 as in the journal issue).

### 3.H Computational verification

| Tag | Role |
|-----|------|
| **`[bib]` Oliveira e Silva 2010** | Classical large-scale empirical verification survey chapter |
| **`[bib]` Barina 2021** | Verification to \(2^{68}\) |
| **`[bib]` Barina 2025** | Verification to \(2^{71}\) — manuscript's published hypothesis |

29. **`[bib]` Oliveira e Silva, T. (2010).** Empirical verification of the
    \(3x+1\) and related conjectures. In Lagarias (ed.), *The Ultimate
    Challenge*, AMS, 189–207.

30. **`[bib]` Barina, D. (2021).** Convergence verification of the Collatz
    problem. *J. Supercomput.* **77**(3), 2681–2688.
    doi:[10.1007/s11227-020-03368-x](https://doi.org/10.1007/s11227-020-03368-x).
    **Crossref verified 2026-07-18.**

31. **`[bib]` Barina, D. (2025).** Improved verification limit for the
    convergence of the Collatz conjecture. *J. Supercomput.* **81**(7), 810.
    doi:[10.1007/s11227-025-07337-0](https://doi.org/10.1007/s11227-025-07337-0).
    **Crossref verified 2026-07-18.** Headline published limit \(N=2^{71}\).

### 3.I Formalization frontier (Tier 3 G10 pointer)

Not a bibliographic claim of the paper; recorded for G10 positioning.

32. **`[formal]` Lean 4 / mathlib4 community.** [leanprover-community.github.io](https://leanprover-community.github.io/).

33. **`[formal]` Collatz Conjecture Challenge (ccchallenge).** Community effort
    to formalize Collatz-related results in Lean; natural home for a
    machine-checked `thm:main`. Site: [ccchallenge.org](https://ccchallenge.org/).

34. **`[formal]` This repository, `lean/`.** Lake project (Lean 4.24.0, pure
    stdlib) proving the arithmetic core of `thm:main`
    (`modular_obstruction_arith`, `modular_obstruction_integer_form`). See
    `lean/README.md`.

---

## 4. Priority questions — verdicts

### Q1 — Priority of the modular-Lyapunov no-go

**Verdict: no prior explicit statement located.** Underlying phenomenon
(class \(-1\bmod 2^k\) rises for \(k\) steps) is Terras/Everett folklore;
packaging as nonexistence for \(V=\log_2 n+w(n\bmod 2^j)\) on \(\mathbb{Z}_+\)
was not found. Closest reputable relative: **Kohl (2008)** (RCWA conjugacy
no-go, different object). Contamination literature asserts the opposite.

**Consequence (applied).** Cite Kohl in `rem:originality`; hedge as documented
negative search, not proof of absence.

### Q2 — Wasserstein / mixing state of the art

**Verdict: ingredients classical; coefficient packaging is this project's.**

- \(\tau(P_k)\le 1/3\) is elementary from \(|3|_3=1/3\). Tao 2022 is *far
  stronger* (TV equidistribution of Syracuse r.v.'s).
- \(\mathbb{Z}_2\) finite-time Haar averaging is the functional reading of
  Terras / Bernstein–Lagarias / KLPS 2009–2011.
- **Update vs earlier draft of this review:** the manuscript now proves
  \(\tau(P)=1/3\) exactly with closed form
  \(\tau(P_k)=\tfrac13(1-q_k^2)/(1+q_k+q_k^2)\), \(q_k=2^{-2\cdot 3^{k-2}}\),
  and **non-attainment** on \(\mathbb{Z}_3\) (`thm:tausharp`). The old “τ
  exactness open” clause in a previous version of §Q2 is **superseded**.

**Consequence (applied).** Cite KLPS 2009/2011; keep Tao as the stronger mixing
result; present \(\tau=1/3\) closed form as the project's sharp packaging.

### Q3 — Closed-form \(W_1\) on ultrametric quotients

**Verdict: known exactly as Evans–Matsen (2012) eq. (5) specialized to the
rooted \(p\)-ary tree of depth \(k\); Kloeckner (2015) is the ultrametric
framework.** Self-contained proof retained for reproducibility. G6 closed
(re-verified arXiv:1005.1699 and arXiv:1304.5219, 2026-07-17/18).

### Q4 — Priority of the variable-depth no-go

**Verdict: no prior statement located.** Ingredients folklore; packaging as
nonexistence for bounded \(w\) under adapted rules / expansion rate / exact
boundary \(\Lambda\) not found. Engaged boundary object: Terras–Garner
coefficient stopping time conjecture (open; truth \(\Rightarrow\) no nontrivial
cycles, Lagarias 1985). Garner 1981 added to the bibliography.

**Consequence (applied).** `rem:stoppingoriginality`; cite Garner with Terras;
`thm:exactboundary` makes the boundary a theorem, not a remark.

---

## 5. Mapping: manuscript claims → literature

| Manuscript claim / object | Primary literature | This project's contribution |
|---------------------------|--------------------|----------------------------|
| Almost-all finite stopping | Terras, Everett | Formalize + exact bad-set rationals (`density.py`) |
| Almost-all almost-bounded | Tao 2022 | Cite; G11 program, no new theorem |
| Cycle exclusion Diophantine | Eliahou, Simons–de Weger | Exact convergent certification |
| Cycle combinatorial record | Hercher 2023 | Cite; do not claim improvement |
| Verification limit \(2^{71}\) | Barina 2025 | Conditional bounds at that \(N\) |
| Parity bijection / shift | Terras; Bernstein–Lagarias | Exact checks mod \(2^k\) |
| \(p\)-adic Bernoulli | KLPS 2009/2011 | Wasserstein re-reading (`thm:z2`) |
| Chains mod \(3^k\) | Matthews–Watts | Exact stationary + rank collapse |
| Modular Lyapunov no-go | Folklore (Terras/Everett); no prior thm | `thm:main` + Lean arithmetic core |
| RCWA relative | Kohl 2008 | Delimit novelty |
| Variable-depth no-go | — (search negative) | `thm:stopping`, `thm:expansion`, `thm:exactboundary` |
| Coefficient CSTC | Terras, Garner, Lagarias | Boundary prototype of the no-go |
| \(W_1\) on trees / ultrametrics | Evans–Matsen; Kloeckner | Specialize + self-contained proof |
| \(\tau(P)=1/3\) sharp | — (upper bound folklore) | Closed form + non-attainment |
| Max-mean cycle algorithm | Karp 1978 | Residue-graph certificate |

---

## 6. Consequences for repository files

| File | Status |
|------|--------|
| `paper/references.bib` | Contains all **`[bib]`** entries; Sinai DOI corrected to `10.1002/cpa.10084` if needed |
| `paper/main.tex` | Cites the thematic core; originality hedges match Q1/Q4 |
| `REPORT.md` / `RELATORIO.md` | Mirror substantive citations bilingually |
| `todo/G11_PROGRAM.md` | Research program for §3.B beyond the submission |
| `lean/README.md` | Formalization status for §3.I |
| `collatz/density.py` | Laboratory hooks for Terras bad-set / log-density partials |

**DOI fix applied with this revision:** Sinai (2003) in `references.bib` must
use `doi = {10.1002/cpa.10084}` (not `…10082`). Bernstein–Lagarias DOI may use
Crossref's canonical `10.4153/cjm-1996-060-x`.

---

## 7. Limitations of this review

1. **Negative results (Q1, Q4) are documented searches, not proofs of
   absence.** MathSciNet review text was not exhaustively mined beyond
   Lagarias's curated corpus, arXiv, Crossref, and forward citation chasing.
2. **Pre-digital venues** (Allouche séminaire notes; Korec *Math. Slovaca*
   1994) may lack Crossref DOIs; they are retained via the Tao/Lagarias
   citation chain with that caveat marked.
3. **Q1** concerns the *specific* additive class \(\log_2 n+w(n\bmod 2^j)\).
   Logically equivalent statements under different terminology could exist.
4. **G11 almost-all program** is deliberately *not* folded into the
   manuscript's claimed results; §3.B is orientation, not a theorem list for
   the paper.
5. **Formalization literature** is a living frontier; §3.I will date quickly.

---

## 8. Quick reference — all DOIs (Crossref-audited 2026-07-18)

| Key | DOI |
|-----|-----|
| terras1976 | 10.4064/aa-30-3-241-252 |
| everett1977 | 10.1016/0001-8708(77)90087-1 |
| garner1981 | 10.1090/S0002-9939-1981-0603593-2 |
| lagarias1985 | 10.1080/00029890.1985.11971528 |
| eliahou1993 | 10.1016/0012-365X(93)90052-U |
| bernsteinlagarias1996 | 10.4153/cjm-1996-060-x |
| krasikovlagarias2003 | 10.4064/aa109-3-4 |
| sinai2003 | **10.1002/cpa.10084** |
| simonsdeweger2005 | 10.4064/aa117-1-3 |
| kontorovichsinai2007 | 10.1016/j.crma.2007.09.006 |
| kohl2008 | 10.1142/S1793042108001237 |
| kingsberyetal2009 | 10.1090/S0002-9947-08-04686-2 |
| kingsberyetal2011 | 10.3934/dcds.2011.30.209 |
| evansmatsen2012 | 10.1111/j.1467-9868.2011.01018.x |
| kloeckner2015 | 10.1112/S0025579314000059 |
| wirsching1998 | 10.1007/BFb0095985 |
| villani2009 | 10.1007/978-3-540-71050-9 |
| tao2022 | 10.1017/fmp.2022.8 |
| barina2021 | 10.1007/s11227-020-03368-x |
| barina2025 | 10.1007/s11227-025-07337-0 |
| karp1978 | 10.1016/0012-365X(78)90011-0 |
| matthewswatts1985 | 10.4064/aa-45-1-29-42 |
| hercher2023 | arXiv:2201.00406 (JIS 26 (2023) Art. 23.3.5) |

arXiv companions: Lagarias bib. `math/0309224`, `math/0608208`; Tao
`1909.03562`; Evans–Matsen `1005.1699`; Kloeckner `1304.5219`; KLPS
`0710.5562`, `0903.4226`; Hercher `2201.00406`.
