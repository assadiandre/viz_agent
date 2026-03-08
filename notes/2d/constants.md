# Manim Constants Reference
> Manim v0.20.1

---

## Directions

| Constant | Value | Description |
|---|---|---|
| `ORIGIN` | `(0, 0, 0)` | The center of the coordinate system |
| `UP` | `(0, 1, 0)` | One unit in the positive Y direction |
| `DOWN` | `(0, -1, 0)` | One unit in the negative Y direction |
| `RIGHT` | `(1, 0, 0)` | One unit in the positive X direction |
| `LEFT` | `(-1, 0, 0)` | One unit in the negative X direction |
| `OUT` | `(0, 0, 1)` | One unit in the positive Z direction (toward viewer) |
| `IN` | `(0, 0, -1)` | One unit in the negative Z direction (away from viewer) |

### Diagonal shorthands

| Constant | Equivalent | Description |
|---|---|---|
| `UL` | `UP + LEFT` | Upper-left |
| `UR` | `UP + RIGHT` | Upper-right |
| `DL` | `DOWN + LEFT` | Lower-left |
| `DR` | `DOWN + RIGHT` | Lower-right |

Directions can be scaled to control distance:
```python
obj.move_to(2 * UP)
obj.shift(0.5 * LEFT)
obj.next_to(other, UR, buff=0.2)
```

---

## Axes

| Constant | Value | Description |
|---|---|---|
| `X_AXIS` | `(1, 0, 0)` | Unit vector along X |
| `Y_AXIS` | `(0, 1, 0)` | Unit vector along Y |
| `Z_AXIS` | `(0, 0, 1)` | Unit vector along Z |

Mainly used as the `axis=` argument for rotations:
```python
obj.rotate(PI / 4, axis=Z_AXIS)
```

---

## Buffers (spacing)

| Constant | Value | Description |
|---|---|---|
| `SMALL_BUFF` | `0.1` | Tight spacing |
| `MED_SMALL_BUFF` | `0.25` | Default mobject-to-mobject gap |
| `MED_LARGE_BUFF` | `0.5` | Default mobject-to-edge gap |
| `LARGE_BUFF` | `1.0` | Wide spacing |

Used with `buff=` in layout methods:
```python
obj.next_to(other, RIGHT, buff=SMALL_BUFF)
obj.to_edge(UP, buff=MED_LARGE_BUFF)
```

---

## Math Constants

| Constant | Value | Description |
|---|---|---|
| `PI` | `3.14159…` | `numpy.pi` |
| `TAU` | `6.28318…` | Full turn in radians (`2 * PI`) |
| `DEGREES` | `TAU / 360` | Converts degrees to radians |

```python
obj.rotate(90 * DEGREES)   # rotate 90 degrees
obj.rotate(TAU / 4)        # same thing
```

---

## Default Sizes

| Constant | Value | Description |
|---|---|---|
| `DEFAULT_DOT_RADIUS` | `0.08` | Radius of a `Dot` |
| `DEFAULT_SMALL_DOT_RADIUS` | `0.04` | Radius of a `SmallDot` |
| `DEFAULT_DASH_LENGTH` | `0.05` | Length of each dash in `DashedLine` |
| `DEFAULT_ARROW_TIP_LENGTH` | `0.35` | Length of an arrow tip |
| `DEFAULT_STROKE_WIDTH` | `4` | Default stroke width for VMobjects |
| `DEFAULT_FONT_SIZE` | `48` | Default font size for `Text` / `Tex` |

---

## Font Styles (for `Text`)

| Constant | Description |
|---|---|
| `NORMAL` | Regular weight, upright |
| `BOLD` | Bold weight |
| `ITALIC` | Italic style |
| `OBLIQUE` | Oblique style (slanted, not true italic) |
| `THIN` | Thinnest weight |
| `ULTRALIGHT` | Very light weight |
| `LIGHT` | Light weight |
| `SEMILIGHT` | Semi-light weight |
| `BOOK` | Book weight |
| `MEDIUM` | Medium weight |
| `SEMIBOLD` | Semi-bold weight |
| `ULTRABOLD` | Extra bold weight |
| `HEAVY` | Heavy weight |
| `ULTRAHEAVY` | Heaviest weight |

```python
Text("Hello", weight=BOLD, slant=ITALIC)
```
