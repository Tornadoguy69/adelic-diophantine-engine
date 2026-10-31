#!/usr/bin/env python3
"""
verify_s_block_theorems.py
==========================
Standalone Benchmark & Reproduction Script for Block-Level Theorems:
  - Table 3: Classical Eliahou Bound vs. Dual-Block Drift Bound (Theorems 3.1 & 3.2)
  - Table 4: General s-Block Exponential Seesaw Exponents & Thresholds (Theorem 3.3)
  - Table 5: Discrete Integer-Rigidity Minimax vs. Continuous Bound (Theorem 3.5)
  - Table 6: Sturmian Attractor Rational Cyclic Inversion (Theorem 3.6)
  - Table 7: Combinatorial Density Deficit & Sturmian 2-Adic Annihilation (Theorem 3.7)

Author: Tornado Guy
Date: October 2026
License: MIT
"""

import math
import time
from fractions import Fraction
from itertools import combinations


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


def reproduce_table_5():
    theta = math.log2(3.0)
    print("\n" + "=" * 105)
    print("TABLE 5: Discrete Integer-Rigidity Minimax vs Continuous Seesaw Bound (Theorem 3.5)")
    print("=" * 105)
    print(f"{'k':>2} | {'s':>2} | {'Continuous Bound s*2^(-Cs*k)':>29} | {'Discrete Integer Max':>21} | {'Tightening':>11} | {'Optimal Discrete rho'}")
    print("-" * 105)
    for k, S in [(17, 27), (29, 46), (41, 65)]:
        E_total = S - k
        for s in [2, 3, 4, 6, 8, E_total]:
            c_s = (theta - 1.0) / ((theta ** s) - 1.0)
            cont_bound = s * (2.0 ** (-c_s * k))

            raw_geom = [theta ** m for m in range(s)]
            rho_A = [max(1, int(round(k * x / sum(raw_geom)))) for x in raw_geom]
            while sum(rho_A) > k:
                idx = max(range(s), key=lambda i: rho_A[i])
                rho_A[idx] -= 1
            while sum(rho_A) < k:
                rho_A[-1] += 1
            beta_A = [1] * (s - 1) + [E_total - (s - 1)]

            rho_B = [((m + 1) * k) // s - (m * k) // s for m in range(s)]
            beta_B = [((m + 1) * E_total) // s - (m * E_total) // s for m in range(s)]

            def eval_config(rhos, betas):
                min_u = float('inf')
                for m in range(s):
                    suf = 0.0
                    terms_sum = 0.0
                    for j in range(s, 0, -1):
                        if j < s:
                            idx = (m + j) % s
                            suf += (theta - 1.0) * rhos[idx] - betas[idx]
                        b_curr = betas[(m + j - 1) % s]
                        terms_sum += (2.0 ** suf) * (1.0 - 2.0 ** (-b_curr))
                    u_r = (2.0 ** (-rhos[m])) * terms_sum
                    if u_r < min_u:
                        min_u = u_r
                return min_u

            best_val = 0.0
            best_rho = None
            for r_init, b_init in [(rho_A, beta_A), (rho_B, beta_B)]:
                curr_r = list(r_init)
                curr_b = list(b_init)
                curr_v = eval_config(curr_r, curr_b)
                improved = True
                while improved:
                    improved = False
                    for i in range(s):
                        if curr_r[i] <= 1:
                            continue
                        for j in range(s):
                            if i == j:
                                continue
                            curr_r[i] -= 1
                            curr_r[j] += 1
                            v = eval_config(curr_r, curr_b)
                            if v > curr_v + 1e-12:
                                curr_v = v
                                improved = True
                                break
                            curr_r[i] += 1
                            curr_r[j] -= 1
                        if improved:
                            break
                    for i in range(s):
                        if curr_b[i] <= 1:
                            continue
                        for j in range(s):
                            if i == j:
                                continue
                            curr_b[i] -= 1
                            curr_b[j] += 1
                            v = eval_config(curr_r, curr_b)
                            if v > curr_v + 1e-12:
                                curr_v = v
                                improved = True
                                break
                            curr_b[i] += 1
                            curr_b[j] -= 1
                        if improved:
                            break
                if curr_v > best_val:
                    best_val = curr_v
                    best_rho = list(curr_r)

            ratio = cont_bound / best_val if best_val > 0 else 0.0
            rho_str = str(best_rho[:7]) + ("..." if len(best_rho) > 7 else "")
            print(f"{k:2d} | {s:2d} | {cont_bound:29.6f} | {best_val:21.6f} | {ratio:10.2f}x | {rho_str}")


def reproduce_table_6(max_s: int = 50):
    print("\n" + "=" * 78)
    print("TABLE 6: Sturmian Attractor Rational Cyclic Inversion (Theorem 3.6)")
    print("=" * 78)
    print(f"{'Blocks s':>8} | {'Sturmian Pattern rho':<25} | {'Exact Rational u_1':>20} | {'Numerator Bits':>16}")
    print("-" * 78)
    for s in range(5, max_s + 1, 5):
        rhos = [2 if (i % 3 != 0) else 1 for i in range(s)]
        mat = [[Fraction(0) for _ in range(s)] for _ in range(s)]
        vec = [Fraction(1) for _ in range(s)]
        for m in range(s):
            mat[m][m] = -Fraction(3 ** rhos[m])
            mat[m][(m + 1) % s] = Fraction(1 << (rhos[(m + 1) % s] + 1))

        m_matrix = [row[:] for row in mat]
        v_vec = list(vec)
        for i in range(s):
            pivot = i
            while pivot < s and m_matrix[pivot][i] == 0:
                pivot += 1
            if pivot == s:
                continue
            m_matrix[i], m_matrix[pivot] = m_matrix[pivot], m_matrix[i]
            v_vec[i], v_vec[pivot] = v_vec[pivot], v_vec[i]

            fac = m_matrix[i][i]
            for j in range(i, s):
                m_matrix[i][j] /= fac
            v_vec[i] /= fac

            for r in range(s):
                if r != i and m_matrix[r][i] != 0:
                    factor = m_matrix[r][i]
                    for j in range(i, s):
                        m_matrix[r][j] -= factor * m_matrix[i][j]
                    v_vec[r] -= factor * v_vec[i]

        u_1 = v_vec[0]
        u_1_float = float(u_1) if u_1 > 0 else 0.0
        bits = u_1.numerator.bit_length() if u_1 > 0 else 0
        rho_str = str(rhos[:6]) + ("..." if len(rhos) > 6 else "")
        print(f"{s:8d} | {rho_str:<25} | {u_1_float:20.4f} | {bits:16d}")


def reproduce_table_7():
    print("\n" + "=" * 98)
    print("TABLE 7 (Part 1): Canonical Sturmian Word Shifts vs. 2-Adic Scrambler (Theorem 3.7)")
    print("=" * 98)
    resonants = [
        (5, 8), (12, 19), (17, 27), (22, 35), (29, 46),
        (34, 54), (41, 65), (53, 84), (94, 149), (306, 485)
    ]
    print(f"{'k':>3} | {'S':>3} | {'s=S-k':>5} | {'Max u1_arch':>11} | {'Min u1_2adic':>22} | {'Bits of u1_2adic':>18} | {'Bit Fill Ratio'}")
    print("-" * 98)

    for k, S in resonants:
        s = S - k
        D = abs((1 << S) - (3 ** k))
        rhos_base = [((m + 1) * k) // s - (m * k) // s for m in range(s)]

        max_u_arch = 0.0
        min_u_2adic = 1 << S
        best_bits = (S, S)

        for shift in range(s):
            rhos = rhos_base[shift:] + rhos_base[:shift]
            rho0 = rhos[0]
            mod_bits = S - rho0
            M2 = 1 << mod_bits
            inv_neg3k = pow(-(3 ** k), -1, M2)

            U1 = 0
            r_tilde = k - rho0
            r_plus_b_prefix = 0
            for j in range(1, s + 1):
                if j > 1:
                    r_tilde -= rhos[j - 1]
                    r_plus_b_prefix += rhos[j - 1] + 1
                U1 += (3 ** r_tilde) << r_plus_b_prefix

            u_arch = U1 / D
            u_2adic = (U1 * inv_neg3k) & (M2 - 1)

            if u_arch > max_u_arch:
                max_u_arch = u_arch
            if u_2adic < min_u_2adic:
                min_u_2adic = u_2adic
                best_bits = (u_2adic.bit_length(), mod_bits)

        b_len, m_bits = best_bits
        u2_str = f"{min_u_2adic:,}" if min_u_2adic < 10**15 else f"~2^{min_u_2adic.bit_length()-1}"
        print(f"{k:3d} | {S:3d} | {s:5d} | {max_u_arch:11.2f} | {u2_str:>22} | {b_len:7d} / {m_bits:<8d} | {100.0*b_len/m_bits:13.1f}%")

    print("\n" + "=" * 112)
    print("TABLE 7 (Part 2): Exhaustive Scan Across ALL C(S-k, 2k-S) Words in {1,2}^s (Theorem 3.7)")
    print("=" * 112)
    print(f"{'k':>2} | {'S':>2} | {'s':>2} | {'Count C(s,2k-S)':>15} | {'Expected Min n0':>18} | {'Actual Min n0_2adic':>20} | {'Min u1_2adic':>16} | {'Target u1_arch'}")
    print("-" * 112)

    for k, S in [(5, 8), (12, 19), (17, 27), (22, 35), (29, 46), (34, 54), (41, 65)]:
        s = S - k
        k2 = 2 * k - S
        D = (1 << S) - (3 ** k)
        M2 = 1 << S
        c3_inv = [pow(-(3 ** (i + 1)), -1, M2) for i in range(k)]
        pow3_k = [3 ** (k - 1 - i) for i in range(k)]

        lut_c3 = [[c3_inv[m + c] << (2 * m + c + 1) for c in range(k2 + 1)] for m in range(s)]
        lut_p3 = [[pow3_k[m + c] << (2 * m + c + 1) for c in range(k2 + 1)] for m in range(s)]

        min_n0 = M2
        min_u1 = M2
        target_u1_arch = 0.0

        rhos = [1] * s
        for two_positions in combinations(range(s), k2):
            for pos in two_positions:
                rhos[pos] = 2
            rho0 = rhos[0]

            c = 0
            n0_plus_1_2adic = 0
            sparse_arch_num = 0
            for m in range(s):
                if rhos[m] == 2:
                    c += 1
                    rhos[m] = 1
                n0_plus_1_2adic += lut_c3[m][c]
                sparse_arch_num += lut_p3[m][c]

            n0_plus_1_2adic &= (M2 - 1)
            n0_2adic = (n0_plus_1_2adic - 1) & (M2 - 1)
            u1_2adic = n0_plus_1_2adic >> rho0
            u1_arch = sparse_arch_num / ((1 << rho0) * D)

            if n0_2adic < min_n0:
                min_n0 = n0_2adic
            if u1_2adic < min_u1:
                min_u1 = u1_2adic
                target_u1_arch = u1_arch

        cnt = math.comb(s, k2)
        exp_min = (1 << S) / (2.0 * cnt)
        print(f"{k:2d} | {S:2d} | {s:2d} | {cnt:15,d} | {exp_min:18,.1f} | {min_n0:20,d} | {min_u1:16,d} | {target_u1_arch:14.2f}")


if __name__ == "__main__":
    t0 = time.time()
    reproduce_table_3()
    reproduce_table_4()
    reproduce_table_5()
    reproduce_table_6()
    reproduce_table_7()
    print(f"\nAll benchmark tables reproduced in {time.time() - t0:.3f} seconds.")
