import argparse
import re
from typing import Dict, List, Tuple


class LengthDoesntMatchError(Exception):
    def __init__(self, message='Length of the two given lists do not match.'):
        super().__init__(message)


class ProbabilitySumToOneError(Exception):
    def __init__(self, message='Probabilities should sum to 1.'):
        super().__init__(message)


def huffman(alphabet: List[Tuple[List[str], float]],
            verbose: bool = False) -> Dict[str, str]:
    encoding = dict()
    # Sort by probability descending
    for i in range(len(alphabet) - 1):
        alphabet = sorted(alphabet, key=lambda x: x[1], reverse=True)
        alphabet, two_min = alphabet[:-2], alphabet[-2:]
        combined_key, combined_prob = two_min[0][0] + two_min[1][0], two_min[0][1] + two_min[1][1]
        if verbose:
            print(f"Iteration {i+1}: combine '{', '.join(two_min[0][0])}' and '{', '.join(two_min[1][0])}' "
                  f"to have a probability of {two_min[0][1] + two_min[1][1]}")
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


def main(alphabet: List[str], probabilities: List[float], to_encode: str,
         verbose: bool = False) -> None:
    if len(alphabet) != len(probabilities):
        raise LengthDoesntMatchError(f'Length of the two lists, alphabet and probability, do not match.')
    epsilon = 0.00001
    if sum(probabilities) >= 1 + epsilon or sum(probabilities) <= 1 - epsilon:
        raise ProbabilitySumToOneError()
    encoding = huffman(list(zip([[symbol] for symbol in alphabet], probabilities)), verbose)
    new_line_tab = '\n\t'
    tab = '\t'

    print(
        f'The Huffman code table of: ({", ".join(alphabet)}) is:\n\t{new_line_tab.join(reversed([f"{i + tab} {j}" for i, j in list(encoding.items())]))}')
    if to_encode is not None:
        print(f'The huffman encoding of "{to_encode}" is {" ".join([encoding[i] for i in to_encode])}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Retrieve the Huffman Coding of a given alphabet.')
    parser.add_argument('-a', '--alphabet', type=str, nargs='+', required=True,
                        help='List of symbols in the alphabet.')
    parser.add_argument('-p', '--probability', type=float, nargs='+', required=True,
                        help='Probabilities of given symbols.')
    parser.add_argument('-e', '--encode', type=str, required=False, default=None,
                        help='Input to encode. (Optional)')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Verbose output.')
    args = parser.parse_args()

    main(args.alphabet, args.probability, args.encode, args.verbose)
