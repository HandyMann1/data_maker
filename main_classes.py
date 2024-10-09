import datetime
import random
from math import radians, sin, cos, asin, sqrt

import config


class Train:
    def __init__(self):
        self.date_departure: datetime = None
        self.date_arrival: datetime = None
        self.station_departure = None
        self.station_arrival = None
        self.train_number = None
        self.train_name = None
        self.train_type = None
        self.number_of_wagons: int = 10
        self.wagons_list = []
        self.distance = None
        self.free_seats: int = 0

    def calculate_dist(self, xA: float, yA: float, xB: float, yB: float):  # https://dzen.ru/a/WyQuefRW4ACp2JIN
        r = 6371  # Earth radius
        latA = radians(xA)
        latB = radians(xB)
        lonA = radians(yA)
        lonB = radians(yB)

        sinlat = sin((latB - latA) / 2)
        sinlon = sin((lonB - lonA) / 2)

        coslonA = cos(latA)
        coslonB = cos(latB)

        h = pow(sinlat, 2) + coslonA * coslonB * pow(sinlon, 2)
        d = 2 * r * asin(sqrt(h))
        self.distance = int(d)

    def choose_train_name_and_type(self, available_numbers):
        train_number = random.choice(available_numbers)
        if 1 <= train_number <= 300:
            self.train_type = "скорый"
        elif 301 <= train_number <= 700:
            self.train_type = "пассажирский"
        elif 701 <= train_number <= 750:
            self.train_type = "сапсан"
        else:
            self.train_type = "стриж"
        self.train_number = train_number
        self.train_name = f"{'0' * (3 - len(str(train_number)))}{train_number}{random.choice(config.russian_letters)}"

    def calculate_moving_time_in_hours(self, train_number):
        if 1 <= train_number <= 300:
            train_speed = 60
        elif 301 <= train_number <= 598:
            train_speed = 50
        elif 701 <= train_number <= 750:
            train_speed = 91
        elif 751 <= train_number <= 788:
            train_speed = 161
        else:
            train_speed = 50
        total_seconds = int(self.distance / train_speed * 3600)
        delta = datetime.timedelta(seconds=total_seconds)
        return delta

    def create_random_dates(self, start_date: datetime, end_date: datetime):
        total_seconds = (end_date - start_date).total_seconds()
        random_seconds = random.randint(180, int(total_seconds))
        self.date_departure = start_date + datetime.timedelta(seconds=random_seconds)
        self.date_arrival = self.date_departure + self.calculate_moving_time_in_hours(self.train_number)

    def create_route(self, stations_info: list[tuple[str, float, float]], routes_set: set):
        while True:
            departure = random.choice(stations_info)
            arrival = random.choice(stations_info)
            route = (str(departure[0]), str(arrival[0]))
            if departure != arrival and route not in routes_set:
                self.station_departure = departure
                self.station_arrival = arrival
                self.calculate_dist(departure[1], departure[2], arrival[1], arrival[2])
                self.create_random_dates(config.start_date, config.end_date)
                routes_set.add(route)
                break

    def add_wagon(self):
        for i in range(1, self.number_of_wagons + 1):
            wagon = Wagon(i, self.train_type, self.distance, self.train_name)
            self.wagons_list.append(wagon)
            self.free_seats += wagon.wagon_size


class Person:
    def __init__(self):
        self.name = {"surname": None, "first_name": None, "patronymic": None}
        self.passport_number = None
        self.card_number = None
        self.train_name = None
        self.wagon_number = None
        self.seat_number = None
        self.cost = None
        self.date_departure: datetime = None
        self.date_arrival: datetime = None
        self.station_departure = None
        self.station_arrival = None
        self.bank = None
        self.payment_system = None

    def generate_passport_numbers(self, region_numbers: list, used_passports_set: set):
        while True:
            region_code = random.choice(tuple(region_numbers))
            birth_code = str(random.randint(1, 99))
            serial_1 = str(random.randint(100, 999))
            serial_2 = str(random.randint(100, 999))
            passport_number = (
                f"{'0' * (2 - len(region_code)) + region_code} {'0' * (2 - len(birth_code)) + birth_code}"
                f" {serial_1}{serial_2}")
            if passport_number not in used_passports_set:
                used_passports_set.add(passport_number)
                self.passport_number = passport_number
                break

    def choose_pay_system_and_bank(self, sber_prob: float, vtb_prob: float, visa_prob: float, mastercard_prob: float):
        rand_bank = 100 * random.random()
        rand_pay_system = 100 * random.random()
        if rand_bank <= sber_prob:
            self.bank = 'Сбер'
        elif sber_prob < rand_bank <= sber_prob + vtb_prob:
            self.bank = 'ВТБ'
        else:
            self.bank = 'Тинькофф'

        if rand_pay_system <= visa_prob:
            self.payment_system = 'Visa'
        elif visa_prob < rand_bank <= visa_prob + mastercard_prob:
            self.payment_system = 'MasterCard'
        else:
            self.payment_system = 'Мир'

    def generate_card_number(self, used_cards):
        if self.payment_system == 'Мир':
            if self.bank == 'Сбер':
                numbers = '2202'
            elif self.bank == 'Тинькофф':
                numbers = '2200'
            elif self.bank == 'ВТБ':
                numbers = '2204'
            else:
                numbers = '2206'
        elif self.payment_system == 'MasterCard':
            if self.bank == 'Сбер':
                numbers = '5469'
            elif self.bank == 'Тинькофф':
                numbers = '5489'
            elif self.bank == 'ВТБ':
                numbers = '5443'
            else:
                numbers = '5406'
        else:
            if self.bank == 'Сбер':
                numbers = '4276'
            elif self.bank == 'Тинькофф':
                numbers = '4277'
            elif self.bank == 'ВТБ':
                numbers = '4272'
            else:
                numbers = '4279'
        while True:
            rand_numbers = ['1000', '1000', '1000']
            for i in range(3):
                rand_numbers[i] = str(random.randint(1000, 9999))
            card_number = numbers + ' ' + rand_numbers[0] + ' ' + rand_numbers[1] + ' ' + rand_numbers[2]
            if card_number in used_cards:
                if used_cards[card_number] < 5:
                    used_cards[card_number] += 1
                    break
            else:
                used_cards[card_number] = 1
                break

        self.card_number = card_number

    def generate_full_name(self, full_name_set: set, slavic_male_surnames,
                           slavic_male_names,
                           slavic_male_patronymics,
                           slavic_female_surnames, slavic_female_names,
                           slavic_female_patronymics, male_coef: float = 0.5):

        total_male_combinations = len(slavic_male_surnames) * len(slavic_male_names) * len(slavic_male_patronymics)
        total_female_combinations = len(slavic_female_surnames) * len(slavic_female_names) * len(
            slavic_female_patronymics)
        if len(full_name_set) >= total_male_combinations + total_female_combinations:
            print("No more unique full names can be generated.")
            return
        while True:
            if male_coef > random.random():
                full_name = {
                    'surname': random.choice(slavic_male_surnames),
                    'first_name': random.choice(slavic_male_names),
                    'patronymic': random.choice(slavic_male_patronymics)
                }
            else:
                full_name = {
                    'surname': random.choice(slavic_female_surnames),
                    'first_name': random.choice(slavic_female_names),
                    'patronymic': random.choice(slavic_female_patronymics)
                }
            full_name_frozenset = frozenset(full_name.items())

            if full_name_frozenset not in full_name_set:
                full_name_set.add(full_name_frozenset)
                break

        self.name = full_name


class Wagon:
    def __init__(self, wagon_number, train_type, distance, train_name):
        self.wagon_number = wagon_number
        self.wagon_size: int = 54
        self.wagon_type = None
        self.wagon_cost = None
        self.train_name = train_name
        self.passengers = []
        self.train_type = train_type
        self.distance: int = distance
        self.create_wagon()
        self.occupied_seats = 0

    def create_wagon(self):
        self.wagon_type = random.choice(list(config.train_type_name[self.train_type].keys()))
        self.wagon_cost = config.train_type_name[self.train_type][self.wagon_type] * self.distance

    def add_passenger(self, person: Person, seat):
        person.train_name = self.train_name
        person.wagon_number = self.wagon_number
        person.seat = seat


def prep_stations_info(filename):
    stations_prepped = []
    with open(file=filename, mode='r') as stations:
        for line in stations:
            line_prepped = line.strip().split()
            station_name = line_prepped[:-2]
            station_lat = line_prepped[-2]
            station_lon = line_prepped[-1]
            stations_prepped.append((station_name, float(station_lat), float(station_lon)))
    return stations_prepped


def prep_names(filename):
    prepped_names = []
    with open(file=filename, mode='r') as names:
        for name in names:
            prepped_names.append(name.strip())
    return prepped_names


def generate_train_numbers():
    train_numbers = []
    for i in range(1, 788):
        train_numbers.append(i)

    return train_numbers
