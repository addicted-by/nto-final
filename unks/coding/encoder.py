#!/usr/bin/python3
def chars_to_bin(chars):
    """
    Преобразование символов в бинарный формат
    """
    return ''.join([bin(ord(c))[2:].zfill(8) for c in chars])


def block_iterator(text_bin, block_size):
    """
    Поблочный вывод бинарных данных
    """
    for i in range(len(text_bin)):
        if not i % block_size:
            yield text_bin[i:i + block_size]


def get_check_bits_data(value_bin):
    """
    Получение информации о контрольных битах из бинарного блока данных
    """
    check_bits_count_map = {k: 0 for k in CHECK_BITS}
    for index, value in enumerate(value_bin, 1):
        if int(value):
            bin_char_list = list(bin(index)[2:].zfill(8))
            bin_char_list.reverse()
            for degree in [2 ** int(i) for i, value in enumerate(bin_char_list) if int(value)]:
                check_bits_count_map[degree] += 1
    check_bits_value_map = {}
    for check_bit, count in check_bits_count_map.items():
        check_bits_value_map[check_bit] = 0 if not count % 2 else 1
    return check_bits_value_map


def set_empty_check_bits(value_bin):
    """
    Добавить в бинарный блок "пустые" контрольные биты
    """
    for bit in CHECK_BITS:
        value_bin = value_bin[:bit - 1] + '0' + value_bin[bit - 1:]
    return value_bin


def set_check_bits(value_bin):
    """
    Установить значения контрольных бит
    """
    value_bin = set_empty_check_bits(value_bin)
    check_bits_data = get_check_bits_data(value_bin)
    for check_bit, bit_value in check_bits_data.items():
        value_bin = '{0}{1}{2}'.format(
            value_bin[:check_bit - 1], bit_value, value_bin[check_bit:])
    return value_bin


def get_check_bits(value_bin):
    """
    Получить информацию о контрольных битах из блока бинарных данных
    """
    check_bits = {}
    for index, value in enumerate(value_bin, 1):
        if index in CHECK_BITS:
            check_bits[index] = int(value)
    return check_bits


def exclude_check_bits(value_bin):
    """
    Исключить информацию о контрольных битах из блока бинарных данных
    """
    clean_value_bin = ''
    for index, char_bin in enumerate(list(value_bin), 1):
        if index not in CHECK_BITS:
            clean_value_bin += char_bin

    return clean_value_bin

def check_and_fix_error(encoded_chunk):
    """
    Проверка и исправление ошибки в блоке бинарных данных
    """
    check_bits_encoded = get_check_bits(encoded_chunk)
    check_item = exclude_check_bits(encoded_chunk)
    check_item = set_check_bits(check_item)
    check_bits = get_check_bits(check_item)
    if check_bits_encoded != check_bits:
        invalid_bits = []
        for check_bit_encoded, value in check_bits_encoded.items():
            if check_bits[check_bit_encoded] != value:
                invalid_bits.append(check_bit_encoded)
        num_bit = sum(invalid_bits)
        encoded_chunk = '{0}{1}{2}'.format(
            encoded_chunk[:num_bit - 1],
            int(encoded_chunk[num_bit - 1]) ^ 1,
            encoded_chunk[num_bit:])
    return encoded_chunk


def get_diff_index_list(value_bin1, value_bin2):
    """
    Получить список индексов различающихся битов
    """
    diff_index_list = []
    for index, char_bin_items in enumerate(zip(list(value_bin1), list(value_bin2)), 1):
        if char_bin_items[0] != char_bin_items[1]:
            diff_index_list.append(index)
    return diff_index_list


def encode(source):
    """
    Кодирование данных
    """
    text_bin = chars_to_bin(source)
    result = ''
    for chunk_bin in block_iterator(text_bin, BLOCK_SIZE):
        chunk_bin = set_check_bits(chunk_bin)
        result += chunk_bin
    return result


def decode(encoded, fix_errors=True):
    """
    Декодирование данных
    """
    decoded_value = ''
    fixed_encoded_list = []
    for encoded_chunk in block_iterator(encoded, BLOCK_SIZE + len(CHECK_BITS)):
        if fix_errors:
            encoded_chunk = check_and_fix_error(encoded_chunk)
        fixed_encoded_list.append(encoded_chunk)

    clean_chunk_list = []
    for encoded_chunk in fixed_encoded_list:
        encoded_chunk = exclude_check_bits(encoded_chunk)
        clean_chunk_list.append(encoded_chunk)

    for clean_chunk in clean_chunk_list:
        for clean_char in [clean_chunk[i:i + 8] for i in range(len(clean_chunk)) if not i % 8]:
            decoded_value += chr(int(clean_char, 2))
    return decoded_value


def encoder(filein,fileout):
    global BLOCK_SIZE, CHECK_BITS
    BLOCK_SIZE=8
    CHECK_BITS = [i for i in range(1, BLOCK_SIZE + 1) if not i & (i - 1)]
    s=filein.read()

    encoded = encode(s.decode('utf8'))
    fileout.write(encoded.encode())