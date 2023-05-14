import collections

CITIES_LIST_FILENAME = "GeoLite2-City-Locations.csv"
IPV4_CITIES_FILENAME = "GeoLite2-City-Blocks-IPv4.csv"
IPV6_CITIES_FILENAME = "GeoLite2-City-Blocks-IPv6.csv"
IPV4_ORGANIZATION_FILENAME = "GeoLite2-ASN-Blocks-IPv4.csv"
IPV6_ORGANIZATION_FILENAME = "GeoLite2-ASN-Blocks-IPv6.csv"

LocationBinaryFileConfig = collections.namedtuple('LocationBinaryFileConfig',
                                                  'filename code_type format format_idx index_offset')
NetworkBinaryFileConfig = collections.namedtuple('NetworkBinaryFileConfig',
                                                 'filename code_type code_size ip_ver index_offset')

FILE_CONFIG_LOCATION_CITY = LocationBinaryFileConfig('city_locations', 'int', '<I40s80s80s80s60s30s', '<2I', 200)

NETWORK_FILE_CONFIG_CITY_IP4 = NetworkBinaryFileConfig('city_ip4', 'ip', 18, 4,  500)
NETWORK_FILE_CONFIG_CITY_IP6 = NetworkBinaryFileConfig('city_ip6', 'ip', 43, 6,  400)
NETWORK_FILE_CONFIG_ORG_IP4 = NetworkBinaryFileConfig('org_ip4',   'ip', 18, 4,  300)
NETWORK_FILE_CONFIG_ORG_IP6 = NetworkBinaryFileConfig('org_ip6',   'ip', 43, 6,  200)


def get_struct_network_format_dat(file_config):
    if file_config.filename.startswith('city'):
        format_dat = f'<{file_config.code_size}sI'
    elif file_config.filename.startswith('org'):
        format_dat = f'<{file_config.code_size}s100s'
    else:
        raise ValueError("Недопустимый конфиг файла")
    return format_dat


def get_struct_network_format_idx(file_config):
    return f'<{file_config.code_size - 3}sI'
