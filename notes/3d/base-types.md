# Manim Base Mobject Types Reference
> Manim v0.20.1

These are the foundational classes everything else inherits from.

---

## `Mobject`
The base class for all mathematical objects in Manim. Manages points, submobjects, color, transformations, and updaters.
```python
Mobject(
    color: ParsableManimColor | list[ParsableManimColor] = WHITE,
    name: str | None = None,
    dim: int = 3,
    target=None,
    z_index: float = 0,
)
```

**Key methods:**
| Method | Description |
|---|---|
| `add(*mobjects)` | Add mobjects as submobjects |
| `remove(*mobjects)` | Remove submobjects |
| `shift(*vectors)` | Translate by the sum of vectors |
| `scale(factor, about_point=ORIGIN)` | Scale uniformly |
| `rotate(angle, axis=OUT, about_point=None)` | Rotate |
| `move_to(point_or_mobject)` | Move center to a point or another mobject's center |
| `next_to(mobject, direction, buff)` | Position adjacent to another mobject |
| `to_edge(edge, buff)` | Move to the edge of the frame |
| `to_corner(corner, buff)` | Move to a corner of the frame |
| `align_to(mobject_or_point, direction)` | Align edge with another mobject |
| `set_color(color)` | Set color |
| `set_opacity(alpha)` | Set opacity |
| `copy()` | Return a deep copy |
| `save_state()` | Save current state for later `Restore` |
| `restore()` | Restore to the last saved state |
| `generate_target()` | Populate `.target` with a copy for `MoveToTarget` |
| `add_updater(func, index=None)` | Add a per-frame updater function `func(mob)` or `func(mob, dt)` |
| `remove_updater(func)` | Remove a specific updater |
| `clear_updaters()` | Remove all updaters |
| `get_center()` | Return the center point as a numpy array |
| `get_width()` / `get_height()` | Return bounding box dimensions |
| `get_left()` / `get_right()` / `get_top()` / `get_bottom()` | Return edge points |
| `get_bounding_box_point(direction)` | Return an arbitrary bounding box point |
| `set_x(x)` / `set_y(y)` / `set_z(z)` | Set individual coordinates |
| `flip(axis=UP)` | Flip across an axis |
| `surround(mobject, buff)` | Scale and position to surround another mobject |
| `put_start_and_end_on(start, end)` | Stretch and position between two points |
| `become(mobject)` | Replace this mobject's points/style with another's |
| `match_color(mobject)` | Copy the color of another mobject |
| `match_height(mobject)` / `match_width(mobject)` | Match dimensions |
| `.animate` | Property that returns an `_AnimationBuilder` — chain methods and pass to `play()` |

---

## `VMobject`
Extends `Mobject`. The base class for all vectorized (Bézier-curve-based) mobjects — anything with a stroke and fill.
```python
VMobject(
    fill_color: ParsableManimColor | None = None,
    fill_opacity: float = 0.0,
    stroke_color: ParsableManimColor | None = None,
    stroke_opacity: float = 1.0,
    stroke_width: float = DEFAULT_STROKE_WIDTH,
    background_stroke_color: ParsableManimColor | None = BLACK,
    background_stroke_opacity: float = 1.0,
    background_stroke_width: float = 0,
    sheen_factor: float = 0.0,
    joint_type: LineJointType | None = None,
    sheen_direction: Vector3DLike = UL,
    close_new_points: bool = False,
    **kwargs,
)
```

**Key additional methods:**
| Method | Description |
|---|---|
| `set_fill(color, opacity)` | Set fill color and/or opacity |
| `set_stroke(color, width, opacity)` | Set stroke color, width, and/or opacity |
| `set_style(...)` | Set multiple style properties at once |
| `get_fill_color()` / `get_stroke_color()` | Get current colors |
| `set_points_as_corners(*points)` | Set path as straight line segments through points |
| `set_points_smoothly(*points)` | Set path as a smooth curve through points |
| `make_smooth()` | Smooth out the existing path |
| `apply_function(func)` | Apply a pointwise function to all points |
| `get_start()` / `get_end()` | Return the first/last point of the path |
| `get_midpoint()` | Return the midpoint of the path |
| `point_from_proportion(alpha)` | Return a point at a given proportion along the path |
| `reverse_direction()` | Reverse the winding direction of the path |
| `add_line_to(point)` | Extend the path to a point with a straight line |
| `add_smooth_curve_to(point)` | Extend with a smooth curve |

---

## `VGroup`
A group of `VMobject` instances that can be transformed together. Supports `+`, `+=`, `-`, `-=` operators.
```python
VGroup(*vmobjects: VMobject, **kwargs)
```

**Key additional methods:**
| Method | Description |
|---|---|
| `arrange(direction=RIGHT, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER, center=True)` | Arrange submobjects in a line |
| `arrange_in_grid(rows, cols, buff, ...)` | Arrange submobjects in a grid |

---

## `Group`
Like `VGroup` but accepts any `Mobject` (not restricted to `VMobject`). Used when mixing VMobjects with non-vectorized objects like `ImageMobject`.
```python
Group(*mobjects: Mobject, **kwargs)
```
