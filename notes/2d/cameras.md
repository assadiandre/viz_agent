# Manim Cameras Reference

## 2D Cameras

### `Camera`
> Base class for all cameras. Renders to a 2D pixel array using Cairo.

```python
Camera(
    background_image: str | None = None,
    frame_center: Point3D = ORIGIN,
    image_mode: str = "RGBA",
    n_channels: int = 4,
    pixel_array_dtype: str = "uint8",
    cairo_line_width_multiple: float = 0.01,
    use_z_index: bool = True,
    background: PixelArray | None = None,
    pixel_height: int | None = None,
    pixel_width: int | None = None,
    frame_height: float | None = None,
    frame_width: float | None = None,
    frame_rate: float | None = None,
    background_color: ParsableManimColor | None = None,
    background_opacity: float | None = None,
    **kwargs,
)
```

---

### `MovingCamera`
> Extends `Camera`. Adds a movable frame rectangle — used for panning and zooming.

```python
MovingCamera(
    frame: Mobject | None = None,
    fixed_dimension: int = 0,  # 0 = fix width, 1 = fix height
    default_frame_stroke_color: ManimColor = WHITE,
    default_frame_stroke_width: int = 0,
    **kwargs,
)
```

---

### `MultiCamera`
> Extends `MovingCamera`. Renders multiple sub-cameras, each outputting to an `ImageMobjectFromCamera`.

```python
MultiCamera(
    image_mobjects_from_cameras: Iterable[ImageMobjectFromCamera] | None = None,
    allow_cameras_to_capture_their_own_display: bool = False,
    **kwargs,
)
```


