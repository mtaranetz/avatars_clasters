import json

# Функция для анализа аватаров пользователей и вывода ID и URL
# с возможностью начать с определенного идентификатора и записи в файл
def analyze_avatars_summary(json_file_path, start_id=None):
    # Загрузка JSON-файла
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    print("Выделенные URL фотографий пользователей:")
    start_processing = not bool(start_id)  # Начинаем обработку, если идентификатор не задан

    with open("id_and_links.txt", 'a', encoding='utf-8') as output_file:
        for user in data:
            if "id" in user and "photo_100" in user:
                user_id = user["id"]
                url = user["photo_100"]

                # Пропуск пользователей до достижения нужного идентификатора
                if not start_processing:
                    if user_id == start_id:
                        start_processing = True
                    else:
                        continue

                # Выводим ID пользователя и ссылку на аватарку
                print(f"{user_id} {url}")
                # Дописываем ID и URL в файл
                output_file.write(f"{user_id} {url}\n")

# Пример использования функции для анализа и вывода ID и URL аватаров
json_file_path = "users.json"
start_id = input("Введите идентификатор пользователя, с которого начать обработку (оставьте пустым для начала с первой записи): ").strip()
analyze_avatars_summary(json_file_path, start_id=start_id)
