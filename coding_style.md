# Coding Style

## Notation

**Force Abbreviation / Unification**

- img: img, image
- crop: crop, cropped
- val: val, value
- show: show, view
- load: load, read
- pos: position, pos, p // tuple(y, x)

**No Abbreviation**

- left, right, top, bottom (x: l/r/t/b)
- value (x: v, val)

**Depending on the situation**

- H/height: only image
- W/width: only image
- C/channel: only image

## Tensor Index

- img: [H, W, C]

(not [W, H, C])

- `y` と `x` を使う場合、`y` を先頭に置く
  - e.g. height, width = ...

## Priority

- center >> top > bottom >> left > right