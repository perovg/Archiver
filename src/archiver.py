import sys

from shennon import Shennon
from caesar import Caesar

match sys.argv:
    case _, 'sh', '-e', encode_file:  # Encoding a file using the Shennon algorithm
        Shennon.encoding(encode_file)

    case _, 'sh', '-d', decode_file:  # Decoding a file encoded by the Shennon algorithm
        Shennon.decoding(decode_file)

    case _, 'caesar', '-e', encode_file:  # Encoding a file using the Caesar cipher
        Caesar.encoding(encode_file)

    case _, 'caesar', '-d', decode_file:  # Decoding a file encoded by the Caesar cipher
        Caesar.decoding(decode_file)
