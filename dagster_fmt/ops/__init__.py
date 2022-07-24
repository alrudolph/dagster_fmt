import ast
from shared.read_context import get_config_field_names, get_resource_names
from typing import List

from shared.insert import InsertText


def is_op_node(node) -> bool:
    # the hastattr makes sure not to include ops with some
    # config already
    return isinstance(node, ast.FunctionDef) and any(
        [hasattr(n, "id") and "op" == n.id for n in node.decorator_list]
    )


def get_op_decorator_node(node: ast.FunctionDef):

    for decorator in node.decorator_list:

        if decorator.id == "op":
            return decorator


def create_required_resource_keys(resources: List[str]) -> str:
    if len(resources) == 0:
        return "", False

    return 'required_resource_keys={"' + '","'.join(resources) + '"},', True


def create_op_config(config_names: List[str]) -> str:
    if len(config_names) == 0:
        return "", False

    return (
        "config_schema={"
        + ",".join([f'"{c}": Field(Any, description="")' for c in config_names])
        + "},",
        True,
    )


def get_op_ins(node: ast.FunctionDef) -> List[str]:
    output = []

    for arg in node.args.args:

        if arg.arg != "context":
            output.append(arg.arg)

    return output


def create_op_ins(ins: List[str]):
    if len(ins) == 0:
        return "", False

    return (
        "ins={"
        + ",".join([f'"{c}": In(description="")' for c in ins])
        + ',"run_after": In(dagster_type=Nothing)'
        + "},",
        True,
    )


def get_op_out(node: ast.FunctionDef):
    output_type = {"Output": "Out", "DynamicOutput": "DynamicOut"}
    output = []
    for return_node in ast.walk(node):
        ot = "Output"
        name = "op_output"

        if not isinstance(return_node, ast.Yield) and not isinstance(
            return_node, ast.Return
        ):
            continue

        if isinstance(return_node.value, ast.Call):
            ot = return_node.value.func.id

            if ot not in output_type.keys():
                continue

            name = [k for k in return_node.value.keywords if k.arg == "output_name"][
                0
            ].value.value
        elif not isinstance(return_node.value, ast.Constant):
            continue

        output.append({"name": name, "type": output_type[ot]})

    return output


def create_op_out(out):
    if len(out) == 0:
        return "", False

    return (
        "out={"
        + ",".join(
            [
                '"' + c["name"] + f'" : {c["type"]}(description="", is_required=True)'
                for c in out
            ]
        )
        + "},",
        True,
    )


def add_op_decorator(node: ast.FunctionDef):
    output = []

    #
    # get existing config
    #

    decorator_node = get_op_decorator_node(node)

    i_str, include = create_op_ins(get_op_ins(node))
    if include:
        output.append(InsertText.after_node(i_str, decorator_node))

    c_str, include = create_op_config(get_config_field_names("op_config", node))
    if include:
        output.append(InsertText.after_node(c_str, decorator_node))

    o_str, include = create_op_out(get_op_out(node))
    if include:
        output.append(InsertText.after_node(o_str, decorator_node))

    r_str, include = create_required_resource_keys(get_resource_names(node))
    if include:
        output.append(InsertText.after_node(r_str, decorator_node))

    return [
        InsertText("(", decorator_node.lineno - 1, decorator_node.end_col_offset),
        *output,
        InsertText(")", decorator_node.lineno - 1, decorator_node.end_col_offset),
    ]
