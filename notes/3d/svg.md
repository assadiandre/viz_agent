# Manim SVG Reference
> Manim v0.20.1

---

## `SVGMobject`
Imports an SVG file and converts it to a `VMobject` (vectorized, fully animatable). Each SVG element becomes a submobject.
```python
SVGMobject(
    file_name: str | os.PathLike | None = None,
    should_center: bool = True,
    height: float | None = 2,
    width: float | None = None,
    color: ParsableManimColor | None = None,
    opacity: float | None = None,
    fill_color: ParsableManimColor | None = None,
    fill_opacity: float | None = None,
    stroke_color: ParsableManimColor | None = None,
    stroke_opacity: float | None = None,
    stroke_width: float | None = None,
    svg_default: dict | None = None,
    path_string_config: dict | None = None,
    use_svg_cache: bool = True,
    **kwargs,
)
```

**Parameters:**
- `file_name` — path to the `.svg` file (searched in the asset directories)
- `height` / `width` — scale the imported SVG to a target height or width; if both are `None`, it is imported at its native size
- `color` — override both fill and stroke colors for all elements; `None` preserves the SVG's own colors
- `opacity` — override both fill and stroke opacities; `None` preserves the SVG's own values
- `svg_default` — dict of fallback style values applied to elements that don't specify their own style
- `use_svg_cache` — cache the parsed result so repeated imports of the same file are fast

**Usage:**
```python
logo = SVGMobject("logo.svg")
logo = SVGMobject("logo.svg", height=3, color=WHITE)

# Access individual elements as submobjects
logo[0].set_color(RED)
```

**Notes:**
- SVG `<text>` elements are not supported and will be skipped with a warning
- The SVG is flipped vertically on import to match Manim's coordinate system (y-up)
- Repeated calls with the same file and settings reuse a cached copy unless `use_svg_cache=False`

---

## `VMobjectFromSVGPath`
A `VMobject` representing a single parsed SVG `<path>` element. Created automatically by `SVGMobject` — rarely used directly.
```python
VMobjectFromSVGPath(
    path_obj: se.Path,
    long_lines: bool = False,
    should_subdivide_sharp_curves: bool = False,
    should_remove_null_curves: bool = False,
    **kwargs,
)
```
