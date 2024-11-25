import requests
import random
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

# Функция для отображения аватарок разных кластеров

def display_random_avatars(cluster_file_path, link_file_path, cluster_number, sample_size=100):
    # Загрузка данных о пользователях и кластерах из файла
    user_clusters = []
    with open(cluster_file_path, 'r', encoding='utf-8') as cluster_file:
        for line in cluster_file:
            parts = line.strip().split(' - Кластер ')
            if len(parts) == 2 and parts[1] == str(cluster_number):
                user_clusters.append(parts[0])

    if not user_clusters:
        print(f"Не найдено пользователей в кластере {cluster_number}.")
        return

    # Выбираем случайные пользователи из заданного кластера
    selected_users = random.sample(user_clusters, min(sample_size, len(user_clusters)))

    # Сопоставление идентификаторов пользователей с их ссылками на аватарки
    user_links = {}
    with open(link_file_path, 'r', encoding='utf-8') as link_file:
        for line in link_file:
            parts = line.strip().split(maxsplit=1)
            if len(parts) == 2 and parts[0] in selected_users:
                user_links[parts[0]] = parts[1]

    # Отображение аватарок
    plt.figure(figsize=(15, 15))
    cols = 10
    rows = (len(user_links) // cols) + 1
    for idx, (user_id, url) in enumerate(user_links.items()):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
            plt.subplot(rows, cols, idx + 1)
            plt.imshow(image)
            plt.axis('off')
            plt.title(f'User {user_id[:6]}...', fontsize=8)
        except requests.RequestException as e:
            print(f"Ошибка при загрузке аватарки пользователя {user_id}: {e}")
            continue

    plt.tight_layout()
    plt.show()

# Пример использования функции
cluster_file_path = "user_cluster_labels.txt"
link_file_path = "id_and_links.txt"
try:
    cluster_number = int(input("Введите номер кластера для отображения аватарок: ").strip())
except ValueError:
    cluster_number = 0

display_random_avatars(cluster_file_path, link_file_path, cluster_number)
