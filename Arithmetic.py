import argparse
from typing import List, Tuple


def arithmetic_encoding(alphabet: List[Tuple[str, float]], to_encode: str) -> Tuple[float, float]:
    alphabet = sorted(alphabet, key=lambda x: x[1], reverse=True)

    lower_limit = 0
    upper_limit = 1

    for char in to_encode:
        limit_range = upper_limit - lower_limit

        char_index = [symbol[0] for symbol in alphabet].index(char)
        prob_below = sum([alphabet[i][1] for i in range(char_index)])
        prob_above = 1 - (prob_below + alphabet[char_index][1])
        lower_limit += (limit_range * prob_below)
        upper_limit -= (limit_range * prob_above)

    return lower_limit, upper_limit


def main(alphabet: List[str], probabilities: List[float], to_encode: str):
    lower_limit, upper_limit = arithmetic_encoding(list(zip(alphabet, probabilities)), to_encode)
    print(f'The range of the encoded symbol is {lower_limit}, {upper_limit}.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Retrieve the Arithmetic code for a set of symbols.')
    parser.add_argument('-a', '--alphabet', type=str, nargs='+', required=True,
                        help='List of symbols in the alphabet.')
    parser.add_argument('-p', '--probability', type=float, nargs='+', required=True,
                        help='Probabilities of given symbols.')
    parser.add_argument('-s', '--string', type=str, required=True,
                        help='String to encode.')
    args = parser.parse_args()

    main(args.alphabet, args.probability, args.string)
