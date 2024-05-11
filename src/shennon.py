from math import copysign, fabs, floor, isfinite, modf, ceil, log


class Shennon:
    # --------------------ENCODING--------------------

    """ Main encoding method. """
    @staticmethod
    def encoding(encode_file):
        with open(encode_file, encoding='utf-8') as file_from:
            read_file = file_from.read()

            keys = Shennon.shennon(read_file)
            bin_code = Shennon.encode(read_file, keys)

            encoded_file = (str(Shennon.compress(bin_code)[1]) + '$').encode('utf-8')
            keys = Shennon.write_keys(keys).encode('utf-8')
            last_char = Shennon.compress(bin_code)[0].encode('utf-8')
            less = (keys + encoded_file + last_char)

            file_to_name = f"{encode_file.split('.')[0]}.prar"
            file_to = open(file_to_name, 'wb')
            file_to.write(less)
            file_to.close()

    """ Translation the file to encrypted form. """
    @staticmethod
    def encode(string, key):
        binary_string = ''
        substring = ''
        for sym in string:
            substring += sym
            if substring in key:
                binary_string += key[substring]
                substring = ''
        return binary_string

    """ Converting fractional numbers to binary number system. """
    @staticmethod
    def bi(fractional_number):
        if not isfinite(fractional_number):
            return repr(fractional_number)  # inf nan

        sign = '-' * (copysign(1.0, fractional_number) < 0)
        frac, fint = modf(fabs(fractional_number))  # split on fractional, integer parts
        numerator, denominator = frac.as_integer_ratio()  # frac = numerator / denominator
        assert denominator & (denominator - 1) == 0  # power of two
        return f'{sign}{floor(fint):b}.{numerator:0{denominator.bit_length() - 1}b}'

    """ Determining encryption keys. """
    @staticmethod
    def shennon(string):
        statistics = {}

        for sym in string:
            statistics[sym] = statistics.get(sym, 0) + 1
        for sym in statistics:
            statistics[sym] = statistics[sym] / len(string)
        statistics = dict(sorted(statistics.items(), key=lambda x: x[1], reverse=True))

        auxiliary_dict = {}
        step = []
        for sym in range(len(list(statistics.values()))):
            step.append(sum(list(statistics.values())[:sym]))
            step[sym] = float(step[sym])

        for sym in statistics:
            auxiliary_dict[sym] = ceil(-(log(statistics[sym], 2)))  # powers of two

        for sym in range(len(step)):
            step[sym] = str(Shennon.bi(step[sym]))[2:]
        sim = dict(zip(statistics.keys(), step))

        keys_dict = {}
        for sym in sim:
            if len(sim[sym]) < auxiliary_dict[sym]:
                while len(sim[sym]) < auxiliary_dict[sym]:
                    sim[sym] += '0'
            keys_dict[sym] = sim[sym][:auxiliary_dict[sym]]
        return keys_dict

    """ File compression. """
    @staticmethod
    def compress(string):
        cnt = 0
        while len(string) % 8 != 0:
            string += '0'
            cnt += 1

        text = ''
        for i in range(0, len(string), 8):
            sym = chr(int(string[i:i + 8], 2))
            text += sym
        return text, cnt

    """ Preparing encryption keys for recording. """
    @staticmethod
    def write_keys(keys_dictionary):
        keys_string = ''
        for key in keys_dictionary:
            keys_string += key + keys_dictionary[key] + '||'
        keys_string += '$'
        return keys_string

    # -------------------DECODING--------------------

    """ Main decoding method. """
    @staticmethod
    def decoding(decode_file):
        with open(decode_file, 'rb').read() as file_from:
            read_file = file_from.decode('utf-8')

            border_1_idx = read_file.find('$')
            keys = dict(Shennon.search_keys(read_file[:border_1_idx + 1], '$', '||'))
            border_2_idx = read_file.find('$', border_1_idx + 1)
            extra_char = int(read_file[border_1_idx + 1:border_2_idx])
            encoded_file = read_file[border_2_idx + 1:]
            decoded_file = Shennon.expand(encoded_file, extra_char)

            file_to_name = f"{decode_file.split('.')[0]}.txt"
            file_to = open(file_to_name, 'w', encoding='utf-8')
            file_to.write(Shennon.decode(decoded_file, keys))
            file_to.close()

    """ Translated file from encrypted form. """
    @staticmethod
    def decode(string, key):
        binary_string = ''
        substring = ''
        for sym in string:
            substring += sym
            if substring in key:
                binary_string += key[substring]
                substring = ''
        return binary_string

    """ Finding an almost decrypted string. """
    @staticmethod
    def expand(string, extra_char):
        output_string = ''
        for num in string:
            sym = str(bin(ord(num))[2:])
            while len(sym) % 8 != 0:
                sym = '0' + sym
            output_string += sym
        if extra_char != 0:
            output_string = output_string[:-extra_char]
        return output_string

    """ Reading encryption keys at the beginning of a file. """
    @staticmethod
    def search_keys(string, sim, delimiter):
        header_string = ''
        for sym in string:
            if sym != sim:
                header_string += sym
        split_header_string = header_string.split(delimiter)[:-1]
        key = []
        values = []
        for sym in split_header_string:
            key.append(sym[0])
            values.append(sym[1:])
        keys_dict = dict(zip(values, key))
        return keys_dict
