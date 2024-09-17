import random
from typing import List


def generate_full_name(slavic_male_surnames: List[str], slavic_male_names: List[str],
                       slavic_male_patronymics: List[str],
                       slavic_female_surnames: List[str], slavic_female_names: List[str],
                       slavic_female_patronymics: List[str], male_coef: float = 0.5) -> str:
    if male_coef > random.random():
        full_name = random.choice(slavic_male_surnames) + '' + random.choice(slavic_male_names) + ' ' + random.choice(
            slavic_male_patronymics)
    else:
        full_name = random.choice(slavic_female_surnames) + ' ' + random.choice(
            slavic_female_names) + ' ' + random.choice(
            slavic_female_patronymics)
    return full_name


def generate_passport_numbers(region_numbers: List[str], used_passports_list: List[str]) -> str:
    while True:
        passport_number = random.choice(region_numbers) + str(random.randint(0, 99)) + random.randint(100000, 999999)
        if passport_number not in used_passports_list:
            return passport_number
