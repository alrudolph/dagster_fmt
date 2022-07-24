import ast

# import astpretty

from ops import is_op_node, add_op_decorator
from ops.run_function import add_context_type_annotation
from shared.insert import write_file
import sys

if __name__ == "__main__":
    file_name = sys.argv[1]

    with open(file_name, "r") as file:
        file_contents = file.read()

    tree = ast.parse(file_contents)

    inserts = []

    for node in ast.walk(tree):

        if not is_op_node(node):
            continue

        # astpretty.pprint(node)
        # build_op(node)

        output = add_context_type_annotation(node)

        if output is not None:
            inserts.append(output[0])

        inserts.extend(add_op_decorator(node))

    write_file(file_name, file_contents, inserts)
