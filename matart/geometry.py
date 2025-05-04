"""
geometry.py

Defines geometric primitives and transformation API.
"""

from typing import NamedTuple, List

class Shape(NamedTuple):
    # Basic placeholder; extent and position data will go here.
    name: str
    params: dict

def generate_next(shape: Shape, rule: str, **kwargs) -> Shape:
    """
    Given a shape and a rule identifier, generate the next shape.
    For v1, rules stub out behavior.
    """
    # TODO: implement real math for each rule
    return Shape(name=shape.name, params=shape.params)

if __name__ == "__main__":
    # Simple CLI smoke test
    s = Shape(name="square", params={"size": 100})
    next_s = generate_next(s, rule="scale_by_diagonal")
    print(f"Generated shape: {next_s}")
