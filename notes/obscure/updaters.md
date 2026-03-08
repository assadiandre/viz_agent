# Obscure Updaters
> Manim v0.20.1

---

### `MaintainPositionRelativeTo`
Keeps a mobject at a fixed offset from a tracked mobject throughout an animation. The `add_updater` pattern is more flexible and covers this use case.
```python
MaintainPositionRelativeTo(
    mobject: Mobject,
    tracked_mobject: Mobject,
    **kwargs,
)
```
