# Adelic Diophantine Engine (`adelic-diophantine-engine`)

**An Open-Source Computational Notebook, Modular Dynamics Suite, and Interactive 3D Visualizer for $(2,3)$-Adic Carry Mechanics and Collatz Cycle Equations.**

[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](#quick-start--reproduction)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](#license)
[![Math: Number Theory](https://img.shields.io/badge/MSC2020-11B83_%7C_11D41-red.svg)](#mathematical-architecture--theorems)
[![Live 3D Visualizer](https://img.shields.io/badge/🎮_Live_Demo-3D_Visualizer-crimson.svg)](#-interactive-3d-webgl-visualizer)

This repository is an open-source educational and computational laboratory exploring the interplay between local $p$-adic modular carry chains ($p \in \{2, 3\}$), Archimedean cycle equations, and block decompositions in the $3n+1$ (Collatz) dynamical system and generalized Fermat-type Diophantine equations.

It provides a zero-dependency Python verification suite reproducing all modular identities and cycle equations in **$<3$ seconds**, alongside an interactive 3D WebGL phase-space simulator.

---

## 📌 Context & Relationship to the Mathematical Literature

To maintain clear mathematical context, this repository should be understood alongside the established literature on the Collatz conjecture:

1. **The Computational Horizon ($2^{71}$):**
   - Through distributed computation, David Barina (*Journal of Supercomputing*, 2025) and previously Oliveira e Silva et al. (2010) have verified that all starting integers $n < 2^{71} \approx 2.36 \times 10^{21}$ converge to 1.
   - Consequently, the smallest element $m$ of any hypothetical non-trivial cycle must satisfy $m > 2^{71}$. Combined with Eliahou's theorem (below), this implies that any non-trivial cycle must have at least **$k > 3.55 \times 10^{11}$ odd steps**. Small values of $k$ (such as $k \le 306$) are already ruled out by these computational verifications.

2. **Cycle Upper Bounds (Eliahou, 1993):**
   - Shalom Eliahou (*Discrete Mathematics* 118, 1993) established the standard upper bound on the minimal element $m$ of a cycle:
     $$m \le \frac{k}{3 \ln(2^S / 3^k)}$$
     At $k = 306, S = 485$, Eliahou's bound yields $m \le 99,700$.
   - The block-core envelope bound derived here, $B_{\text{Spitzer}}(k, S) = \lfloor (S - k) \frac{2^S}{2^S - 3^k} - 1 \rfloor \approx 175,194$, is an elementary combinatorial consequence of requiring each discrete block core $u_m \ge 1$. While it provides a pedagogical illustration of how discrete block-core rigidity bounds the cycle envelope without transcendental estimates, it is numerically larger (weaker) than Eliahou's 1993 bound.

3. **$m$-Cycles in the Literature (Simons & de Weger, Hercher):**
   - In the literature, an **$m$-cycle** is defined as a cycle with $m$ local minima (i.e. $m$ circuit blocks of odd steps), **not** $k$ odd steps.
   - Ray Steiner (1977) ruled out 1-cycles ($m = 1$).
   - John Simons (2005) completely resolved 2-cycles ($m = 2$).
   - Simons and Benne de Weger (*Acta Arithmetica* 117, 2005) proved there are no $m$-cycles for $m \le 68$.
   - Christian Hercher (*Journal of Integer Sequences* 26, 2023) extended this to prove there are no $m$-cycles for $m \le 91$.

4. **Scope of This Project:**
   - This project does **not** claim to prove the Collatz conjecture or establish new global cycle non-existence bounds beyond the literature.
   - It is an exploratory computational toolkit and visualizer that makes $(2,3)$-modular dynamics, 2-adic Hensel lifting, and block-core algebra accessible, interactive, and transparently reproducible.

---

## 🎮 Interactive 3D WebGL Visualizer

The visualizer renders the $(2,3)$-Adelic phase space in 3D, allowing real-time exploration of how modular trajectories drift relative to the hypothetical cycle diagonal.

### How to Run:
* **Option A: Local Server (Recommended for Best Performance):**
  ```bash
  python -m http.server 8000 --directory .
  ```
  Then open `http://localhost:8000/index.html` in your browser.
* **Option B: Direct File Open:**
  Open [`index.html`](index.html) or [`adelic_diophantine_visualizer.html`](adelic_diophantine_visualizer.html) directly in Chrome, Edge, or Firefox.
* **Option C: Online Preview:**
  [Launch via HTMLPreview](https://htmlpreview.github.io/?https://github.com/Tornadoguy69/adelic-diophantine-engine/blob/main/index.html) (requires WebGL-compatible browser).

---

## 📁 Repository Structure

| File | Description | Language |
| :--- | :--- | :---: |
| 🎮 [**`index.html`**](index.html) / [`adelic_diophantine_visualizer.html`](adelic_diophantine_visualizer.html) | Interactive 3D Three.js Phase Space & `BigInt` Bit-Scrambler | HTML5 / WebGL |
| 🐍 [**`adelic_diophantine_engine.py`**](adelic_diophantine_engine.py) | Master verification suite reproducing all 9 theorems and 7 data tables in $2.74\text{s}$ | Python 3 |
| 📊 [**`verify_s_block_theorems.py`**](verify_s_block_theorems.py) | Benchmark engine verifying block-core equations and phase transitions in $0.24\text{s}$ | Python 3 |
| 📐 [**`prove_no_2block_cycles.py`**](prove_no_2block_cycles.py) | Pedagogical reproduction of the 2-block cycle obstruction | Python 3 |
| 📄 [**`adelic_carry_obstructions.tex`**](adelic_carry_obstructions.tex) | Complete AMS-LaTeX manuscript documenting the modular algebra | LaTeX |

---

## 🔬 Mathematical Architecture & Theorems

### Part I: The Collatz Cycle Equation ($n_0(2^S - 3^k) = \mathcal{N}(\mathcal{A})$)

* **Theorem 2.1 (2-Adic Bit-Freezing Law & Telescoping Identity):** For any cumulative parity vector $\mathcal{A} = (0 = A_0 < A_1 < \dots < A_{k-1} < S)$, fixing $A_{i+1}$ freezes the bottom $A_{i+1}+1$ binary digits of the 2-adic starting state $n_{0,\text{2-adic}}(\mathcal{A}) = (-3^{-k}\mathcal{N}(\mathcal{A})) \bmod 2^S$. Along the trajectory, $\mathcal{N}(\mathcal{A})$ telescopes identically to:
  $$\mathcal{N}(\mathcal{A}) = 3^k n_0 \left( \prod_{t=0}^{k-1} \left(1 + \frac{1}{3n_t}\right) - 1 \right)$$

* **Theorem 2.2 (Forward-2-Adic Bijection):** The map $\mathcal{A} \mapsto n_{0,\text{2-adic}}(\mathcal{A})$ maps the $\binom{S-1}{k-1}$ combinatorial parity vectors onto the odd integers $n_0 \in [1, 2^S - 1]$ satisfying $A_{k-1}(n_0) < S \le A_k(n_0)$, enabling minimum extraction via forward trajectory evaluation.

* **Theorem 2.3 (Modular Discrepancy Identity):** The gap between the Archimedean quotient $n_{0,\text{arch}}(\mathcal{A}) = \mathcal{N}(\mathcal{A})/(2^S - 3^k)$ and the 2-adic integer realization $n_0$ satisfies:
  $$\left\vert n_{0,\text{arch}}(\mathcal{A}) - n_0 \right\vert = \left(\frac{2^S}{|2^S - 3^k|}\right) \cdot \left\vert 2^{A_k - S} n_k - n_0 \right\vert$$

* **Theorem 2.5 ($(2,3)$-Adic Duality):** For the rational cycle quotient $\mathcal{R}(\mathcal{A}) = \mathcal{N}(\mathcal{A})(2^S - 3^k)^{-1}$, its 2-adic projection is the starting state $\mathcal{R}_2(\mathcal{A}) \bmod 2^S = n_0$, while its 3-adic projection is the ending state $\mathcal{R}_3(\mathcal{A}) \bmod 3^k = 2^{A_k - S} n_k$. Divisibility by any prime factor $p \mid (2^S - 3^k)$ requires $\mathcal{R}_3(\mathcal{A}) \equiv \mathcal{R}_2(\mathcal{A}) \pmod p$.

* **Theorems 3.1 & 3.2 (Sparse Block Decomposition & Dual-Product Identity):** Grouping steps into $s$ blocks with odd cores $u_m = (n_{\text{start}(m)} + 1)/2^{\rho_m}$ yields the cyclic bidiagonal system $2^{\rho_{m+1}+\beta_m} u_{m+1} - 3^{\rho_m} u_m = 2^{\beta_m} - 1$ and the Dual-Product Identity:
  $$\frac{2^S}{3^k} = \prod_{m=1}^s \left( 1 + \frac{2^{\beta_m} - 1}{3^{\rho_m} u_m} \right) = \prod_{m=1}^s \left( 1 - \frac{1 - 2^{-\beta_m}}{2^{\rho_{m+1}} u_{m+1}} \right)^{-1}$$

* **Theorem 3.3 ($s$-Block Exponential Decay via Spitzer's Lemma):** In any $s$-block cycle of length $k$, at least one block core $u_m \in \mathbb{Z}_{\text{odd}}^+$ satisfies:
  $$\frac{2^S - 3^k}{2^S} \le u_m \left(\frac{2^S - 3^k}{2^S}\right) < s \cdot 2^{-C_s k}, \quad C_s = \frac{\log_2 3 - 1}{(\log_2 3)^s - 1}$$

* **Theorem 3.5 (Block-Core Envelope Bound):** Requiring every integer block core $u_m \ge 1$ across $1 \le s \le S - k$ imposes the envelope bound:
  $$n_0 \le B_{\text{Spitzer}}(k, S) \coloneqq \left\lfloor (S - k) \frac{2^S}{2^S - 3^k} - 1 \right\rfloor = \lfloor (S - k) Q(k, S) - 1 \rfloor$$
  *(Note: At $k = 306, S = 485$, this gives $B_{\text{Spitzer}} = 175,194$. While this dramatically improves upon the naive product bound $B_{\max} \approx (1.5)^k Q \approx 7.94 \times 10^{56}$, Eliahou's 1993 bound already provided $m \le 99,700$, and computational checks have since verified $n < 2^{71}$).*

---

### Part II: Finite Computational Sieve for Generalized Fermat Equations

* **Proposition 4.1 (Hensel Carry-Overflow in $A^x + B^y = C^z$):** For $C^z - A^x = 2^S B_{\text{odd}}^y$ ($S = by, 2 \nmid z$), the bottom $S$ bits of $C$ are uniquely determined by $A$ via $C_0(A) = A^{x z^{-1} \bmod 2^{S-1}} \bmod 2^S$.
* The repository includes a computational multi-layer sieve demonstration (Archimedean floor, 2-adic power sieve, and splitting primes $p \le 181$) testing small coprime bases $A \le 4000$. *(This is a numerical search demonstration and does not prove the general Beal Conjecture).*

---

## 📊 Summary of Data Tables & Benchmarks

The suite reproduces the following data tables in $2.74\text{s}$:

### 1. Collatz Global Minimum Extraction ($n_{0,\text{2-adic}} > 1$, Table 1)
Forward trajectory evaluation extracts the minimal 2-adic seed:

| $k$ | $S$ | Parity Vectors $\binom{S-1}{k-1}$ | $\min n_{0,\text{2-adic}}$ | Top Bits Cancelled | Execution Time |
| :---: | :---: | :---: | :---: | :---: | :---: |
| $17$ | $27$ | $5,311,735$ | $165$ | $19 / 27$ | $0.74\text{ ms}$ |
| $29$ | $46$ | $1,103,068,603,890$ | $91$ | $39 / 46$ | $0.68\text{ ms}$ |
| $41$ | $65$ | $250,649,105,469,666,120$ | $73$ | $58 / 65$ | $0.75\text{ ms}$ |
| $53$ | $84$ | $59,488,706,401,523,551,644,624$ | $871$ | $74 / 84$ | $11.31\text{ ms}$ |

### 2. Dual-Block Drift on Exact-Shift Trajectories (Table 3)
Evaluation of the dual-block identity on exact-shift near-miss orbits:

| $(k,S)$ | $n_0$ | Active Blocks $s/k$ | Classical $\frac{k}{3n_{\min}}$ | Dual-Block Bound | Exact Sum $\sum \ln(1 + \frac{1}{3n_i})$ |
| :---: | :---: | :---: | :---: | :---: | :---: |
| $(17, 27)$ | $231$ | $6 / 17$ | $0.182796$ | $0.047662$ | $0.047186$ |
| $(22, 35)$ | $171$ | $11 / 22$ | $0.236559$ | $0.067508$ | $0.067011$ |
| $(29, 46)$ | $323$ | $11 / 29$ | $0.106227$ | $0.031246$ | $0.031187$ |
| $(41, 65)$ | $313$ | $17 / 41$ | $0.150183$ | $0.049087$ | $0.049085$ |

### 3. Block-Core Envelope Bound Comparison (Table 5)

| $k$ | $S$ | Naive Bound $B_{\max}$ | Envelope Bound $B_{\text{Spitzer}}$ | Eliahou (1993) Bound | Verified Range (Barina 2025) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| $17$  | $27$  | $26,044$              | $263$     | $16$   | Checked to $2^{71}$ |
| $29$  | $46$  | $5,174,697$           | $687$     | $48$   | Checked to $2^{71}$ |
| $41$  | $65$  | $1.46 \times 10^9$    | $2,104$   | $172$  | Checked to $2^{71}$ |
| $306$ | $485$ | $7.94 \times 10^{56}$ | $175,194$ | $99,700$ | Checked to $2^{71}$ |

### 4. Dynamical Drift & Exact-Shift Floor (Table 6)
An empirical demonstration of the two-slope drift heuristic: while the resonant target slope is $\log_2 3 \approx 1.585$, typical Syracuse orbits exhibit a drift slope of $\approx 2.0$, creating an average shift overshoot of $+0.415$ bits/step for non-cyclic trajectories.

| $k$ | $S = \lceil k \log_2 3 \rceil$ | Resonant? | Envelope Bound $B_{\text{Spitzer}}$ | Minimal Exact-Shift $n_0$ | Status vs Envelope |
| :---: | :---: | :---: | :---: | :---: | :---: |
| $17$ | $27$  | Yes | $263$   | $165$    | Inside Envelope ($165 \le 263$) |
| $22$ | $35$  | Yes | $148$   | $171$    | Exceeds Envelope ($171 > 148$) |
| $29$ | $46$  | Yes | $687$   | $313$    | Inside Envelope ($313 \le 687$) |
| $41$ | $65$  | Yes | $2,104$ | $313$    | Inside Envelope ($313 \le 2104$) |
| $58$ | $92$  | Yes | $695$   | $3,097$  | Exceeds Envelope ($3,097 > 695$) |
| $70$ | $111$ | Yes | $1,143$ | $24,601$ | Exceeds Envelope ($24,601 > 1143$) |

---

## 🚀 Quick Start & Reproduction

### Python Verification Suite (Python 3.9+, Zero Dependencies)
```bash
git clone https://github.com/Tornadoguy69/adelic-diophantine-engine.git
cd adelic-diophantine-engine

# Run master verification suite (verifies all theorems & tables in ~2.7s)
python adelic_diophantine_engine.py

# Run standalone benchmark suite (<0.3s)
python verify_s_block_theorems.py
```

---

## License

This project is open-source under the [MIT License](LICENSE).
