import random

from openpyxl import Workbook

import config as c
import main_classes as m


def generate_data(sber_prob, vtb_prob, visa_prob, mastercard_prob, num_of_people):
    available_train_numbers = m.generate_train_numbers()
    routes_set = set()
    trains_list = []
    full_name_set = set()
    used_cards = {}
    used_passports = set()
    persons_list: list[m.Person] = []

    stations_list = m.prep_stations_info(c.stations)
    slavic_male_surnames = m.prep_names(c.slavic_male_surnames)
    slavic_male_names = m.prep_names(c.slavic_male_names)
    slavic_male_patronymics = m.prep_names(c.slavic_male_patronymics)
    slavic_fem_surnames = m.prep_names(c.slavic_fem_surnames)
    slavic_fem_names = m.prep_names(c.slavic_fem_names)
    slavic_fem_patronymics = m.prep_names(c.slavic_fem_patronymics)
    region_numbers_list = m.prep_names(c.reg_passport_nums)

    for i in range(c.num_routes):  # генерируем маршруты
        train = m.Train()
        train.choose_train_name_and_type(available_train_numbers)
        train.create_route(stations_list, routes_set)
        trains_list.append(train)

    for train in trains_list:  # генерируем вагоны
        for j in range(train.number_of_wagons):
            train.add_wagon()

    for i in range(num_of_people):  # генерируем людей и рассаживаем их в вагоны
        person = m.Person()
        person.generate_full_name(full_name_set, slavic_male_surnames, slavic_male_names, slavic_male_patronymics,
                                  slavic_fem_surnames, slavic_fem_names, slavic_fem_patronymics)
        person.choose_pay_system_and_bank(sber_prob, vtb_prob, visa_prob, mastercard_prob)
        person.generate_card_number(used_cards)
        person.generate_passport_numbers(region_numbers_list, used_passports)
        while True:
            selected_train: m.Train = random.choice(trains_list)
            if selected_train.free_seats > 0:
                person.station_arrival = selected_train.station_arrival[0]
                person.station_departure = selected_train.station_departure[0]
                person.date_departure = selected_train.date_departure
                person.date_arrival = selected_train.date_arrival
                selected_train.free_seats -= 1
                person.train_name = selected_train.train_name
                while True:
                    selected_wagon: m.Wagon = random.choice(selected_train.wagons_list)
                    if selected_wagon.occupied_seats < selected_wagon.wagon_size:
                        selected_wagon.occupied_seats += 1
                        selected_wagon.add_passenger(person, selected_wagon)
                        person.wagon_number = selected_wagon.wagon_number
                        person.cost = selected_wagon.wagon_cost
                        person.seat_number = selected_wagon.occupied_seats
                        break
                break
        persons_list.append(person)

    workbook = Workbook()  # создаём excel файл
    worksheet = workbook.active
    worksheet["A1"] = "ФИО"
    worksheet["B1"] = "Паспортные данные"
    worksheet["C1"] = "Откуда"
    worksheet["D1"] = "Куда"
    worksheet["E1"] = "Дата отъезда"
    worksheet["F1"] = "Дата приезда"
    worksheet["G1"] = "Рейс"
    worksheet["H1"] = "Выбор вагона и места"
    worksheet["I1"] = "Стоимость"
    worksheet["J1"] = "Карта оплаты"

    for person in persons_list:
        formatted_fio = "{} {} {}".format(person.name['first_name'], person.name['patronymic'],
                                          person.name['surname'])
        formatted_station_dep = ' '.join(person.station_departure)
        formatted_station_arr = ' '.join(person.station_arrival)
        formatted_date_dep = person.date_departure.strftime("%Y-%m-%dT%H:%M")
        formatted_date_arr = person.date_arrival.strftime("%Y-%m-%dT%H:%M")
        formatted_wagon_and_seat_num = (f'{person.wagon_number}-{person.seat_number}'
                                        f' ({person.wagon_number} вагон, {person.seat_number} место)')
        formatted_price = f'{int(person.cost)} руб'

        row = [formatted_fio, person.passport_number, formatted_station_dep, formatted_station_arr, formatted_date_dep,
               formatted_date_arr, person.train_name, formatted_wagon_and_seat_num, formatted_price, person.card_number]
        worksheet.append(row)

    workbook.save('data.xlsx')

    print("Excel file 'data' was created")
