from dagster import (
    op,
    In,
    Output,
    Field,
    Out,
    Any,
    Nothing,
    DynamicOutput,
    DynamicOut,
    AssetMaterialization,
    OpExecutionContext,
)


@op
def some_op(context, a: str, b):
    """ """
    c = context.op_config["c_field"]
    context.resources.redshift(a, b, c)

    return 1


@op
def some_op1(context, a: str, b):
    c = context.op_config["c_field"]
    context.resources.redshift(a, b, c)

    return Output(1, output_name="a")


@op(ins={"a": In()})
def some_op2(context, a: str, b):
    c = context.op_config["c_field"]
    c = context.op_config["d_field"]
    context.resources.redshift(a, b, c)

    yield AssetMaterialization()
    yield Output(1, output_name="a")
    yield Output(2, output_name="b")


@op
def some_op2(context):
    c = context.op_config["c_field"]
    context.resources.redshift(c)

    for a in [1, 2, 3]:
        yield DynamicOutput(1, output_name="a")


def some_other_func():
    ...
