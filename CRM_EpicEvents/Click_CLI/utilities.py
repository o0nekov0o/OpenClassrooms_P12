from Click_CLI.constants import NULL_VALUE


def format_date_json(date_str):
    if date_str == NULL_VALUE:
        return date_str
    else:
        return date_str[6:10] + "-" + date_str[3:5] + "-" + date_str[0:2]
