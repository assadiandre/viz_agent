# Manim 3D Mobjects Reference

## Basic 3D Shapes

### `Sphere`
```python
Sphere(
    center: Point3DLike = ORIGIN,
    radius: float = 1,
    resolution: int | Sequence[int] | None = None,
    u_range: tuple[float, float] = (0, TAU),
    v_range: tuple[float, float] = (0, PI),
    **kwargs,
)
```

### `Dot3D`
```python
Dot3D(
    point: Point3D = ORIGIN,
    radius: float = DEFAULT_DOT_RADIUS,
    color: ParsableManimColor = WHITE,
    resolution: int | tuple[int, int] | None = (8, 8),
    **kwargs,
)
```

### `Cube`
```python
Cube(
    side_length: float = 2,
    fill_opacity: float = 0.75,
    fill_color: ParsableManimColor = BLUE,
    stroke_width: float = 0,
    **kwargs,
)
```

### `Prism`
```python
Prism(
    dimensions: Vector3DLike = [3, 2, 1],
    **kwargs,
)
```

### `Cone`
```python
Cone(
    base_radius: float = 1,
    height: float = 1,
    direction: Vector3DLike = Z_AXIS,
    show_base: bool = False,
    v_range: tuple[float, float] = (0, TAU),
    u_min: float = 0,
    checkerboard_colors: Iterable[ParsableManimColor] | Literal[False] = False,
    **kwargs,
)
```

### `Cylinder`
```python
Cylinder(
    radius: float = 1,
    height: float = 2,
    direction: Vector3DLike = Z_AXIS,
    v_range: tuple[float, float] = (0, TAU),
    show_ends: bool = True,
    resolution: int | tuple[int, int] = (24, 24),
    **kwargs,
)
```

### `Torus`
```python
Torus(
    major_radius: float = 3,
    minor_radius: float = 1,
    u_range: tuple[float, float] = (0, TAU),
    v_range: tuple[float, float] = (0, TAU),
    resolution: int | tuple[int, int] | None = None,
    **kwargs,
)
```

---

## 3D Lines & Arrows

### `Line3D`
```python
Line3D(
    start: Point3DLike = LEFT,
    end: Point3DLike = RIGHT,
    thickness: float = 0.02,
    color: ParsableManimColor | None = None,
    resolution: int | tuple[int, int] = 24,
    **kwargs,
)
```

### `Arrow3D`
```python
Arrow3D(
    start: Point3DLike = LEFT,
    end: Point3DLike = RIGHT,
    thickness: float = 0.02,
    height: float = 0.3,
    base_radius: float = 0.08,
    color: ParsableManimColor = WHITE,
    resolution: int | tuple[int, int] = 24,
    **kwargs,
)
```

---

## Parametric Surfaces

### `Surface`
```python
Surface(
    func: Callable[[float, float], np.ndarray],
    u_range: tuple[float, float] = (0, 1),
    v_range: tuple[float, float] = (0, 1),
    resolution: int | Sequence[int] = 32,
    surface_piece_config: dict = {},
    fill_color: ParsableManimColor = BLUE_D,
    fill_opacity: float = 1.0,
    checkerboard_colors: Iterable[ParsableManimColor] | Literal[False] = [BLUE_D, BLUE_E],
    stroke_color: ParsableManimColor = LIGHT_GREY,
    stroke_width: float = 0.5,
    should_make_jagged: bool = False,
    **kwargs,
)
```

---

## Polyhedra

### `Polyhedron`
```python
Polyhedron(
    vertex_coords: Iterable[Iterable[float]],
    faces_list: Iterable[Iterable[int]],
    faces_config: dict | None = None,
    graph_config: dict | None = None,
    **kwargs,
)
```

### `Tetrahedron`
```python
Tetrahedron(
    edge_length: float = 1,
    **kwargs,
)
```

### `Octahedron`
```python
Octahedron(
    edge_length: float = 1,
    **kwargs,
)
```

### `Icosahedron`
```python
Icosahedron(
    edge_length: float = 1,
    **kwargs,
)
```

### `Dodecahedron`
```python
Dodecahedron(
    edge_length: float = 1,
    **kwargs,
)
```

---

## 3D Coordinate Systems

### `ThreeDAxes`
```python
ThreeDAxes(
    x_range: Sequence[float] | None = (-6, 6, 1),
    y_range: Sequence[float] | None = (-5, 5, 1),
    z_range: Sequence[float] | None = (-4, 4, 1),
    x_length: float | None = None,
    y_length: float | None = None,
    z_length: float | None = None,
    z_axis_config: dict | None = None,
    z_normal: Vector3DLike = OUT,
    num_axis_pieces: int = 20,
    light_source: Point3DLike = (9, 3, 5),
    **kwargs,
)
```
