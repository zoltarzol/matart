# geometry.py
# 
# Defines geometric primitives, transformation rules, and presets for generative art.

import math
from typing import NamedTuple, List, Dict

class Shape(NamedTuple):
    """
    A geometric shape with a name and parameters dictionary.
    params may include:
      - x, y: center coordinates
      - size: scale or radius
      - angle: rotation in degrees
      - hue: color hue (0–360)
      - For line: x1, y1, x2, y2
    """
    name: str
    params: Dict[str, float]

# --- Primitive Rule Implementations ---------------------------------------------------

def rule_scale_by_diagonal(shape: Shape, **kwargs) -> Shape:
    size = shape.params.get("size", 1)
    diag = size * math.sqrt(2)
    x = shape.params.get("x", 0) + (size + diag) / 2
    y = shape.params.get("y", 0)
    return Shape(
        name=shape.name,
        params={"x": x, "y": y, "size": diag,
                "angle": shape.params.get("angle", 0),
                "hue": shape.params.get("hue", 0)}
    )

def rule_uniform_scale(shape: Shape, **kwargs) -> Shape:
    factor = kwargs.get("scale_factor", 1.1)
    prev = shape.params.get("size", 1)
    new_size = prev * factor
    x = shape.params.get("x", 0) + (prev + new_size) / 2
    y = shape.params.get("y", 0)
    return Shape(
        name=shape.name,
        params={"x": x, "y": y, "size": new_size,
                "angle": shape.params.get("angle", 0),
                "hue": shape.params.get("hue", 0)}
    )

def rule_rotate(shape: Shape, **kwargs) -> Shape:
    inc = kwargs.get("rotation_increment", 30)
    angle = (shape.params.get("angle", 0) + inc) % 360
    return Shape(
        name=shape.name,
        params={"x": shape.params.get("x", 0),
                "y": shape.params.get("y", 0),
                "size": shape.params.get("size", 1),
                "angle": angle,
                "hue": shape.params.get("hue", 0)}
    )

def rule_translate(shape: Shape, **kwargs) -> Shape:
    dx = kwargs.get("translate_dx", shape.params.get("size", 1))
    dy = kwargs.get("translate_dy", 0)
    return Shape(
        name=shape.name,
        params={"x": shape.params.get("x", 0) + dx,
                "y": shape.params.get("y", 0) + dy,
                "size": shape.params.get("size", 1),
                "angle": shape.params.get("angle", 0),
                "hue": shape.params.get("hue", 0)}
    )

def rule_hue_shift(shape: Shape, **kwargs) -> Shape:
    delta = kwargs.get("hue_shift", 10)
    hue = (shape.params.get("hue", 0) + delta) % 360
    return Shape(
        name=shape.name,
        params={"x": shape.params.get("x", 0),
                "y": shape.params.get("y", 0),
                "size": shape.params.get("size", 1),
                "angle": shape.params.get("angle", 0),
                "hue": hue}
    )

# --- Preset Generators --------------------------------------------------------------

def generate_fibonacci_spiral(start: Shape, iterations: int = 5, **kwargs) -> List[Shape]:
    # Fibonacci sequence of sizes
    fib = [start.params.get("size", 1)] * 2
    for _ in range(2, iterations):
        fib.append(fib[-1] + fib[-2])
    seq: List[Shape] = []
    # Four direction cycle: right, up, left, down
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    x, y = start.params.get("x", 0), start.params.get("y", 0)
    for i, size in enumerate(fib[:iterations]):
        dx, dy = dirs[i % 4]
        if i > 0:
            prev = fib[i - 1]
            x += dx * (prev + size) / 2
            y += dy * (prev + size) / 2
        seq.append(Shape(
            name=start.name,
            params={"x": x, "y": y, "size": size,
                    "angle": (i % 4) * 90,
                    "hue": start.params.get("hue", 0)}
        ))
    return seq


def generate_koch_snowflake(start: Shape, iterations: int = 3, **kwargs) -> List[Shape]:
    # Simple placeholder: returns initial triangle as 3 lines
    size = start.params.get("size", 1)
    # Equilateral triangle vertices
    p1 = (0.0, 0.0)
    p2 = (size, 0.0)
    p3 = (size / 2, size * math.sin(math.radians(60)))
    shapes: List[Shape] = []
    for (a, b) in ((p1, p2), (p2, p3), (p3, p1)):
        shapes.append(Shape(
            name="line",
            params={"x1": a[0], "y1": a[1], "x2": b[0], "y2": b[1],
                    "hue": start.params.get("hue", 0)}
        ))
    return shapes

# --- Rule & Preset Registry --------------------------------------------------------

PRIMITIVE_RULES = {
    "scale_by_diagonal": rule_scale_by_diagonal,
    "uniform_scale": rule_uniform_scale,
    "rotate": rule_rotate,
    "translate": rule_translate,
    "hue_shift": rule_hue_shift,
}

PRESETS = {
    "fibonacci_spiral": generate_fibonacci_spiral,
    "koch_snowflake": generate_koch_snowflake,
}

# Combined keys for UI
RULES = {**PRIMITIVE_RULES, **PRESETS}

# --- Sequence Generation ----------------------------------------------------------

def generate_sequence(
    start: Shape,
    rule_key: str,
    iterations: int = 10,
    **kwargs
) -> List[Shape]:
    """
    Generate shapes by either applying a primitive rule iteratively,
    or by invoking a preset generator.
    """
    if rule_key in PRESETS:
        return PRESETS[rule_key](start, iterations=iterations, **kwargs)
    if rule_key not in PRIMITIVE_RULES:
        raise ValueError(f"Unknown rule or preset: {rule_key}")
    seq: List[Shape] = [start]
    for _ in range(iterations - 1):
        seq.append(PRIMITIVE_RULES[rule_key](seq[-1], **kwargs))
    return seq

if __name__ == "__main__":
    # CLI demo
    s = Shape(name="square", params={"x": 0, "y": 0, "size": 100, "angle": 0, "hue": 0})
    for key in RULES:
        seq = generate_sequence(s, key, iterations=5)
        print(f"Preset/Rule: {key}, generated {len(seq)} shapes")
