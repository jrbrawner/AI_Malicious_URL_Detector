from basic_features import BasicFeatures
from external_features import ExternalFeatures


column_names = ['num_@', 'url_length', 'host_length', 'num_.', 'num_-', 'num_?', 'num_&',
                'num_=', 'num_', 'num_~', 'num_%', 'num_/',
                'num_*', 'num_:', 'num_comma', 'num_;', 'num_$',
                'numSpaces', 'num_www', 'num_com', 'num_bslash', 'num_digits', 'num_params', 'is_https',
                'hostname_2length_ratio', 'url_entropy', 'contains_port',
                'http_in_query', 'tld_in_path', 'shortener_url', 'is_ip', 'url_length_sus', 'sus_extension_type',
                 'phish_hints', 'count_fragment', 'months_since_creation',
                'months_since_expired', 'url_is_live', 'num_redirects', 'body_length', 'numLinks',
                'numImages', 'script_length', 'specialCharacters', 'scriptBodyRatio']


def build_dataset(url):
    # basic features
    features_list = []

    basicfeatures = BasicFeatures(url)
    for i in basicfeatures.build():
        features_list.append(i)

    externalfeatures = ExternalFeatures(url)
    for i in externalfeatures.build():
        features_list.append(i)

    return features_list


def write_csv(filename, url_list):
    count = 0
    num = len(url_list)
    with open(filename, 'w') as write_obj:
        for i in range(len(column_names)):
            try:
                if i == len(column_names) - 1:
                    write_obj.write(str(column_names[i]) + '\n')
                else:
                    write_obj.write(str(column_names[i]) + ',')
            except IndexError:
                write_obj.write(str(column_names[i]) + '\n')
        for i in url_list:
            temp = build_dataset(i)
            count = count + 1
            print((str(count) + ' URLs analyzed out of ' + str(num) + '.'))
            for x in range(len(temp)):
                try:
                    #if temp[0].count(',') > 0:
                     #   temp[0] = temp[0].replace(',', '(COMMA)')
                    if x == len(temp) - 1:
                        write_obj.write(str(temp[x]) + '\n')
                    else:
                        write_obj.write(str(temp[x]) + ',')
                except IndexError:
                    write_obj.write(str(temp[x]) + '\n')
    write_obj.close()
    print('Dataset built.')
