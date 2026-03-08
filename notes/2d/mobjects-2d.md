# Manim 2D Mobjects Reference
> Manim v0.20.1

## Geometry — Arcs & Circles

### `Arc`
A circular arc defined by a radius, start angle, and sweep angle.
```python
Arc(
    radius: float | None = 1.0,
    start_angle: float = 0,
    angle: float = TAU / 4,
    num_components: int = 9,
    arc_center: Point3DLike = ORIGIN,
    **kwargs,
)
```

### `Circle`
A full circle.
```python
Circle(
    radius: float | None = None,
    color: ParsableManimColor = RED,
    **kwargs,
)
```

### `Dot`
A small filled circle, typically used to mark a point.
```python
Dot(
    point: Point3DLike = ORIGIN,
    radius: float = DEFAULT_DOT_RADIUS,
    stroke_width: float = 0,
    fill_opacity: float = 1.0,
    color: ParsableManimColor = WHITE,
    **kwargs,
)
```

### `AnnotationDot`
A larger, outlined dot styled for annotations.
```python
AnnotationDot(
    radius: float = DEFAULT_DOT_RADIUS * 1.3,
    stroke_width: float = 5,
    stroke_color: ParsableManimColor = WHITE,
    fill_color: ParsableManimColor = BLUE,
    **kwargs,
)
```

### `LabeledDot`
A dot with a text or LaTeX label inside it.
```python
LabeledDot(
    label: str | Tex | MathTex | Text,
    radius: float | None = None,
    **kwargs,
)
```

### `Ellipse`
An ellipse with configurable width and height.
```python
Ellipse(
    width: float = 2,
    height: float = 1,
    **kwargs,
)
```

### `AnnularSector`
A pie-slice-shaped region cut from a ring (annulus).
```python
AnnularSector(
    inner_radius: float = 1,
    outer_radius: float = 2,
    angle: float = TAU / 4,
    start_angle: float = 0,
    **kwargs,
)
```

### `Sector`
A pie-slice region of a circle (filled arc from center).
```python
Sector(
    radius: float = 1,
    **kwargs,
)
```

### `Annulus`
A ring shape — the region between two concentric circles.
```python
Annulus(
    inner_radius: float = 1,
    outer_radius: float = 2,
    fill_opacity: float = 1,
    stroke_width: float = 0,
    color: ParsableManimColor = WHITE,
    mark_paths_closed: bool = False,
    **kwargs,
)
```

### `ArcBetweenPoints`
An arc connecting two specific points with a given sweep angle.
```python
ArcBetweenPoints(
    start: Point3DLike,
    end: Point3DLike,
    angle: float = TAU / 4,
    **kwargs,
)
```

### `CurvedArrow`
An arc with an arrowhead at the end.
```python
CurvedArrow(
    start_point: Point3DLike,
    end_point: Point3DLike,
    **kwargs,
)
```

### `CurvedDoubleArrow`
An arc with arrowheads at both ends.
```python
CurvedDoubleArrow(
    start_point: Point3DLike,
    end_point: Point3DLike,
    **kwargs,
)
```

### `CubicBezier`
A cubic Bézier curve defined by two anchors and two control handles.
```python
CubicBezier(
    start_anchor: Point3DLike,
    start_handle: Point3DLike,
    end_handle: Point3DLike,
    end_anchor: Point3DLike,
    **kwargs,
)
```

### `ArcPolygon`
A polygon where each side is replaced by an arc.
```python
ArcPolygon(
    *vertices: Point3DLike,
    angle: float | None = None,
    radius: float | None = None,
    arc_config: dict | list[dict] | None = None,
    **kwargs,
)
```

---

## Geometry — Lines & Arrows

### `Line`
A straight line segment between two points or mobjects.
```python
Line(
    start: Point3DLike | Mobject = LEFT,
    end: Point3DLike | Mobject = RIGHT,
    buff: float = 0,
    path_arc: float = 0,
    **kwargs,
)
```

### `DashedLine`
A line rendered as a series of dashes.
```python
DashedLine(
    *args,
    dash_length: float = DEFAULT_DASH_LENGTH,
    dashed_ratio: float = 0.5,
    **kwargs,
)
```

### `TangentLine`
A line tangent to a VMobject at a given position along its path.
```python
TangentLine(
    vmob: VMobject,
    alpha: float,
    length: float = 1,
    d_alpha: float = 1e-6,
    **kwargs,
)
```

### `Elbow`
A right-angle elbow marker, often used to indicate perpendicularity.
```python
Elbow(
    width: float = 0.2,
    angle: float = 0,
    **kwargs,
)
```

### `Arrow`
A line with a tip, used to indicate direction or pointing.
```python
Arrow(
    *args,
    stroke_width: float = 6,
    buff: float = MED_SMALL_BUFF,
    max_tip_length_to_length_ratio: float = 0.3,
    max_stroke_width_to_length_ratio: float = 11,
    **kwargs,
)
```

### `Vector`
An arrow from the origin in a given direction, sized to represent a vector.
```python
Vector(
    direction: Vector2DLike | Vector3DLike = RIGHT,
    buff: float = 0,
    **kwargs,
)
```

### `DoubleArrow`
An arrow with tips at both ends.
```python
DoubleArrow(
    *args,
    **kwargs,
)
```

### `Angle`
Draws the angle between two lines, optionally as an arc or with a dot for right angles.
```python
Angle(
    line1: Line,
    line2: Line,
    radius: float | None = None,
    quadrant: tuple[int, int] = (1, 1),
    other_angle: bool = False,
    dot: bool = False,
    dot_radius: float = 0.04,
    dot_color: ParsableManimColor = WHITE,
    stroke_width: float = 2,
    arc_type: str = "arc",
    color: ParsableManimColor = WHITE,
    **kwargs,
)
```

### `RightAngle`
A square marker indicating a 90° angle between two lines.
```python
RightAngle(
    line1: Line,
    line2: Line,
    length: float = 0.5,
    **kwargs,
)
```

---

## Geometry — Polygons

### `Polygram`
A generalized polygon that supports multiple disconnected vertex groups (star polygons, etc.).
```python
Polygram(
    *vertex_groups: Point3DLike_Array,
    color: ParsableManimColor = BLUE,
    **kwargs,
)
```

### `Polygon`
A closed polygon defined by an arbitrary list of vertices.
```python
Polygon(
    *vertices: Point3DLike,
    **kwargs,
)
```

### `RegularPolygram`
A regular star polygon with evenly spaced vertices and a configurable density (skip interval).
```python
RegularPolygram(
    num_vertices: int,
    *,
    density: int = 2,
    radius: float = 1,
    start_angle: float | None = None,
    **kwargs,
)
```

### `RegularPolygon`
A regular polygon with `n` equal sides.
```python
RegularPolygon(
    n: int = 6,
    **kwargs,
)
```

### `Star`
A star shape with `n` points and configurable inner/outer radii.
```python
Star(
    n: int = 5,
    *,
    outer_radius: float = 1,
    inner_radius: float | None = None,
    density: int = 2,
    start_angle: float | None = None,
    **kwargs,
)
```

### `Triangle`
An equilateral triangle.
```python
Triangle(
    **kwargs,
)
```

### `Rectangle`
A rectangle with optional internal grid lines.
```python
Rectangle(
    color: ParsableManimColor = WHITE,
    height: float = 2.0,
    width: float = 4.0,
    grid_xstep: float | None = None,
    grid_ystep: float | None = None,
    mark_paths_closed: bool = True,
    close_new_points: bool = True,
    **kwargs,
)
```

### `Square`
A rectangle with equal sides.
```python
Square(
    side_length: float = 2.0,
    **kwargs,
)
```

### `RoundedRectangle`
A rectangle with rounded corners.
```python
RoundedRectangle(
    corner_radius: float | list[float] = 0.5,
    **kwargs,
)
```

### `Cutout`
Subtracts one or more shapes from a main shape, creating holes.
```python
Cutout(
    main_shape: VMobject,
    *mobjects: VMobject,
    **kwargs,
)
```

---

## Geometry — Boolean Operations

### `Union`
The combined area of multiple overlapping shapes.
```python
Union(
    *vmobjects: VMobject,
    **kwargs,
)
```

### `Difference`
The first shape with all subsequent shapes subtracted from it.
```python
Difference(
    *vmobjects: VMobject,
    **kwargs,
)
```

### `Intersection`
The overlapping region shared by all given shapes.
```python
Intersection(
    *vmobjects: VMobject,
    **kwargs,
)
```

### `Exclusion`
The area covered by exactly one of the shapes (symmetric difference).
```python
Exclusion(
    *vmobjects: VMobject,
    **kwargs,
)
```

---

## Geometry — Shape Matchers

### `SurroundingRectangle`
A rectangle that auto-fits around a given mobject with optional padding.
```python
SurroundingRectangle(
    mobject: Mobject,
    color: ParsableManimColor = YELLOW,
    buff: float = MED_BUFF,
    stroke_width: float = 8,
    stroke_color: ParsableManimColor | None = None,
    corner_radius: float = MED_SMALL_BUFF,
    **kwargs,
)
```

### `BackgroundRectangle`
A semi-transparent filled rectangle placed behind a mobject for readability.
```python
BackgroundRectangle(
    mobject: Mobject,
    color: ParsableManimColor = BLACK,
    buff: float = 0,
    opacity: float = 0.7,
    **kwargs,
)
```

### `Cross`
Two diagonal lines forming an X over a mobject, indicating rejection or removal.
```python
Cross(
    mobject: Mobject,
    stroke_color: ParsableManimColor = RED,
    stroke_width: float | None = None,
    **kwargs,
)
```

### `Underline`
A horizontal line placed beneath a mobject.
```python
Underline(
    mobject: Mobject,
    buff: float = SMALL_BUFF,
    **kwargs,
)
```

---

## Geometry — Arrow Tips

### `ArrowTip`
Base class for all arrow tip styles.
```python
ArrowTip(**kwargs)
```

### `StealthTip`
A sleek, swept-back "stealth" arrowhead.
```python
StealthTip(**kwargs)
```

### `ArrowTriangleTip`
An outlined triangle arrowhead.
```python
ArrowTriangleTip(**kwargs)
```

### `ArrowTriangleFilledTip`
A solid filled triangle arrowhead.
```python
ArrowTriangleFilledTip(**kwargs)
```

### `ArrowCircleTip`
An outlined circle arrowhead.
```python
ArrowCircleTip(**kwargs)
```

### `ArrowCircleFilledTip`
A solid filled circle arrowhead.
```python
ArrowCircleFilledTip(**kwargs)
```

### `ArrowSquareTip`
An outlined square arrowhead.
```python
ArrowSquareTip(**kwargs)
```

### `ArrowSquareFilledTip`
A solid filled square arrowhead.
```python
ArrowSquareFilledTip(**kwargs)
```

---

## Geometry — Labeled Shapes

### `Label`
A text label optionally wrapped in a box or frame.
```python
Label(
    label: str | Tex | MathTex | Text,
    label_config: dict | None = None,
    box_config: dict | None = None,
    frame_config: dict | None = None,
    **kwargs,
)
```

### `LabeledLine`
A line with a label placed along its midpoint.
```python
LabeledLine(
    label: str | Tex | MathTex | Text,
    line: Line,
    label_config: dict | None = None,
    **kwargs,
)
```

### `LabeledArrow`
An arrow with a label placed along its body.
```python
LabeledArrow(
    label: str | Tex | MathTex | Text,
    *args,
    label_config: dict | None = None,
    **kwargs,
)
```

### `LabeledPolygram`
A polygram with a label centered inside it.
```python
LabeledPolygram(
    label: str | Tex | MathTex | Text,
    *args,
    label_config: dict | None = None,
    **kwargs,
)
```

---

## Braces

### `Brace`
A curly brace that spans a mobject, pointing in a given direction.
```python
Brace(
    mobject: Mobject,
    direction: Vector3DLike = DOWN,
    buff: float = 0.2,
    sharpness: float = 2,
    stroke_width: float = 0,
    fill_opacity: float = 1.0,
    background_stroke_width: float = 0,
    background_stroke_color: ParsableManimColor = BLACK,
    **kwargs,
)
```

### `BraceLabel`
A brace paired with a label rendered next to it.
```python
BraceLabel(
    brace: Brace,
    label: str | Tex | MathTex | Text,
    label_constructor: type[VMobject] = MathTex,
    font_size: float = DEFAULT_FONT_SIZE,
    **kwargs,
)
```

### `BraceText`
A brace paired with a plain text label.
```python
BraceText(
    brace: Brace,
    text: str,
    **kwargs,
)
```

### `BraceBetweenPoints`
A brace spanning between two explicit points.
```python
BraceBetweenPoints(
    point1: Point3DLike,
    point2: Point3DLike,
    direction: Vector3DLike = UP,
    **kwargs,
)
```

### `ArcBrace`
A brace that follows the curve of an arc.
```python
ArcBrace(
    arc: Arc,
    direction: Vector3DLike = UP,
    **kwargs,
)
```

---

## Text & LaTeX

### `MathTex`
Renders a LaTeX math expression (wrapped in an `align*` environment by default).
```python
MathTex(
    *args: str,
    arg_separator: str = " ",
    stroke_width: float = 0,
    should_center: bool = True,
    height: float | None = None,
    organize_left_to_right: bool = False,
    tex_environment: str | None = "align*",
    tex_template: TexTemplate | None = None,
    font_size: float = DEFAULT_FONT_SIZE,
    color: ParsableManimColor | None = None,
    **kwargs,
)
```

### `Tex`
Renders arbitrary LaTeX markup (not limited to math mode).
```python
Tex(
    *args: str,
    **kwargs,
)
```

### `BulletedList`
A vertical list of items, each prefixed with a bullet dot.
```python
BulletedList(
    *args: str,
    buff: float = MED_LARGE_BUFF,
    dot_scale_factor: float = 2,
    **kwargs,
)
```

### `Title`
A large, centered text heading scaled for use as a scene title.
```python
Title(
    *args: str,
    scale_factor: float = 1.5,
    **kwargs,
)
```

### `Text`
Renders plain text using a system font (via Pango/Cairo), with rich per-character styling options.
```python
Text(
    text: str,
    *,
    font: str = DEFAULT_FONT,
    font_size: float = DEFAULT_FONT_SIZE,
    lsh: float = DEFAULT_LINE_SPACING_HEIGHT,
    tab_width: float = 4,
    should_center: bool = True,
    height: float | None = None,
    width: float | None = None,
    color: ParsableManimColor | None = None,
    stroke_color: ParsableManimColor | None = None,
    stroke_width: float = 0,
    slant: float = NORMAL,
    weight: str = NORMAL,
    t2c: dict[str, ParsableManimColor] | None = None,
    t2f: dict[str, str] | None = None,
    t2g: dict[str, ParsableManimColor] | None = None,
    t2s: dict[str, float] | None = None,
    t2w: dict[str, str] | None = None,
    gradient: tuple[ParsableManimColor, ParsableManimColor] | None = None,
    line_to_initial_point_buff: float = 0.2,
    justify: bool = False,
    warn_missing_font: bool = True,
    **kwargs,
)
```

### `MarkupText`
Renders text with Pango markup tags for inline styling (bold, italic, color, etc.).
```python
MarkupText(
    text: str,
    **kwargs,
)
```

### `Paragraph`
Multiple lines of text with controllable line spacing.
```python
Paragraph(
    *lines: str,
    line_spacing: float = DEFAULT_LINE_SPACING_HEIGHT,
    **kwargs,
)
```

### `Code`
Displays syntax-highlighted source code with optional line numbers and a styled background.
```python
Code(
    code_file: StrPath | None = None,
    code_string: str | None = None,
    language: str | None = None,
    formatter_style: str = "vim",
    tab_width: int = 4,
    add_line_numbers: bool = True,
    line_number_buff: float = 0.3,
    style: str = "native",
    background: str = "rectangle",
    background_stroke_width: float = 1,
    background_stroke_color: ParsableManimColor = WHITE,
    insert_line_no: bool = True,
    line_no_start: int = 1,
    line_no_buff: float = 0.4,
    font: str = "Monospace",
    font_size: float = DEFAULT_FONT_SIZE,
    font_color: ParsableManimColor = WHITE,
    corner_radius: float = 0.2,
    margin: float = 0.3,
    padding: float = 0.2,
    background_config: dict | None = None,
    paragraph_config: dict | None = None,
    **kwargs,
)
```

---

## Numbers

### `DecimalNumber`
Displays a floating-point number with configurable decimal places and formatting.
```python
DecimalNumber(
    number: float = 0,
    num_decimal_places: int = 2,
    mob_class: type[VMobject] = MathTex,
    include_sign: bool = False,
    group_with_commas: bool = True,
    digit_buff_per_font_unit: float = 0.001,
    show_ellipsis: bool = False,
    unit: str | None = None,
    unit_buff_per_font_unit: float = 0,
    include_background_rectangle: bool = False,
    edge_to_fix: Sequence[float] = (1, 1),
    font_size: float = DEFAULT_FONT_SIZE,
    **kwargs,
)
```

### `Integer`
Displays an integer value (no decimal places).
```python
Integer(
    number: int = 0,
    **kwargs,
)
```

### `Variable`
A labeled numeric display that updates live as its tracked value changes.
```python
Variable(
    var: float = 0.0,
    label: str | Tex | MathTex | Text | None = None,
    num_decimal_places: int = 0,
    **kwargs,
)
```

---

## Graphing & Plotting

### `ParametricFunction`
Plots a curve defined by a parametric function `f(t) → (x, y, z)`.
```python
ParametricFunction(
    function: Callable[[float], np.ndarray],
    t_range: tuple[float, float] | tuple[float, float, float] | None = None,
    scaling: _ScaleBase | None = None,
    use_smoothing: bool = True,
    use_vectorized: bool = False,
    discontinuities: Iterable[float] | None = None,
    dt: float = 1e-8,
    **kwargs,
)
```

### `FunctionGraph`
Plots a single-variable function `f(x)` along the x-axis.
```python
FunctionGraph(
    function: Callable[[float], Any],
    x_range: tuple[float, float] | tuple[float, float, float] | None = None,
    color: ParsableManimColor = PURE_YELLOW,
    **kwargs,
)
```

### `ImplicitFunction`
Plots the zero-level contour of a function `f(x, y) = 0`.
```python
ImplicitFunction(
    func: Callable[[float, float], float],
    color: ParsableManimColor = YELLOW,
    min_depth: int = 3,
    max_quads: int = 6144,
    **kwargs,
)
```

### `NumberLine`
A horizontal (or rotated) axis with tick marks and optional number labels.
```python
NumberLine(
    x_range: Sequence[float] | None = None,
    length: float | None = None,
    unit_size: float = 1,
    include_ticks: bool = True,
    tick_size: float = 0.1,
    numbers_with_elongated_ticks: Iterable[float] | None = None,
    longer_tick_multiple: int = 2,
    rotation: float = 0,
    stroke_width: float = 2.0,
    include_tip: bool = False,
    tip_width: float = 0.35,
    tip_height: float = 0.35,
    tip_shape: type[ArrowTip] | None = None,
    include_numbers: bool = False,
    scaling: _ScaleBase = LinearBase(),
    font_size: float = DEFAULT_FONT_SIZE,
    label_direction: Vector3DLike = DOWN,
    label_constructor: type[VMobject] = DecimalNumber,
    line_to_number_buff: float = MED_SMALL_BUFF,
    decimal_number_config: dict | None = None,
    numbers_to_exclude: Iterable[float] | None = None,
    numbers_to_include: Iterable[float] | None = None,
    **kwargs,
)
```

### `UnitInterval`
A `NumberLine` pre-configured for the range [0, 1].
```python
UnitInterval(**kwargs)
```

### `Axes`
A 2D coordinate system with x and y axes.
```python
Axes(
    x_range: Sequence[float] | None = None,
    y_range: Sequence[float] | None = None,
    x_length: float | None = None,
    y_length: float | None = None,
    axis_config: dict | None = None,
    x_axis_config: dict | None = None,
    y_axis_config: dict | None = None,
    tips: bool = True,
    **kwargs,
)
```

### `NumberPlane`
A 2D grid of axes with background grid lines, useful for showing coordinate spaces.
```python
NumberPlane(
    x_range: Sequence[float] | None = None,
    y_range: Sequence[float] | None = None,
    x_length: float | None = None,
    y_length: float | None = None,
    background_line_style: dict | None = None,
    grid_lines: list[VMobject] | None = None,
    axis_config: dict | None = None,
    x_axis_config: dict | None = None,
    y_axis_config: dict | None = None,
    **kwargs,
)
```

### `PolarPlane`
A polar coordinate grid with radial and angular divisions.
```python
PolarPlane(
    radius_max: float = config["frame_y_radius"],
    size: float | None = None,
    radius_step: float = 1,
    radius_config: dict | None = None,
    angle_step: float = TAU / 12,
    angle_config: dict | None = None,
    azimuth_step: float | None = None,
    **kwargs,
)
```

### `BarChart`
A vertical bar chart from a list of values.
```python
BarChart(
    values: Iterable[float],
    bar_names: Iterable[str] | None = None,
    y_range: Sequence[float] | None = None,
    x_length: float | None = None,
    y_length: float = 6,
    bar_colors: Iterable[ParsableManimColor] | None = None,
    bar_width: float = 0.6,
    bar_fill_opacity: float = 1.0,
    bar_stroke_width: float = 0,
    **kwargs,
)
```

---

## Graphs & Networks

### `Graph`
An undirected graph of vertices connected by edges, with flexible layout algorithms.
```python
Graph(
    vertices: Iterable[Hashable],
    edges: Iterable[tuple[Hashable, Hashable]],
    labels: bool | dict = False,
    label_fill_color: ParsableManimColor = WHITE,
    layout: str | dict | LayoutFunction = "spring",
    layout_config: dict | None = None,
    layout_scale: float = 2,
    vertex_type: type[Mobject] = Dot,
    vertex_config: dict | None = None,
    vertex_mobjects: dict[Hashable, Mobject] | None = None,
    edge_type: type[VMobject] = Line,
    edge_config: dict | None = None,
    edge_stroke_width: float = DEFAULT_STROKE_WIDTH,
    **kwargs,
)
```

### `DiGraph`
A directed graph where edges have arrows indicating direction.
```python
DiGraph(
    vertices: Iterable[Hashable],
    edges: Iterable[tuple[Hashable, Hashable]],
    **kwargs,
)
```

---

## Matrices

### `Matrix`
Renders a 2D array as a mathematical matrix with brackets.
```python
Matrix(
    matrix: np.ndarray | list[list[float]],
    v_buff: float = 0.8,
    h_buff: float = 1.3,
    bracket_h_buff: float = MED_SMALL_BUFF,
    bracket_v_buff: float = MED_SMALL_BUFF,
    add_background_rectangles_to_entries: bool = False,
    include_background_rectangle: bool = False,
    element_to_mobject: type[VMobject] = MathTex,
    element_to_mobject_config: dict | None = None,
    element_alignment_corner: tuple[float, float] = DR,
    left_bracket: str = "[",
    right_bracket: str = "]",
    stretch_brackets: bool = True,
    bracket_config: dict | None = None,
    **kwargs,
)
```

---

## Tables

### `Table`
A grid table from a 2D list of strings or numbers, with optional row/column labels.
```python
Table(
    table: Iterable[Iterable[str | float]],
    row_labels: Iterable[VMobject] | None = None,
    col_labels: Iterable[VMobject] | None = None,
    top_left_entry: VMobject | None = None,
    v_buff: float = 0.8,
    h_buff: float = 1.3,
    include_outer_lines: bool = False,
    add_background_rectangles_to_entries: bool = False,
    entries_background_color: ParsableManimColor | None = None,
    include_background_rectangle: bool = False,
    background_rectangle_color: ParsableManimColor | None = None,
    element_to_mobject: type[VMobject] = Paragraph,
    element_to_mobject_config: dict | None = None,
    arrange_in_grid_config: dict | None = None,
    line_config: dict | None = None,
    **kwargs,
)
```

### `MathTable`
A table where entries are rendered as LaTeX math.
```python
MathTable(
    table: Iterable[Iterable[str | float]],
    **kwargs,
)
```

---

## Vector Fields

### `ArrowVectorField`
Visualizes a vector field as a grid of arrows, colored by magnitude.
```python
ArrowVectorField(
    func: Callable[[Point3D], Vector3D],
    color: ParsableManimColor | None = None,
    color_scheme: Callable[[Vector3D], float] | None = None,
    min_color_scheme_value: float = 0,
    max_color_scheme_value: float = 2,
    colors: Sequence[ParsableManimColor] = DEFAULT_VECTOR_FIELD_COLORS,
    **kwargs,
)
```

### `StreamLines`
Visualizes a vector field as animated flowing lines that follow the field direction.
```python
StreamLines(
    func: Callable[[Point3D], Vector3D],
    color: ParsableManimColor | None = None,
    color_scheme: Callable[[Vector3D], float] | None = None,
    min_color_scheme_value: float = 0,
    max_color_scheme_value: float = 2,
    colors: Sequence[ParsableManimColor] = DEFAULT_VECTOR_FIELD_COLORS,
    **kwargs,
)
```

---

## Value Trackers

### `ValueTracker`
An invisible mobject that holds a scalar float value, useful for driving animations via `add_updater`.
```python
ValueTracker(
    value: float = 0,
    **kwargs,
)
```

### `ComplexValueTracker`
A `ValueTracker` that holds a complex number instead of a float.
```python
ComplexValueTracker(
    value: complex = 0j,
    **kwargs,
)
```

---

## Images

### `ImageMobject`
Displays a raster image from a file or numpy array.
```python
ImageMobject(
    filename_or_array: StrPath | npt.NDArray,
    scale_to_resolution: int = QUALITIES[DEFAULT_QUALITY]["pixel_height"],
    invert: bool = False,
    image_mode: str = "RGBA",
    **kwargs,
)
```

---

## Frame / Screen

### `ScreenRectangle`
A rectangle matching a given aspect ratio, useful for framing content like slides or video.
```python
ScreenRectangle(
    aspect_ratio: float | None = None,
    height: float | None = None,
    width: float | None = None,
    **kwargs,
)
```

### `FullScreenRectangle`
A rectangle that fills the entire scene frame.
```python
FullScreenRectangle(**kwargs)
```
