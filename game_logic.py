
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
