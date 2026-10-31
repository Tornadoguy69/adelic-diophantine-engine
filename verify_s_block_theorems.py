#!/usr/bin/env python3
"""
verify_s_block_theorems.py
==========================
Standalone Benchmark & Reproduction Script for Theorems 3.1, 3.2, and 3.3:
  - Table 3: Classical Eliahou Bound vs. Dual-Block Drift Bound
  - Table 4: General s-Block Exponential Seesaw Exponents & Asymptotic Thresholds

Author: Tornado Guy
Date: October 2026
License: MIT
"""

import math
import time


def reproduce_table_3():
    print("=" * 88)
    print("TABLE 3: Classical Eliahou Bound vs. Dual-Block Drift Bound (Theorems 3.1 & 3.2)")
    print("=" * 88)
    configs = [
        (17, 27, 231),
        (22, 35, 171),
        (29, 46, 323),
        (41, 65, 313)
    ]
    print(f"{'k':>2} | {'S':>2} | {'n0':>4} | {'Active s / k':>12} | {'Classical Eliahou':>18} | {'Dual-Block Drift':>18} | {'Exact Trajectory ln-Sum':>24}")
    print("-" * 88)
    for k, S, n0 in configs:
        curr = n0
        traj = [curr]
        shifts = []
        for _ in range(k):
            val = 3 * curr + 1
            v2 = (val & -val).bit_length() - 1
            shifts.append(v2)
            curr = val >> v2
            traj.append(curr)

        s = sum(1 for a in shifts if a >= 2)
        n_min = min(traj[:-1])
        eliahou_bound = k / (3.0 * n_min)

        rhos, betas, u_starts = [], [], []
        r_count = 0
        start_n = traj[0]
        for idx, a in enumerate(shifts):
            if a == 1:
                r_count += 1
            else:
                rhos.append(r_count + 1)
                betas.append(a - 1)
                u_starts.append(start_n)
                start_n = traj[idx + 1]
                r_count = 0

        drift_terms = []
        for m in range(len(rhos)):
            rho = rhos[m]
            beta = betas[m]
            u_m = (u_starts[m] + 1) // (1 << rho)
            n_next = u_starts[(m + 1) % len(rhos)]
            t1 = ((1 << beta) - 1) / ((3 ** rho) * u_m)
            t2 = (1.0 - 2.0**(-beta)) / n_next
            drift_terms.append(min(t1, t2))
        dual_drift = sum(drift_terms)
        exact_sum = sum(math.log(1.0 + 1.0 / (3.0 * x)) for x in traj[:-1])
        s_k_str = f"{s} / {k}"
        print(f"{k:2d} | {S:2d} | {n0:4d} | {s_k_str:>12} | {eliahou_bound:18.6f} | {dual_drift:18.6f} | {exact_sum:24.6f}")


def reproduce_table_4():
    theta = math.log2(3.0)
    print("\n" + "=" * 90)
    print("TABLE 4: General s-Block Exponential Seesaw Exponents & Thresholds (Theorem 3.3)")
    print("=" * 90)
    print(f"{'Blocks s':>8} | {'Exact Exponent -C_s':>21} | {'Decay Base 2^(-C_s)':>21} | {'Unconditional Threshold k_0(s)':>32}")
    print("-" * 90)
    for s in [1, 2, 3, 4, 5, 6, 8]:
        Cs = (theta - 1.0) / ((theta ** s) - 1.0)
        base = 2.0 ** (-Cs)
        k0 = 10
        while s * (base ** k0) >= 0.0002 * (k0 ** -13.3):
            k0 += 1
        k0_str = f"k_0 = {k0:,d}"
        print(f"{s:8d} | {-Cs:21.6f} | {base:21.6f} | {k0_str:>32}")


if __name__ == "__main__":
    t0 = time.time()
    reproduce_table_3()
    reproduce_table_4()
    print(f"\nBenchmark completed in {time.time() - t0:.3f} seconds.")
