# Obscure Cameras
> Manim v0.20.1

---

### `MappingCamera`
Extends `Camera`. Applies a spatial mapping/distortion function to all rendered objects.
```python
MappingCamera(
    mapping_func: Callable = lambda p: p,
    min_num_curves: int = 50,
    allow_object_intrusion: bool = False,
    **kwargs,
)
```

---

### `OldMultiCamera`
Deprecated. Multiple cameras with explicit pixel positions. Use `MultiCamera` instead.
```python
OldMultiCamera(
    *cameras_with_start_positions,  # tuples of (Camera, (start_y, start_x))
    **kwargs,
)
```

### `SplitScreenCamera`
Deprecated. Two cameras split side-by-side. Use `MultiCamera` instead.
```python
SplitScreenCamera(
    left_camera: Camera,
    right_camera: Camera,
    **kwargs,
)
```
