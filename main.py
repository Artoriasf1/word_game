from game_logic import LinkedList, WordChain, WordChainError


def split_words(text):
    words = LinkedList()
    current_word = ""
    for character in text:
        if character.isspace():
            if current_word:
                words.append(current_word)
                current_word = ""
        else:
            current_word += character
    if current_word:
        words.append(current_word)
    return words


def load_words(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            words = split_words(f.read())
        if not words:
            print("Файл пуст.")
            return None
        return words
    except FileNotFoundError:
        print("Ошибка: файл не найден.")
    except (OSError, UnicodeError) as e:
        print("Ошибка при чтении файла:", e)
    return None


def save_result(filename, result):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(result)
        return True
    except OSError as e:
        print("Ошибка при записи файла:", e)
        return False


def build_and_save(words, output_filename):
    try:
        game = WordChain(words)
        if game.build():
            result = " ".join(game.get_chain())
        else:
            result = "Решений не существует."

        if save_result(output_filename, result):
            print("Результат записан в файл:", output_filename)
            print(result)
    except WordChainError as e:
        print("Ошибка:", e)


def print_menu():
    print()
    print("ИГРА В СЛОВА")
    print()
    print(
        "Внимание! Слова в файле должны быть написаны строчными "
        "буквами русского алфавита. Формат файла должен быть .txt"
    )
    print()
    print("1. Загрузить слова из файла")
    print("0. Выйти")
    print()


def main():
    words = None

    while True:
        print_menu()
        choice = input("Выберите пункт меню: ").strip()

        if choice == "1":
            filename = input("Введите имя файла: ").strip()
            if not filename:
                print("Ошибка: имя файла не введено.")
            elif not filename.lower().endswith(".txt"):
                print("Ошибка: файл должен быть текстовым (.txt).")
            else:
                loaded = load_words(filename)
                if loaded is not None:
                    output_filename = input(
                        "Введите имя выходного файла: ").strip()
                    if not output_filename:
                        print("Ошибка: имя выходного файла не введено.")
                    elif not output_filename.lower().endswith(".txt"):
                        print("Ошибка: файл должен быть текстовым (.txt).")
                    else:
                        words = loaded
                        build_and_save(words, output_filename)

        elif choice == "0":
            break

        else:
            print("Неверный пункт меню. Введите 0 или 1.")

        input("Нажмите Enter, чтобы продолжить...")


if __name__ == "__main__":
    main()
