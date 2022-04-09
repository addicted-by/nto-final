def chars_to_bin(chars):
    """
    Преобразование символов в бинарный формат
    """
    return ''.join([bin(ord(c))[2:].zfill(8) for c in chars])


def block_iterator(text_bin, block_size: int):
    """
    Поблочный вывод бинарных данных
    """
    for i in range(len(text_bin)):
        if not i % block_size:
            yield text_bin[i:i + block_size]


def get_check_bits_data(value_bin: list, check_bits: list) -> map:
    """
    Получение информации о контрольных битах из бинарного блока данных
    """
    check_bits_count_map = {k: 0 for k in check_bits}
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


def set_empty_check_bits(value_bin: list, check_bits: list) -> list:
    """
    Добавить в бинарный блок "пустые" контрольные биты
    """
    for bit in check_bits:
        value_bin = value_bin[:bit - 1] + '0' + value_bin[bit - 1:]
    return value_bin


def set_check_bits(value_bin: list, check_bits: list):
    """
    Установить значения контрольных бит
    """
    value_bin = set_empty_check_bits(value_bin, check_bits)
    check_bits_data = get_check_bits_data(value_bin, check_bits)
    for check_bit, bit_value in check_bits_data.items():
        value_bin = '{0}{1}{2}'.format(
            value_bin[:check_bit - 1], bit_value, value_bin[check_bit:])
    return value_bin


def get_check_bits(value_bin: list, check_bits: list) -> map:
    """
    Получить информацию о контрольных битах из блока бинарных данных
    """
    check_bits_map = {}
    for index, value in enumerate(value_bin, 1):
        if index in check_bits:
            check_bits_map[index] = int(value)
    return check_bits_map


def exclude_check_bits(value_bin: list, check_bits: list) -> str:
    """
    Исключить информацию о контрольных битах из блока бинарных данных
    """
    clean_value_bin = ''
    for index, char_bin in enumerate(list(value_bin), 1):
        if index not in check_bits:
            clean_value_bin += char_bin

    return clean_value_bin

def check_and_fix_error(encoded_chunk, check_bits):
    """
    Проверка и исправление ошибки в блоке бинарных данных
    """
    check_bits_encoded = get_check_bits(encoded_chunk, check_bits)
    check_item = exclude_check_bits(encoded_chunk, check_bits)
    check_item = set_check_bits(check_item, check_bits)
    check_bits_ = get_check_bits(check_item, check_bits)
    if check_bits_encoded != check_bits_:
        invalid_bits = []
        for check_bit_encoded, value in check_bits_encoded.items():
            if check_bits_[check_bit_encoded] != value:
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
