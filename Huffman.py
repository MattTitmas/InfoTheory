import argparse
import re
from typing import Dict, List, Tuple


class LengthDoesntMatchError(Exception):
    def __init__(self, message='Length of the two given lists do not match.'):
        super().__init__(message)


class ProbabilitySumToOneError(Exception):
    def __init__(self, message='Probabilities should sum to 1.'):
        super().__init__(message)


def Huffman(alphabet: List[Tuple[List[str], float]]) -> Dict[str, str]:
    encoding = dict()
    # Sort by probability descending
    while len(alphabet) > 1:
        alphabet = sorted(alphabet, key=lambda x: x[1], reverse=True)
        alphabet, two_min = alphabet[:-2], alphabet[-2:]
        combined_key, combined_prob = two_min[0][0] + two_min[1][0], two_min[0][1] + two_min[1][1]
        for i in range(0, len(alphabet) + 1):
            if i == len(alphabet):
                alphabet.append((combined_key, combined_prob))
            if alphabet[i][1] < combined_prob:
                alphabet.insert(i, (combined_key, combined_prob))
                break

        for symbol in two_min[0][0]:
            encoding[symbol] = '0' + encoding.get(symbol, '')

        for symbol in two_min[1][0]:
            encoding[symbol] = '1' + encoding.get(symbol, '')

    return encoding


def main(alphabet: List[str], probabilities: List[float]) -> None:
    if len(alphabet) != len(probabilities):
        raise LengthDoesntMatchError(f'Length of the two lists, alphabet and probability, do not match.')
    epsilon = 0.00001
    if sum(probabilities) >= 1 + epsilon or sum(probabilities) <= 1 - epsilon:
        raise ProbabilitySumToOneError()
    encoding = Huffman(list(zip([[symbol] for symbol in alphabet], probabilities)))
    new_line_tab = '\n\t'

    print(f'The Huffman encoding of: ({", ".join(alphabet)}) is:\n\t{new_line_tab.join(reversed([f"{i}: {j}" for i, j in list(encoding.items())]))}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Retrieve the Huffman Coding of a given alphabet.')
    parser.add_argument('-a', '--alphabet', type=str, nargs='+', required=True,
                        help='List of symbols in the alphabet.')
    parser.add_argument('-p', '--probability', type=float, nargs='+', required=True,
                        help='Probabilities of given symbols.')
    args = parser.parse_args()

    main(args.alphabet, args.probability)
