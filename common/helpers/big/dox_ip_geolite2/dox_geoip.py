from abc import abstractmethod
from .. import dox_ip_geolite2
from django.utils.functional import cached_property
from ipaddress import ip_address, ip_network, IPv4Address, IPv6Address, IPv4Network, IPv6Network


import os
import struct
import collections

from ...small.dox_lib import unpack_string


class DoxGeoIp:
    def __init__(self, base_folder, used_localize=None):
        """
        Конструктор

        :param str base_folder: каталог в котором располагаются базы данных
        :param str used_localize: локализация в которой требуется найти данные
        """
        self._base_folder = base_folder
        self._localize = []
        self._reade_config()
        # self._used_localize = None
        if used_localize is not None:
            if used_localize not in self._localize:
                raise DoxGeoIPError(f"Localization {used_localize} not found.")
            else:
                self._used_localize = used_localize
        # if used_localize not in self._localize:
        #     raise DoxGeoIPError(f"Локализаци {used_localize} не найдена.")

    @property
    def localize(self):
        """ Возвращает список локализаций """
        return self._localize

    @property
    def used_localize(self):
        """  Возвращает используемую локализацию"""
        return self._used_localize

    @used_localize.setter
    def used_localize(self, value):
        """ Устанавливает испольуемую локализацию """
        if value is None:
            raise DoxGeoIPError("Class " + self.__class__.__name__ + "requires you to specify the localization.")
        if value not in self._localize:
            raise DoxGeoIPError(f"Localization {value} not found.")
        self._used_localize = value

    def _reade_config(self):
        """ Считывает конфигурационный файл """
        uint16 = struct.Struct("<H")
        filename = os.path.join(self._base_folder, 'config.dat')
        conf_file = open(filename, "rb")
        loc_size_data = conf_file.read(uint16.size)
        loc_size = uint16.unpack(loc_size_data)[0]
        for i in range(0, loc_size):
            self._localize.append(unpack_string(conf_file))
        conf_file.close()

    def has_localize(self, loc):
        """ Есть ли такая локализация """
        return loc in self._localize

    def get_city_location(self, network):
        """
        Возвращает геолокацию по сетевому адресу

        :param network: Сетевой адрес
        :rtype: collections.namedtuple
        """
        file_config = self._get_network_config_city(network)
        with LocationCityFile(self._base_folder,
                              dox_ip_geolite2.FILE_CONFIG_LOCATION_CITY, self._used_localize, self._used_localize) \
                as location_city_file, \
                NetworkFile(self._base_folder, file_config) as network_file:
            geoname_id = network_file[network]
            return location_city_file[geoname_id]

    def get_timezone(self, network):
        """ Возвращает временную зону по сетевому адресу """
        location_city = self.get_city_location(network)
        if location_city.timezone != '':
            return location_city.timezone
        else:
            raise DoxGeoIPError(f"At the address {network} time zone is not detected.")

    def get_organization(self, network):
        """ Возвращет организацию по сетевому адресу """
        file_config = self._get_network_config_organization(network)
        with NetworkFile(self._base_folder, file_config) as network_file:
            org = network_file[network]
            if org != '':
                return org
            else:
                raise DoxGeoIPError(f"At the address {network} organizations not detected.")

    def _get_network_config_city(self, network):
        """ Возвращает конфигурационный файл локации городов """
        ver_ip = self._get_ver_ip(network)
        if ver_ip == 4:
            file_config = dox_ip_geolite2.NETWORK_FILE_CONFIG_CITY_IP4
        else:
            file_config = dox_ip_geolite2.NETWORK_FILE_CONFIG_CITY_IP6
        return file_config

    def _get_network_config_organization(self, network):
        """ Возвращает конфигурационный файл организаций """
        ver_ip = self._get_ver_ip(network)
        if ver_ip == 4:
            file_config = dox_ip_geolite2.NETWORK_FILE_CONFIG_ORG_IP4
        else:
            file_config = dox_ip_geolite2.NETWORK_FILE_CONFIG_ORG_IP6
        return file_config

    @staticmethod
    def _get_ver_ip(network):
        """ Возвращает версию переданного IP адреса """
        try:
            # Попробуем создать объект IP адреса.
            obj = ip_address(network)
            # Далее проверяем какой объект IP адреса у нас создан.
            if isinstance(obj, IPv4Address):
                return 4
            elif isinstance(obj, IPv6Address):
                return 6
            else:
                raise DoxGeoIPError("Unknown error the format of IP addresses.")
        except ValueError:
            # Если возникла ошибка, значит и не IP адрес был передан.
            raise DoxGeoIPError("Incorrect format of IP addresses.")


class BinaryFile:
    _ITER_ITEMS, _ITER_CODES, _ITER_VALUES = (1, 2, 3)
    _code_type = 'int'  # Тип кода числовой или строковый.

    def __init__(self, base_folder, file_config):
        self._base_folder = base_folder         # Каталог расположения файлов данных.
        self._file_config = file_config         # Конфигурация переданного файла данных.
        self._filename_dat = file_config.filename   # Имя бинарного файла.
        self._filename_idx = file_config.filename   # Имя индексного файла.
        self._fh = None                         # Дескриптор файла данных.
        self._fhi = None                        # Дескриптор индексного файла.
        self._iter_index = None                   # Текущий номер индекса итератора.
        self._start_iter_index = None           # Начальный индекс итератора.
        self._end_iter_index = None             # Конечноый индекс итератора.
        self._count_rows = None                 # Количество строк данных файла.
        self._count_rows_indexes = None         # Количество строк индексов
        self._iter_type = self._ITER_ITEMS      # Тип итератора (коды, значения, коды и значения).
        self._format_dat = self._get_format_dat()
        self._format_idx = self._get_format_idx()

    def __enter__(self):
        filename = os.path.join(self._base_folder, f'{self._filename_dat}.dat')
        self._fh = open(filename, "rb")

        filename_idx = os.path.join(self._base_folder, f'{self._filename_idx}.idx')
        self._fhi = open(filename_idx, "rb")
        self._count_rows_indexes = self._get_count_rows_indexes()

        self._count_rows = self._get_count_rows()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._fh.close()
        if self._fhi is not None:
            self._fhi.close()

    def __len__(self):
        return self._count_rows

    def __iter__(self):
        # Если начальный итератор отсутствует, то он будет равен -1.
        self._iter_index = -1 if self._start_iter_index is None else self._start_iter_index
        # Если конечный итератор отсутсвует,
        if self._end_iter_index is None:
            # то он будет равен количеству строк.
            self._end_iter_index = self._count_rows
        return self

    def __next__(self):
        self._iter_index += 1
        if self._iter_index < self._end_iter_index:
            if self._iter_type == self._ITER_ITEMS:
                result = self.get_item_by_index(self._iter_index)
            elif self._iter_type == self._ITER_CODES:
                result = self.get_code_by_index(self._iter_index)
            elif self._iter_type == self._ITER_VALUES:
                result = self.get_value_by_index(self._iter_index)
            else:
                raise ValueError("Error type of the iterator")
            return result
        else:
            raise StopIteration

    def __getitem__(self, code):
        return self.find_value(code)

    @staticmethod
    def open(base_folder, file_config):
        """
        Открывает справочный файл для работы

        :param base_folder: путь к файлам базы данных
        :param file_config: конфигурация файла
        :return:
        """
        raise NotImplementedError("Required implementation of the method 'open'")

    @abstractmethod
    def _get_format_dat(self):
        """  Возвращает формат структуры строки данных """

    @abstractmethod
    def _get_format_idx(self):
        """ Возвращает формат структуры индексного файла """

    @abstractmethod
    def _get_devalue(self, row):
        """
        Возвращает декодированное значение

        :param row:
        :rtype: (int, str)
        """

    @abstractmethod
    def _get_decode(self, row):
        """
        Возвращает декодированный код

        :param row:
        :rtype: (int, str)
        """

    @abstractmethod
    def find_value(self, code):
        """ Ищет значение по коду """

    @abstractmethod
    def find_code(self, value):
        """ Ищет код по значению """

    @cached_property
    def _row_size_dat(self):
        """ Возвращает размер структуры данных """
        return struct.calcsize(self._format_dat)

    @cached_property
    def _row_size_idx(self):
        """ Возвращает размер структуры данных индексного файла """
        return struct.calcsize(self._format_idx)

    @property
    def start_iter_index(self):
        """ Возвращает начальный индекс итерирования """
        return self._start_iter_index

    @start_iter_index.setter
    def start_iter_index(self, value):
        """ Устанавливает начальный индекс итерирования """
        if value < -1:
            raise ValueError("The start index cannot be less than -1.")
        elif self._end_iter_index is not None and value > self._end_iter_index:
            raise ValueError("The start index cannot be greater than the final index.")
        self._start_iter_index = value

    @property
    def end_iter_index(self):
        """ Возвращает конечный индекс итерирования """
        return self._end_iter_index

    @end_iter_index.setter
    def end_iter_index(self, value):
        """ Устанавливает коненчый индекс итерирования """
        if value > self._count_rows:
            raise ValueError("The leaf index cannot be more than the number of rows of data.")
        elif self._start_iter_index is not None and value < self._start_iter_index:
            raise ValueError("The leaf index cannot be smaller than the starting index.")

    def close(self):
        """ Закрывает файл для работы """
        self._fh.close()
        if self._fhi is not None:
            self._fhi.close()

    def _get_data_by_index(self, index):
        """ Получает строку данных по индексу """
        # Проверим, чтобы указанный индекс не выходил за границы файла.
        self._is_out_index(index)
        # Далее спозиционируем курсор в файле в соответствии с указанным индексом,
        self._fh.seek(self._row_size_dat * index)
        # и прочитаем из него строку данных.
        data = self._fh.read(self._row_size_dat)
        # Далее распакуем двоичные данные, и вернем их.
        return struct.unpack(self._format_dat, data)

    def get_item_by_index(self, index):
        """ Возвращает код и значение по индексу """
        # Получим строку с данными,
        row = self._get_data_by_index(index)
        # выделим из нее код,
        code = self._get_decode(row)
        # и значение,
        val = self._get_devalue(row)
        # и вернем их.
        return code, val

    def get_code_by_index(self, index):
        """
        Получить код по индексу

        :param index:
        :return:
        """
        # Получим строку с данными,
        row = self._get_data_by_index(index)
        # и вернем из нее код.
        return self._get_decode(row)

    def get_value_by_index(self, index):
        """ Получить значение по индексу """
        # Получим строку с данными.
        row = self._get_data_by_index(index)
        # и вернем из нее значение.
        return self._get_devalue(row)

    def _get_count_rows(self):
        """ Возвращает количество строк данных """
        # перейдем в конец файла,
        self._fh.seek(0, os.SEEK_END)
        # и получем его размер.
        file_size = self._fh.tell()
        # Далее разделив размер файла на размер одной записи вернем количество данных
        return file_size // self._row_size_dat

    def _get_count_rows_indexes(self):
        """ Возвращает количество строк индексов """
        if self._fhi is None:
            return None
        self._fhi.seek(0, os.SEEK_END)
        file_size = self._fhi.tell()
        return file_size // self._row_size_idx

    def items(self, start=None, end=None):
        """
        Возвращает итератор по кодам и значениям

        :param start: начальный индекс итеартора
        :param end: конечный индекс итератора
        :return:
        """
        self._start_iter_index = start
        self._end_iter_index = end
        self._iter_type = self._ITER_ITEMS
        return iter(self)

    def codes(self, start=None, end=None):
        """
        Возвращает итератор по кодам

        :param start: начальный индекс итеартора
        :param end: конечный индекс итератора
        :return:
        """
        self._start_iter_index = start
        self._end_iter_index = end
        self._iter_type = self._ITER_CODES
        return iter(self)

    def values(self, start=None, end=None):
        """
        Возвращает итератор по значениям

        :param start: начальный индекс итеартора
        :param end: конечный индекс итератора
        :return:
        """
        self._start_iter_index = start
        self._end_iter_index = end
        self._iter_type = self._ITER_VALUES
        return iter(self)

    def get_dict_idx(self):
        """ Возвращает словарь индексного файла """
        dict_idx = {}
        self._fhi.seek(0)
        for i in range(0, self._count_rows_indexes):
            data = self._fhi.read(self._row_size_idx)
            row = struct.unpack(self._format_idx, data)
            code = row[0] if self._code_type == 'int' else row[0].decode("utf8").rstrip()
            dict_idx[code] = row[1]
        return dict_idx

    def _is_out_index(self, index):
        """
        Проверяет не выходит ли индекс за границы файла

        :param int index: номер индекса строки
        :return:
        """
        # Если индекс меньше нуля,
        filename = self._filename_dat
        error = f'Index "{index}" is out of bounds of the file "{filename}"'
        if index < 0:
            # то сразу вернем ошибку выход за границы файла.
            raise IndexError(error)
        # Иначе идем в конец файла,
        self._fh.seek(0, os.SEEK_END)
        # и считываем его позицию.
        end = self._fh.tell()
        # Далее вычисляем смещение в файле по индексу,
        offset = index * self._row_size_dat
        # и если смещение превышает максимальную позицию файла.
        if offset >= end:
            # то вернем ошибку выхода за границу файла
            raise IndexError(error)


class LocationCityFile(BinaryFile):
    def __init__(self, base_folder, file_config, localize, used_localize):
        if localize is None or len(localize) == 0:
            raise DoxGeoIPError("No localization specified.")
        if used_localize not in localize:
            raise DoxGeoIPError(f"Localization {used_localize} not found.")
        self._localize = localize  # Список локализаций.

        super().__init__(base_folder, file_config)
        self._filename_dat = f"{file_config.filename}-{used_localize}"   # Имя бинарного файла.
        self._filename_idx = f"{file_config.filename}-{used_localize}"   # Имя индексного файла.

    @staticmethod
    def open(base_folder, file_config, localize=None, used_localize=None):
        """
        Открывает справочный файл для работы

        :param base_folder: путь к файлам базы данных
        :param file_config: конфигурация файла
        :param dict localize: список локализаций
        :param used_localize: используемая локализация
        :return:
        """
        cls = LocationCityFile(base_folder, file_config, localize, used_localize)
        filename = os.path.join(base_folder, f'{file_config.filename}.dat')
        cls._fh = open(filename, "rb")

        filename_idx = os.path.join(base_folder, f'{file_config.filename}.idx')
        cls._fhi = open(filename_idx, "rb")
        cls._count_rows_indexes = cls._get_count_rows_indexes()

        cls._count_rows = cls._get_count_rows
        return cls

    def _get_format_dat(self):
        return dox_ip_geolite2.FILE_CONFIG_LOCATION_CITY.format

    def _get_format_idx(self):
        return dox_ip_geolite2.FILE_CONFIG_LOCATION_CITY.format_idx

    def _get_devalue(self, row):
        """ Возвращает декодированное значение """
        CityLocation = collections.namedtuple('CityLocation',
                                              "continent country subdivision1 subdivision2 city timezone")
        continent = row[1].decode('utf8').rstrip()
        country = row[2].decode('utf8').rstrip()
        subdivision_1 = row[3].decode('utf8').rstrip()
        subdivision_2 = row[4].decode('utf8').rstrip()
        city = row[5].decode('utf8').rstrip()
        timezone = row[6].decode('utf8').rstrip()

        return CityLocation(continent, country, subdivision_1, subdivision_2, city, timezone)

    def _get_decode(self, row):
        """ Возвращает декодированный код """
        return row[0]

    def find_value(self, code):
        """ Ищет значение по коду """
        start, end = self._get_start_end_find_position(code)
        # Спозиционируем курсор в начало файла.
        self._fh.seek(start * self._row_size_dat)
        # Пройдемся по определенному диапазону.
        for i in range(start, end):
            # Считаем порцию данных,
            data = self._fh.read(self._row_size_dat)
            # и распакуем их,
            item = struct.unpack(self._format_dat, data)
            # и возьмем из них код.
            _code = self._get_decode(item)
            # Далее проверим, если указанный код равен коду взятому из данных файла,
            if _code == code:
                # то вернем найденные данные.
                return self._get_devalue(item)
        # Если ничего найдено не было, то вернем ошибку.
        raise IndexError(f'Geolocation code "{code}" not found')

    def find_code(self, value):
        raise NotImplementedError("This method is not implemented")

    def _get_start_end_find_position(self, code):
        """ Возвращает начальную и конечную позицию поиска """
        # Для начала назначим начальные значения для начальной и конечной позиции.
        temp_int_code = 0
        end = self._count_rows
        self._fhi.seek(0)
        # Далее пройдемся по каждому индексу,
        for i in range(0, self._count_rows_indexes):
            # считаем его
            data = self._fhi.read(self._row_size_idx)
            # и распакуем.
            item = struct.unpack(self._format_idx, data)
            # Далее выделим из строки код,
            _code = item[0]
            # и будем искать до тех пор, пока найденный код меньше искомого,
            if _code <= code:
                # и будем сохранять его позицию во временной переменной.
                temp_int_code = item[1]
            else:
                # Но, как только найдется код код который больше искомого,
                # то мы укажим  текущий найденый код как конечной поиск,
                end = item[1]
                # и закончим поиск кодов.
                break
        start = temp_int_code
        return start, end


class NetworkFile(BinaryFile):
    _IP_ADDRESS, _IP_NETWORK = (1, 2)

    def __init__(self, base_folder, file_config):
        self._code_type = file_config.code_type
        super().__init__(base_folder, file_config)
        self._ip_ver = file_config.ip_ver

    @staticmethod
    def open(base_folder, file_config):
        """
        Открывает справочный файл для работы

        :param base_folder: путь к файлам базы данных
        :param file_config: конфигурация файла
        :return:
        """
        cls = NetworkFile(base_folder, file_config)
        filename = os.path.join(base_folder, f'{file_config.filename}.dat')
        cls._fh = open(filename, "rb")
        if cls._file_config.has_indexes:
            filename_idx = os.path.join(base_folder, f'{file_config.filename}.idx')
            cls._fhi = open(filename_idx, "rb")
            cls._count_rows_indexes = cls._get_count_rows_indexes()
        cls._count_rows = cls._get_count_rows
        return cls

    def _get_format_dat(self):
        """ Возвращает формат структуры строки данных """
        return dox_ip_geolite2.get_struct_network_format_dat(self._file_config)

    def _get_format_idx(self):
        """ Возвращает формат структуры индексного файла """
        return dox_ip_geolite2.get_struct_network_format_idx(self._file_config)

    def _get_devalue(self, row):
        """ Возвращает декодированное значение """
        if self._file_config.filename.startswith('city'):
            return row[1]
        elif self._file_config.filename.startswith('org'):
            return row[1].decode('utf8')
#        return row[1]

    def _get_decode(self, row):
        """ Возвращает декодированный код """
        return row[0].decode("utf8").rstrip()

    def find_value(self, code):
        """ Ищет значение по коду """
        # Для начала узнаем в каком виде передали код, в виде адреса, или подсети.
        type_code = self._check_code(code)
        if type_code == self._IP_ADDRESS:
            start, end = self._get_start_end_find_position(code)
        else:
            start, end = 0, self._count_rows
        # определим нужные классы для сравнения ip адресов.
        _ip_address = self._get_ip_address_class()
        _ip_network = self._get_ip_network_class()
        # Спозиционируем курсор в начало поиска кода в файле.
        self._fh.seek(start * self._row_size_dat)
        # Пройдемся по определенному диапазону.
        for i in range(start, end):
            # Считаем порцию данных,
            data = self._fh.read(self._row_size_dat)
            # и распакуем их.
            item = struct.unpack(self._format_dat, data)
            # Получим из этих данных код.
            _code = self._get_decode(item)
            # Если код передали в виде адреса,
            if type_code == self._IP_ADDRESS:
                # то проверим, входит ли этот адрес в найденную подсеть.
                if _ip_address(code) in _ip_network(_code):
                    # Если входит, то вернем из данных соответствующее значение.
                    return self._get_devalue(item)
            else:
                # Иначе код передали в виде подсети. В этом случае сравним очередной полученный код, с указанным.
                if code == _code:
                    # Если код найден, то вернем из данных соответствующее значение.
                    return self._get_devalue(item)
        # Если ничего найдено не было, то вернем ошибку.
        str_type_code = "Address" if type_code == self._IP_ADDRESS else "Subnet"
        error = f'{str_type_code} "{code}" not found'
        raise IndexError(error)

    def find_code(self, value, localize=None):
        """ Ищет код по значению """
        values = []
        # Спозиционируем курсор в начало файла.
        self._fh.seek(0)
        # Пройдемся по всем данным.
        for i in range(0, self._count_rows):
            # Считаем порцию данных,
            data = self._fh.read(self._row_size_dat)
            # и распакуем их.
            item = struct.unpack(self._format_dat, data)
            # Далее проверим, если искомое значение равно значению из данных,
            if value == self._get_devalue(item):
                # то добавим это значение в список кодов.
                values.append(self._get_decode(item))
        return values

    def _check_code(self, code):
        """ Проверяет указанный код на правильный формат IP адреса или IP подсети """
        try:
            # Попробуем получить объект ip-адреса.
            obj = ip_address(code)
            # Если получили объект сети IP4,
            if isinstance(obj, IPv4Address):
                # а у нас по конфигурации версия ip 6,
                if self._ip_ver == 6:
                    # значит создадим исключение, что передали не ту версию IP
                    raise DoxGeoIPError("Passed the wrong version of the IP address.")
                # Иначе отметим, что передали именно адрес.
                type_code = self._IP_ADDRESS
            elif isinstance(obj, IPv6Address):
                if self._ip_ver == 4:
                    raise DoxGeoIPError("Passed the wrong version of the IP address.")
                type_code = self._IP_ADDRESS
            else:
                raise DoxGeoIPError("Incorrect IP format passed.")
        except ValueError:
            # Если при создании обхекта ip-адреса возникла ошибка,
            try:
                # то попробуем создать объект ip-сети.
                obj = ip_network(code)
                # Далее, если мы получиили обхект сети версии 4,
                if isinstance(obj, IPv4Network):
                    # а у нас по конфигурации должна быть версия 6,
                    if self._ip_ver == 6:
                        # то вернем исклюяение с соответствующей ошибкой.
                        raise DoxGeoIPError("Passed the wrong version of the IP subnet.")
                    type_code = self._IP_NETWORK
                elif isinstance(obj, IPv6Network):
                    if self._ip_ver == 4:
                        raise DoxGeoIPError("Passed the wrong version of the IP subnet.")
                    type_code = self._IP_NETWORK
                else:
                    raise DoxGeoIPError("Incorrect IP format passed.")
            except ValueError:
                # Если был передан и не адрес и не сеть, значит вернем ошибку.
                raise DoxGeoIPError("Incorrect IP format passed.")

        return type_code

    def _get_start_end_find_position(self, code):
        """ Находит и возвращает начальную и конечную позицию диапазона поиска значения """
        # Для начала назначим начальные значения для начальной и конечной позиции,
        temp_network = 0
        end = self._count_rows
        # и определим нужный класс для сравнения ip адресов.
        _ip_address = self._get_ip_address_class()
        self._fhi.seek(0)
        # Далее пройдемся по каждому индексу,
        for i in range(0, self._count_rows_indexes):
            # считаем его
            data = self._fhi.read(self._row_size_idx)
            # и распакуем.
            item = struct.unpack(self._format_idx, data)
            # Далее выделим из строки сетевой адрес.
            _code = item[0].decode('utf8').rstrip()
            # Будем искать до тех пор, пока найденный адрес меньше искомого,
            if _ip_address(_code) <= _ip_address(code):
                # при будем сохранять его позицию во временной переменной.
                temp_network = item[1]
            else:
                # Но, как только найдется код код который больше искомого,
                # то мы укажим текущую позицию как конечный поиск,
                end = item[1]
                # и закончим поиск позиций кодов.
                break
        start = temp_network
        return start, end

    def _get_ip_address_class(self):
        """ Возвращает нужный класс для работы с IP адресом """
        if self._ip_ver == 4:
            return IPv4Address
        else:
            return IPv6Address

    def _get_ip_network_class(self):
        """ Возвращает нужный класс для работы с IP подсетями """
        if self._ip_ver == 4:
            return IPv4Network
        else:
            return IPv6Network


class DoxGeoIPError(Exception):
    pass
