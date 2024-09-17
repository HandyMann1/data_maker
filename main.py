import random
from typing import List


def generate_full_name(slavic_male_surnames: List[str], slavic_male_names: List[str],
                       slavic_male_patronymics: List[str],
                       slavic_female_surnames: List[str], slavic_female_names: List[str],
                       slavic_female_patronymics: List[str], male_coef: float = 0.5) -> dict:
    full_name = {'surname': '', 'name': '', 'patronymic': ''}
    if male_coef > random.random():
        full_name['surname'] = random.choice(slavic_male_surnames)
        full_name['name'] = random.choice(slavic_male_names)
        full_name['patronymic'] = random.choice(slavic_male_patronymics)
    else:
        full_name['surname'] = random.choice(slavic_female_surnames)
        full_name['name'] = random.choice(slavic_female_names)
        full_name['patronymic'] = random.choice(slavic_female_patronymics)
    return full_name


def generate_passport_numbers(region_numbers: List[str], used_passports_list: List[str]) -> str:
    while True:
        passport_number = random.choice(region_numbers) + str(random.randint(0, 99)) + ' ' + random.randint(100000,
                                                                                                            999999)
        if passport_number not in used_passports_list:
            return passport_number


def generate_card_number(used_cards, pay_system, bank) -> str:
    if pay_system == 'Мир':
        if bank == 'Сбербанк':
            numbers = '2202'
        elif bank == 'Тинькофф':
            numbers = '2200'
        elif bank == 'ВТБ':
            numbers = '2204'
        else:
            numbers = '2206'
    elif pay_system == 'MasterCard':
        if bank == 'Сбербанк':
            numbers = '5469'
        elif bank == 'Тинькофф':
            numbers = '5489'
        elif bank == 'ВТБ':
            numbers = '5443'
        else:
            numbers = '5406'
    else:
        if bank == 'Сбербанк':
            numbers = '4276'
        elif bank == 'Тинькофф':
            numbers = '4277'
        elif bank == 'ВТБ':
            numbers = '4272'
        else:
            numbers = '4279'
    while True:
        rand_numbers = []
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

    return card_number
