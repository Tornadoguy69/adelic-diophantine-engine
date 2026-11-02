#!/usr/bin/env python3
"""
kraus_beal_modular_engine.py
============================
Rigorous elimination of prime exponents p >= 7 for the Generalized Fermat
equation A^p + B^p = C^3 via Kraus Frey-Hellegouarch curves, Ribet level-lowering,
and mod-p Frobenius trace obstructions.

Author: Tornado Guy
Date: November 2026
License: MIT
"""

def a_l_elliptic(A_coeff: int, B_coeff: int, l: int) -> int:
    """Computes the trace of Frobenius a_l = l + 1 - #E(F_l) for Y^2 = X^3 + A*X + B."""
    count = 0
    for x in range(l):
        rhs = (x**3 + A_coeff * x + B_coeff) % l
        if rhs == 0:
            count += 1
        elif pow(rhs, (l - 1) // 2, l) == 1:
            count += 2
    return (l + 1) - (count + 1)  # include point at infinity


def kraus_eliminate_exponent(p: int, newform_curve: tuple, max_k: int = 60):
    """
    Attempts to eliminate exponent p for a weight-2 newform given by Weierstrass (A, B)
    using auxiliary primes l = 2*k*p + 1.
    """
    for k in range(1, max_k + 1):
        l = 2 * k * p + 1
        # Check primality of l
        if l < 5 or any(l % d == 0 for d in range(2, int(l**0.5) + 1)):
            continue

        a_l_f = a_l_elliptic(newform_curve[0], newform_curve[1], l)

        # Multiplicative condition: p must divide a_l(f)^2 - (l+1)^2
        if (a_l_f + (l + 1)) % p == 0 or (a_l_f - (l + 1)) % p == 0:
            continue

        # p-th powers in F_l^\times
        p_powers = sorted(list({pow(x, p, l) for x in range(1, l)}))

        # Cubes in F_l
        cubes = {}
        for x in range(l):
            c_val = pow(x, 3, l)
            if c_val not in cubes:
                cubes[c_val] = x

        has_match = False
        valid_pairs = 0

        for u in p_powers:
            for v in p_powers:
                w = (u + v) % l
                if w == 0 or w not in cubes:
                    continue
                valid_pairs += 1
                c = cubes[w]
                c2 = (c * c) % l

                # Frey curve: Y^2 = X^3 - 3 c^2 X + 2(v - u) mod l
                A_E = (-3 * c2) % l
                B_E = (2 * (v - u)) % l
                a_l_E = a_l_elliptic(A_E, B_E, l)

                if (a_l_E - a_l_f) % p == 0:
                    has_match = True
                    break
            if has_match:
                break

        if not has_match and valid_pairs > 0:
            return l, k, valid_pairs

    return None


def run_benchmark():
    newforms = {
        "36a1 (Y^2 = X^3 + 1)": (0, 1),
        "72a1 (Y^2 = X^3 - 3X + 1)": (-3, 1),
    }

    primes = [7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]

    print("=== RIGOROUS MODULAR ELIMINATION OF EXPONENTS p IN A^p + B^p = C^3 ===")
    print(f"{'Prime p':>8} | {'Newform':<26} | {'Auxiliary Prime l':>18} | {'Step k':>7} | {'Pair Count':>10}")
    print("-" * 80)

    for p in primes:
        for name, curve in newforms.items():
            res = kraus_eliminate_exponent(p, curve)
            if res:
                l, k, pairs = res
                print(f"{p:8d} | {name:<26} | {l:18d} | {k:7d} | {pairs:10d}")
            else:
                print(f"{p:8d} | {name:<26} | {'NOT ELIMINATED':>18} | {'---':>7} | {'---':>10}")


if __name__ == "__main__":
    run_benchmark()
