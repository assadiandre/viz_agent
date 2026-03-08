# Manim Animations Reference
> Manim v0.20.1

---

## Creation / Introduction

### `Create`
Incrementally draws a VMobject onto the scene along its path.
```python
Create(
    mobject: VMobject,
    lag_ratio: float = 1.0,
    introducer: bool = True,
    **kwargs,
)
```

### `Uncreate`
Reverses `Create` — erases a VMobject along its path.
```python
Uncreate(
    mobject: VMobject,
    reverse_rate_function: bool = True,
    remover: bool = True,
    **kwargs,
)
```

### `DrawBorderThenFill`
Draws the stroke of a VMobject first, then fills it in.
```python
DrawBorderThenFill(
    vmobject: VMobject,
    run_time: float = 2,
    rate_func: Callable = double_smooth,
    stroke_width: float = 2,
    stroke_color: str = None,
    introducer: bool = True,
    **kwargs,
)
```

### `Write`
Simulates hand-writing text or hand-drawing a VMobject.
```python
Write(
    vmobject: VMobject,
    rate_func: Callable = linear,
    reverse: bool = False,
    **kwargs,
)
```

### `Unwrite`
Simulates erasing text or a VMobject by hand.
```python
Unwrite(
    vmobject: VMobject,
    rate_func: Callable = linear,
    reverse: bool = True,
    **kwargs,
)
```

### `SpiralIn`
Introduces submobjects by flying them in along spiral trajectories.
```python
SpiralIn(
    shapes: Mobject,
    scale_factor: float = 8,
    fade_in_fraction: float = 0.3,
    **kwargs,
)
```

### `ShowIncreasingSubsets`
Reveals submobjects one by one, leaving all previous ones visible.
```python
ShowIncreasingSubsets(
    group: Mobject,
    suspend_mobject_updating: bool = False,
    int_func: Callable = np.floor,
    reverse_rate_function: bool = False,
    **kwargs,
)
```

### `ShowSubmobjectsOneByOne`
Shows one submobject at a time, removing the previous one before showing the next.
```python
ShowSubmobjectsOneByOne(
    group: Iterable[Mobject],
    int_func: Callable = np.ceil,
    **kwargs,
)
```

### `AddTextLetterByLetter`
Reveals a `Text` mobject character by character.
```python
AddTextLetterByLetter(
    text: Text,
    suspend_mobject_updating: bool = False,
    int_func: Callable = np.ceil,
    rate_func: Callable = linear,
    time_per_char: float = 0.1,
    run_time: float | None = None,
    reverse_rate_function: bool = False,
    introducer: bool = True,
    **kwargs,
)
```

### `RemoveTextLetterByLetter`
Removes a `Text` mobject character by character.
```python
RemoveTextLetterByLetter(
    text: Text,
    time_per_char: float = 0.1,
    **kwargs,
)
```

### `TypeWithCursor`
Like `AddTextLetterByLetter` but shows a cursor mobject trailing the last typed letter.
```python
TypeWithCursor(
    text: Text,
    cursor: Mobject,
    buff: float = 0.1,
    keep_cursor_y: bool = True,
    leave_cursor_on: bool = True,
    time_per_char: float = 0.1,
    **kwargs,
)
```

### `UntypeWithCursor`
Like `RemoveTextLetterByLetter` but shows a cursor mobject.
```python
UntypeWithCursor(
    text: Text,
    cursor: VMobject | None = None,
    time_per_char: float = 0.1,
    **kwargs,
)
```

---

## Fading

### `FadeIn`
Fades one or more mobjects into the scene, optionally shifting or scaling while appearing.
```python
FadeIn(
    *mobjects: Mobject,
    shift: np.ndarray | None = None,
    target_position: np.ndarray | Mobject | None = None,
    scale: float = 1,
    **kwargs,
)
```

### `FadeOut`
Fades one or more mobjects out of the scene, optionally shifting or scaling while disappearing.
```python
FadeOut(
    *mobjects: Mobject,
    shift: np.ndarray | None = None,
    target_position: np.ndarray | Mobject | None = None,
    scale: float = 1,
    **kwargs,
)
```

---

## Transform

### `Transform`
Morphs a mobject into a target mobject, mutating the original in place.
```python
Transform(
    mobject: Mobject | None,
    target_mobject: Mobject | None = None,
    path_func: Callable | None = None,
    path_arc: float = 0,
    path_arc_axis: np.ndarray = OUT,
    path_arc_centers: Point3DLike | None = None,
    replace_mobject_with_target_in_scene: bool = False,
    **kwargs,
)
```

### `ReplacementTransform`
Like `Transform`, but the original mobject is removed from the scene and replaced by the target.
```python
ReplacementTransform(
    mobject: Mobject,
    target_mobject: Mobject,
    **kwargs,
)
```

### `TransformFromCopy`
Transforms a copy of the source into the target, leaving the original unchanged.
```python
TransformFromCopy(
    mobject: Mobject,
    target_mobject: Mobject,
    **kwargs,
)
```

### `ClockwiseTransform`
Transforms a mobject into another along a clockwise arc path.
```python
ClockwiseTransform(
    mobject: Mobject,
    target_mobject: Mobject,
    path_arc: float = -PI,
    **kwargs,
)
```

### `CounterclockwiseTransform`
Transforms a mobject into another along a counterclockwise arc path.
```python
CounterclockwiseTransform(
    mobject: Mobject,
    target_mobject: Mobject,
    path_arc: float = PI,
    **kwargs,
)
```

### `MoveToTarget`
Transforms a mobject to the state stored in its `.target` attribute (set via `.generate_target()`).
```python
MoveToTarget(
    mobject: Mobject,
    **kwargs,
)
```

### `ApplyMethod`
Animates a mobject by applying one of its own methods (the method must return the mobject).
```python
ApplyMethod(
    method: Callable,
    *args,
    **kwargs,
)
```

### `ApplyFunction`
Transforms a mobject by applying an arbitrary function that returns a new mobject.
```python
ApplyFunction(
    function: Callable[[Mobject], Mobject],
    mobject: Mobject,
    **kwargs,
)
```

### `ApplyMatrix`
Applies a 2×2 or 3×3 linear transformation matrix to a mobject's points.
```python
ApplyMatrix(
    matrix: np.ndarray,
    mobject: Mobject,
    about_point: np.ndarray = ORIGIN,
    **kwargs,
)
```

### `ApplyPointwiseFunction`
Applies an arbitrary pointwise function to every point of a mobject.
```python
ApplyPointwiseFunction(
    function: Callable,
    mobject: Mobject,
    run_time: float = DEFAULT_POINTWISE_FUNCTION_RUN_TIME,
    **kwargs,
)
```

### `FadeToColor`
Animates a color change on a mobject.
```python
FadeToColor(
    mobject: Mobject,
    color: str,
    **kwargs,
)
```

### `ScaleInPlace`
Scales a mobject by a given factor in place.
```python
ScaleInPlace(
    mobject: Mobject,
    scale_factor: float,
    **kwargs,
)
```

### `ShrinkToCenter`
Shrinks a mobject to a single point at its center.
```python
ShrinkToCenter(
    mobject: Mobject,
    **kwargs,
)
```

### `Restore`
Transforms a mobject back to the state saved by `.save_state()`.
```python
Restore(
    mobject: Mobject,
    **kwargs,
)
```

### `CyclicReplace`
Moves each mobject to the position of the next one in a cycle.
```python
CyclicReplace(
    *mobjects: Mobject,
    path_arc: float = 90 * DEGREES,
    **kwargs,
)
```

### `Swap`
Alias for `CyclicReplace` — swaps two mobjects' positions.
```python
Swap(*mobjects: Mobject, **kwargs)
```

### `FadeTransform`
Fades one mobject into another (cross-fade), removing the original.
```python
FadeTransform(
    mobject: Mobject,
    target_mobject: Mobject,
    stretch: bool = True,
    dim_to_match: int = 1,
    **kwargs,
)
```

### `FadeTransformPieces`
Like `FadeTransform` but matches and cross-fades submobjects individually.
```python
FadeTransformPieces(
    mobject: Mobject,
    target_mobject: Mobject,
    **kwargs,
)
```

### `TransformMatchingShapes`
Transforms two groups by matching submobjects with the same shape (by point-hash).
```python
TransformMatchingShapes(
    mobject: Mobject,
    target_mobject: Mobject,
    transform_mismatches: bool = False,
    fade_transform_mismatches: bool = False,
    key_map: dict | None = None,
    **kwargs,
)
```

### `TransformMatchingTex`
Transforms two LaTeX mobjects by matching submobjects with the same `tex_string`.
```python
TransformMatchingTex(
    mobject: Mobject,
    target_mobject: Mobject,
    transform_mismatches: bool = False,
    fade_transform_mismatches: bool = False,
    key_map: dict | None = None,
    **kwargs,
)
```

---

## Growing

### `GrowFromPoint`
Introduces a mobject by growing it from a specified point.
```python
GrowFromPoint(
    mobject: Mobject,
    point: Point3DLike,
    point_color: ParsableManimColor | None = None,
    **kwargs,
)
```

### `GrowFromCenter`
Introduces a mobject by growing it from its own center.
```python
GrowFromCenter(
    mobject: Mobject,
    point_color: ParsableManimColor | None = None,
    **kwargs,
)
```

### `GrowFromEdge`
Introduces a mobject by growing it from one of its bounding box edges.
```python
GrowFromEdge(
    mobject: Mobject,
    edge: Vector3DLike,
    point_color: ParsableManimColor | None = None,
    **kwargs,
)
```

### `GrowArrow`
Introduces an arrow by growing it from its start point toward its tip.
```python
GrowArrow(
    arrow: Arrow,
    point_color: ParsableManimColor | None = None,
    **kwargs,
)
```

### `SpinInFromNothing`
Introduces a mobject by simultaneously growing and spinning it from its center.
```python
SpinInFromNothing(
    mobject: Mobject,
    angle: float = PI / 2,
    point_color: ParsableManimColor | None = None,
    **kwargs,
)
```

---

## Rotation

### `Rotate`
Rotates a mobject to a target angle (Transform-based, interpolates the rotation).
```python
Rotate(
    mobject: Mobject,
    angle: float = PI,
    axis: Vector3DLike = OUT,
    about_point: Point3DLike | None = None,
    about_edge: Vector3DLike | None = None,
    **kwargs,
)
```

### `Rotating`
Continuously rotates a mobject (Animation-based, good for `run_time`-controlled looping).
```python
Rotating(
    mobject: Mobject,
    angle: float = TAU,
    axis: Vector3DLike = OUT,
    about_point: Point3DLike | None = None,
    about_edge: Vector3DLike | None = None,
    run_time: float = 5,
    rate_func: Callable = linear,
    **kwargs,
)
```

---

## Movement

### `MoveAlongPath`
Moves a mobject along the path of another VMobject.
```python
MoveAlongPath(
    mobject: Mobject,
    path: VMobject,
    suspend_mobject_updating: bool = False,
    **kwargs,
)
```

### `Homotopy`
Continuously deforms a mobject's points via a 4D function `(x, y, z, t) → (x', y', z')`.
```python
Homotopy(
    homotopy: Callable[[float, float, float, float], tuple],
    mobject: Mobject,
    run_time: float = 3,
    apply_function_kwargs: dict | None = None,
    **kwargs,
)
```

### `PhaseFlow`
Moves a mobject's points by integrating a vector field function over time.
```python
PhaseFlow(
    function: Callable[[np.ndarray], np.ndarray],
    mobject: Mobject,
    virtual_time: float = 1,
    suspend_mobject_updating: bool = False,
    rate_func: Callable = linear,
    **kwargs,
)
```

---

## Indication

### `FocusOn`
Shrinks a large semi-transparent spotlight circle down to a point.
```python
FocusOn(
    focus_point: Point3DLike | Mobject,
    opacity: float = 0.2,
    color: ParsableManimColor = GREY,
    run_time: float = 2,
    **kwargs,
)
```

### `Indicate`
Briefly scales up and recolors a mobject to draw attention to it.
```python
Indicate(
    mobject: Mobject,
    scale_factor: float = 1.2,
    color: ParsableManimColor = PURE_YELLOW,
    rate_func: RateFunction = there_and_back,
    **kwargs,
)
```

### `Flash`
Emits short lines radiating outward from a point or mobject.
```python
Flash(
    point: Point3DLike | Mobject,
    line_length: float = 0.2,
    num_lines: int = 12,
    flash_radius: float = 0.1,
    line_stroke_width: int = 3,
    color: ParsableManimColor = PURE_YELLOW,
    time_width: float = 1,
    run_time: float = 1.0,
    **kwargs,
)
```

### `ShowPassingFlash`
Animates a moving highlight that travels along a VMobject's stroke.
```python
ShowPassingFlash(
    mobject: VMobject,
    time_width: float = 0.1,
    **kwargs,
)
```

### `Circumscribe`
Temporarily draws a rectangle or circle around a mobject to highlight it.
```python
Circumscribe(
    mobject: Mobject,
    shape: type = Rectangle,
    fade_in: bool = False,
    fade_out: bool = False,
    time_width: float = 0.3,
    buff: float = SMALL_BUFF,
    color: ParsableManimColor = PURE_YELLOW,
    run_time: float = 1,
    stroke_width: float = DEFAULT_STROKE_WIDTH,
    **kwargs,
)
```

### `ApplyWave`
Sends a wave distortion through a mobject.
```python
ApplyWave(
    mobject: Mobject,
    direction: Vector3DLike = UP,
    amplitude: float = 0.2,
    wave_func: RateFunction = smooth,
    time_width: float = 1,
    ripples: int = 1,
    run_time: float = 2,
    **kwargs,
)
```

### `Wiggle`
Briefly scales and rotates a mobject back and forth to make it wiggle.
```python
Wiggle(
    mobject: Mobject,
    scale_value: float = 1.1,
    rotation_angle: float = 0.01 * TAU,
    n_wiggles: int = 6,
    scale_about_point: Point3DLike | None = None,
    rotate_about_point: Point3DLike | None = None,
    run_time: float = 2,
    **kwargs,
)
```

### `Blink`
Toggles a mobject's opacity on and off a given number of times.
```python
Blink(
    mobject: Mobject,
    time_on: float = 0.5,
    time_off: float = 0.5,
    blinks: int = 1,
    hide_at_end: bool = False,
    **kwargs,
)
```

---

## Composition

### `AnimationGroup`
Plays multiple animations simultaneously (or with a lag ratio).
```python
AnimationGroup(
    *animations: Animation,
    group: Group | VGroup | None = None,
    run_time: float | None = None,
    rate_func: Callable = linear,
    lag_ratio: float = 0,
    **kwargs,
)
```

### `Succession`
Plays a series of animations one after another (lag_ratio defaults to 1).
```python
Succession(
    *animations: Animation,
    lag_ratio: float = 1,
    **kwargs,
)
```

### `LaggedStart`
Plays animations with a staggered start time controlled by `lag_ratio`.
```python
LaggedStart(
    *animations: Animation,
    lag_ratio: float = 0.05,
    **kwargs,
)
```

### `LaggedStartMap`
Applies an animation class to each submobject of a mobject with a lag.
```python
LaggedStartMap(
    animation_class: type[Animation],
    mobject: Mobject,
    arg_creator: Callable | None = None,
    run_time: float = 2,
    lag_ratio: float = 0.05,
    **kwargs,
)
```
