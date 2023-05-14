from .. import dox_ip_geolite2
from .. dox_ip_geolite2 import get_struct_network_format_dat, get_struct_network_format_idx
from common.helpers.three.dox_lib import pack_string

import re
import os
import csv
import sys
import struct


class CreatorGeoipFiles:
    _CITIES_IP, _ORGANIZATIONS_IP = (1, 2)

    def __init__(self, import_folder, base_folder):
        self._import_folder = import_folder
        self._base_folder = base_folder
        self._localize, self._file_localize = [], {}
        self._current_percent = -1

    @property
    def import_folder(self):
        return self._import_folder

    def run(self):
        """ Запускает процесс создания бинарных данных """
        self._localize, self._file_localize = self._define_localization()
        self._create_config_file()
        self._creation_city_location_all_localize()
        self._creation_ip_file(dox_ip_geolite2.NETWORK_FILE_CONFIG_CITY_IP4, self._CITIES_IP)
        self._creation_ip_file(dox_ip_geolite2.NETWORK_FILE_CONFIG_CITY_IP6, self._CITIES_IP)
        self._creation_ip_file(dox_ip_geolite2.NETWORK_FILE_CONFIG_ORG_IP4, self._ORGANIZATIONS_IP)
        self._creation_ip_file(dox_ip_geolite2.NETWORK_FILE_CONFIG_ORG_IP6, self._ORGANIZATIONS_IP)

    def _define_localization(self):
        """ Определяет локализации данных """
        localize = []
        file_localize = {}
        # Разделим название файла на непосредственно название и расширение.
        cities_list_filename, ext = os.path.splitext(dox_ip_geolite2.CITIES_LIST_FILENAME)
        # Далее создадим шаблон для определения в названии файла локализации.
        pattern = re.compile(r'{}-*(.+?){}'.format(cities_list_filename, ext))
        # Найдеи в каталоге импорта все файлы, которые начинаются с названия файла городов.
        files = (file for file in os.listdir(self._import_folder)
                 if os.path.basename(file).startswith(cities_list_filename))
        # Пройдемся по всем найденым файлам,
        for file in files:
            # и с помощью регулярного выражения выделим из названия файла локализацию.
            loc = pattern.search(file).group(1)
            # Далее, если локализация из названия файла была выделена,
            if loc:
                # то добавим эту локализацию в список локализаций,
                localize.append(loc)
                # а также сохраним название файла под конкретной локализацией в словарь файлов csv.
                file_localize[loc] = file
        sys.stdout.write(f"Обнаружено {len(localize)} локализации: {', '.join(localize)}.\n")
        # Вернем список локализаций и словарь файлов локализации.
        return localize, file_localize

    def _creation_city_location_all_localize(self):
        """ Создает бинарные файлы локации городов для каждой найденной локализации """
        for loc in self._localize:
            csv_filename = os.path.join(self._import_folder, self._file_localize[loc])
            self. _creation_city_location_file(csv_filename, loc)

    def _creation_city_location_file(self, csv_filename, localize):
        """
         Создает бинарный файл к указанному csv файлу с указанной локализацией

        :param str csv_filename:
        :param str localize: локализация файла
        """
        format_dat = dox_ip_geolite2.FILE_CONFIG_LOCATION_CITY.format
        format_idx = dox_ip_geolite2.FILE_CONFIG_LOCATION_CITY.format_idx
        index_offset = dox_ip_geolite2.FILE_CONFIG_LOCATION_CITY.index_offset
        val_sizes = format_dat[2:].split('s')
        # Для начала подсчитаем количество строк в csv файле.
        count_rows = self._calculating_row_count(csv_filename)
        # Далее сформируем наименование бинарного файла.
        filename = f"{dox_ip_geolite2.FILE_CONFIG_LOCATION_CITY.filename}-{localize}"
        sys.stdout.write(f"Формируется файл {filename}.dat\n")
        # Теперь к наименованию файла добавим путь.
        full_filename = os.path.join(self._base_folder, filename)
        # Откроем файлы на чтения и на запись,
        with open(csv_filename, 'r', encoding='utf-8') as csv_file, \
            open(f'{full_filename}.dat', "w+b") as dat_file, \
                open(f'{full_filename}.idx', "w+b") as idx_file:
            # и сразу считаем csv файл в словарь.
            reader = csv.DictReader(csv_file, delimiter=',')
            # Пробежимся по словарю,
            for i, row in enumerate(reader, start=1):
                # и запишем каждую строку в бинарный файл.
                self._city_location_write_dat(dat_file, row, format_dat, val_sizes)
                self._city_location_write_idx(idx_file, row['geoname_id'], i, format_idx, index_offset)
                self._show_percent(i, count_rows)
            sys.stdout.write("\n")
            sys.stdout.write(f"обработано {i} строк данных.\n")

    # noinspection PyMethodMayBeStatic
    def _city_location_write_dat(self, fh_dat, row, format_dat, val_sizes):
        """
        Записывает строку данных в бинарный файл

        :param fh_dat: дескриптор файла
        :param dict row: строка данных
        :param str format_dat: формат структуры даных
        :param list val_sizes:
        """
        geoname_id = int(row['geoname_id'])
        continent = f"{row['continent_name']:<{val_sizes[0]}}".encode('utf8')
        country = f"{row['country_name']:<{val_sizes[1]}}".encode('utf8')
        subdivision_1 = f"{row['subdivision_1_name']:<{val_sizes[2]}}".encode('utf8')
        subdivision_2 = f"{row['subdivision_2_name']:<{val_sizes[3]}}".encode('utf8')
        city = f"{row['city_name']:<{val_sizes[4]}}".encode('utf8')
        timezone = f"{row['time_zone']:<{val_sizes[5]}}".encode('utf8')
        fh_dat.write(struct.pack(format_dat, geoname_id, continent, country, subdivision_1, subdivision_2,
                                 city, timezone))

    # noinspection PyMethodMayBeStatic
    def _city_location_write_idx(self, fh_idx, key, i, format_idx, index_offset):
        """ Записывает индексную информацию """
        # то в случае, если номер строки без остатка делиться на размер смещения индекса (кратен),
        if i % index_offset == 0:
            # то добавим этот ключ с порядковым номером его в строке файла данных, в байтовый массив.
            fh_idx.write(struct.pack(format_idx, int(key), i))

    def _creation_ip_file(self, file_config, view_ip):
        """ Создает рабочий файл адресов IP городов """
        if view_ip == self._CITIES_IP:
            name = 'городов'
        elif view_ip == self._ORGANIZATIONS_IP:
            name = 'организаций'
        else:
            raise ValueError("Неверное значение типа идентификатора IP")
        # format_idx = get_struct_network_format_dat(file_config)
        format_idx = get_struct_network_format_idx(file_config)

        sys.stdout.write(f"Формирование файла адресов IP{file_config.ip_ver} {name}...\n")
        filename_bin = os.path.join(self._base_folder, file_config.filename)
        filename_csv = os.path.join(self._import_folder, self._choice_csv_filename(file_config))
        count_rows = self._calculating_row_count(filename_csv)
        with open(f'{filename_bin}.dat', 'w+b') as file_dat, open(f'{filename_bin}.idx', 'w+b') as file_idx, \
                open(filename_csv, 'r',  encoding='utf-8') as file_csv:
            reader = csv.DictReader(file_csv, delimiter=',')
            for i, row in enumerate(reader, start=1):
                self. _network_write_dat(file_dat, row, file_config, view_ip)
                # network = f"{row['network']:<{file_config.code_size}}".encode('utf8')
                network = row['network']
                # self._ref_data_idx_write(file_idx, network, i, format_idx, file_config)
                self._network_write_idx(file_idx, network, i, format_idx, file_config)
                self._show_percent(i, count_rows)
            sys.stdout.write(f"\nОбработано {i} строк данных.\n")

    # noinspection PyMethodMayBeStatic
    def _choice_csv_filename(self, file_config):
        """ Возвращает наименование csv файла в зависимости от конфигурации """
        csv_files = {'city_ip4':  dox_ip_geolite2.IPV4_CITIES_FILENAME,
                     'city_ip6': dox_ip_geolite2.IPV6_CITIES_FILENAME,
                     'org_ip4': dox_ip_geolite2.IPV4_ORGANIZATION_FILENAME,
                     'org_ip6': dox_ip_geolite2.IPV6_ORGANIZATION_FILENAME}

        return csv_files[file_config.filename]

    def _network_write_dat(self, fh_dat, row, file_config, view_ip):
        """ Записывает данные сети в двоичный массив """
        if view_ip == self._CITIES_IP:
            field_id = 'geoname_id'
        elif view_ip == self._ORGANIZATIONS_IP:
            field_id = 'autonomous_system_organization'
        else:
            raise ValueError("Неверное значение типа идентификатора IP")
        format_dat = get_struct_network_format_dat(file_config)
        network = f"{row['network']:<{file_config.code_size}}".encode('utf8')
        field_data = ''
        if view_ip == self._CITIES_IP:
            field_data = int(row[field_id]) if row[field_id] != '' else 0
        elif view_ip == self._ORGANIZATIONS_IP:
            field_data = f"{row[field_id]:<100}".encode('utf8')
#        id_ = int(row[field_id]) if row[field_id] != '' else 0
        try:
            fh_dat.write(struct.pack(format_dat, network, field_data))
        except struct.error as err:
            print("ERROR", file_config.filename, format_dat, field_data)
            raise Exception(err)

    # noinspection PyMethodMayBeStatic
    def _network_write_idx(self, fh_idx, network, i, format_idx, file_config):
        """ Записывает данные сети в инедексный файл """
        # Если номер строки без остатка делиться на размер смещения индекса (кратен),
        if i % file_config.index_offset == 0:
            # то добавим этот адрес с порядковым номером его в строке файла данных, в байтовый массив.
            # Для этого возьмем только ip адрес (уберем префикс подсети).
            ip, _ = network.split('/')
            # Далее скорректируем длинну данных с ip адресом,
            ip = f'{ip:<{file_config.code_size - 3}}'.encode('utf8')
            # и запишем даынне в файл
            fh_idx.write(struct.pack(format_idx, ip, i))

    def _show_percent(self, num, all_count):
        """
        Отображает прогресс выполнения импортирования

        :param int num: текущее значение номер записи
        :param int all_count: общее количество записей
        :return:
        """
        # Для начала вычислим процент, который надо указать.
        percent = int(round(num/(all_count/100), 4))
        # Далее, если значения проценто изменилось по отношению к последнему значению,
        if percent != self._current_percent:
            # то выведим значение прогресса, причем без перевода строки.
            sys.stdout.write(f'\rвыполнено {percent}%')
            # Зафиксируем изменение значения процента.
            self._current_percent = percent

    def _create_config_file(self):
        """ Создает кофигурационный файл для наших баз данных """
        data = bytearray()
        sys.stdout.write("Формирование конфигурационного файла: ")
        # Добавим в байтовый массив количество локализаций.
        data.extend(struct.pack('<H', len(self._localize)))
        # Пройдемся по всем локализациям,
        for loc in self._localize:
            # и добавим их в байтовый массив
            data.extend(pack_string(loc))
        # Далее сформируем имя конфигурационного файла,
        filename = os.path.join(self._base_folder, 'config.dat')
        # откроем этот файл на запись,
        file = open(filename, "w+b")
        # и запишем туда наши данные.
        file.write(data)
        # В фконце запкроем файл.
        file.close()
        sys.stdout.write("Ок. \n")

    def _calculating_row_count(self, filename):
        """
        Определяет общее количество строк указанного csv-файла

        :param filename:
        :return:
        """
        count = 0
        # Откроем указанный файл на чтение,
        with open(os.path.join(self.import_folder, filename), 'r', encoding='utf-8') as file:
            # и пробежимся по всем его строкам,
            # noinspection PyUnusedLocal
            for row in file.readlines():
                # подсчитывая количество строк.
                count += 1
        # Далее определим переменную общего количества строк.
        # Вычтим из значения единицу (заголовок данных)
        return count - 1
