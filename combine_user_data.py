import csv

# Функция для связывания данных из нескольких файлов по идентификатору пользователя
def combine_user_data(colors_file, links_file, clusters_file, status_file, output_file):
    # Загружаем данные из всех файлов в словари по идентификатору пользователя
    colors_data = {}
    with open(colors_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(' ', 1)
            if len(parts) == 2:
                colors_data[parts[0]] = parts[1]

    links_data = {}
    with open(links_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(' ', 1)
            if len(parts) == 2:
                links_data[parts[0]] = parts[1]

    clusters_data = {}
    with open(clusters_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(' - Кластер ')
            if len(parts) == 2:
                clusters_data[parts[0]] = parts[1]

    status_data = {}
    with open(status_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(' ', 3)
            if len(parts) == 4:
                user_id = parts[0]
                free_status = 'Да' if parts[1] == '1' else 'Нет'
                young_status = 'Да' if parts[2] == '1' else 'Нет'
                sex = parts[3]
                status_data[user_id] = {'Свободен': free_status, 'Молодой': young_status, 'Пол': sex}

    # Создаем CSV файл для вывода объединенных данных
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = ['ID', 'Цвета', 'Ссылка на аватар', 'Кластер', 'Свободен', 'Молодой', 'Пол']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Объединяем данные по идентификатору и записываем в выходной файл
        all_user_ids = set(colors_data.keys()) | set(links_data.keys()) | set(clusters_data.keys()) | set(status_data.keys())
        for user_id in all_user_ids:
            row = {
                'ID': user_id,
                'Цвета': colors_data.get(user_id, 'Неизвестно'),
                'Ссылка на аватар': links_data.get(user_id, 'Неизвестно'),
                'Кластер': clusters_data.get(user_id, 'Неизвестно'),
                'Свободен': status_data.get(user_id, {}).get('Свободен', 'Неизвестно'),
                'Молодой': status_data.get(user_id, {}).get('Молодой', 'Неизвестно'),
                'Пол': status_data.get(user_id, {}).get('Пол', 'Неизвестно')
            }
            writer.writerow(row)

# Пример использования функции
colors_file = "id_and_colors.txt"
links_file = "id_and_links.txt"
clusters_file = "user_cluster_labels.txt"
status_file = "user_status_output.txt"
output_file = "combined_user_data.csv"
combine_user_data(colors_file, links_file, clusters_file, status_file, output_file)
