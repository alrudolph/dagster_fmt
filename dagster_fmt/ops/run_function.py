import ast
from typing import Optional, Any
from shared.insert import InsertText


def add_context_type_annotation(
    function_node: ast.FunctionDef, type_name: str = "OpExecutionContext"
) -> Optional[Any]:
    """Add the type annotation to optional context param in the op's execution function.

    For example,

    >>> @op
    >>> def my_op(context: OpExecutionContext):
    ...    ...

    Params
    ------
    function_node: ast.FunctionDef
        AST node for the op execution function

    Returns
    -------
    dagster_import_name: Optional[Any]
        If an annotation is added, the name of the module and name of the class to
        add an import for. In this case: ('dagster', 'OpExecutionContext')
    """
    if len(function_node.args.args) == 0:
        return

    possible_context_arg = function_node.args.args[0]

    if (
        possible_context_arg.arg == "context"
        and possible_context_arg.annotation is None
    ):
        return InsertText.after_node(f": {type_name}", possible_context_arg), (
            "dagster",
            type_name,
        )


def type_out_resources():
    """
    convert
    -------

    context.resources.redshift(a, b, c)

    to
    --

    redshift: Any = context.resources.redshift
    redshift(a, b c)
    """


def destructor_context():
    """
    convert
    -------

    context.op_config["a"]

    to
    --

    a = context.op_config["a"]
    a

    """


def add_op_docstring():
    ...
