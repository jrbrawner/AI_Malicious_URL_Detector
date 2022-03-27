import basic_features
import external_features

column_names = ['url', 'num_@', 'url_length', 'num_.', 'num_-', 'num_?', 'num_&', 'num_=', 'num_','num_%',
                'num_/',
                'num_*', 'num_:', 'num_comma', 'num_;', 'num_$',
                'numSpaces', 'num_www', 'num_com', 'num_bslash', 'num_digits', 'num_params', 'is_https',
                'hostname_2length_ratio', 'url_entropy', 'contains_port',
                'http_in_query', 'tld_in_path', 'shortener_url', 'is_ip']

url_list = []


def build_basic_features(url):
    # basic features
    features_list = []

    features_list.append(url)
    features_list.append(basic_features.count_at(url))
    features_list.append(basic_features.count_url_length(url))
    features_list.append(basic_features.count_host_length(url))
    features_list.append(basic_features.count_dots(url))
    features_list.append(basic_features.count_hyphens(url))
    features_list.append(basic_features.count_question_marks(url))
    features_list.append(basic_features.count_and(url))
    features_list.append(basic_features.count_eq(url))
    features_list.append(basic_features.count_underscore(url))
    features_list.append(basic_features.count_tilde(url))
    features_list.append(basic_features.count_percent(url))
    features_list.append(basic_features.count_slash(url))
    features_list.append(basic_features.count_star(url))
    features_list.append(basic_features.count_colon(url))
    features_list.append(basic_features.count_comma(url))
    features_list.append(basic_features.count_semicolon(url))
    features_list.append(basic_features.count_dollar(url))
    features_list.append(basic_features.count_space(url))
    features_list.append(basic_features.count_www(url))
    features_list.append(basic_features.count_com(url))
    features_list.append(basic_features.count_bslash(url))
    features_list.append(basic_features.count_digits(url))
    features_list.append(basic_features.count_url_params(url))
    features_list.append(basic_features.is_https(url))
    features_list.append(basic_features.ratio_hostname_2length(url))
    features_list.append(basic_features.url_entropy(url))
    features_list.append(basic_features.contains_port(url))
    features_list.append(basic_features.http_in_query(url))
    features_list.append(basic_features.tld_in_path(url))
    features_list.append(basic_features.shortener_url(url))
    features_list.append(basic_features.is_ip(url))

    return features_list


def write_csv(filename):
    with open(filename, 'w') as write_obj:
        for i in range(len(column_names)):
            try:
                j = (column_names[i + 1])
                write_obj.write(str(column_names[i]) + ',')
            except IndexError:
                write_obj.write(str(column_names[i]) + '\n')
        for i in url_list:
            temp = build_basic_features(i)
            for x in temp:
                write_obj(str(temp) + ',')


        print('Done')
    write_obj.close()
