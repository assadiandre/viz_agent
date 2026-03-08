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


