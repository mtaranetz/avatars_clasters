import numpy as np
import requests
from sklearn.cluster import KMeans
from io import BytesIO
from PIL import Image, UnidentifiedImageError
import time

# Функция для извлечения главных цветов изображения по ссылке
def extract_dominant_colors(image_url, k=3):
    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content)).convert('RGB')
        pixels = np.array(image).reshape((-1, 3))
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(pixels)
        return kmeans.cluster_centers_
    except (requests.RequestException, UnidentifiedImageError) as e:
        print(f"Ошибка при обработке изображения {image_url}: {e}")
        return None

# Функция для анализа цветов аватаров пользователей и вывода их на консоль и в файл
def analyze_avatars_summary(links_file_path, start_line=0):
    try:
        with open(links_file_path, 'r') as file:
            user_data = [line.strip().split(maxsplit=1) for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Файл {links_file_path} не найден.")
        return

    total_users = len(user_data)
    print("Выделенные URL фотографий пользователей:")
    skip_count = 0
    start_time = time.time()

    with open("id_and_colors.txt", 'a') as output_file:
        for index in range(start_line, total_users):
            user_id, url = user_data[index]
            dominant_colors = extract_dominant_colors(url)
            if dominant_colors is None:
                skip_count += 1
                continue

            hex_colors = ['#{:02x}{:02x}{:02x}'.format(int(color[0]), int(color[1]), int(color[2])) for color in dominant_colors]
            print(f"{user_id} {', '.join(hex_colors)}")
            output_file.write(f"{user_id} {', '.join(hex_colors)}\n")

            processed_count = index - start_line + 1
            elapsed_time = time.time() - start_time
            estimated_remaining_time = (elapsed_time / processed_count) * (total_users - index - 1)
            print(f"Прогресс: {processed_count}/{total_users - start_line}. Приблизительное оставшееся время: {estimated_remaining_time:.2f} секунд")

    print(f"Количество пропущенных аватаров: {skip_count}")

# Пример использования функции для анализа и вывода главных цветов аватаров
links_file_path = "id_and_links.txt"
try:
    start_line = int(input("Введите номер строки, с которой начать обработку: ").strip())
except ValueError:
    start_line = 0
analyze_avatars_summary(links_file_path, start_line=start_line)
