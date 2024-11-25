import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

# Функция для выбора строки в файле id_and_links.txt и отображения аватарки

def display_avatar(link_file_path, color_file_path, user_id):
    # Поиск нужной строки в файле с ссылками на аватарки
    avatar_url = None
    with open(link_file_path, 'r', encoding='utf-8') as link_file:
        for line in link_file:
            parts = line.strip().split()
            if len(parts) == 2 and parts[0] == user_id:
                avatar_url = parts[1]
                break

    if avatar_url is None:
        print(f"Пользователь с идентификатором {user_id} не найден в файле {link_file_path}.")
        return

    # Поиск нужной строки в файле с цветами и визуализация цветов
    colors = None
    with open(color_file_path, 'r', encoding='utf-8') as color_file:
        for line in color_file:
            parts = line.strip().replace(',', '').split()
            if len(parts) == 4 and parts[0] == user_id:
                colors = parts[1:]
                break

    if colors is None:
        print(f"Цвета для пользователя с идентификатором {user_id} не найдены в файле {color_file_path}.")
        return

    # Отображение цветов в виде полос над аватаркой
    plt.figure(figsize=(3, 3))
    plt.subplot(2, 1, 1)
    for idx, color in enumerate(colors):
        color = color.strip().replace(',', '')  # Удаляем лишние запятые и пробелы
        plt.bar(idx, 1, color=color)
        plt.text(idx, 0.5, color, color='black', ha='center', va='center', fontsize=10)
    plt.xticks(range(len(colors)), [f'Цвет {i+1}' for i in range(len(colors))])
    plt.ylim(0, 1)
    plt.axis('off')
    plt.title(f'Основные цвета аватарки пользователя {user_id}', fontsize=7)

    # Загрузка и отображение аватарки
    try:
        response = requests.get(avatar_url)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        plt.subplot(2, 1, 2)
        plt.imshow(image)
        plt.axis('off')
        plt.title(f'Аватар пользователя {user_id}', fontsize=7)  # Уменьшение размера заголовка
        plt.tight_layout()
        plt.show()
    except requests.RequestException as e:
        print(f"Ошибка при загрузке аватарки по ссылке {avatar_url}: {e}")
        return

# Пример использования функции
link_file_path = "id_and_links.txt"
color_file_path = "id_and_colors.txt"
user_id = input("Введите идентификатор пользователя для отображения аватарки и цветов: ").strip()
display_avatar(link_file_path, color_file_path, user_id)
