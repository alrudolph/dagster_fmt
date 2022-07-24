Run:

```bash
python dagster_fmt ./path/to/file.py
```

## Example

Source:

```py
@op
def some_op(context, a: str, b):
    c = context.op_config["c_field"]
    context.resources.some_resource.method(a, b, c)

    return Output(1, output_name="a")
```

After formatting:

```py
@op(
    ins={
        "a": In(description=""),
        "b": In(description=""),
        "run_after": In(dagster_type=Nothing),
    },
    config_schema={"c_field": Field(Any, description="")},
    out={"a": Out(description="", is_required=True)},
    required_resource_keys={"some_resource"},
)
def some_op(context: OpExecutionContext, a: str, b):
    c = context.op_config["c_field"]
    context.resources.some_resource.method(a, b, c)

    return Output(1, output_name="a")
```
