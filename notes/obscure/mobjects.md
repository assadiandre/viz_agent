# Obscure Mobjects
> Manim v0.20.1

---

## Geometry

### `ArcPolygonFromArcs`
Builds an arc polygon directly from a sequence of `Arc` objects. Use `ArcPolygon` instead for most cases.
```python
ArcPolygonFromArcs(
    *arcs: Arc,
    **kwargs,
)
```

### `ConvexHull`
The smallest convex polygon enclosing a set of points.
```python
ConvexHull(
    *points: Point3DLike,
    tolerance: float = 1e-5,
    **kwargs,
)
```

---

## Graphing

### `ComplexPlane`
A `NumberPlane` where the axes represent the real and imaginary parts of complex numbers.
```python
ComplexPlane(**kwargs)
```

### `SampleSpace`
A rectangle representing a probability sample space, intended to be subdivided into regions.
```python
SampleSpace(
    height: float = 3,
    width: float = 3,
    fill_color: ParsableManimColor = DARK_GREY,
    fill_opacity: float = 1,
    stroke_width: float = 0.5,
    stroke_color: ParsableManimColor = LIGHT_GREY,
    default_label_scale_val: float = 1,
)
```

---

## Matrices

### `DecimalMatrix`
A matrix where entries are rendered as `DecimalNumber` objects.
```python
DecimalMatrix(
    matrix: np.ndarray | list[list[float]],
    element_to_mobject: type[VMobject] = DecimalNumber,
    **kwargs,
)
```

### `IntegerMatrix`
A matrix where entries are rendered as integers.
```python
IntegerMatrix(
    matrix: np.ndarray | list[list[int]],
    **kwargs,
)
```

### `MobjectMatrix`
A matrix whose entries are arbitrary mobjects.
```python
MobjectMatrix(
    matrix: np.ndarray,
    **kwargs,
)
```

---

## Tables

### `MobjectTable`
A table whose cells contain arbitrary mobjects.
```python
MobjectTable(
    table: Iterable[Iterable[Mobject]],
    **kwargs,
)
```

### `IntegerTable`
A table where entries are rendered as integers.
```python
IntegerTable(
    table: Iterable[Iterable[int]],
    **kwargs,
)
```

### `DecimalTable`
A table where entries are rendered as decimal numbers.
```python
DecimalTable(
    table: Iterable[Iterable[float]],
    **kwargs,
)
```
