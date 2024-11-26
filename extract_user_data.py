import json
from datetime import datetime


# Функция для определения статуса "свободен" на основе данных о семейном положении
# Семейное положение = 0 считается "свободным"
def is_free(relation_status):
    return relation_status == 0


# Функция для определения возраста пользователя
# Возраст до 30 лет считается "молодым"
def is_young(birth_date):
    if not birth_date:
        return False
    try:
        birth_year = int(birth_date.split('.')[-1])
        current_year = datetime.now().year
        age = current_year - birth_year
        return age < 30
    except ValueError:
        return False


# Основная функция для обработки JSON файла
# Открываем файл, анализируем данные и записываем результат в новый файл
def extract_user_data(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        users = json.load(infile)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for user in users:
            user_id = user.get("id", "unknown")
            relation_status = user.get("relation", 0)
            birth_date = user.get("bdate", "")
            sex = user.get("sex", 0)

            # Определяем параметры
            free_status = is_free(relation_status)
            young_status = is_young(birth_date)
            sex_str = "мужчина" if sex == 2 else "женщина" if sex == 1 else "неизвестно"

            # Записываем результат
            outfile.write(
                f"{user_id} {'1' if free_status else '0'} {'1' if young_status else '0'} {sex_str}\n")


# Пример использования функции
input_file = "users.json"
output_file = "user_status_output.txt"
extract_user_data(input_file, output_file)
