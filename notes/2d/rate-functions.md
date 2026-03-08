# Manim Rate Functions Reference
> Manim v0.20.1

Rate functions control the speed curve of animations — they map the animation's progress `t ∈ [0, 1]` to an output value, also in `[0, 1]`. Pass them via `rate_func=` on any animation.

```python
self.play(Create(circle), rate_func=there_and_back)
```

---

## Exported (use directly)

| Function | Description |
|---|---|
| `linear` | Constant speed — no easing |
| `smooth` | Slow in, slow out (sigmoid-based). The default for most animations. |
| `rush_into` | Accelerates quickly at the start, then levels off |
| `rush_from` | Starts slow, then rushes to the end |
| `slow_into` | Decelerates toward the end (arc-based) |
| `double_smooth` | Two back-to-back `smooth` curves — very smooth over the full range |
| `there_and_back` | Goes from 0 → 1 → 0, peaking at the midpoint. Useful for temporary effects. |
| `there_and_back_with_pause` | Like `there_and_back` but holds at the peak for a configurable duration |
| `lingering` | Moves to the target in the first 80% of the time, then holds |
| `exponential_decay` | Rapidly approaches 1 then decays — good for "settling" effects |
| `wiggle` | Oscillates back and forth, returning to 0 |

---

## Higher-Order Functions

### `squish_rate_func(func, a=0.4, b=0.6)`
Squishes a rate function so it only runs during the time window `[a, b]` — holding at 0 before and 1 after.
```python
# Only animate during the middle 20% of the runtime
rate_func = squish_rate_func(smooth, 0.4, 0.6)
```

### `not_quite_there(func=smooth, proportion=0.7)`
Scales a rate function so it only reaches `proportion` of its full value — the mobject never fully arrives.
```python
rate_func = not_quite_there(smooth, proportion=0.5)
```

---

## Standard Easing Functions (not exported — use via `rate_functions` module)

```python
from manim.utils import rate_functions
self.play(Create(circle), rate_func=rate_functions.ease_in_sine)
```

| Function | Description |
|---|---|
| `ease_in_sine` / `ease_out_sine` / `ease_in_out_sine` | Sine-based easing |
| `ease_in_quad` / `ease_out_quad` / `ease_in_out_quad` | Quadratic easing |
| `ease_in_cubic` / `ease_out_cubic` / `ease_in_out_cubic` | Cubic easing |
| `ease_in_quart` / `ease_out_quart` / `ease_in_out_quart` | Quartic easing |
| `ease_in_quint` / `ease_out_quint` / `ease_in_out_quint` | Quintic easing |
| `ease_in_expo` / `ease_out_expo` / `ease_in_out_expo` | Exponential easing |
| `ease_in_circ` / `ease_out_circ` / `ease_in_out_circ` | Circular easing |
| `ease_in_back` / `ease_out_back` / `ease_in_out_back` | Overshoots before settling |
| `ease_in_elastic` / `ease_out_elastic` / `ease_in_out_elastic` | Spring/elastic oscillation |
| `ease_in_bounce` / `ease_out_bounce` / `ease_in_out_bounce` | Bouncing effect |
