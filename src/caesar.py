import math


class Caesar:
    # --------------------ENCODING--------------------

    @staticmethod
    def encoding(encode_file):
        if encode_file[-4:] != ".txt":
            exit(print("Error: Invalid file name"))
        file_from = open(encode_file, encoding='utf-8')
        file_to_name = list(str(encode_file).split("."))[0] + "_caesar.txt"
        read_file = file_from.read()
        file_from.close()
        open(file_to_name, 'wb').close()
        file_to = open(file_to_name, 'ab')

        encoded_string = ""
        file_length = math.ceil(len(read_file) / 10000)
        for i in range(file_length):
            if i < file_length - 1:
                block = read_file[i * 10000: (i + 1) * 10000]
            else:
                block = read_file[i * 10000:]
            for j in range(len(block)):
                encoded_string += chr((ord(block[j]) + 3) % 1114112)
            file_to.write(encoded_string.encode(encoding='utf-8'))
            encoded_string = ""
        file_to.close()

    # --------------------DECODING--------------------

    @staticmethod
    def decoding(decode_file):
        if decode_file[-11:] != "_caesar.txt":
            exit(print("Error: Invalid file name"))
        file_from = open(decode_file, 'rb').read()
        read_file = file_from.decode('utf-8')
        file_to_name = list(str(decode_file).split("."))[0].split("_")[0] + ".txt"
        open(file_to_name, 'w', encoding='utf-8').close()
        file_to = open(file_to_name, 'a', encoding='utf-8')

        decode_string = ""
        file_length = math.ceil(len(read_file) / 10000)
        for i in range(file_length):
            if i < file_length - 1:
                block = read_file[i * 10000: (i + 1) * 10000]
            else:
                block = read_file[i * 10000:]
            for j in range(len(block)):
                decode_string += chr((ord(block[j]) + 1114109) % 1114112)
            file_to.write(decode_string)
            decode_string = ""
        file_to.close()
