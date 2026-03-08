# Manim Scenes Reference
> Manim v0.20.1

Scenes are the containers everything runs inside. Subclass one and override `construct()` to build your animation.

---

## `Scene`
The base scene. Uses the Cairo 2D renderer. All other scene types inherit from this.
```python
Scene(
    renderer: CairoRenderer | OpenGLRenderer | None = None,
    camera_class: type[Camera] = Camera,
    always_update_mobjects: bool = False,
    random_seed: int | None = None,
    skip_animations: bool = False,
)
```

**Key methods:**
| Method | Description |
|---|---|
| `construct()` | Override this with your animation code |
| `play(*animations, run_time=..., rate_func=...)` | Play one or more animations |
| `wait(duration=1)` | Pause for a given number of seconds |
| `add(*mobjects)` | Add mobjects to the scene instantly |
| `remove(*mobjects)` | Remove mobjects from the scene instantly |
| `clear()` | Remove all mobjects from the scene |
| `bring_to_front(*mobjects)` | Move mobjects to the top of the render stack |
| `bring_to_back(*mobjects)` | Move mobjects to the bottom of the render stack |
| `add_sound(sound_file)` | Play a sound file during the animation |

---

## `ThreeDScene`
Extends `Scene` with a `ThreeDCamera`, enabling 3D perspective, rotation, and shading.
```python
ThreeDScene(
    camera_class=ThreeDCamera,
    ambient_camera_rotation=None,
    default_angled_camera_orientation_kwargs=None,
    **kwargs,
)
```

**Key methods (in addition to `Scene`):**
| Method | Description |
|---|---|
| `set_camera_orientation(phi, theta, gamma, zoom)` | Set the 3D camera angles and zoom |
| `begin_ambient_camera_rotation(rate, about)` | Continuously rotate the camera |
| `stop_ambient_camera_rotation()` | Stop the ambient rotation |
| `move_camera(phi, theta, gamma, zoom, run_time)` | Animate the camera to a new orientation |

---

## `SpecialThreeDScene`
Extends `ThreeDScene` with pre-configured axes, sphere defaults, and shading enabled by default.
```python
SpecialThreeDScene(
    cut_axes_at_radius: bool = True,
    camera_config: dict = {"should_apply_shading": True, "exponential_projection": True},
    three_d_axes_config: dict = {...},
    sphere_config: dict = {"radius": 2, "resolution": (24, 48)},
    **kwargs,
)
```

---

## `MovingCameraScene`
Extends `Scene` with a `MovingCamera` — allows the camera frame to be panned, zoomed, and animated like a mobject.
```python
MovingCameraScene(
    camera_class: type[Camera] = MovingCamera,
    **kwargs,
)
```

Access the camera frame via `self.camera.frame` and animate it with `.animate`:
```python
self.play(self.camera.frame.animate.move_to(some_mobject))
self.play(self.camera.frame.animate.scale(0.5))
```

---

## `ZoomedScene`
Extends `MovingCameraScene` with a secondary zoomed viewport displayed on screen — useful for magnifying a region of the scene.
```python
ZoomedScene(
    camera_class: type[Camera] = MultiCamera,
    zoomed_display_height: float = 3,
    zoomed_display_width: float = 3,
    zoomed_display_center: Point3DLike | None = None,
    zoomed_display_corner: Vector3D = UP + RIGHT,
    zoomed_display_corner_buff: float = DEFAULT_MOBJECT_TO_EDGE_BUFFER,
    zoomed_camera_config: dict = {"default_frame_stroke_width": 2, "background_opacity": 1},
    zoomed_camera_frame_starting_position: Point3DLike = ORIGIN,
    zoom_factor: float = 0.15,
    image_frame_stroke_width: float = 3,
    **kwargs,
)
```

**Key methods:**
| Method | Description |
|---|---|
| `activate_zooming(animate=False)` | Show the zoomed display |
| `deactivate_zooming()` | Hide the zoomed display |

---

## `VectorScene`
Extends `Scene` with helpers for visualizing vectors and vector operations on a coordinate plane.
```python
VectorScene(
    basis_vector_stroke_width: float = 6.0,
    **kwargs,
)
```

**Key methods:**
| Method | Description |
|---|---|
| `add_plane(animate=False)` | Add a `NumberPlane` background grid |
| `add_vector(vector, color, animate)` | Add and optionally animate a vector arrow |
| `write_vector_coordinates(vector)` | Show the coordinates of a vector |
| `get_basis_vectors()` | Return the i-hat and j-hat basis vectors |

---

## `LinearTransformationScene`
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

**Key methods:**
| Method | Description |
|---|---|
| `apply_matrix(matrix)` | Animate applying a 2×2 matrix transformation to the plane |
| `apply_nonlinear_transformation(func)` | Animate a nonlinear transformation |
| `apply_function(func)` | Animate an arbitrary point transformation |
