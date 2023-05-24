import argparse
import math


def lempel_ziv_welch_encode(to_compress: str, no_of_bits: int):
    characters = list(dict.fromkeys(to_compress))
    dictionary = dict()

    current_val = -1
    for char in characters:
        current_val += 1
        dictionary[char] = current_val

    encoding = ""
    p = to_compress[0]
    for char in to_compress[1:]:
        if p + char in dictionary:
            p = p + char
        else:
            encoding += bin(dictionary[p])[2:].zfill(no_of_bits) + ' '
            if current_val < 2 ** no_of_bits - 1:
                dictionary[p + char] = (current_val := current_val + 1)
            p = char
    return encoding + bin(dictionary[to_compress[-1]])[2:].zfill(no_of_bits)


def lempel_ziv_welch_decode(encoding, letters, bits: int = 3):
    dictionary = {count: letter for count, letter in enumerate(letters)}
    next = len(letters)
    chunks = [
        encoding[i * bits:(i * bits) + bits]
        for i in range(math.ceil(len(encoding) / bits))
    ]
    oldcode = 0
    str2 = ''
    decoding = []
    for chunk in chunks:
        newcode = int(chunk, 2)
        if newcode not in dictionary:
            str1 = dictionary[oldcode]
            str1 += str2
        else:
            str1 = dictionary[newcode]
        decoding += str1
        str2 = str1[0]
        if oldcode in dictionary and dictionary[oldcode] + str2 not in dictionary.values() and next <= (2 ** bits - 1):
            dictionary[next] = dictionary[oldcode] + str2
            next += 1
        oldcode = newcode
    return ''.join(decoding)


def main(plain: str,
         bits: int):
    encoding = lempel_ziv_welch_encode(plain, bits)
    print(f'The LZW encoding of {plain} using a {bits} bit dictionary is:\n\t{encoding}')
    decoding = lempel_ziv_welch_decode(''.join(encoding.split(' ')), list(dict.fromkeys(plain)), bits)
    print(f'The LZW decoding of {encoding} using a {bits} bit dictionary is:\n\t{decoding}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Perform LZW on a string')
    parser.add_argument('-p', '--plain', type=str, required=True,
                        help='Plaintext to compress.')
    parser.add_argument('-b', '--bits', type=int, required=False, default=3,
                        help='Number of bits in the dictionary. (Default=3)')
    args = parser.parse_args()
    main(args.plain, args.bits)
