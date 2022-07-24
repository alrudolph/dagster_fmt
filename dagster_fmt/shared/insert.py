from collections import defaultdict
from typing import List


class InsertText:
    def __init__(self, text: str, lineno: int, col_offset: int):
        self.text = text
        self.lineno = lineno
        self.col_offset = col_offset

    @classmethod
    def after_node(cls, text, node):
        return cls(text, node.lineno - 1, node.end_col_offset)


def grouped(list, key):
    output = defaultdict(lambda: [])

    for item in list:
        output[key(item)].append(item)

    return output


def write_file(file_path: str, starting_text: str, inserts=List[InsertText]):
    lines = starting_text.splitlines()

    for lineno, line_inserts in grouped(inserts, key=lambda x: x.lineno).items():

        line_acc = 0

        for insert in sorted(line_inserts, key=lambda x: x.col_offset):
            idx = line_acc + insert.col_offset
            lines[lineno] = lines[lineno][:idx] + insert.text + lines[lineno][idx:]
            line_acc += len(insert.text)

    with open(file_path, "w") as out_file:
        out_file.write("\n".join(lines))
