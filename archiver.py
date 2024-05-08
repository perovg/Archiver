import sys

from src.caesar import Caesar
from src.shennon import Shennon


""" Check received file extension """
def check_file_extension(filename, expected_ext):
    if not filename.endswith(expected_ext):
        raise ValueError(f"Error: Invalid file extension '{filename}'. Expected '{expected_ext}'.")


match sys.argv:
    case _, 'sh', '-e', encode_file:
        """ Encoding a file using the Shennon algorithm """

        check_file_extension(encode_file, '.txt')
        Shennon.encoding(encode_file)

    case _, 'sh', '-d', decode_file:
        """ Decoding a file encoded by the Shennon algorithm """

        check_file_extension(decode_file, '.prar')
        Shennon.decoding(decode_file)

    case _, 'caesar', '-e', encode_file:
        """ Encoding a file using the Caesar cipher """

        check_file_extension(encode_file, '.txt')
        Caesar.encoding(encode_file)

    case _, 'caesar', '-d', decode_file:
        """ Decoding a file encoded by the Caesar cipher """

        check_file_extension(decode_file, '_caesar.txt')
        Caesar.decoding(decode_file)
