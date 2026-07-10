"""
collatz — Computational laboratory for the Collatz Conjecture.

A set of algorithms to search for invariants, symmetries, and structural
properties of the 3n+1 dynamics that might point to a proof or a
counterexample to the conjecture.

Modules
-------
core        Maps (Collatz, accelerated T, Syracuse), trajectories, stopping times.
search      Direct counterexample search: verification sieve, cycle
            detection (Brent), divergence probing, records.
cycles      EXACT enumeration of cycles via parity vectors (rational
            fixed point) and cycle exclusion via continued fractions of log2(3).
padic       2-adic structure: Terras bijection Q_k, conjugacy with the shift,
            binomial census of parities.
invariants  Modular invariants (induced maps, conserved partitions),
            drift by residue class, search for a Lyapunov function
            via maximum mean cycle (Karp's algorithm).
symmetries  Search for affine conjugacies between 3n+d systems and affine
            automorphisms of the modular transition graphs.
spectral    Syracuse transfer operator on (Z/3^k)*: exact stationary
            distribution and spectral gap.
transfer    INFINITE transfer operator: Koopman operator of the Syracuse
            chain on Lip(Z_3) (Wasserstein contraction <= 1/3, uniform in k),
            transfer operator of T on Lip(Z_2) (contraction 1/2, Haar invariant)
            and the Z_+ face (nilpotent sections, obstruction to n^theta
            weights, density contraction).
tree        Inverse tree (preimages of 1): coverage density and growth
            rate.
report      Orchestrates all modules and produces a report of findings.
"""

__version__ = "0.1.0"
