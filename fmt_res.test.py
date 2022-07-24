from typing import Any

import dagster
from dagster import (
    AssetMaterialization,
    DynamicOut,
    DynamicOutput,
    Field,
    In,
    Nothing,
    OpExecutionContext,
    Out,
    Output,
    op,
)


@op(
    ins={
        "a": In(description=""),
        "b": In(dagster_type=Any, description=""),
        "run_config": In(
            dagster_type=Nothing,
            description="Placeholder dependency for orchestration with other ops.",
        ),
    },
    config_schema={
        "c_field": Field(
            config=dagster.Any, description="", is_required=True, default_value=None
        )
    },
    out={
        "maybe_out_0": Out(dagster_type=int, description="", is_required=True),
        "maybe_out_1": Out(dagster_type=int, description="", is_required=True),
    },
    required_resource_keys={"redshift"},
)
def some_op(context: OpExecutionContext, a: str, b):
    """hello there"""

    c = context.op_config["c_field"]
    context.resources.redshift(a, b, c)

    return 1, 2


@op(
    ins={
        "a": In(description=""),
        "b": In(dagster_type=Any, description=""),
        "run_config": In(
            dagster_type=Nothing,
            description="Placeholder dependency for orchestration with other ops.",
        ),
    },
    config_schema={
        "c_field": Field(
            config=dagster.Any, description="", is_required=True, default_value=None
        )
    },
    out={"op_output": Out(dagster_type=Any, description="", is_required=True)},
    required_resource_keys={"redshift"},
)
def some_op(context: OpExecutionContext, a: str, b):
    """hello there"""

    c = context.op_config["c_field"]
    context.resources.redshift(a, b, c)

    return 1


@op(
    ins={
        "a": In(description=""),
        "b": In(dagster_type=Any, description=""),
        "run_config": In(
            dagster_type=Nothing,
            description="Placeholder dependency for orchestration with other ops.",
        ),
    },
    config_schema={
        "c_field": Field(
            config=dagster.Any, description="", is_required=True, default_value=None
        )
    },
    out={"a": Out(dagster_type=Any, description="", is_required=True)},
    required_resource_keys={"some_resource"},
)
def some_op1(context: OpExecutionContext, a: str, b):
    """Op description"""

    context.log.info("hello")

    c = context.op_config["c_field"]
    context.resources.some_resource(a, b, c)

    return Output(1, output_name="a")


@op(ins={"a": In()})
def some_op2(context, a: str, b):
    c = context.op_config["c_field"]
    c = context.op_config["d_field"]
    context.resources.redshift(a, b, c)

    yield AssetMaterialization()
    yield Output(1, output_name="a")
    yield Output(2, output_name="b")


@op(
    config_schema={
        "c_field": Field(
            config=dagster.Any, description="", is_required=True, default_value=None
        )
    },
    out={"a": DynamicOut(dagster_type=Any, description="", is_required=True)},
    required_resource_keys={"redshift"},
)
def some_op2(context: OpExecutionContext):
    """Op description"""

    c = context.op_config["c_field"]
    context.resources.redshift(c)

    for a in [1, 2, 3]:
        yield DynamicOutput(1, output_name="a")


def some_other_func():
    ...
