# Индивидуальный проект.

**Дисциплина:** «Языки программирования»  
**Тема проекта:** «Игра в слова»  
**Выполнил:** студент группы ИТ-2, Окулов А.А.    
**Дата:** 12 июня 2026 г.  
**Город:** Пермь

---

## Постановка задачи

Игра в слова. Дан набор слов. Известно, что эти слова использовались для
игры, в которой очередное слово должно заканчиваться той буквой, на
которую закончилось предыдущее слово. С какого слова начинается игра, не
имеет значения. Если слово оканчивается на «ь», то используется предыдущая
буква. Последнее слово цепочки должно заканчиваться буквой первого слова
цепочки. Входной файл содержит все слова в одной строке, слова записаны
строчными буквами русского алфавита, между словами может быть один или
более пробелов. Требуется выстроить данные слова в цепочку согласно
правилам игры. Достаточно найти одно подходящее решение. Возможен
вариант, что решений не существует. 

Пример 1:
(файл входных данных)
хмель мороз налог лимон запах дым лошадь холм гол молох
(файл выходных данных)
налог гол лошадь дым мороз запах холм молох хмель лимон

Пример 2:
(файл входных данных)
аквариум сирень жатва заноза нож авось тормоз мост
(файл выходных данных)
авось сирень нож жатва аквариум мост тормоз заноза

## Алгоритм решения

Задача сводится к поиску эйлерова цикла в ориентированном графе. Каждая буква рассматривается как вершина графа, а каждое слово — как направленное ребро от первой буквы слова к последней значимой букве. Требование использовать все слова ровно один раз соответствует проходу по всем ребрам графа один раз. Требование замкнуть последнее слово на первое соответствует эйлерову циклу.

### Обоснование структур данных

| Класс | Назначение |
|---|---|
| `Node` | Узел собственного связного списка. Хранит данные и ссылку на следующий узел. |
| `LinkedList` | Собственная динамическая структура. Используется для хранения слов, вершин графа, списков исходящих слов и стеков алгоритма. |
| `Word` | Класс слова. Хранит исходный текст, первую букву и последнюю значимую букву с учетом правила для «ь». |
| `GraphVertex` | Вершина графа: буква, список исходящих слов, входящая и исходящая степени. |
| `WordGraph` | Граф слов, реализованный через собственные списки вершин и списки ребер. |
| `WordChain` | Основной класс задачи: строит цепочку и возвращает результат. |
| `WordChainError` | Собственное исключение для ошибок предметной области. |

Выбор эйлерова цикла позволяет избежать полного перебора перестановок слов. Полный перебор имеет факториальную сложность, тогда как алгоритм Хиерхольцера обрабатывает каждое слово-ребро один раз. При этом все динамические структуры, используемые в основной логике, представлены собственными классами, что соответствует требованиям проекта.

### Порядок работы алгоритма

1. Считать слова из входного файла в собственный связный список.
2. Проверить, что каждое слово непустое и состоит только из строчных букв русского алфавита.
3. Для каждого слова создать ребро графа: первая буква — начало ребра, последняя значимая буква — конец ребра.
4. Проверить баланс степеней: для каждой вершины число входящих ребер должно совпадать с числом исходящих.
5. Если баланс нарушен, сразу вернуть отсутствие решения.
6. Построить эйлеров цикл алгоритмом Хиерхольцера, используя собственные связанные списки как стеки.
7. Проверить, что в результате использованы все слова. Если часть слов не использована, граф несвязен и решения нет.
8. Записать найденную цепочку или сообщение об отсутствии решения в выходной файл.

### Псевдокод

```text
build(words):
    graph = WordGraph()
    for word in words:
        graph.add_word(word)

    if graph has vertex with in_degree != out_degree:
        return no_solution

    push start vertex to vertex_stack
    while vertex_stack is not empty:
        current = top vertex
        if current has outgoing words:
            word = remove first outgoing word
            push word.last vertex to vertex_stack
            push word to word_stack
        else:
            remove current from vertex_stack
            if word_stack is not empty:
                move top word from word_stack to result

    if number of words in result != number of input words:
        return no_solution
    return result
```

### Сложность алгоритма

Пусть `n` — количество слов, `k` — количество различных букв. Формально поиск вершины в собственном списке дает сложность `O(n·k)`. Для русского алфавита `k` не превышает 33, поэтому на практике алгоритм работает линейно по числу слов. Память составляет `O(n + k)`, так как хранятся слова, вершины и рабочие стеки.

### Архитектура программы

| Файл | Ответственность |
|---|---|
| `main.py` | Консольное меню, чтение входного файла, запись выходного файла, обработка пользовательских ошибок. |
| `game_logic.py` | Классы предметной области, собственный связный список, граф слов и алгоритм построения цепочки. |

## Тестирование

Тестирование проводилось вручную через консольное меню программы. Проверялись основные сценарии построения цепочки, граничные случаи, отсутствие решения, некорректный ввод пользователя, ошибки чтения входных файлов и ошибки записи результата.


| № | Сценарий | Ожидаемый результат | Итог |
|---:|---|---|---|
| 1 | Пример 1 из задания | Найдена корректная замкнутая цепочка | Пройден |
| 2 | Пример 2 из задания | Найдена любая корректная цепочка | Пройден |
| 3 | `конь нос сок` | Правильно учтён мягкий знак | Пройден |
| 4 | `ага` | Одно слово замыкается само на себя | Пройден |
| 5 | `аба аба` | Одинаковые слова используются как отдельные элементы | Пройден |
| 6 | `аб вг` | Выведено `Решений не существует.` | Пройден |
| 7 | `Москва`, `кот1`, `кот!`, `cat` | Некорректные слова отклоняются | Пройден |
| 8 | Пустой файл | Программа не падает, сообщает об ошибке | Пройден |
| 9 | Отсутствующий файл | Программа не падает, сообщает об ошибке | Пройден |
| 10 | Неверный путь выходного файла | Ошибка записи обработана | Пройден |
| 11 | Неверный пункт меню | Показана ошибка, меню продолжает работу | Пройден |
| 12 | Файл с расширением `.csv` | Показана ошибка формата файла, меню продолжает работу | Пройден |
| 13 | `ь` | Слово, состоящее только из мягкого знака, отклоняется | Пройден |

Итог ручного тестирования: все 13 проверенных сценариев выполнены успешно.

## Код программы

Ниже приведен полный листинг файлов проекта. Файлы находятся в рабочей папке проекта: `main.py`, `game_logic.py`.

### Листинг файла `game_logic.py`

```python

class WordChainError(Exception):
    pass


_RUSSIAN_LOWER = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"


def _is_russian_lower(text):
    return all(ch in _RUSSIAN_LOWER for ch in text)


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def append(self, data):
        node = Node(data)
        if self.tail:
            self.tail.next = node
        else:
            self.head = node
        self.tail = node
        self._size += 1

    def push_front(self, data):
        node = Node(data)
        node.next = self.head
        self.head = node
        if not self.tail:
            self.tail = node
        self._size += 1

    def pop_front(self):
        if not self.head:
            raise WordChainError("Список пуст")
        data = self.head.data
        self.head = self.head.next
        if not self.head:
            self.tail = None
        self._size -= 1
        return data

    def remove(self, data):
        prev = None
        cur = self.head
        while cur:
            if cur.data == data:
                if prev:
                    prev.next = cur.next
                else:
                    self.head = cur.next
                if cur == self.tail:
                    self.tail = prev
                self._size -= 1
                return
            prev = cur
            cur = cur.next
        raise WordChainError(f"Элемент не найден: {data}")

    def pop(self):
        if not self.tail:
            raise WordChainError("Список пуст")
        data = self.tail.data
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            cur = self.head
            while cur.next != self.tail:
                cur = cur.next
            cur.next = None
            self.tail = cur
        self._size -= 1
        return data

    def is_empty(self):
        return self._size == 0

    def __len__(self):
        return self._size

    def __iter__(self):
        cur = self.head
        while cur:
            yield cur.data
            cur = cur.next


class Word:
    def __init__(self, text: str):
        if not text or not _is_russian_lower(text):
            raise WordChainError(f"Некорректное слово: {text}")
        self.text = text
        self.first = text[0]
        if text[-1] == "ь":
            if len(text) == 1:
                raise WordChainError(
                    f"Слово не может состоять только из 'ь': {text}")
            self.last = text[-2]
        else:
            self.last = text[-1]

    def __str__(self):
        return self.text


class GraphVertex:
    def __init__(self, letter):
        self.letter = letter
        self.outgoing_words = LinkedList()
        self.in_degree = 0
        self.out_degree = 0


class WordGraph:
    def __init__(self):
        self.vertices = LinkedList()

    def get_or_create_vertex(self, letter):
        vertex = self.find_vertex(letter)
        if vertex is None:
            vertex = GraphVertex(letter)
            self.vertices.append(vertex)
        return vertex

    def find_vertex(self, letter):
        for vertex in self.vertices:
            if vertex.letter == letter:
                return vertex
        return None

    def add_word(self, word):
        start_vertex = self.get_or_create_vertex(word.first)
        end_vertex = self.get_or_create_vertex(word.last)
        start_vertex.outgoing_words.append(word)
        start_vertex.out_degree += 1
        end_vertex.in_degree += 1

    def has_balanced_degrees(self):
        for vertex in self.vertices:
            if vertex.in_degree != vertex.out_degree:
                return False
        return True


class WordChain:
    def __init__(self, words):
        if not words:
            raise WordChainError("Список слов пуст")
        self.words = LinkedList()
        for text in words:
            self.words.append(Word(text))
        self._chain = None

    def build(self) -> bool:
        self._chain = None

        graph = WordGraph()
        for word in self.words:
            graph.add_word(word)

        if not graph.has_balanced_degrees():
            return False

        start_vertex = graph.find_vertex(self.words.head.data.first)
        vertex_stack = LinkedList()
        word_stack = LinkedList()
        result = LinkedList()
        vertex_stack.push_front(start_vertex)

        # Алгоритм Хиерхольцера строит замкнутую цепочку, удаляя каждое
        # слово-ребро из графа ровно один раз.
        while not vertex_stack.is_empty():
            vertex = vertex_stack.head.data
            if not vertex.outgoing_words.is_empty():
                word = vertex.outgoing_words.pop_front()
                next_vertex = graph.find_vertex(word.last)
                vertex_stack.push_front(next_vertex)
                word_stack.push_front(word)
            else:
                vertex_stack.pop_front()
                if not word_stack.is_empty():
                    result.push_front(word_stack.pop_front())

        if len(result) != len(self.words):
            return False

        self._chain = result
        return True

    def get_chain(self):
        if self._chain is None:
            return None
        result = LinkedList()
        for word in self._chain:
            result.append(str(word))
        return result
```

### Листинг файла `main.py`

```python
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
```
