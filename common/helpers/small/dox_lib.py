import struct


class Flags:
    """
    Класс работы с битовыми флагами

    >>> f = Flags(0, Flags.PARAM_BITS)
    Traceback (most recent call last):
        ...
    TypeError: Неправильное значение. Количество битов должно быть целым положительным числом.
    >>> f = Flags(10, 0)
    Traceback (most recent call last):
        ...
    TypeError: Неправильное значение. Значение должно быть Flags.PARAM_BYTE(1) или Flags.PARAM_BYTES(2).
    >>> f = Flags(2, Flags.PARAM_BYTES)
    >>> f.number_of_bits
    16
    """

    PARAM_BITS, PARAM_BYTES = (1, 2)
    ANY, ALL = (1, 2)

    def __init__(self, number=1, param=PARAM_BITS, bit_mask=None):
        """
        Инициализирует флаги битов. Если "bit_mask" не определен, то флаги остаются нулевый

        >>> f = Flags(1, Flags.PARAM_BYTES, '11000011')
        >>> f.str_bits
        '11000011'
        >>>

        @param number: количество битов или байтов, в зависимости от значения параметра "param"
        @type number: int
        @param param: если PARAM_BITS, то будет создано указанное количество бит,
                    если PARAM_BYTES, то будет создано бит в соответствии с указанным количеством байт
        @type param: PARAM_BITS|PARAM_BYTES
        @param bit_mask: битовая маска указанная в виде строки битов,
                        последовательности порядковых чисел, или целовго неотрицательного числа
        @type bit_mask: str|list|tuple|set|int
        @param bit_mask:
        """
        if not (isinstance(number, int) and number > 0):
            raise TypeError("Неправильное значение. Количество {0} должно быть целым положительным числом.".
                            format("битов" if param == Flags.PARAM_BITS else "байтов"))
        if param not in (1, 2):
            raise TypeError("Неправильное значение. Значение должно быть Flags.PARAM_BYTE(1) или Flags.PARAM_BYTES(2).")
        # Если передали байты,
        if param == 2:
            # то подсчитаем, сколько это бит.
            bits = number * 8
        else:
            # Иначе запомним сколько передали именно в битах
            bits = number
        # Запомним сколько битов используется
        self.__number_of_bits = bits
        # Далее сформируем нулевой список рабочих бит
        self.__bits = 0
        """@param _list_bits: список рабочих битов
           @type _list_bits: list """
        # Если была сразу передана битовая маска,
        if bit_mask is not None:
            # то преобразуем переданную битовую маску для проверки,
            bit_mask = self.__convert_bit_mask(bit_mask)
            # и произведем установку бит по битовой маске.
            self.__bits |= bit_mask

    @property
    def value(self):
        """
        Возвращает состояние битовой маски в виде целого числа

        >>> f = Flags(4, Flags.PARAM_BITS)
        >>> f.value
        0
        >>> f.value = 15
        >>> f.value
        15
        >>> f.str_bits
        '1111'
        """
        return self.int_bits

    @value.setter
    def value(self, bit_mask):
        """ Устанавливает состояние битовой маски """
        # Для начала сбросим все биты в ноль.
        self.__bits = 0
        if bit_mask is not None:
            # Далее преобразуем переданную битовую маску для проверки,
            bit_mask = self.__convert_bit_mask(bit_mask)
            # и произведем установку бит по битовой маске.
            self.__bits |= bit_mask

    @property
    def number_of_bits(self):
        """
        Возвращает количество используемых бит

        :return:
        """
        return self.__number_of_bits

    def __get_all_bits(self):
        """
        Вовзвращает биты со всеми установленными флагами
        :return:
        """
        all_bits = 0
        for num in range(0, self.number_of_bits):
            all_bits |= 1 << num
        return all_bits

    @property
    def bin_bits(self):
        """
        Возвращает битовую последовательность в виде значения bin

        @return:
        """
        return bin(self.__bits)

    @property
    def int_bits(self):
        """
        Возвращает битовую последовательность в виде целого числа

        @return:
        """
        return self.__bits

    @property
    def str_bits(self):
        """
        Возвращает битовую последовательность в виде строки

        @return:
        """
        return self.__get_to_str()

    def __get_to_str(self):
        """
        Возвращает битовую последовательность в виде строки

        @return:
        """
        str_bits = ""
        for bit in range(0, self.__number_of_bits):
            str_bits += "1" if (self.__bits & (1 << bit)) else "0"
        return str_bits

    def get_bit(self, num):
        """
        Возвращает состояние указанного бита.

        >>> f = Flags(1, Flags.PARAM_BYTES)
        >>> f.set_bits((2,4,5,6), 1)
        >>> f.str_bits
        '01011100'
        >>> f.get_bit(2)
        1
        >>> f.get_bit(3)
        0
        >>>

        @param num: порядковый номер бита, который надо вернуть
        @type num: int
        @return:
        @raise TypeError: Проверяемый бит должен быть указан как неотрицательный порядковый
                            номер бита в битовой последовательности.
        """
        if not self.__validate_not_negative_int(num):
            raise TypeError("Проверяемый бит должен быть указан как неотрицательный порядковый "
                            "номер бита в битовой последовательности.")
        if num == 0:
            return 0
        return 1 if self.__bits & 1 << num - 1 != 0 else 0

    def get_bit_bool(self, num):
        """
        Возвращает состояние указанного бита в виде логического значения

        >>> f = Flags(1, Flags.PARAM_BYTES)
        >>> f.set_bits((2,4,5,6), 1)
        >>> f.str_bits
        '01011100'
        >>> f.get_bit_bool(2)
        True
        >>> f.get_bit_bool(3)
        False
        >>>

        @param num: порядковый номер бита, который надо вернуть
        @type num: int
        @return:
        @raise TypeError: Проверяемый бит должен быть указан как неотрицательный порядковый
                            номер бита в битовой последовательности.
        """
        return True if self.get_bit(num) == 1 else False

    def set_bit(self, num_bit, val):
        """
        Устанавливает указанный бит

        >>> f = Flags(1, Flags.PARAM_BYTES)
        >>> f.str_bits
        '00000000'
        >>> f.set_bit(3, 1)
        >>> f.str_bits
        '00100000'
        >>> f.set_bit(2, 2)
        Traceback (most recent call last):
            ...
        TypeError: Значение может быть только логическое, либо 1 или 0.

        @param num_bit: Порядковый номер бита в битовой последоваетельнсоти, который нужно
                        перевести в состояние указанное в аргументе val
        @type num_bit: int
        @param val:  логическое значение или 1 или 0, в которое надо перевести указанный бит
        @type val: bool|int
        @return:
        @raise TypeError: Изменяемый бит должен быть указан как порядковый номер бита
                          больше нуля в битовой последовательности.
        """
        if not self.__validate_not_negative_int(num_bit):
            raise TypeError("Изменяемый бит должен быть указан как неотрицательный порядковый "
                            "номер бита в битовой последовательности.")

        # Если передали 0, то ничего делать не надо.
        if num_bit == 0:
            return

        bit_mask = 1 << num_bit - 1
        self.set_bits(bit_mask, val)

    def set_bits(self, bit_mask, val):
        """
        Устанавливает биты в соответствии битовой маске,
        в состояние указанное аргументом val

        >>> f = Flags(1, Flags.PARAM_BYTES)
        >>> f.str_bits
        '00000000'
        >>> f.set_bits("1001001", True)
        >>> f.str_bits
        '10010010'
        >>> f = Flags(1, Flags.PARAM_BYTES)
        >>> f.str_bits
        '00000000'
        >>> f.set_bits("1001001", True)
        >>> f.str_bits
        '10010010'

        @param bit_mask: битовая маска указанная в виде строки битов,
                        последовательности порядковых чисел, или целовго неотрицательного числа
        @type bit_mask: str|list|tuple|set|int
        @param val: логическое значение или 1 или 0, в которое надо установить указанные в битовой маске биты
        @type val: bool|int
        @return:
        @raise TypeError: Битовая маска не может быть отрицательной. |
                          Недопустимый тип битовой маски.
        """
        # Для начала преобразуем переданную битовую маску для проверки.
        bit_mask = self.__convert_bit_mask(bit_mask)

        if self.__convert_val_to_bool(val):
            # Произведем установку бит по битовой маске.
            self.__bits |= bit_mask
        else:
            # Или же произведем сброс по битовой маске.
            self.__bits &= ~bit_mask

    def check_bit(self, num_bit, val):
        """
        Проверяет битовый массив значений на соответствие переданному порядковому номеру бита

        >>> f = Flags(1, Flags.PARAM_BYTES)
        >>> f.set_bits((2,4,5,6), 1)
        >>> f.str_bits
        '01011100'
        >>> f.check_bit(1, 1)
        False
        >>> f.check_bit(1, 0)
        True
        >>> f.check_bit(2, 1)
        True
        >>> f.check_bit(2, 0)
        False
        >>>

        @param num_bit: Порядковый номер бита в битовой последоваетельнсоти, который нужно
                       проверить на состояние указанное в аргументе val
        @type num_bit: int
        @param val:  логическое значение или 1 или 0, на которое надо проверить указанный бит
        @type val: bool|int
        @return:
        @raise TypeError: Проверямый бит должен быть указан как порядковый номер бита
                          больше нуля в битовой последовательности.
        """
        if not self.__validate_not_negative_int(num_bit):
            raise TypeError("Изменяемый бит должен быть указан как неотрицательный порядковый "
                            "номер бита в битовой последовательности.")

        # Если передали 0, то ничего делать не надо.
        if num_bit == 0:
            return

        bit_mask = (num_bit,)
        return self.check_bits(bit_mask, val)

    def check_bits(self, bit_mask, val, condition=ALL):
        """
        Проверяет битовый массив значений на соответствие битовой строке
        или массиву порядковых номеров битов

        >>> f = Flags(1, Flags.PARAM_BYTES)
        >>> f.set_bits((2,4,5,6), 1)
        >>> f.str_bits
        '01011100'
        >>> f.check_bits('01011100', 1, Flags.ALL)
        True
        >>> f.check_bits('00011100', 1, Flags.ALL)
        True
        >>> f.check_bits('11011100', 1, Flags.ALL)
        False
        >>> f.check_bits('00000100', 1, Flags.ANY)
        True
        >>>

        @param bit_mask: битовая маска указанная в виде строки битов,
                        последовательности порядковых чисел, или целого неотрицательного числа
        @type bit_mask: str|list|tuple|set|int
        @param val: логическое значение или 1 или 0, на которое надо проверить указанные в битовой маске биты
        @type val: bool|int
        @param condition:
        @return:
        @raise TypeError: Условие может быть только Flags.ANY (1) или Flags.ALL (2).
        """
        if condition not in (1, 2):
            raise TypeError("Условие может быть только Flags.ANY (1) или Flags.ALL (2).")

        # Для начала преобразуем переданную битовую маску для проверки.
        bit_mask = self.__convert_bit_mask(bit_mask)

        # Если надо проверить биты на установку,
        if self.__convert_val_to_bool(val):
            # то их можно проверить на любой из установленых битов,
            if condition == self.ANY:
                return self.__bits & bit_mask != 0
            else:
                # или на то, чтобы бы все проверяемые биты были установлены.
                return self.__bits & bit_mask == bit_mask
        # Иначе проверить биты на сброс. Для этого нам надо бует инверсировать битовый массив значений
        else:
            # Их так же можно проверить на любой из сброшенных битов,
            if condition == self.ANY:
                return ~self.__bits & bit_mask != 0
            else:
                # или на то, чтобы бы все проверяемые биты были сброшены.
                return ~self.__bits & bit_mask == bit_mask

    def inverse_bit(self, num_bit):
        """
        Переключает указанный бит в противоположенное значение

        >>> f = Flags(1, Flags.PARAM_BYTES)
        >>> f.set_bits((2,4,5,6), 1)
        >>> f.str_bits
        '01011100'
        >>> f.inverse_bit(6)
        >>> f.str_bits
        '01011000'
        >>>

        @param num_bit: Порядковый номер бита в битовой последоваетельнсоти, который нужно
                       переключить в противоположенное состояние
        @type num_bit: int
        @return:
        """
        if not self.__validate_not_negative_int(num_bit):
            raise TypeError("Переключаемый бит должен быть указан как неотрицательный порядковый "
                            "номер бита в битовой последовательности.")

        # Если передали 0, то ничего делать не надо.
        if num_bit == 0:
            return

        bit_mask = (num_bit,)
        self.inverse_bits(bit_mask)

    def inverse_bits(self, bit_mask):
        """
        Переключает биты указанные в битовой маске в противоположенное значение

        >>> f = Flags(1, Flags.PARAM_BYTES)
        >>> f.set_bits((2,4,5,6), 1)
        >>> f.str_bits
        '01011100'
        >>> f.inverse_bits('11110000')
        >>> f.str_bits
        '10101100'
        >>>

        @param bit_mask: битовая маска указанная в виде строки битов,
                        последовательности порядковых чисел, или целого неотрицательного числа
        @type bit_mask: str|list|tuple|set|int
        @return:
        """
        # Для начала преобразуем переданную битовую маску для инверсии.
        bit_mask = self.__convert_bit_mask(bit_mask)
        self.__bits ^= bit_mask

    def __convert_bit_mask(self, bit_mask):
        """
        Конвертирует битовую маску в зависимости от того, в каком виде она была передана
        @param bit_mask: битовая маска
        @type bit_mask: str|list|tuple|set|int
        @return:
        @raise TypeError: Битовая маска не может быть отрицательной. |
                            Недопустимый тип битовой маски.
        """
        # Для начала преобразуем переданную битовую маску для проверки.
        if isinstance(bit_mask, str):
            bit_mask = self.util_convert_str_to_bit_mask(bit_mask)
        elif isinstance(bit_mask, (list, tuple, set)):
            bit_mask = self.util_convert_list_num_to_bit_mask(bit_mask)
        elif isinstance(bit_mask, int):
            if bit_mask < 0:
                raise TypeError("Битовая маска не может быть отрицательной.")
        else:
            raise TypeError("Недопустимый тип битовой маски.")
        return bit_mask

    @staticmethod
    def util_convert_str_to_bit_mask(str_):
        """
        Статический метод преобразует битовую строку в битовую маску

        >>> num = Flags.util_convert_str_to_bit_mask("10110011")
        >>> num
        205
        >>> Flags.util_int_to_bitstring(num)
        '10110011'
        >>>
        @param str_: битовая строка типа: "10110011"
        @type str_: string
        @return:
        @raise TypeError: Биты могут иметь значения только 1 или 0
        """
        list_num = []
        i = 1
        for char in str_:
            if char == '1':
                list_num.append(i)
            elif char != '0':
                raise TypeError("Биты могут иметь значения только 1 или 0.")
            i += 1
        return Flags.util_convert_list_num_to_bit_mask(list_num)

    @staticmethod
    def util_convert_list_num_to_bit_mask(list_num):
        """
        Статический метод преобразует список порядковых чисел в битовую маску.

        >>> lst = (1, 4, 6, 7, 8)
        >>> num = Flags.util_convert_list_num_to_bit_mask(lst)
        >>> Flags.util_int_to_bitstring(num)
        '10010111'
        >>>

        @param list_num: список порядковых чисел
        @type list_num: tuple|list
        @return:
        """
        num_bit = 0

        # Пробежимся по всему списку
        for num in list_num:
            # и установим каждый бит по указанному порядковому номеру
            num_bit |= 1 << num - 1
        return num_bit

    @classmethod
    def util_int_to_bitstring(cls, val):
        """
        Статический метод отображает числа в виде строки битов.

        >>> Flags.util_int_to_bitstring(7)
        '111'
        >>> Flags.util_int_to_bitstring(8)
        '0001'

        @param val: целое неотрицательное число, которое надо преобразовать в строку битов.
        @type val: int
        @return: строка битов.
        @raise TypeError: Значение должно быть целым неотрицательным числом.
        """
        # Для начала проверим, что было передано неотрицательное целое число.
        if not cls.__validate_not_negative_int(val):
            raise TypeError("Значение должно быть целым неотрицательным числом.")
        # Если передали ноль,
        if val == 0:
            # то и вернем ноль.
            return "0"
        num = 0
        str_bits = ""
        # Иначе будем проходить до тех пор, пока не найдем сколько бит потребуется
        # для формирования переданного числа.
        while True:
            if val < (1 << num):
                break
            num += 1
        # Теперь пройдемся по каждому биту,
        for bit in range(0, num):
            # и если этот бит в числе установлен, то укажим его как 1, иначе 0
            str_bits += "1" if (val & (1 << bit)) else "0"
        return str_bits

    @staticmethod
    def __convert_val_to_bool(val):
        """
        Преобразует 1 и 0 в логический тип, или возвращает значение,
        если переданное значение уже логическое.

        @param val:
        @type val: bool|int
        @return:
        @raise TypeError: Значение может быть только логическое, либо 1 или 0.
        """
        if isinstance(val, bool):
            return val
        elif val in (0, 1):
            return True if val == 1 else False
        else:
            raise TypeError("Значение может быть только логическое, либо 1 или 0.")

    @staticmethod
    def __validate_not_negative_int(num):
        """
        Проверяет заначение на целое неотрицательное число
        @param num:
        @return:
        """
        return False if (not isinstance(num, int) or num < 0) else True

    def __str__(self):
        return self.__get_to_str()

    def __int__(self):
        return self.__bits

    def __repr__(self):
        return "Flags({0}, Flags.PARAM_BITS, '{1}')".format(self.number_of_bits, self.str_bits)

    def __eq__(self, other):
        """
        Равно

        @param other:
        @type other: Flags
        @return:
        """
        return self.__bits == other.__bits

    def __lt__(self, other):
        """
        Меньшше

        @param other:
        @type other: Flags
        @return:
        """
        return self.__bits < other.__bits

    def __le__(self, other):
        """
        Меньше либо равно

        @param other:
        @type other: Flags
        @return:
        """
        return self.__bits <= other.__bits

    def __and__(self, other):
        """
        Битовый и логический оператор И (&)

        @param other:
        @type other: Flags
        @return:
        """
        return Flags(self.number_of_bits, self.PARAM_BITS, self.__bits & other.__bits)

    def __iand__(self, other):
        """
        Битовый и логический оператор присваивания И (&=)

        @param other:
        @type other: Flags
        @return:
        """
        self.__bits &= other.__bits
        return self

    def __or__(self, other):
        """
        Битовый и логический оператор ИЛИ (|)

        @param other:
        @type other: Flags
        @return:
        """
        return Flags(self.number_of_bits, self.PARAM_BITS, self.__bits | other.__bits)

    def __ior__(self, other):
        """
        Битовый и логический оператор присваивания И(|=)

        @param other:
        @type other: Flags
        @return:
        """
        self.__bits |= other.__bits
        return self

    def __xor__(self, other):
        """
        Битовый и логический оператор исключающее ИЛИ (^)

        @param other:
        @type other: Flags
        @return:
        """
        return Flags(self.number_of_bits, self.PARAM_BITS, self.__bits ^ other.__bits)

    def __ixor__(self, other):
        """
        Битовый и логический оператор исключающее ИЛИ (^=)

        @param other:
        @type other: Flags
        @return:
        """
        self.__bits ^= other.__bits
        return self

    def __invert__(self):
        """
        Битовый и логический оператор НЕТ (~)

        @return:
        """
        return Flags(self.number_of_bits, self.PARAM_BITS, self.__bits ^ self.__get_all_bits())

    def __add__(self, other):
        """
        Арфмитическая операция +

        @param other:
        @type other: Flags
        @return:
        """
        return Flags(self.number_of_bits, self.PARAM_BITS, self.__bits | other.__bits)

    def __iadd__(self, other):
        """
        Арфмитическая операция +=

        @param other:
        @type other: Flags
        @return:
        """
        self.__bits |= other.__bits
        return self

    def __sub__(self, other):
        """
        Арфмитическая операция -

        @param other:
        @type other: Flags
        @return:
        """
        return Flags(self.number_of_bits, self.PARAM_BITS, self.__bits ^ other.__bits)

    def __isub__(self, other):
        """
        Арфмитическая операция -=

        @param other:
        @type other: Flags
        @return:
        """
        self.__bits ^= other.__bits
        return self

    def __neg__(self):
        """
       Арифимитическая операция отрицания (-x)

        @return:
        """
        return Flags(self.number_of_bits, self.PARAM_BITS, self.__bits ^ self.__get_all_bits())

    def __hash__(self):
        return hash(self.__bits)

    def __len__(self):
        return self.__number_of_bits

    def __bytes__(self):
        return bytes(self.__bits)


def pack_string(string):
    """
    Запаковывает строку в байтовый массив

    :param string: строка данных
    :return:
    """
    data = string.encode('utf8')
    data_length = len(data)
    format_str = f"<H{data_length}s"
    return struct.pack(format_str, data_length, data)


def unpack_string(fh, eof_is_error=True):
    """
    Вытаскивает строку из файла и распаковывает ее.

    :param fh: дескриптор файла
    :param eof_is_error: если true то в случае не нахождения очередной строки будет ошибка.
    :return:
    """
    uint16 = struct.Struct("<H")
    data_length = fh.read(uint16.size)
    if not data_length:
        if eof_is_error:
            raise ValueError("Отсутствует или поврежден размер строки.")
        return None
    length = uint16.unpack(data_length)[0]
    if length == 0:
        return ""
    data = fh.read(length)
    if not data or len(data) != length:
        raise ValueError("Строка отсутствует или повреждена")
    format_str = f"<{length}s"
    return struct.unpack(format_str, data)[0].decode("utf8")


def normalize_email(email):
    """
    Normalize the email address by lowercasing the domain part of it.
    """
    email = email or ''
    try:
        email_name, domain_part = email.strip().rsplit('@', 1)
    except ValueError:
        pass
    else:
        email = '@'.join([email_name, domain_part.lower()])
    return email