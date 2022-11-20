import argparse
from typing import List


def main(alphabet: List[str], probability: List[float], to_encode: str):
    pass


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
