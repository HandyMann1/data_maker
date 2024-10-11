import datetime

import pandas as pd

pd.set_option('display.max_columns', 5)
items = ["ФИО", "Паспортные данные", "Откуда", "Куда", "Дата отъезда", "Дата приезда", "Рейс", "Выбор вагона и места",
         "Стоимость", "Карта оплаты"]


def calculate_k_anonymity(quasi_ident: dict, filename):
    df = pd.read_excel(filename)

    unique_rows: pd.DataFrame = pd.DataFrame()
    grouped = df.groupby(items).size().reset_index(name='counts')

    k_anonymity = grouped['counts'].min()

    total_records = len(df)

    worst_k_values: pd.DataFrame = (grouped
                                    .assign(percentage=lambda x: (x['counts'] / total_records) * 100)
                                    .groupby('counts', as_index=False)
                                    .agg({'percentage': 'sum'})
                                    )

    if len(worst_k_values) > 5:
        worst_k_values = worst_k_values.head(5)

    if k_anonymity == 1:
        unique_rows = df.drop_duplicates(subset=quasi_ident.keys(), keep=False)

    return k_anonymity, unique_rows, worst_k_values


def remove_bottom_5_percent(df: pd.DataFrame):
    grouped: pd.DataFrame = df.groupby(items).size().reset_index(name='counts')
    grouped = grouped[grouped['counts'] > 0]

    threshold = grouped["counts"].quantile(0.05)
    filtered_df = df[df.groupby(items).transform('size') > threshold]
    return filtered_df


def depersonalize_data(quasi_ident, filename):
    df = pd.read_excel(filename)
    used_idents = []
    for ident in quasi_ident:
        if quasi_ident[ident]:
            used_idents.append(ident)
    if "ФИО" in used_idents:
        fio_depersonalization(df)
    if "Паспортные данные" in used_idents:
        passport_depersonalization(df)
    if "Откуда" in used_idents:
        replace_stations_with_region(df, from_bool=True)
    if "Куда" in used_idents:
        replace_stations_with_region(df, to_bool=True)
    if "Дата отъезда" in used_idents:
        from_time_depersonalization(df)
    if "Дата приезда" in used_idents:
        to_time_depersonalization(df)
    if "Рейс" in used_idents:
        train_name_depersonalization(df)
    if "Выбор вагона и места" in used_idents:
        wagon_and_seat_depersonalization(df)
    if "Стоимость" in used_idents:
        cost_depersonalization(df)
    if "Карта оплаты" in used_idents:
        card_number_depersonalization(df)
    df = remove_bottom_5_percent(df)

    df.to_excel('depersonalized_data.xlsx', index=False)
    print("done")


def passport_depersonalization(df: pd.DataFrame):
    df["Паспортные данные"] = df["Паспортные данные"].apply(maskerize_passport)


def card_number_depersonalization(df: pd.DataFrame):
    df["Карта оплаты"] = df["Карта оплаты"].str[:4].apply(change_bank_number_to_name)


def cost_depersonalization(df: pd.DataFrame):
    df["Стоимость"] = pd.to_numeric(df["Стоимость"].str[:-4])
    df["Стоимость"] = pd.cut(df["Стоимость"], bins=[0, 1000, 5000, 10000, 25000, 1000000],
                             labels=["0-1000", "1001-5000", "5001-10000", "10001-25000",
                                     "25000+"])


def fio_depersonalization(df: pd.DataFrame):
    df["ФИО"] = df["ФИО"].apply(get_sex)


def from_time_depersonalization(df: pd.DataFrame):
    df["Дата отъезда"] = df["Дата отъезда"].apply(get_quarter)


def to_time_depersonalization(df: pd.DataFrame):
    df["Дата приезда"] = df["Дата приезда"].apply(get_quarter)


def train_name_depersonalization(df: pd.DataFrame):
    df["Рейс"] = df["Рейс"].str[:3].apply(get_train_type)


def wagon_and_seat_depersonalization(df: pd.DataFrame):
    df["Выбор вагона и места"] = "**"


###helpful functions
def get_quarter(date_str):
    date = datetime.datetime.fromisoformat(date_str)
    month = date.month

    if month in [1, 2, 3]:
        return "Q1"
    elif month in [4, 5, 6]:
        return "Q2"
    elif month in [7, 8, 9]:
        return "Q3"
    else:
        return "Q4"


def get_train_type(number_str):
    train_number = int(number_str)
    if 1 <= train_number <= 300:
        return "Скорый"
    elif 301 <= train_number <= 700:
        return "Пассажирский"
    elif 701 <= train_number <= 750:
        return "Сапсан"
    else:
        return "Стриж"


def change_bank_number_to_name(numbers):
    if numbers == '2202' or numbers == '5469' or numbers == '4276':
        bank_name = 'Сбер'
    elif numbers == '2200' or numbers == '5489' or numbers == '4277':
        bank_name = 'Тинькофф'
    else:
        bank_name = 'ВТБ'
    return bank_name


def get_sex(full_name):
    station_name_parts = full_name.split()
    last_letters_female = ["а", "я"]
    if station_name_parts[0][-1] in last_letters_female:
        return "F"
    else:
        return "M"


def maskerize_passport(passport_numbers):
    return "** ** ******"


def replace_stations_with_region(df: pd.DataFrame, from_bool=False, to_bool=False):
    replacement_dict = {}
    with open(file="D:\\python_projects\\names\\stations_with_regions.txt", mode="r") as stations:
        for line in stations:
            line_arr = line.split(sep=" ")
            replacement_dict[" ".join(line_arr[:-1])] = line_arr[-1].strip()
    if from_bool:
        df["Куда"] = df["Куда"].replace(replacement_dict)
    if to_bool:
        df["Откуда"] = df["Откуда"].replace(replacement_dict)
