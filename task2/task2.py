import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

import string

from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict

import requests


def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Перевірка на помилки HTTP
        return response.text
    except requests.RequestException as e:
        print(e)
        return None


# Функція для видалення знаків пунктуації
def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))


def map_function(word):
    return word, 1


def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()


def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)


# Виконання MapReduce
def map_reduce(text, search_words=None):
    # Видалення знаків пунктуації
    text = remove_punctuation(text)
    words = text.split()

    # Якщо задано список слів для пошуку, враховувати тільки ці слова
    if search_words:
        words = [word for word in words if word in search_words]

    # Паралельний Мапінг
    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    # Крок 2: Shuffle
    shuffled_values = shuffle_function(mapped_values)

    # Паралельна Редукція
    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)


def visualize_top_words(sorted_result):
    fig, ax = plt.subplots()
    words = [x[0] for x in sorted_result]
    counts = [x[1] for x in sorted_result]

    bar_colors = list(mcolors.CSS4_COLORS)[: len(sorted_result)]

    ax.bar(words, counts, label=words, color=bar_colors)
    ax.set_facecolor("yellow")
    ax.set_ylabel("Word count")
    ax.set_title("Words")
    ax.legend(title="TOP Word counts")

    plt.show()


if __name__ == "__main__":
    # Вхідний текст для обробки
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"
    text = get_text(url)
    if text:
        # Виконання MapReduce на вхідному тексті
        search_words = []
        result = map_reduce(text, search_words)

        print("Результат підрахунку слів:", result)

        sorted_result = sorted(result.items(), key=lambda x: x[1], reverse=True)[:15]
        print("\n\nРезультат підрахунку слів (top 15):", sorted_result)

        visualize_top_words(sorted_result)

    else:
        print("Помилка: Не вдалося отримати вхідний текст.")


# if __name__ == "__main__":

#     link = "https://gutenberg.net.au/ebooks01/0100021.txt"
#     try:
#         f = urllib.request.urlopen(link)
#     except Exception as e:
#         print(e)
#         exit()
#     # Вхідний текст для обробки
#     text = f.read().decode().translate(str.maketrans("", "", string.punctuation))

#     # Виконання MapReduce на вхідному тексті
#     result = map_reduce(text)

#     print("Результат підрахунку слів:", result)
#     sorted_result = sorted(result.items(), key=lambda x: x[1], reverse=True)[:15]
#     print("\n\nРезультат підрахунку слів (top 15):", sorted_result)

#     visualize_top_words(sorted_result)
