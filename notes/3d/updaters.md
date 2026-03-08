# Manim Updaters Reference
> Manim v0.20.1

Updaters are functions attached to mobjects that run every frame, keeping them in sync with other values or mobjects. There are two ways to use them:

---

## Mobject updaters (via `add_updater`)

The most common pattern. Attach a function directly to a mobject so it updates every frame.

```python
# func(mob) — called every frame
dot.add_updater(lambda d: d.move_to(tracker.get_value() * RIGHT))

# func(mob, dt) — also receives the time delta since the last frame
arrow.add_updater(lambda a, dt: a.rotate(dt))
```

**Relevant `Mobject` methods:**
| Method | Description |
|---|---|
| `add_updater(func, index=None, call_updater=False)` | Attach an updater function |
| `remove_updater(func)` | Detach a specific updater |
| `clear_updaters(recursive=True)` | Remove all updaters |
| `suspend_updating()` | Temporarily pause all updaters |
| `resume_updating()` | Resume paused updaters |

---

## Animation-based updaters

These are `Animation` subclasses that call an update function each frame during a `play()` call — useful for syncing one mobject to another during an animation.

### `UpdateFromFunc`
Calls `update_function(mobject)` each frame, ignoring animation progress. Use when the mobject's state depends on something else being animated simultaneously.
```python
UpdateFromFunc(
    mobject: Mobject,
    update_function: Callable[[Mobject], Any],
    suspend_mobject_updating: bool = False,
    **kwargs,
)
```

```python
label = DecimalNumber(0)
tracker = ValueTracker(0)
label.add_updater(lambda l: l.set_value(tracker.get_value()))

self.play(
    tracker.animate.set_value(10),
    UpdateFromFunc(label, lambda l: l.set_value(tracker.get_value())),
)
```

### `UpdateFromAlphaFunc`
Like `UpdateFromFunc`, but also passes the current animation progress `alpha ∈ [0, 1]` as the second argument.
```python
UpdateFromAlphaFunc(
    mobject: Mobject,
    update_function: Callable[[Mobject, float], Any],
    **kwargs,
)
```

```python
self.play(
    UpdateFromAlphaFunc(circle, lambda c, a: c.set_opacity(a))
)
```

### `MaintainPositionRelativeTo`
Keeps a mobject at a fixed offset from a tracked mobject throughout the animation.
```python
MaintainPositionRelativeTo(
    mobject: Mobject,
    tracked_mobject: Mobject,
    **kwargs,
)
```

---

## `ValueTracker` pattern

The most common updater pattern combines `ValueTracker` with `add_updater`:

```python
tracker = ValueTracker(0)

dot = Dot()
dot.add_updater(lambda d: d.move_to(tracker.get_value() * RIGHT))

label = DecimalNumber(0)
label.add_updater(lambda l: l.set_value(tracker.get_value()))

self.add(dot, label)
self.play(tracker.animate.set_value(3), run_time=2)
```

`ValueTracker` and `ComplexValueTracker` are defined in the 2D mobjects reference.
