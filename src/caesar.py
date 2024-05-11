import math


# ----------------WORK WITH FILES----------------


def read_file_contents(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()


def write_file_contents(filename, contents, mode='w'):
    with open(filename, mode, encoding='utf-8') as file:
        file.write(contents)


class Caesar:
    # --------------------ENCODING--------------------
    @staticmethod
    def encode_text(text, shift=3):
        return ''.join(chr((ord(char) + shift) % 1114112) for char in text)

    @staticmethod
    def encoding(encode_file):
        with open(encode_file, encoding='utf-8') as file_from:
            file_to_name = f"{encode_file.split('.')[0]}_caesar.txt"
            read_file = file_from.read()
            file_from.close()
            file_to = open(file_to_name, 'ab')

            file_length = math.ceil(len(read_file) / 10000)
            for i in range(file_length):
                if i < file_length - 1:
                    block = read_file[i * 10000: (i + 1) * 10000]
                else:
                    block = read_file[i * 10000:]
                encoded_string = Caesar.encode_text(block)
                file_to.write(encoded_string.encode(encoding='utf-8'))
            file_to.close()

    # --------------------DECODING--------------------

    @staticmethod
    def decode_text(text, shift=3):
        return ''.join(chr((ord(char) - shift) % 1114112) for char in text)

    @staticmethod
    def decoding(decode_file):
        with open(decode_file, 'rb').read() as file_from:
            read_file = file_from.decode('utf-8')
            file_to_name = f"{decode_file.split('.')[0]}.txt"
            file_to = open(file_to_name, 'a', encoding='utf-8')

            file_length = math.ceil(len(read_file) / 10000)
            for i in range(file_length):
                if i < file_length - 1:
                    block = read_file[i * 10000: (i + 1) * 10000]
                else:
                    block = read_file[i * 10000:]
                decode_string = Caesar.decode_text(block)
                file_to.write(decode_string)
            file_to.close()
