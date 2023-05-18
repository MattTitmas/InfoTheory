import argparse
from typing import List, Set
from functools import lru_cache


def c_inf(codes: Set[str]):
    seen = set(frozenset(codes))
    c_infinity = set()

    current_c = 0
    while True:
        c_set = generate_cn(codes, current_c := current_c + 1)
        c_infinity = c_infinity.union(c_set)
        seen.add(frozenset(c_set))
        if len(c_set) == 0 or c_set in seen:
            break
    return c_infinity


@lru_cache()
def generate_cn(c, n):
    if n == 0:
        return set(c)
    else:
        # create a set to hold our new elements
        cn = set()

        # generate c_(n-1)
        cn_minus_1 = generate_cn(c, n - 1)

        for u in c:
            for v in cn_minus_1:
                if (len(u) > len(v)) and u.find(v) == 0:
                    cn.add(u[len(v):])
        for u in cn_minus_1:
            for v in c:
                if len(u) > len(v) and u.find(v) == 0:
                    cn.add(u[len(v):])
        return cn


def main(codes: List[str],
         symbols: List[str] | None):
    print(c_inf(frozenset(codes)).isdisjoint(set(codes)))

    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Perform the Sardinas-Patterson algorithm on a code.')
    parser.add_argument('-c', '--codes', nargs='+', required=True, type=str,
                        help='Code words.')
    parser.add_argument('-s', '--symbols', nargs='+', required=False, type=str,
                        help='Corresponding symbols to the inputted code words.')
    args = parser.parse_args()
    main(args.codes, args.symbols)
