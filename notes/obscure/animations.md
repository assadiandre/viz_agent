# Obscure Animations
> Manim v0.20.1

---

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

### `AddTextWordByWord`
Show a `Text` word by word. **Currently broken in the source.**
```python
AddTextWordByWord(
    text_mobject: Text,
    run_time: float = None,
    time_per_char: float = 0.06,
    **kwargs,
)
```
