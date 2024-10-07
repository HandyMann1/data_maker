from datetime import datetime

num_routes = 100
num_of_people = 50000
start_date = datetime(2024, 1, 1, 0, 0)
end_date = datetime(2024, 12, 31, 23, 59)
russian_letters = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У',
                   'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']
banks = ["Сбер", "ВТБ", "Тинькофф"]
payment_systems = ["Visa", "Mastercard", "Мир"]

train_type_name = {
    'сапсан': {
        '1Р': 5.0,  # Купе-переговорная
        '1В': 3.0,  # Места в вагоне 1 класса
        '1С': 3.5,  # Вагон бизнес-класса
        '2С': 2.0,  # Сидячий вагон эконом-класса
        '2В': 2.2,  # Экономический+
        '2E': 1.8  # Вагон-бистро
    },
    'стриж': {
        '1Е': 6.0,  # СВ (VIP)
        '1Р': 3.0,  # Сидячие вагоны 1 класса
        '2С': 2.0  # Сидячие вагоны 2 класса
    },
    'скорый': {
        '3Э': 1.2,  # Плацкартный вагон
        '2Э': 3.5,  # Кондиционируемый вагон повышенной комфортности
        '1Б': 7.0,  # Бизнес-класс
        '1Л': 6.5,  # Вагон СВ
        '1А': 4.0,  # Вагон с баром
        '1И': 3.8  # Вагон без бара
    },
    'пассажирский': {
        '3Э': 1.2,  # Плацкартный вагон
        '2Э': 3.5,  # Кондиционируемый вагон повышенной комфортности
        '1Б': 7.0,  # Бизнес-класс
        '1Л': 6.5,  # Вагон СВ
        '1А': 4.0,  # Вагон с баром
        '1И': 3.8  # Вагон без бара
    }
}
stations = "names/stations.txt"
reg_passport_nums = "names/region_passport_numbers.txt"
slavic_fem_names = "names/slavic_female_names.txt"
slavic_fem_surnames = "names/slavic_female_surnames.txt"
slavic_fem_patronymics = "names/slavic_female_patronymics.txt"
slavic_male_names = "names/slavic_male_names.txt"
slavic_male_surnames = "names/slavic_male_surnames.txt"
slavic_male_patronymics = "names/slavic_male_patronymics.txt"
