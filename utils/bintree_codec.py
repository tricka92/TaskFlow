"""ЛР21, Раздел 2, задание 3: serialize()/deserialize() для бинарного дерева.
Без pickle и json - формат придумываем сами.
"""
import struct
from dataclasses import dataclass

MAGIC = b"BT1"        # подпись: по ней понимаем, что файл именно нашего формата
EMPTY = 0             # маркер "пусто"
NODE = 1              # маркер "тут узел"


@dataclass
class TreeNode:
    value: int
    left: "TreeNode | None" = None
    right: "TreeNode | None" = None


def serialize(root) -> bytes:
    out = bytearray(MAGIC)            # начинаем с заголовка

    def walk(node):
        if node is None:
            out.append(EMPTY)         # пишем один байт 0
            return
        out.append(NODE)              # байт 1: "дальше идёт узел"
        out.extend(struct.pack(">i", node.value))  # 4 байта: число
        walk(node.left)               # сначала левое поддерево
        walk(node.right)              # потом правое

    walk(root)
    return bytes(out)


def deserialize(data: bytes):
    if data[:3] != MAGIC:
        raise ValueError("Это не наш формат: неверный заголовок")
    pos = 3                           # указатель: сколько байт уже прочитали

    def read():
        nonlocal pos
        if pos >= len(data):
            raise ValueError("Данные оборвались раньше времени")
        marker = data[pos]
        pos += 1
        if marker == EMPTY:
            return None
        if marker != NODE:
            raise ValueError(f"Неизвестный маркер: {marker}")
        if pos + 4 > len(data):
            raise ValueError("Данные оборвались внутри числа")
        (value,) = struct.unpack_from(">i", data, pos)
        pos += 4
        node = TreeNode(value)
        node.left = read()            # ровно в том же порядке, как писали
        node.right = read()
        return node

    root = read()
    if pos != len(data):
        raise ValueError("После дерева остались лишние байты")
    return root


def save_tree(root, path) -> None:
    with open(path, "wb") as f:
        f.write(serialize(root))


def load_tree(path):
    with open(path, "rb") as f:
        return deserialize(f.read())
