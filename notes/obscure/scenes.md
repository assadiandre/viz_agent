# Obscure Scenes
> Manim v0.20.1

---

### `VectorScene`
Extends `Scene` with helpers for visualizing vectors and vector operations on a coordinate plane.
```python
VectorScene(
    basis_vector_stroke_width: float = 6.0,
    **kwargs,
)
```

| Method | Description |
|---|---|
| `add_plane(animate=False)` | Add a `NumberPlane` background grid |
| `add_vector(vector, color, animate)` | Add and optionally animate a vector arrow |
| `write_vector_coordinates(vector)` | Show the coordinates of a vector |
| `get_basis_vectors()` | Return the i-hat and j-hat basis vectors |

---

### `LinearTransformationScene`
Extends `VectorScene` with tools for demonstrating 2D linear transformations on a plane.
```python
LinearTransformationScene(
    include_background_plane: bool = True,
    include_foreground_plane: bool = True,
    background_plane_kwargs: dict | None = None,
    foreground_plane_kwargs: dict | None = None,
    show_coordinates: bool = False,
    show_basis_vectors: bool = True,
    basis_vector_stroke_width: float = 6,
    i_hat_color: ParsableManimColor = GREEN_C,
    j_hat_color: ParsableManimColor = RED_C,
    leave_ghost_vectors: bool = False,
    **kwargs,
)
```

| Method | Description |
|---|---|
| `apply_matrix(matrix)` | Animate applying a 2×2 matrix transformation to the plane |
| `apply_nonlinear_transformation(func)` | Animate a nonlinear transformation |
| `apply_function(func)` | Animate an arbitrary point transformation |
