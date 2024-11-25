import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import silhouette_score

# Загрузка данных из файла id_and_colors.txt
# Формат данных: идентификатор и три главных цвета в HEX-кодах
data = []
with open("id_and_colors.txt", 'r', encoding='utf-8') as file:
    for line in file:
        parts = line.strip().split()
        if len(parts) == 4:
            user_id = parts[0]
            colors = [parts[1], parts[2], parts[3]]
            data.append((user_id, colors))

# Преобразование HEX-кодов в RGB значения
def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

# Создание списка идентификаторов и RGB значений
user_ids = []
rgb_values = []
for user_id, colors in data:
    user_ids.append(user_id)
    # Рассчитываем среднее значение цвета, используя взвешенное среднее для более точного определения основного цвета
    avg_color = np.median([hex_to_rgb(color) for color in colors], axis=0)  # Используем медиану для устойчивости к выбросам
    rgb_values.append(avg_color)

# Использование метода локтя для определения оптимального количества кластеров
sum_of_squared_distances = []
k_range = range(1, 11)
for k in k_range:
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(rgb_values)
    sum_of_squared_distances.append(kmeans.inertia_)

# Построение графика метода локтя
plt.figure(figsize=(10, 6))
plt.plot(k_range, sum_of_squared_distances, 'bx-')
plt.xlabel('Количество кластеров (k)')
plt.ylabel('Сумма квадратов расстояний до центроидов')
plt.title('Метод локтя для определения оптимального количества кластеров')
plt.show()

# Определение оптимального количества кластеров на основании метода локтя
optimal_k = 1
for i in range(1, len(sum_of_squared_distances)):
    if sum_of_squared_distances[i] - sum_of_squared_distances[i - 1] < 0.1 * (sum_of_squared_distances[0] - sum_of_squared_distances[-1]):
        optimal_k = i + 1
        break

print(f"Оптимальное количество кластеров: {optimal_k}")
optimal_k = 10
# Кластеризация с использованием KMeans с оптимальным количеством кластеров
kmeans = KMeans(n_clusters=optimal_k)
kmeans.fit(rgb_values)
labels = kmeans.labels_

# Оценка качества кластеризации с использованием коэффициента силуэта
silhouette_avg = silhouette_score(rgb_values, labels)
print(f"Средний коэффициент силуэта для {optimal_k} кластеров: {silhouette_avg:.2f}")

# Запись результатов кластеризации в файл
with open("user_cluster_labels.txt", 'w', encoding='utf-8') as output_file:
    for user_id, label in zip(user_ids, labels):
        output_file.write(f"{user_id} - Кластер {label}\n")

print("Кластеризация завершена. Результаты сохранены в user_cluster_labels.txt.")

# Визуализация центроидов кластеров
cluster_colors = kmeans.cluster_centers_
plt.figure(figsize=(10, 5))
for idx, color in enumerate(cluster_colors):
    plt.bar(idx, 1, color=np.array(color) / 255.0, edgecolor='black')
    hex_color = '#{:02x}{:02x}{:02x}'.format(int(color[0]), int(color[1]), int(color[2]))
    plt.text(idx, 0.5, hex_color, color='black', ha='center', va='center')
plt.xticks(range(optimal_k), [f'Кластер {i}' for i in range(optimal_k)])
plt.title('Цвета центроидов кластеров пользователей')
plt.show()
