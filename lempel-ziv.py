import argparse
from typing import List


def lempel_ziv(to_encode: str, no_of_bits: int = 3):
    highest_value = (2 ** no_of_bits)
    current_value = 0
    encodings = dict()
    for i in set(to_encode):
        encodings[i] = bin(current_value)[2:].zfill(no_of_bits)
        current_value += 1

    encoding = ''
    start = 0
    i = 1
    while i < len(to_encode) + 1:
        if to_encode[start:i] in encodings.keys():
            i += 1
            continue
        s = to_encode[start:i - 1]
        encoding += encodings[s]
        X = to_encode[i - 1]
        if current_value < highest_value:
            encodings[s+X] = bin(current_value)[2:].zfill(no_of_bits)
            current_value += 1

        start = i - 1

    return encoding

def main(to_encode: str, bits: int):
    encoding = lempel_ziv(to_encode, no_of_bits=bits)
    print(encoding)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Retrieve the Arithmetic code for a set of symbols.')
    parser.add_argument('-s', '--string', type=str, required=True,
                        help='String to encode.')
    parser.add_argument('-b', '--bits', type=int, required=False, default=3,
                        help='Number of bits to use in the dictionary.')
    args = parser.parse_args()

    main(args.string, args.bits)


