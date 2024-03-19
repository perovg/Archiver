import sys
import math
from math import copysign, fabs, floor, isfinite, modf

match sys.argv:
    case _, 'sh', '-e', encode_file:  # Encoding a file using the Shennon algorithm
        def encoding():
            def encode(string, key):  # Translation the file to encrypted form
                binn = ''
                j = ''
                for i in string:
                    j += i
                    if j in key:
                        binn += key[j]
                        j = ''
                return binn

            def bi(f):  # Converting fractional numbers to binary number system
                if not isfinite(f):
                    return repr(f)  # inf nan

                sign = '-' * (copysign(1.0, f) < 0)
                frac, fint = modf(fabs(f))  # split on fractional, integer parts
                n, d = frac.as_integer_ratio()  # frac = numerator / denominator
                assert d & (d - 1) == 0  # power of two
                return f'{sign}{floor(fint):b}.{n:0{d.bit_length() - 1}b}'

            def shennon(string):  # Determining encryption keys
                statistics = {}

                for i in string:
                    statistics[i] = statistics.get(i, 0) + 1
                for i in statistics:
                    statistics[i] = statistics[i] / len(string)
                statistics = dict(sorted(statistics.items(), key=lambda x: x[1], reverse=True))

                auxiliary_dict = {}
                step = []
                for i in range(len(list(statistics.values()))):
                    step.append(sum(list(statistics.values())[:i]))
                    step[i] = float(step[i])

                for i in statistics:
                    auxiliary_dict[i] = math.ceil(-(math.log(statistics[i], 2)))  # powers of two

                for i in range(len(step)):
                    step[i] = str(bi(step[i]))[2:]
                sim = dict(zip(statistics.keys(), step))

                keys_dict = {}
                for i in sim:
                    if len(sim[i]) < auxiliary_dict[i]:
                        while len(sim[i]) < auxiliary_dict[i]:
                            sim[i] += '0'
                    keys_dict[i] = sim[i][:auxiliary_dict[i]]
                return keys_dict

            def compress(string):  # File compression
                cnt = 0
                while len(string) % 8 != 0:
                    string += '0'
                    cnt += 1

                text = ''
                for i in range(0, len(string), 8):
                    sym = chr(int(string[i:i + 8], 2))
                    text += sym
                return text, cnt

            def write_keys(keys_dictionary):  # Preparing encryption keys for recording
                keys_string = ''
                for i in keys_dictionary:
                    keys_string += i + keys_dictionary[i] + '||'
                keys_string += '$'
                return keys_string
            if (encode_file[-4:] != ".txt"):
                exit(print("Error: Invalid file name"))
            file_from = open(encode_file, encoding='utf-8')
            read_file = file_from.read()

            keys = shennon(read_file)
            bin_code = encode(read_file, keys)

            encoded_file = (str(compress(bin_code)[1]) + '$').encode('utf-8')
            keys = write_keys(keys).encode('utf-8')
            last_char = compress(bin_code)[0].encode('utf-8')
            less = (keys + encoded_file + last_char)

            file_to_name = list(str(encode_file).split("."))[0] + ".prar"
            file_to = open(file_to_name, 'wb')
            file_to.write(less)
            file_to.close()
        encoding()

    case _, 'sh', '-d', decode_file:  # Decoding a file encoded by the Shennon algorithm
        def decoding():
            def decode(string, key):  # Translated file from encrypted form
                binn = ''
                j = ''
                for i in string:
                    j += i
                    if j in key:
                        binn += key[j]
                        j = ''
                return binn

            def expand(st, extra_char):  # Finding an almost decrypted string
                string = ''
                for i in st:
                    sym = str(bin(ord(i))[2:])
                    while len(sym) % 8 != 0:
                        sym = '0' + sym
                    string += sym
                if extra_char != 0:
                    string = string[:-extra_char]
                return string

            def search_keys(string, sim, delimiter):  # Reading encryption keys at the beginning of a file
                b = ''
                for i in string:
                    if i != sim:
                        b += i
                s = b.split(delimiter)[:-1]
                key = []
                values = []
                for i in s:
                    key.append(i[0])
                    values.append(i[1:])
                keys_dict = dict(zip(values, key))
                return keys_dict

            if (decode_file[-5:] != ".prar"):
                exit(print("Error: Invalid file name"))
            file_from = open(decode_file, 'rb').read()
            read_file = file_from.decode('utf-8')

            border_1_idx = read_file.find('$')
            keys = dict(search_keys(read_file[:border_1_idx + 1], '$', '||'))
            border_2_idx = read_file.find('$', border_1_idx + 1)
            extra_char = int(read_file[border_1_idx + 1:border_2_idx])
            encoded_file = read_file[border_2_idx + 1:]
            decoded_file = expand(encoded_file, extra_char)

            file_to_name = list(str(decode_file).split("."))[0] + ".txt"
            file_to = open(file_to_name, 'w', encoding='utf-8')
            file_to.write(decode(decoded_file, keys))
            file_to.close()
        decoding()

    case _, 'caesar', '-e', encode_file:  # Encoding a file using the Caesar cipher
        if (encode_file[-4:] != ".txt"):
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

    case _, 'caesar', '-d', decode_file:  # Decoding a file encoded by the Caesar cipher
        if (decode_file[-11:] != "_caesar.txt"):
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
