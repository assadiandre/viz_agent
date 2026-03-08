---
description: Guidelines for writing Manim (ManimCE) animation code
globs: "**/*.py"
alwaysApply: false
---

# Writing Manim Code

## Rules

- Always use `from manim import *` — this is the official ManimCE import convention.
- Subclass `Scene` and put all logic in `construct(self)`. Use `setup(self)` for initialization — never override `__init__`.
- Use `Create` instead of deprecated `ShowCreation`; use `Text` instead of `TextMobject`; use `Tex`/`MathTex` instead of `TexMobject`.
- Prefer `.animate` syntax for property animations: `self.play(mob.animate.shift(RIGHT).set_color(BLUE))`.
- Use `VGroup` to group related mobjects and `arrange()`/`next_to()` for layout — avoid manual coordinate math when possible.
- Use `ReplacementTransform` when you want the target to replace the source in the scene; use `Transform` when you want the source to morph visually but remain the same object.
- Never call `self.play()` with zero animations — it raises `ValueError`.
- Never assign `config = {...}`; use `config.update({})` or `tempconfig({...})` for scoped overrides.
- All mobject positioning met
hods (`shift`, `move_to`, `scale`, `rotate`, `set_color`, `set_fill`, `next_to`, `arrange`) return `Self` and support chaining.
- Animations accept common kwargs: `run_time`, `rate_func`, `lag_ratio`. Pass these to `self.play()` or to the animation constructor.
- Use `LaggedStart` with a `lag_ratio` to stagger multiple animations. Use `AnimationGroup` for parallel execution.
- For 3D scenes, subclass `ThreeDScene` and use `set_camera_orientation(phi, theta)`.
- Quality flags: `-ql` (480p/15fps), `-qm` (720p/30fps), `-qh` (1080p/60fps), `-qk` (4K/60fps). Always use `-ql` during development.
- Name scenes in PascalCase, variables in snake_case.
- Always use raw strings (`r"..."`) for LaTeX in `Tex` and `MathTex` to avoid Python escape conflicts.
- `Tex` renders arbitrary LaTeX; `MathTex` renders inside a math environment (`align*`). For inline math inside `Tex`, wrap with `$...$`.
- Updater lambdas that depend on `dt` must accept two arguments: `lambda mob, dt: ...`. Updaters without `dt` take one: `lambda mob: ...`.
- Call `self.add(tracker)` before using a `ValueTracker` with updaters to ensure the scene processes it each frame.
- `save_state()` / `Restore()` pairs let you snapshot and revert a mobject's position, style, and shape.
- `generate_target()` + `MoveToTarget()` is an alternative to `.animate` for complex multi-step transformations built imperatively on `.target`.
- `become()` replaces a mobject's contents in-place — useful inside updaters to replace one mobject with another each frame.
- Do not mix `Mobject` and `VMobject` in the same `VGroup`; use `Group` instead for heterogeneous collections.
- Angles are always in radians. Use `n * DEGREES` (e.g. `45 * DEGREES`) or the constants `PI`, `TAU` for clarity.
- `to_edge(UP)` places a mobject at the top edge; `to_corner(UL)` places it at the upper-left corner.
- For `MovingCameraScene`, animate the camera via `self.camera.frame.animate.move_to(...)` or `.scale(...)`.

## Library Description

ManimCE (Manim Community Edition, v0.20.1) is a Python library for creating precise, programmatic mathematical animations. It renders scenes frame-by-frame using Cairo (default) or OpenGL. The core abstraction is a `Scene` containing `Mobject`s (mathematical objects) that are manipulated through `Animation`s. Key domains: geometry visualization, LaTeX typesetting, function plotting, graph theory, and 3D surfaces. Mobjects form a hierarchy — `VMobject` (vector graphics) is the most common base, supporting fill, stroke, and path operations. Scenes are rendered via CLI (`manim -p -ql file.py SceneName`) producing MP4/GIF output to `media/`.

**Coordinate system:** The default frame is 8 units tall and ~14.2 units wide. `ORIGIN` is the center. `UP`/`DOWN`/`LEFT`/`RIGHT` are unit vectors along Y+/Y-/X-/X+. `IN`/`OUT` go into/out of the screen along Z. Diagonal shortcuts: `UL`, `UR`, `DL`, `DR`. Buff constants: `SMALL_BUFF=0.1`, `MED_SMALL_BUFF=0.25`, `MED_LARGE_BUFF=0.5`, `LARGE_BUFF=1`.

**Color system:** Colors are strings or `ManimColor` objects. Named colors include `RED`, `GREEN`, `BLUE`, `YELLOW`, `ORANGE`, `PURPLE`, `WHITE`, `BLACK`, `GREY`/`GRAY`, `PINK`, `TEAL`, `MAROON`, `GOLD`. Each has five intensity variants: `_A` (lightest) through `_E` (darkest), e.g. `BLUE_A`, `BLUE_B`, `BLUE_C`, `BLUE_D`, `BLUE_E`. Pure-primary variants: `PURE_RED`, `PURE_GREEN`, `PURE_BLUE`. `LIGHT_GREY`, `DARK_GREY`, `DARK_BROWN`, `LIGHT_BROWN` are also available.

**Math constants:** `PI = np.pi`, `TAU = 2 * PI`, `DEGREES = TAU / 360` (multiply a degree value by `DEGREES` to get radians).

**Scene lifecycle:** `setup()` → `construct()` → `tear_down()`. All animation logic belongs in `construct()`.

**Rendering:** `manim -p -ql scene.py MyScene` renders and previews. `-p` opens the output. Flags `-s` saves the last frame as PNG. `--format gif` outputs a GIF. `manim --help` lists all options.

## Code Snippets

<!-- ─────────────────────────── SCENE BASICS ─────────────────────────── -->

<example>
<signature>class MyScene(Scene): def construct(self) -> None</signature>
<input>Subclass Scene, override construct with animation logic</input>
<output>Rendered video of the scene</output>
</example>

<example>
<signature>Scene.play(self, *args: Animation | Mobject | _AnimationBuilder, **kwargs) -> None</signature>
<input>self.play(Create(circle), run_time=2, rate_func=smooth)</input>
<output>Renders the Create animation over 2 seconds with smooth easing</output>
</example>

<example>
<signature>Scene.wait(self, duration: float = 1.0, stop_condition: Callable | None = None, frozen_frame: bool | None = None) -> None</signature>
<input>self.wait(2)</input>
<output>Pauses the scene for 2 seconds</output>
</example>

<example>
<signature>Scene.add(self, *mobjects: Mobject) -> Self</signature>
<input>self.add(circle, square)</input>
<output>circle and square appear instantly on screen (no animation)</output>
</example>

<example>
<signature>Scene.remove(self, *mobjects: Mobject) -> Self</signature>
<input>self.remove(circle)</input>
<output>circle disappears instantly from the scene</output>
</example>

<example>
<signature>Scene.add_sound(self, sound_file: str, time_offset: float = 0, gain: float | None = None)</signature>
<input>self.add_sound("click.wav", time_offset=0.5)</input>
<output>Plays the sound file 0.5 seconds into the scene</output>
</example>

<example>
<signature>tempconfig(temp: ManimConfig | dict) -> ContextManager</signature>
<input>with tempconfig({"background_color": WHITE, "pixel_width": 1920}): scene.render()</input>
<output>Scene renders with white background and 1920px width, then config reverts</output>
</example>

<example>
<signature>class MyScene(MovingCameraScene): # camera.frame is an animatable Rectangle</signature>
<input>
class ZoomIn(MovingCameraScene):
    def construct(self):
        dot = Dot()
        self.add(dot)
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.scale(0.5).move_to(dot))
        self.wait()
        self.play(Restore(self.camera.frame))
</input>
<output>Zooms the camera in on a dot then restores it</output>
</example>

<example>
<signature>class MyScene(ThreeDScene): # 3D scene with phi/theta camera angles</signature>
<input>
class My3DScene(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        sphere = Sphere(radius=1)
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        self.add(axes, sphere)
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(4)
        self.stop_ambient_camera_rotation()
</input>
<output>A 3D scene with axes and a sphere with the camera slowly rotating</output>
</example>

<!-- ─────────────────────────── GEOMETRY MOBJECTS ─────────────────────────── -->

<example>
<signature>Circle(radius: float | None = None, color: ParsableManimColor = RED, **kwargs) -> Circle</signature>
<input>Circle(radius=1.5, color=BLUE)</input>
<output>A blue circle mobject with radius 1.5</output>
</example>

<example>
<signature>Square(side_length: float = 2.0, **kwargs) -> Square</signature>
<input>Square(side_length=3.0, color=GREEN)</input>
<output>A green square mobject with side length 3.0</output>
</example>

<example>
<signature>Rectangle(color: ParsableManimColor = WHITE, height: float = 2.0, width: float = 4.0, **kwargs) -> Rectangle</signature>
<input>Rectangle(height=1, width=3, color=YELLOW)</input>
<output>A yellow 1x3 rectangle mobject</output>
</example>

<example>
<signature>RoundedRectangle(corner_radius: float = 0.5, **kwargs) -> RoundedRectangle</signature>
<input>RoundedRectangle(corner_radius=0.3, height=2, width=4, color=TEAL)</input>
<output>A teal rectangle with rounded corners</output>
</example>

<example>
<signature>Triangle(**kwargs) -> Triangle</signature>
<input>Triangle(color=ORANGE, fill_opacity=0.5)</input>
<output>An orange triangle with 50% fill opacity</output>
</example>

<example>
<signature>RegularPolygon(n: int = 6, **kwargs) -> RegularPolygon</signature>
<input>RegularPolygon(n=6, color=PURPLE)</input>
<output>A regular hexagon mobject</output>
</example>

<example>
<signature>Star(n: int = 5, outer_radius: float = 1, inner_radius: float | None = None, **kwargs) -> Star</signature>
<input>Star(n=5, outer_radius=1.5, color=GOLD)</input>
<output>A 5-pointed gold star</output>
</example>

<example>
<signature>Polygon(*vertices: Point3DLike, **kwargs) -> Polygon</signature>
<input>Polygon([0,0,0], [1,2,0], [2,0,0], color=RED)</input>
<output>A custom triangle from three vertices</output>
</example>

<example>
<signature>Dot(point: Point3DLike = ORIGIN, radius: float = DEFAULT_DOT_RADIUS, color: ParsableManimColor = WHITE, **kwargs) -> Dot</signature>
<input>Dot(UP + RIGHT, color=YELLOW)</input>
<output>A small yellow dot at position (1, 1, 0)</output>
</example>

<example>
<signature>LabeledDot(label: str | SingleStringMathTex, radius: float | None = None, **kwargs) -> LabeledDot</signature>
<input>LabeledDot(MathTex(r"\pi"), radius=0.3, color=BLUE)</input>
<output>A dot with a pi label inside it</output>
</example>

<example>
<signature>Line(start: Point3DLike | Mobject = LEFT, end: Point3DLike | Mobject = RIGHT, buff: float = 0, **kwargs) -> Line</signature>
<input>Line(ORIGIN, UP * 2)</input>
<output>A vertical line mobject from origin to 2 units up</output>
</example>

<example>
<signature>DashedLine(start: Point3DLike = LEFT, end: Point3DLike = RIGHT, dash_length: float = DEFAULT_DASH_LENGTH, **kwargs) -> DashedLine</signature>
<input>DashedLine(LEFT * 2, RIGHT * 2, dash_length=0.2, color=GREY)</input>
<output>A horizontal dashed line</output>
</example>

<example>
<signature>Arrow(*args, stroke_width: float = 6, buff: float = MED_SMALL_BUFF, **kwargs) -> Arrow</signature>
<input>Arrow(LEFT, RIGHT, color=RED)</input>
<output>A red arrow pointing from left to right</output>
</example>

<example>
<signature>DoubleArrow(*args, **kwargs) -> DoubleArrow</signature>
<input>DoubleArrow(LEFT * 2, RIGHT * 2, color=GREEN)</input>
<output>A green double-headed arrow</output>
</example>

<example>
<signature>Vector(direction: Point3DLike = RIGHT, **kwargs) -> Vector</signature>
<input>Vector(UP + RIGHT, color=YELLOW)</input>
<output>An arrow from ORIGIN to UP+RIGHT direction (buff=0 by default)</output>
</example>

<example>
<signature>Arc(radius: float = 1.0, start_angle: float = 0, angle: float = TAU / 4, **kwargs) -> Arc</signature>
<input>Arc(radius=2, start_angle=0, angle=PI, color=BLUE)</input>
<output>A blue semicircular arc of radius 2</output>
</example>

<example>
<signature>ArcBetweenPoints(start: Point3DLike, end: Point3DLike, angle: float = TAU / 4, **kwargs) -> ArcBetweenPoints</signature>
<input>ArcBetweenPoints(LEFT, RIGHT, angle=PI/2)</input>
<output>An arc curving between two points</output>
</example>

<example>
<signature>CurvedArrow(start_point: Point3DLike, end_point: Point3DLike, radius: float | None = None, **kwargs) -> CurvedArrow</signature>
<input>CurvedArrow(LEFT * 2, RIGHT * 2, radius=3)</input>
<output>A curved arrow from left to right bowing upward</output>
</example>

<example>
<signature>Ellipse(width: float = 2, height: float = 1, **kwargs) -> Ellipse</signature>
<input>Ellipse(width=4, height=2, color=TEAL)</input>
<output>A teal ellipse wider than it is tall</output>
</example>

<example>
<signature>Sector(outer_radius: float = 1, inner_radius: float = 0, angle: float = TAU / 4, start_angle: float = 0, **kwargs) -> Sector</signature>
<input>Sector(outer_radius=2, angle=PI/3, color=ORANGE, fill_opacity=0.7)</input>
<output>An orange pie-slice sector filled at 70% opacity</output>
</example>

<example>
<signature>Annulus(inner_radius: float = 1, outer_radius: float = 2, **kwargs) -> Annulus</signature>
<input>Annulus(inner_radius=0.5, outer_radius=1.5, color=GREEN, fill_opacity=1)</input>
<output>A filled green ring (donut shape)</output>
</example>

<example>
<signature>Angle(line1: Line, line2: Line, radius: float = 0.5, quadrant: AngleQuadrant = (1, 1), **kwargs) -> Angle</signature>
<input>
l1 = Line(ORIGIN, RIGHT)
l2 = Line(ORIGIN, UP)
angle = Angle(l1, l2, radius=0.5, color=YELLOW)
</input>
<output>An arc representing the angle between two lines</output>
</example>

<example>
<signature>RightAngle(line1: Line, line2: Line, length: float = 0.2, **kwargs) -> RightAngle</signature>
<input>RightAngle(Line(ORIGIN, RIGHT), Line(ORIGIN, UP), length=0.25, color=WHITE)</input>
<output>A small square indicating a 90-degree angle</output>
</example>

<example>
<signature>SurroundingRectangle(mobject: Mobject, color: ParsableManimColor = PURE_YELLOW, buff: float = SMALL_BUFF, **kwargs) -> SurroundingRectangle</signature>
<input>SurroundingRectangle(equation, color=YELLOW, buff=0.2)</input>
<output>A yellow rectangle that tightly surrounds the equation</output>
</example>

<example>
<signature>Underline(mobject: Mobject, buff: float = SMALL_BUFF, **kwargs) -> Underline</signature>
<input>Underline(text, color=RED)</input>
<output>A red underline beneath the text mobject</output>
</example>

<example>
<signature>BackgroundRectangle(mobject: Mobject, color: ParsableManimColor = BLACK, fill_opacity: float = 0.75, **kwargs) -> BackgroundRectangle</signature>
<input>BackgroundRectangle(label, color=BLACK, fill_opacity=0.8)</input>
<output>A dark rectangle behind the label to improve contrast</output>
</example>

<!-- ─────────────────────────── TEXT & LATEX ─────────────────────────── -->

<example>
<signature>Text(text: str, font_size: float = DEFAULT_FONT_SIZE, font: str = "", color: ParsableManimColor | None = None, **kwargs) -> Text</signature>
<input>Text("Hello", font_size=48, color=WHITE)</input>
<output>A Pango-rendered text mobject displaying "Hello"</output>
</example>

<example>
<signature>Text with weight and slant</signature>
<input>Text("Bold Italic", weight=BOLD, slant=ITALIC, color=BLUE)</input>
<output>Blue bold-italic Pango text. Weight constants: THIN, ULTRALIGHT, LIGHT, BOOK, NORMAL, MEDIUM, SEMIBOLD, BOLD, ULTRABOLD, HEAVY, ULTRAHEAVY</output>
</example>

<example>
<signature>MarkupText(text: str, **kwargs) -> MarkupText</signature>
<input>MarkupText('Hello <span foreground="red">World</span>', font_size=40)</input>
<output>Text with inline Pango markup for per-character styling</output>
</example>

<example>
<signature>Paragraph(*lines: str, alignment: str = None, line_spacing: float = -1, **kwargs) -> Paragraph</signature>
<input>Paragraph("First line", "Second line", "Third line", alignment="center")</input>
<output>A multi-line paragraph centered; each line is a VGroup of characters</output>
</example>

<example>
<signature>Tex(tex_string: str, font_size: float = DEFAULT_FONT_SIZE, color: ParsableManimColor | None = None, tex_environment: str = "align*", **kwargs) -> Tex</signature>
<input>Tex(r"This is \LaTeX")</input>
<output>A LaTeX-rendered text mobject</output>
</example>

<example>
<signature>MathTex(*tex_strings: str, arg_separator: str = " ", tex_to_color_map: dict | None = None, tex_environment: str = "align*", **kwargs) -> MathTex</signature>
<input>MathTex(r"\sum_{n=1}^\infty \frac{1}{n^2} = \frac{\pi^2}{6}")</input>
<output>A rendered LaTeX equation mobject</output>
</example>

<example>
<signature>MathTex with multiple parts for selective coloring</signature>
<input>
eq = MathTex(r"e^{i\pi}", "+", "1", "=", "0")
eq[0].set_color(BLUE)   # e^{i\pi}
eq[2].set_color(GREEN)  # 1
eq[4].set_color(RED)    # 0
</input>
<output>Euler's identity with colored sub-expressions; each arg is an indexable sub-mobject</output>
</example>

<example>
<signature>MathTex with tex_to_color_map</signature>
<input>MathTex(r"E = mc^2", tex_to_color_map={"E": YELLOW, "m": RED, "c": BLUE})</input>
<output>Equation with each symbol automatically colored</output>
</example>

<example>
<signature>BulletedList(*items: str, bullet: str = r"\cdot", **kwargs) -> BulletedList</signature>
<input>BulletedList("First point", "Second point", "Third point", font_size=36)</input>
<output>A bulleted list rendered as a VGroup of Tex items</output>
</example>

<example>
<signature>Title(title: str, include_underline: bool = True, **kwargs) -> Title</signature>
<input>Title("My Presentation", include_underline=True, color=WHITE)</input>
<output>A title at the top of the screen with an optional underline</output>
</example>

<!-- ─────────────────────────── NUMBERS ─────────────────────────── -->

<example>
<signature>DecimalNumber(number: float = 0, num_decimal_places: int = 2, include_sign: bool = False, unit: str | None = None, **kwargs) -> DecimalNumber</signature>
<input>DecimalNumber(3.14159, num_decimal_places=3, color=YELLOW)</input>
<output>A mobject displaying "3.142" in yellow</output>
</example>

<example>
<signature>Integer(number: float = 0, **kwargs) -> Integer</signature>
<input>Integer(42, color=GREEN)</input>
<output>A mobject displaying the integer 42</output>
</example>

<example>
<signature>Variable(var: float, label: str | Tex, num_decimal_places: int = 2, **kwargs) -> Variable</signature>
<input>
t = ValueTracker(0)
var = Variable(t.get_value(), label=MathTex("t"), num_decimal_places=2)
var.add_updater(lambda v: v.tracker.set_value(t.get_value()))
</input>
<output>A "t = 0.00" display that updates when t changes</output>
</example>

<!-- ─────────────────────────── GROUPS & CONTAINERS ─────────────────────────── -->

<example>
<signature>VGroup(*vmobjects: VMobject, **kwargs) -> VGroup</signature>
<input>VGroup(circle, square, triangle)</input>
<output>A group mobject containing all three shapes, transformable as one unit</output>
</example>

<example>
<signature>Group(*mobjects: Mobject, **kwargs) -> Group</signature>
<input>Group(image, text, circle)</input>
<output>A generic group that accepts any Mobject types (use when mixing VMobject and non-VMobject)</output>
</example>

<!-- ─────────────────────────── VALUE TRACKER ─────────────────────────── -->

<example>
<signature>ValueTracker(value: float = 0) -> ValueTracker</signature>
<input>
tracker = ValueTracker(0)
dot = Dot()
dot.add_updater(lambda d: d.set_x(tracker.get_value()))
self.add(tracker, dot)
self.play(tracker.animate.set_value(3))
</input>
<output>A non-displayed mobject that stores a scalar; animating it drives the updater-linked dot</output>
</example>

<example>
<signature>ComplexValueTracker(value: complex = 0) -> ComplexValueTracker</signature>
<input>
tracker = ComplexValueTracker(-2 + 1j)
dot = Dot().add_updater(lambda d: d.move_to(tracker.points))
self.add(NumberPlane(), dot)
self.play(tracker.animate.set_value(3 + 2j))
</input>
<output>Tracks a complex number; .points[0] encodes (real, imag, 0)</output>
</example>

<!-- ─────────────────────────── POSITIONING ─────────────────────────── -->

<example>
<signature>Mobject.shift(self, *vectors: Vector3DLike) -> Self</signature>
<input>circle.shift(RIGHT * 2 + UP)</input>
<output>circle moves 2 units right and 1 unit up (returns self for chaining)</output>
</example>

<example>
<signature>Mobject.move_to(self, point_or_mobject: Point3DLike | Mobject, aligned_edge: Vector3DLike = ORIGIN) -> Self</signature>
<input>square.move_to(ORIGIN)</input>
<output>square centers at the origin</output>
</example>

<example>
<signature>Mobject.next_to(self, mobject_or_point: Mobject | Point3DLike, direction: Vector3DLike = RIGHT, buff: float = DEFAULT_MOBJECT_TO_MOBJECT_BUFFER) -> Self</signature>
<input>label.next_to(circle, UP, buff=0.3)</input>
<output>label positions itself 0.3 units above circle</output>
</example>

<example>
<signature>Mobject.to_edge(self, edge: Vector3DLike = LEFT, buff: float = DEFAULT_MOBJECT_TO_EDGE_BUFFER) -> Self</signature>
<input>title.to_edge(UP, buff=0.3)</input>
<output>title shifts to the top edge of the frame, 0.3 units from the edge</output>
</example>

<example>
<signature>Mobject.to_corner(self, corner: Vector3DLike = UL, buff: float = DEFAULT_MOBJECT_TO_EDGE_BUFFER) -> Self</signature>
<input>logo.to_corner(DR, buff=0.2)</input>
<output>logo moves to the bottom-right corner</output>
</example>

<example>
<signature>Mobject.align_to(self, mobject_or_point: Mobject | Point3DLike, direction: Vector3DLike) -> Self</signature>
<input>label.align_to(circle, LEFT)</input>
<output>label's left edge aligns with circle's left edge</output>
</example>

<example>
<signature>Mobject.scale(self, scale_factor: float, *, about_point: Point3DLike | None = None) -> Self</signature>
<input>square.scale(0.5)</input>
<output>square shrinks to half its size</output>
</example>

<example>
<signature>Mobject.rotate(self, angle: float, axis: Vector3DLike = OUT, *, about_point: Point3DLike | None = None) -> Self</signature>
<input>arrow.rotate(PI / 4)</input>
<output>arrow rotates 45 degrees counterclockwise</output>
</example>

<example>
<signature>Mobject.flip(self, axis: Vector3DLike = UP) -> Self</signature>
<input>text.flip(UP)</input>
<output>text is reflected about the vertical axis (horizontally mirrored)</output>
</example>

<example>
<signature>Mobject.arrange(self, direction: Vector3DLike = RIGHT, buff: float = DEFAULT_MOBJECT_TO_MOBJECT_BUFFER, center: bool = True) -> Self</signature>
<input>VGroup(a, b, c).arrange(DOWN, buff=0.5)</input>
<output>a, b, c stack vertically with 0.5 unit gaps, centered</output>
</example>

<example>
<signature>Mobject.arrange_in_grid(self, rows: int | None = None, cols: int | None = None, buff: float | tuple = MED_SMALL_BUFF, **kwargs) -> Self</signature>
<input>VGroup(*[Square() for _ in range(9)]).arrange_in_grid(rows=3, cols=3, buff=0.3)</input>
<output>9 squares arranged in a 3x3 grid with 0.3 unit gaps</output>
</example>

<example>
<signature>Mobject.get_center / get_top / get_bottom / get_left / get_right / get_corner</signature>
<input>
center = mob.get_center()        # center point [x, y, z]
top    = mob.get_top()           # topmost point
corner = mob.get_corner(UL)     # upper-left bounding box corner
</input>
<output>Returns numpy arrays of the specified reference point on the mobject's bounding box</output>
</example>

<example>
<signature>Mobject.set_z_index(self, z_index_value: float, family: bool = True) -> Self</signature>
<input>label.set_z_index(2)  # renders on top of z_index=0 and z_index=1 objects</input>
<output>Controls the render order; higher z_index draws on top</output>
</example>

<!-- ─────────────────────────── STYLING ─────────────────────────── -->

<example>
<signature>Mobject.set_color(self, color: ParsableManimColor = PURE_YELLOW, family: bool = True) -> Self</signature>
<input>circle.set_color(BLUE)</input>
<output>circle and all submobjects turn blue</output>
</example>

<example>
<signature>VMobject.set_fill(self, color: ParsableManimColor | None = None, opacity: float | None = None, family: bool = True) -> Self</signature>
<input>circle.set_fill(PINK, opacity=0.5)</input>
<output>circle fills with 50% opaque pink</output>
</example>

<example>
<signature>VMobject.set_stroke(self, color: ParsableManimColor = None, width: float | None = None, opacity: float | None = None) -> Self</signature>
<input>rect.set_stroke(WHITE, width=4)</input>
<output>rect gets a white border with width 4</output>
</example>

<example>
<signature>Mobject.set_opacity(self, opacity: float, family: bool = True) -> Self</signature>
<input>mob.set_opacity(0.5)</input>
<output>mob becomes 50% transparent</output>
</example>

<example>
<signature>Mobject.set_color_by_gradient(self, *colors: ParsableManimColor) -> Self</signature>
<input>text.set_color_by_gradient(RED, YELLOW, GREEN)</input>
<output>text transitions through red → yellow → green along its submobjects</output>
</example>

<example>
<signature>Mobject.fade(self, darkness: float = 0.5, family: bool = True) -> Self</signature>
<input>mob.fade(0.8)</input>
<output>mob becomes 80% darker (more transparent)</output>
</example>

<!-- ─────────────────────────── MOBJECT LIFECYCLE ─────────────────────────── -->

<example>
<signature>Mobject.copy(self) -> Self</signature>
<input>circle_copy = circle.copy().shift(RIGHT * 2)</input>
<output>Independent deep copy of the mobject, shifted right</output>
</example>

<example>
<signature>Mobject.save_state(self) -> Self</signature>
<input>
circle.save_state()
self.play(circle.animate.scale(2).set_color(RED))
self.play(Restore(circle))  # returns to saved state
</input>
<output>Saves the mobject's current state; Restore() animates back to it</output>
</example>

<example>
<signature>Mobject.generate_target(self) -> Self # then modify .target, then MoveToTarget</signature>
<input>
mob.generate_target()
mob.target.shift(RIGHT * 2).set_color(BLUE).scale(0.5)
self.play(MoveToTarget(mob))
</input>
<output>Builds a target state imperatively; MoveToTarget animates to it</output>
</example>

<example>
<signature>Mobject.become(self, mobject: Mobject) -> Self</signature>
<input>
square = Square()
circle = Circle()
square.become(circle)  # square now looks like circle
</input>
<output>Replaces the mobject's points and style with the target's; often used inside updaters</output>
</example>

<example>
<signature>Mobject.add_updater(self, update_function: Updater, index: int | None = None, call_updater: bool = False) -> Self</signature>
<input>dot.add_updater(lambda d: d.move_to(circle.get_center()))</input>
<output>dot follows circle's center every frame</output>
</example>

<example>
<signature>Time-based updater (receives dt)</signature>
<input>
angle = ValueTracker(0)
self.add(angle)
arrow.add_updater(lambda m, dt: m.rotate(dt, about_point=ORIGIN))
self.wait(2)
arrow.clear_updaters()
</input>
<output>Arrow rotates continuously using dt (seconds since last frame)</output>
</example>

<example>
<signature>Mobject.clear_updaters(self, recursive: bool = True) -> Self</signature>
<input>dot.clear_updaters()</input>
<output>Removes all updater functions from the mobject</output>
</example>

<!-- ─────────────────────────── CREATION ANIMATIONS ─────────────────────────── -->

<example>
<signature>Create(mobject: VMobject, lag_ratio: float = 1.0, **kwargs) -> Create</signature>
<input>self.play(Create(Square()))</input>
<output>Square draws itself onto the screen stroke-first</output>
</example>

<example>
<signature>Uncreate(mobject: VMobject, **kwargs) -> Uncreate</signature>
<input>self.play(Uncreate(circle))</input>
<output>circle erases itself (reverse of Create)</output>
</example>

<example>
<signature>DrawBorderThenFill(vmobject: VMobject, run_time: float = 2, **kwargs) -> DrawBorderThenFill</signature>
<input>self.play(DrawBorderThenFill(Square(fill_opacity=1, fill_color=ORANGE)))</input>
<output>First draws the border stroke, then fills the interior</output>
</example>

<example>
<signature>Write(vmobject: VMobject, rate_func: Callable = linear, reverse: bool = False, **kwargs) -> Write</signature>
<input>self.play(Write(Text("Hello World")))</input>
<output>Text appears character by character (handwriting effect)</output>
</example>

<example>
<signature>Unwrite(vmobject: VMobject, reverse: bool = True, **kwargs) -> Unwrite</signature>
<input>self.play(Unwrite(text))</input>
<output>Text erases itself (reverse Write animation)</output>
</example>

<example>
<signature>AddTextLetterByLetter(text: Text, time_per_char: float = 0.1, **kwargs) -> AddTextLetterByLetter</signature>
<input>self.play(AddTextLetterByLetter(Text("Hello"), time_per_char=0.15))</input>
<output>Letters appear one at a time, each taking 0.15 seconds</output>
</example>

<example>
<signature>RemoveTextLetterByLetter(text: Text, time_per_char: float = 0.1, **kwargs) -> RemoveTextLetterByLetter</signature>
<input>self.play(RemoveTextLetterByLetter(text))</input>
<output>Letters disappear one at a time (reverse of AddTextLetterByLetter)</output>
</example>

<example>
<signature>TypeWithCursor(text: Text, cursor: Mobject, buff: float = 0.1, **kwargs) -> TypeWithCursor</signature>
<input>
text = Text("Typing...").to_edge(LEFT)
cursor = Rectangle(width=0.1, height=0.5, fill_opacity=1).move_to(text[0])
self.play(TypeWithCursor(text, cursor))
</input>
<output>Letters appear one by one with a blinking cursor trailing</output>
</example>

<example>
<signature>SpiralIn(shapes: Mobject, scale_factor: float = 8, fade_in_fraction: float = 0.3, **kwargs) -> SpiralIn</signature>
<input>self.play(SpiralIn(VGroup(circle, square)))</input>
<output>Submobjects fly in on spiral trajectories from outside the frame</output>
</example>

<example>
<signature>ShowIncreasingSubsets(group: Mobject, **kwargs) -> ShowIncreasingSubsets</signature>
<input>self.play(ShowIncreasingSubsets(VGroup(d1, d2, d3, d4)))</input>
<output>Submobjects appear one at a time, all remaining visible</output>
</example>

<example>
<signature>ShowSubmobjectsOneByOne(group: Iterable[Mobject], **kwargs) -> ShowSubmobjectsOneByOne</signature>
<input>self.play(ShowSubmobjectsOneByOne(VGroup(a, b, c)))</input>
<output>Only one submobject visible at a time; each replaces the previous</output>
</example>

<!-- ─────────────────────────── FADING ANIMATIONS ─────────────────────────── -->

<example>
<signature>FadeIn(*mobjects: Mobject, shift: np.ndarray | None = None, scale: float = 1, **kwargs) -> FadeIn</signature>
<input>self.play(FadeIn(title, shift=DOWN))</input>
<output>title fades in while sliding downward</output>
</example>

<example>
<signature>FadeOut(*mobjects: Mobject, shift: np.ndarray | None = None, scale: float = 1, **kwargs) -> FadeOut</signature>
<input>self.play(FadeOut(circle, shift=LEFT))</input>
<output>circle fades out while sliding left</output>
</example>

<example>
<signature>FadeIn with target_position (fly-in from another mobject)</signature>
<input>self.play(FadeIn(label, target_position=dot, scale=0.5))</input>
<output>label starts tiny at dot's position, grows to full size while fading in</output>
</example>

<!-- ─────────────────────────── TRANSFORM ANIMATIONS ─────────────────────────── -->

<example>
<signature>Transform(mobject: Mobject, target_mobject: Mobject, path_arc: float = 0, **kwargs) -> Transform</signature>
<input>self.play(Transform(square, circle))</input>
<output>square morphs into circle visually (square object remains in scene)</output>
</example>

<example>
<signature>ReplacementTransform(mobject: Mobject, target_mobject: Mobject, **kwargs) -> ReplacementTransform</signature>
<input>self.play(ReplacementTransform(square, circle))</input>
<output>square morphs into circle and circle replaces square in the scene</output>
</example>

<example>
<signature>TransformFromCopy(mobject: Mobject, target_mobject: Mobject, **kwargs) -> TransformFromCopy</signature>
<input>self.play(TransformFromCopy(source, target))</input>
<output>source stays put; a copy of source transforms into target</output>
</example>

<example>
<signature>ClockwiseTransform(mobject: Mobject, target_mobject: Mobject, **kwargs) -> ClockwiseTransform</signature>
<input>self.play(ClockwiseTransform(circle, square))</input>
<output>Points arc clockwise (path_arc=-PI) as they move to target positions</output>
</example>

<example>
<signature>CounterclockwiseTransform(mobject: Mobject, target_mobject: Mobject, **kwargs)</signature>
<input>self.play(CounterclockwiseTransform(square, triangle))</input>
<output>Points arc counterclockwise (path_arc=PI) to target positions</output>
</example>

<example>
<signature>MoveToTarget(mobject: Mobject, **kwargs) -> MoveToTarget</signature>
<input>
mob.generate_target()
mob.target.scale(2).set_color(RED)
self.play(MoveToTarget(mob))
</input>
<output>Animates mob to its .target state</output>
</example>

<example>
<signature>Restore(mobject: Mobject, **kwargs) -> Restore</signature>
<input>
s = Square()
s.save_state()
self.play(s.animate.scale(3).set_color(RED))
self.play(Restore(s))
</input>
<output>Animates s back to its last saved state</output>
</example>

<example>
<signature>FadeToColor(mobject: Mobject, color: str, **kwargs) -> FadeToColor</signature>
<input>self.play(FadeToColor(text, RED))</input>
<output>Animates a color change to red</output>
</example>

<example>
<signature>ScaleInPlace(mobject: Mobject, scale_factor: float, **kwargs) -> ScaleInPlace</signature>
<input>self.play(ScaleInPlace(mob, 2))</input>
<output>Doubles mob's size in place (about its center)</output>
</example>

<example>
<signature>ShrinkToCenter(mobject: Mobject, **kwargs) -> ShrinkToCenter</signature>
<input>self.play(ShrinkToCenter(mob))</input>
<output>mob shrinks to a point at its center and disappears</output>
</example>

<example>
<signature>CyclicReplace(*mobjects: Mobject, path_arc: float = 90 * DEGREES, **kwargs) -> CyclicReplace</signature>
<input>
group = VGroup(Square(), Circle(), Triangle(), Star()).arrange(RIGHT)
self.play(CyclicReplace(*group))
</input>
<output>Each mobject moves to the position of the next one (cyclically)</output>
</example>

<example>
<signature>FadeTransform(mobject: Mobject, target_mobject: Mobject, stretch: bool = True, **kwargs) -> FadeTransform</signature>
<input>self.play(FadeTransform(rect, circle))</input>
<output>rect fades out while circle fades in, stretching between shapes</output>
</example>

<example>
<signature>ApplyMatrix(matrix: np.ndarray, mobject: Mobject, about_point: np.ndarray = ORIGIN, **kwargs) -> ApplyMatrix</signature>
<input>
matrix = [[1, 1], [0, 1]]  # shear matrix
self.play(ApplyMatrix(matrix, square))
</input>
<output>Applies a 2x2 (or 3x3) linear transformation matrix to all points of the mobject</output>
</example>

<example>
<signature>ApplyPointwiseFunction(function: Callable, mobject: Mobject, run_time: float = 3, **kwargs)</signature>
<input>self.play(ApplyPointwiseFunction(lambda p: p + np.sin(p[0]) * UP, plane))</input>
<output>Warps every point of the mobject by the given function</output>
</example>

<example>
<signature>TransformMatchingShapes(mobject: Mobject, target: Mobject, **kwargs) -> TransformMatchingShapes</signature>
<input>self.play(TransformMatchingShapes(eq1, eq2))</input>
<output>Matches submobjects by shape similarity before transforming; unmatched parts fade</output>
</example>

<example>
<signature>TransformMatchingTex(mobject: MathTex, target: MathTex, **kwargs) -> TransformMatchingTex</signature>
<input>self.play(TransformMatchingTex(MathTex("x^2"), MathTex("x^3")))</input>
<output>Matches LaTeX substrings by content before transforming; great for equation morphing</output>
</example>

<!-- ─────────────────────────── GROWING ANIMATIONS ─────────────────────────── -->

<example>
<signature>GrowFromPoint(mobject: Mobject, point: Point3DLike, **kwargs) -> GrowFromPoint</signature>
<input>self.play(GrowFromPoint(square, ORIGIN))</input>
<output>square grows from the origin outward to its full size</output>
</example>

<example>
<signature>GrowFromCenter(mobject: Mobject, **kwargs) -> GrowFromCenter</signature>
<input>self.play(GrowFromCenter(circle))</input>
<output>circle grows from its own center</output>
</example>

<example>
<signature>GrowFromEdge(mobject: Mobject, edge: Vector3DLike, **kwargs) -> GrowFromEdge</signature>
<input>self.play(GrowFromEdge(rect, DOWN))</input>
<output>rect grows upward from its bottom edge</output>
</example>

<example>
<signature>GrowArrow(arrow: Arrow, **kwargs) -> GrowArrow</signature>
<input>self.play(GrowArrow(Arrow(LEFT * 2, RIGHT * 2)))</input>
<output>Arrow grows from its start point toward its tip</output>
</example>

<example>
<signature>SpinInFromNothing(mobject: Mobject, angle: float = PI / 2, **kwargs) -> SpinInFromNothing</signature>
<input>self.play(SpinInFromNothing(star, angle=PI))</input>
<output>star spins in while growing from its center</output>
</example>

<!-- ─────────────────────────── ROTATION ANIMATIONS ─────────────────────────── -->

<example>
<signature>Rotate(mobject: Mobject, angle: float = PI, axis: Vector3DLike = OUT, about_point: Point3DLike | None = None, **kwargs) -> Rotate</signature>
<input>self.play(Rotate(square, angle=PI/2, about_point=ORIGIN))</input>
<output>Rotates square 90° around the origin (interpolated via Transform arc path)</output>
</example>

<example>
<signature>Rotating(mobject: Mobject, angle: float = TAU, axis: Vector3DLike = OUT, run_time: float = 5, rate_func: Callable = linear, **kwargs) -> Rotating</signature>
<input>self.play(Rotating(gear, angle=TAU, run_time=3, rate_func=linear))</input>
<output>Continuously rotates gear one full revolution (no Transform interpolation)</output>
</example>

<!-- ─────────────────────────── INDICATION ANIMATIONS ─────────────────────────── -->

<example>
<signature>Indicate(mobject: Mobject, scale_factor: float = 1.2, color: ParsableManimColor = PURE_YELLOW, **kwargs) -> Indicate</signature>
<input>self.play(Indicate(equation))</input>
<output>equation briefly scales up and turns yellow, then returns to normal</output>
</example>

<example>
<signature>Flash(point: Point3DLike | Mobject, line_length: float = 0.2, num_lines: int = 12, color: ParsableManimColor = PURE_YELLOW, run_time: float = 1.0, **kwargs) -> Flash</signature>
<input>self.play(Flash(dot, color=YELLOW, line_length=0.5))</input>
<output>Radiates short lines outward from the point (starburst effect)</output>
</example>

<example>
<signature>FocusOn(focus_point: Point3DLike | Mobject, opacity: float = 0.2, color: ParsableManimColor = GREY, run_time: float = 2, **kwargs) -> FocusOn</signature>
<input>self.play(FocusOn(dot))</input>
<output>A large semi-transparent dot shrinks down to the focus point</output>
</example>

<example>
<signature>ShowPassingFlash(mobject: VMobject, time_width: float = 0.1, **kwargs) -> ShowPassingFlash</signature>
<input>self.play(ShowPassingFlash(circle.copy().set_color(YELLOW), time_width=0.3))</input>
<output>A glowing sliver travels around the circle's stroke path</output>
</example>

<example>
<signature>Circumscribe(mobject: Mobject, shape: type = Rectangle, fade_in: bool = False, fade_out: bool = False, color: ParsableManimColor = PURE_YELLOW, run_time: float = 1, **kwargs) -> Circumscribe</signature>
<input>self.play(Circumscribe(label, color=RED, fade_out=True))</input>
<output>Draws a highlighted rectangle around the label then fades it out</output>
</example>

<example>
<signature>ApplyWave(mobject: Mobject, direction: Vector3DLike = UP, amplitude: float = 0.2, run_time: float = 2, **kwargs) -> ApplyWave</signature>
<input>self.play(ApplyWave(text, amplitude=0.3))</input>
<output>A wave ripples through the text distorting it temporarily</output>
</example>

<example>
<signature>Wiggle(mobject: Mobject, scale_value: float = 1.1, rotation_angle: float = 0.01 * TAU, n_wiggles: int = 6, run_time: float = 2, **kwargs) -> Wiggle</signature>
<input>self.play(Wiggle(label, n_wiggles=4))</input>
<output>label wobbles back and forth n_wiggles times</output>
</example>

<example>
<signature>Blink(mobject: Mobject, time_on: float = 0.5, time_off: float = 0.5, blinks: int = 1, **kwargs) -> Blink</signature>
<input>self.play(Blink(cursor, blinks=3))</input>
<output>cursor flashes on/off 3 times</output>
</example>

<!-- ─────────────────────────── MOVEMENT ANIMATIONS ─────────────────────────── -->

<example>
<signature>MoveAlongPath(mobject: Mobject, path: VMobject, **kwargs) -> MoveAlongPath</signature>
<input>
path = Arc(radius=2, angle=PI)
self.play(MoveAlongPath(dot, path, rate_func=linear))
</input>
<output>dot travels along the arc at constant speed</output>
</example>

<example>
<signature>Homotopy(homotopy: Callable[[float,float,float,float], tuple], mobject: Mobject, run_time: float = 3, **kwargs) -> Homotopy</signature>
<input>
def ripple(x, y, z, t):
    return (x, y + 0.2 * np.sin(x * PI + t * TAU), z)
self.play(Homotopy(ripple, text))
</input>
<output>Every point (x,y,z) is transformed by the function at time t∈[0,1]</output>
</example>

<!-- ─────────────────────────── COMPOSITION ANIMATIONS ─────────────────────────── -->

<example>
<signature>AnimationGroup(*animations: Animation, lag_ratio: float = 0, run_time: float | None = None, **kwargs) -> AnimationGroup</signature>
<input>self.play(AnimationGroup(FadeIn(a), FadeIn(b), FadeIn(c), lag_ratio=0))</input>
<output>All three mobjects fade in simultaneously</output>
</example>

<example>
<signature>LaggedStart(*animations: Animation, lag_ratio: float = 0.05, **kwargs) -> LaggedStart</signature>
<input>self.play(LaggedStart(*[Create(s) for s in squares], lag_ratio=0.2))</input>
<output>Squares create one after another with 20% overlap between starts</output>
</example>

<example>
<signature>Succession(*animations: Animation, lag_ratio: float = 1, **kwargs) -> Succession</signature>
<input>
self.play(Succession(
    Create(circle),
    FadeIn(label),
    circle.animate.shift(UP),
))
</input>
<output>Plays each animation fully before starting the next</output>
</example>

<example>
<signature>LaggedStartMap(animation_class: type[Animation], mobject: Mobject, arg_creator: Callable | None = None, run_time: float = 2, lag_ratio: float = 0.05, **kwargs) -> LaggedStartMap</signature>
<input>self.play(LaggedStartMap(FadeIn, VGroup(*dots), run_time=3, lag_ratio=0.1))</input>
<output>Applies FadeIn to each dot in sequence with staggered timing</output>
</example>

<!-- ─────────────────────────── NUMBER ANIMATIONS ─────────────────────────── -->

<example>
<signature>ChangingDecimal(decimal_mob: DecimalNumber, number_update_func: Callable[[float], float], **kwargs) -> ChangingDecimal</signature>
<input>
number = DecimalNumber(0)
self.play(ChangingDecimal(number, lambda a: 100 * a, run_time=3))
</input>
<output>number counts from 0 to 100 over 3 seconds (a goes 0→1)</output>
</example>

<example>
<signature>ChangeDecimalToValue(decimal_mob: DecimalNumber, target_number: int, **kwargs) -> ChangeDecimalToValue</signature>
<input>self.play(ChangeDecimalToValue(counter, 42, run_time=2))</input>
<output>counter animates from its current value to 42</output>
</example>

<!-- ─────────────────────────── .animate SYNTAX ─────────────────────────── -->

<example>
<signature>Mobject.animate -> _AnimationBuilder</signature>
<input>self.play(circle.animate.shift(UP).set_color(RED), run_time=1.5)</input>
<output>circle shifts up and turns red over 1.5 seconds</output>
</example>

<example>
<signature>.animate chaining with multiple properties</signature>
<input>
self.play(
    rect.animate.scale(0.5).set_fill(BLUE, opacity=0.8).to_edge(LEFT),
    run_time=2,
    rate_func=smooth,
)
</input>
<output>rect shrinks, turns blue, and slides left in one smooth 2-second animation</output>
</example>

<!-- ─────────────────────────── COORDINATE SYSTEMS ─────────────────────────── -->

<example>
<signature>Axes(x_range: Sequence[float] | None = None, y_range: Sequence[float] | None = None, x_length: float | None = None, y_length: float | None = None, tips: bool = True, **kwargs) -> Axes</signature>
<input>Axes(x_range=[-3, 3, 1], y_range=[-1, 1, 0.5])</input>
<output>A set of axes from -3 to 3 (x) and -1 to 1 (y) with tick marks at every step</output>
</example>

<example>
<signature>Axes.plot(self, function: Callable[[float], float], x_range: Sequence[float] | None = None, **kwargs) -> ParametricFunction</signature>
<input>graph = axes.plot(lambda x: np.sin(x), color=BLUE)</input>
<output>A blue sine curve ParametricFunction mobject plotted on the axes</output>
</example>

<example>
<signature>Axes.plot_parametric_curve(self, function: Callable[[float], np.ndarray], t_range: Sequence[float], **kwargs)</signature>
<input>axes.plot_parametric_curve(lambda t: [np.cos(t), np.sin(t), 0], t_range=[0, TAU])</input>
<output>A circle traced by the parametric function</output>
</example>

<example>
<signature>Axes.get_area(self, graph: ParametricFunction, x_range: tuple[float, float] | None = None, color: ParsableManimColor = WHITE, opacity: float = 0.3, **kwargs)</signature>
<input>
axes = Axes(x_range=[0, 4], y_range=[0, 5])
graph = axes.plot(lambda x: x ** 2 - 2, color=BLUE)
area = axes.get_area(graph, x_range=(1, 3), color=BLUE, opacity=0.3)
</input>
<output>A shaded region under the curve between x=1 and x=3</output>
</example>

<example>
<signature>Axes.get_graph_label(self, graph: ParametricFunction, label: str | Mobject = "f(x)", x_val: float | None = None, direction: Vector3DLike = UR, **kwargs)</signature>
<input>label = axes.get_graph_label(graph, label=MathTex("f(x)"), x_val=2, direction=UR)</input>
<output>A label placed next to the graph at x=2 pointing upper-right</output>
</example>

<example>
<signature>Axes.get_vertical_line / get_horizontal_line</signature>
<input>
v_line = axes.get_vertical_line(axes.c2p(2, 0), color=YELLOW)
h_line = axes.get_horizontal_line(axes.c2p(0, np.sin(2)), color=RED)
</input>
<output>A vertical line at x=2 and a horizontal line at y=sin(2)</output>
</example>

<example>
<signature>Axes.coords_to_point / c2p and point_to_coords / p2c</signature>
<input>
point = axes.c2p(2, 3)      # data coords (2,3) → screen position
coords = axes.p2c(some_pt)  # screen position → data coords
</input>
<output>Convert between axis coordinate space and scene coordinate space</output>
</example>

<example>
<signature>Axes.get_x_axis_label / get_y_axis_label</signature>
<input>
x_label = axes.get_x_axis_label(MathTex("x"))
y_label = axes.get_y_axis_label(MathTex("f(x)"), edge=LEFT, direction=LEFT)
</input>
<output>Labels positioned at the ends of the x and y axes</output>
</example>

<example>
<signature>NumberPlane(x_range: Sequence[float] | None = None, y_range: Sequence[float] | None = None, **kwargs) -> NumberPlane</signature>
<input>NumberPlane(x_range=[-5, 5], y_range=[-5, 5])</input>
<output>A coordinate grid with axis lines and background grid lines</output>
</example>

<example>
<signature>PolarPlane(radius_max: float = 4, size: float = 6, **kwargs) -> PolarPlane</signature>
<input>PolarPlane(radius_max=3, size=6, azimuth_units="PI radians")</input>
<output>A polar coordinate grid with radius rings and angle lines</output>
</example>

<example>
<signature>ComplexPlane(**kwargs) -> ComplexPlane</signature>
<input>plane = ComplexPlane().add_coordinates()</input>
<output>A NumberPlane labeled with complex numbers along the axes</output>
</example>

<example>
<signature>ThreeDAxes(**kwargs) -> ThreeDAxes</signature>
<input>ThreeDAxes(x_range=[-4, 4], y_range=[-4, 4], z_range=[-3, 3])</input>
<output>3D coordinate axes with X, Y, Z lines</output>
</example>

<example>
<signature>NumberLine(x_range: Sequence[float] | None = None, length: float | None = None, unit_size: float = 1, **kwargs) -> NumberLine</signature>
<input>NumberLine(x_range=[-3, 3, 1], length=6, include_numbers=True)</input>
<output>A labeled number line from -3 to 3</output>
</example>

<example>
<signature>NumberLine.n2p(x) and p2n(point) (number-to-point and point-to-number)</signature>
<input>
nl = NumberLine(x_range=[-5, 5])
pos = nl.n2p(2.5)  # screen position of the value 2.5
val = nl.p2n(pos)  # data value at that position
</input>
<output>Converts between numeric values and scene coordinates on the number line</output>
</example>

<!-- ─────────────────────────── FUNCTION GRAPHS ─────────────────────────── -->

<example>
<signature>ParametricFunction(function: Callable[[float], Point3D], t_range: Sequence[float] = [0, 1], use_smoothing: bool = True, **kwargs) -> ParametricFunction</signature>
<input>
curve = ParametricFunction(
    lambda t: np.array([np.cos(t), np.sin(t), 0]),
    t_range=[0, TAU],
    color=RED,
)
</input>
<output>A red circle drawn by the parametric function</output>
</example>

<example>
<signature>FunctionGraph(function: Callable[[float], float], x_range: Sequence[float] | None = None, **kwargs) -> FunctionGraph</signature>
<input>FunctionGraph(lambda x: np.sin(x), x_range=[-PI, PI], color=BLUE)</input>
<output>A blue sine wave not attached to any Axes object</output>
</example>

<!-- ─────────────────────────── 3D MOBJECTS ─────────────────────────── -->

<example>
<signature>Sphere(center: Point3DLike = ORIGIN, radius: float = 1, **kwargs) -> Sphere</signature>
<input>Sphere(radius=1.5, color=BLUE_D)</input>
<output>A 3D sphere with a checkerboard surface pattern</output>
</example>

<example>
<signature>Cylinder(radius: float = 1, height: float = 2, direction: Vector3DLike = Z_AXIS, **kwargs) -> Cylinder</signature>
<input>Cylinder(radius=0.5, height=3, color=GREEN)</input>
<output>A 3D cylinder standing along the Z axis</output>
</example>

<example>
<signature>Cone(base_radius: float = 1, height: float = 2, direction: Vector3DLike = Z_AXIS, **kwargs) -> Cone</signature>
<input>Cone(base_radius=1, height=2, color=RED)</input>
<output>A 3D cone pointing upward</output>
</example>

<example>
<signature>Cube(side_length: float = 2, **kwargs) -> Cube</signature>
<input>Cube(side_length=1.5, fill_opacity=0.5, color=BLUE)</input>
<output>A 3D cube with semi-transparent blue faces</output>
</example>

<example>
<signature>Torus(major_radius: float = 3, minor_radius: float = 1, **kwargs) -> Torus</signature>
<input>Torus(major_radius=2, minor_radius=0.5, color=YELLOW)</input>
<output>A 3D donut shape</output>
</example>

<example>
<signature>Surface(func: Callable[[float, float], np.ndarray], u_range: tuple = (0, 1), v_range: tuple = (0, 1), resolution: int | Sequence[int] = 32, **kwargs) -> Surface</signature>
<input>
axes = ThreeDAxes()
surface = Surface(
    lambda u, v: axes.c2p(u, v, np.sin(u) * np.cos(v)),
    u_range=[-PI, PI],
    v_range=[-PI, PI],
    checkerboard_colors=[BLUE_D, BLUE_E],
)
</input>
<output>A parametric 3D surface with alternating checkerboard coloring</output>
</example>

<example>
<signature>Arrow3D(start: Point3DLike = LEFT, end: Point3DLike = RIGHT, **kwargs) -> Arrow3D</signature>
<input>Arrow3D(start=ORIGIN, end=[1, 1, 1], color=RED)</input>
<output>A 3D arrow with a cone tip</output>
</example>

<example>
<signature>Line3D(start: Point3DLike = LEFT, end: Point3DLike = RIGHT, **kwargs) -> Line3D</signature>
<input>Line3D(start=ORIGIN, end=UP * 2, color=WHITE)</input>
<output>A 3D line as a thin cylinder between two points</output>
</example>

<example>
<signature>Dot3D(point: Point3DLike = ORIGIN, radius: float = 0.08, **kwargs) -> Dot3D</signature>
<input>Dot3D(point=[1, 2, 0], color=YELLOW)</input>
<output>A small 3D sphere dot at the given point</output>
</example>

<!-- ─────────────────────────── GRAPH THEORY ─────────────────────────── -->

<example>
<signature>Graph(vertices: list[Hashable], edges: list[tuple], layout: str = "spring", layout_scale: float = 2, labels: bool = False, **kwargs) -> Graph</signature>
<input>
graph = Graph(
    [1, 2, 3, 4, 5],
    [(1, 2), (2, 3), (3, 4), (4, 5), (1, 5), (2, 5)],
    layout="circular",
    labels=True,
)
self.add(graph)
</input>
<output>A circular-layout labeled graph with 5 vertices and 6 edges</output>
</example>

<example>
<signature>Graph layout options</signature>
<input>
# Available layouts: "circular", "kamada_kawai", "planar",
# "random", "shell", "spectral", "partite", "tree", "spring"
Graph([1,2,3], [(1,2),(2,3)], layout="spring", layout_scale=3)
</input>
<output>A graph with automatic spring-force layout</output>
</example>

<example>
<signature>DiGraph(vertices, edges, **kwargs) -> DiGraph</signature>
<input>
digraph = DiGraph(
    [1, 2, 3],
    [(1, 2), (2, 3), (3, 1)],
    layout="circular",
    edge_config={(1,2): {"color": RED}},
)
</input>
<output>A directed graph with arrows on edges; edge colors can be configured per-edge</output>
</example>

<!-- ─────────────────────────── MATRICES ─────────────────────────── -->

<example>
<signature>Matrix(matrix: list[list], left_bracket: str = "[", right_bracket: str = "]", **kwargs) -> Matrix</signature>
<input>Matrix([[1, 2], [3, 4]])</input>
<output>A LaTeX-formatted 2x2 matrix with square brackets</output>
</example>

<example>
<signature>IntegerMatrix / DecimalMatrix / MobjectMatrix</signature>
<input>
m1 = IntegerMatrix([[1, 2], [3, 4]], left_bracket="(", right_bracket=")")
m2 = DecimalMatrix([[1.5, 2.3], [0.1, 9.8]], element_to_mobject_config={"num_decimal_places": 1})
m3 = MobjectMatrix([[Circle().scale(0.3), Square().scale(0.3)]])
</input>
<output>Integer matrix with parens; decimal matrix; matrix where cells are arbitrary mobjects</output>
</example>

<!-- ─────────────────────────── TABLES ─────────────────────────── -->

<example>
<signature>Table(table: list[list], row_labels: list | None = None, col_labels: list | None = None, include_outer_lines: bool = False, **kwargs) -> Table</signature>
<input>
table = Table(
    [["Alice", "85"], ["Bob", "92"], ["Carol", "78"]],
    col_labels=[Text("Name"), Text("Score")],
    include_outer_lines=True,
)
</input>
<output>A table with column labels and outer border lines</output>
</example>

<example>
<signature>Table highlight and animation methods</signature>
<input>
table.add_highlighted_cell((2, 2), color=YELLOW)
self.play(table.create())         # animates all elements appearing
self.play(Write(table))           # writes cells one by one
</input>
<output>Highlights a cell and animates the table being drawn</output>
</example>

<example>
<signature>MathTable / IntegerTable / DecimalTable</signature>
<input>
MathTable([[r"\pi", r"e"], [r"\sqrt{2}", r"\phi"]], include_outer_lines=True)
IntegerTable([[1, 2, 3], [4, 5, 6]])
DecimalTable([[1.1, 2.2], [3.3, 4.4]])
</input>
<output>Tables using MathTex, Integer, or DecimalNumber renderers for cells</output>
</example>

<!-- ─────────────────────────── BRACE ─────────────────────────── -->

<example>
<signature>Brace(mobject: Mobject, direction: Vector3DLike = DOWN, buff: float = 0.2, **kwargs) -> Brace</signature>
<input>
eq = MathTex("a + b + c")
brace = Brace(eq, direction=DOWN)
label = brace.get_tex("a+b+c")
self.add(eq, brace, label)
</input>
<output>A curly brace below the equation with a label at its tip</output>
</example>

<example>
<signature>BraceBetweenPoints(point_1: Point3DLike, point_2: Point3DLike, direction: Vector3DLike = UP, **kwargs) -> BraceBetweenPoints</signature>
<input>BraceBetweenPoints(LEFT * 2, RIGHT * 2, direction=UP)</input>
<output>A curly brace spanning between two points, opening upward</output>
</example>

<example>
<signature>Brace.get_text / get_tex / put_at_tip</signature>
<input>
brace = Brace(square, DOWN)
label = brace.get_text("side")       # Text label
tex   = brace.get_tex(r"\ell")       # MathTex label
# Both automatically position at the tip
</input>
<output>Convenience methods to create a labeled mobject positioned at the brace tip</output>
</example>

<!-- ─────────────────────────── RATE FUNCTIONS ─────────────────────────── -->

<example>
<signature>rate_func options for self.play() or Animation constructors</signature>
<input>
# smooth         — ease in-out (default for most animations)
# linear         — constant speed
# there_and_back — goes to target then returns to start
# rush_into      — fast start, slow end
# rush_from      — slow start, fast end
# double_smooth  — smooth applied twice (very smooth ease in-out)
# exponential_decay — starts fast, decays exponentially
# lingering      — animation rushes in then stays near target

self.play(circle.animate.shift(RIGHT), rate_func=there_and_back, run_time=2)
</input>
<output>circle slides right and comes back over 2 seconds</output>
</example>

<example>
<signature>Standard easing (from rate_functions module, not exported by default)</signature>
<input>
from manim.utils import rate_functions
self.play(dot.animate.shift(RIGHT * 4), rate_func=rate_functions.ease_in_out_sine)
</input>
<output>Uses standard CSS-style easing functions: ease_in_sine, ease_out_sine, ease_in_out_sine, ease_in_cubic, ease_in_out_bounce, etc.</output>
</example>

<!-- ─────────────────────────── 3D CAMERA ─────────────────────────── -->

<example>
<signature>ThreeDScene.set_camera_orientation(phi, theta, gamma, zoom, frame_center)</signature>
<input>
# phi:   polar angle from Z axis (0=top, 90°=side)
# theta: azimuthal spin around Z axis
self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
</input>
<output>Sets the 3D camera to look from a standard perspective angle</output>
</example>

<example>
<signature>ThreeDScene.begin_ambient_camera_rotation(rate, about)</signature>
<input>
self.begin_ambient_camera_rotation(rate=0.15, about="theta")
self.wait(4)
self.stop_ambient_camera_rotation()
</input>
<output>Camera slowly rotates around the scene for 4 seconds then stops</output>
</example>

<example>
<signature>ThreeDScene.move_camera(phi, theta, run_time, **kwargs)</signature>
<input>self.move_camera(phi=60 * DEGREES, theta=60 * DEGREES, run_time=2)</input>
<output>Animates the camera smoothly moving to the new orientation over 2 seconds</output>
</example>

<!-- ─────────────────────────── MOVING CAMERA ─────────────────────────── -->

<example>
<signature>MovingCameraScene.camera.frame — animatable camera rectangle</signature>
<input>
# Zoom in on a region
self.play(self.camera.frame.animate.move_to(focus_point).set(width=3))
# Zoom out to full scene
self.play(self.camera.frame.animate.move_to(ORIGIN).set(width=14))
</input>
<output>Pans and zooms the camera frame to any region of the scene</output>
</example>

<example>
<signature>MovingCamera.auto_zoom(mobjects, margin=0, animate=True)</signature>
<input>
group = VGroup(circle, label)
self.play(self.camera.auto_zoom(group, margin=1))
</input>
<output>Camera automatically adjusts to frame the given mobjects with a margin</output>
</example>

<!-- ─────────────────────────── COMPLEX SCENE EXAMPLES ─────────────────────────── -->

<example>
<signature>Full scene: function plot with ValueTracker</signature>
<input>
class FunctionPlotScene(Scene):
    def construct(self):
        axes = Axes(x_range=[-3, 3, 1], y_range=[-2, 2, 1], x_length=7, y_length=5)
        labels = axes.get_axis_labels(MathTex("x"), MathTex("f(x)"))

        tracker = ValueTracker(1)

        graph = always_redraw(
            lambda: axes.plot(
                lambda x: tracker.get_value() * np.sin(x),
                color=BLUE,
            )
        )

        self.add(axes, labels, graph)
        self.play(tracker.animate.set_value(2), run_time=3)
        self.play(tracker.animate.set_value(0.5), run_time=2)
        self.wait()
</input>
<output>A sine curve whose amplitude is controlled by a ValueTracker, updated live</output>
</example>

<example>
<signature>always_redraw — shorthand for add_updater that rebuilds each frame</signature>
<input>
# always_redraw(func) creates a mobject that calls func() and becomes
# the result every frame. Equivalent to mob.add_updater(lambda m: m.become(func()))
dot = always_redraw(lambda: Dot(axes.c2p(tracker.get_value(), 0), color=RED))
self.add(dot)
</input>
<output>dot is re-created every frame at the current tracker position</output>
</example>

<example>
<signature>Full scene: equation morphing with TransformMatchingTex</signature>
<input>
class EquationMorph(Scene):
    def construct(self):
        eq1 = MathTex("e^{i\\theta}", "=", "\\cos(\\theta)", "+", "i\\sin(\\theta)")
        eq2 = MathTex("e^{i\\pi}", "=", "\\cos(\\pi)", "+", "i\\sin(\\pi)")
        eq3 = MathTex("e^{i\\pi}", "+", "1", "=", "0")

        self.play(Write(eq1))
        self.wait()
        self.play(TransformMatchingTex(eq1, eq2))
        self.wait()
        self.play(TransformMatchingTex(eq2, eq3))
        self.wait()
</input>
<output>Euler's formula morphing into the identity equation with matching sub-expressions</output>
</example>

<example>
<signature>Full scene: 3D surface</signature>
<input>
class SaddleSurface(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        surface = Surface(
            lambda u, v: axes.c2p(u, v, u**2 - v**2),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=16,
            checkerboard_colors=[BLUE_D, BLUE_E],
        )
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)
        self.add(axes, surface)
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(5)
</input>
<output>A rotating 3D saddle surface z = x² − y²</output>
</example>

<example>
<signature>Full scene: graph theory with animation</signature>
<input>
class GraphScene(Scene):
    def construct(self):
        g = Graph(
            [1, 2, 3, 4, 5, 6],
            [(1,2),(2,3),(3,4),(4,5),(5,6),(6,1),(1,4),(2,5)],
            layout="circular",
            layout_scale=2.5,
            labels=True,
            vertex_config={1: {"color": RED}},
            edge_config={(1,4): {"color": YELLOW}},
        )
        self.play(Create(g))
        self.play(g.vertices[3].animate.set_color(GREEN))
        self.wait()
</input>
<output>A circular labeled graph with custom vertex and edge colors, created with animation</output>
</example>

<example>
<signature>Full scene: LaTeX proof layout</signature>
<input>
class ProofScene(Scene):
    def construct(self):
        title = Title(r"Pythagorean Theorem")
        statement = MathTex(r"a^2 + b^2 = c^2").scale(1.5)
        proof_steps = VGroup(
            MathTex(r"\text{Let } \triangle ABC \text{ be a right triangle}"),
            MathTex(r"a^2 + b^2 = c^2 \quad \square"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).scale(0.8)

        self.add(title)
        self.play(Write(statement))
        self.wait()
        self.play(statement.animate.to_edge(UP, buff=1.5))
        self.play(LaggedStart(*[FadeIn(s, shift=RIGHT) for s in proof_steps], lag_ratio=0.3))
        self.wait()
</input>
<output>A structured proof with a title, main equation, and staggered proof step reveal</output>
</example>
