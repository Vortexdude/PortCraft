import ast
from functools import wraps


def add_missing_attribute(func):
    @wraps(func)
    def wrapper(self, kwargs):
        response = func(self, kwargs)
        ast.fix_missing_locations(response)
        return response
    return wrapper


def dict_to_ast_node(parsed_data: dict):
    if isinstance(parsed_data, dict):
        return ast.Dict(
            keys=[ast.Constant(key) for key in parsed_data.keys()],
            values=[dict_to_ast_node(value) for value in parsed_data.values()]
        )
    elif isinstance(parsed_data, str) or isinstance(parsed_data, bool):
        return ast.Constant(parsed_data)
    else:
        raise ValueError(f"Unsupported Type {type(parsed_data)}")


def ast_set_attribute(instance, attribute, value):
    if not instance or not attribute or not value:
        raise Exception("Please specify (instance, attribute, value)")

    return ast.Assign(
        targets=[
            ast.Attribute(
                value=ast.Name(id=instance, ctx=ast.Load()),
                attr=attribute,
                ctx=ast.Store()
            )
        ],
        value=dict_to_ast_node(value)
    )


def is_callable_name(node) -> bool:
    if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
        return True
    return False
