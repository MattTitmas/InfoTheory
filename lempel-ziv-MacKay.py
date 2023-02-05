import argparse
from typing import List


def lempel_ziv_encode(to_encode: str) -> str:
    source = {
        0: '',
        1: to_encode[0]
    }
    source_inverse = {
        '': 0,
        to_encode[0]: 1
    }

    codeword = to_encode[0]

    current_string = ''
    current_index = 2

    current_length = 0
    words_added_at_current_length = 0

    for char in to_encode[1:]:
        current_string += char
        if current_string not in source_inverse:
            source[current_index] = current_string
            source_inverse[current_string] = current_index

            binary = bin(source_inverse[current_string[:-1]])[2:]
            binary = binary.zfill(current_length + 1)
            words_added_at_current_length += 1

            if words_added_at_current_length == (2 ** current_length):
                current_length += 1
                words_added_at_current_length = 0
            codeword += binary + current_string[-1] + ' '

            current_string = ""
            current_index += 1

    return codeword + bin(source_inverse[current_string])[2:]


def lempel_ziv_decode(to_decode: str) -> str:
    pointers = {
        "": '',
        "1": to_decode[0]
    }
    # "" instead of "0" as .lstrip(0) changes "0" to ""

    decoded_word = to_decode[0]

    current_word = ''
    current_length = 2
    words_added_at_current_length = 0
    current_index = 2
    for char in to_decode[1:]:
        current_word += char
        if len(current_word) == current_length:
            code_word = pointers[current_word[:-1].lstrip('0')] + current_word[-1]
            pointers[bin(current_index)[2:]] = code_word

            decoded_word += code_word
            current_index += 1
            current_word = ""
            words_added_at_current_length += 1
            if words_added_at_current_length == (2 ** (current_length - 2)):
                words_added_at_current_length = 0
                current_length += 1
    return decoded_word + pointers[current_word.lstrip('0')]


def main(to_encode: str, decode: bool):
    if not decode:
        encoding = lempel_ziv_encode(to_encode)
        print(f'The encoding of {to_encode} is {encoding}.')
        print(f'The length of the original message was {len(to_encode)}, the length of the encoded message is {len(encoding)}')
    else:
        decoding = lempel_ziv_decode(to_encode)
        print(f'The decoding of {to_encode} is {decoding}.')
        print(f'The length of the encoded was {len(to_encode)}, the length of the original message is {len(decoding)}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Retrieve the Arithmetic code for a set of symbols.')
    parser.add_argument('-s', '--string', type=str, required=True,
                        help='String to encode / decode.')
    parser.add_argument('-d', '--decode', action='store_true', required=False,
                        help='Decode the current string?')
    args = parser.parse_args()

    main(args.string, args.decode)
