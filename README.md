# html5-named-entity

A small, zero-dependency Python library for decoding HTML5 named character references, including the legacy entities that may legally appear without a trailing semicolon.

```python
from html5_named_entity import decode, decode_one, NAMED_ENTITIES

decode("Tom &amp; Jerry &lt;3")        # 'Tom & Jerry <3'
decode("&euro;100")                     # '€100'
decode_one("&amp;", 0)                  # ('&', 5)
decode_one("&not", 0)                   # ('¬', 4)
NAMED_ENTITIES["amp;"]                  # ('&', True)
NAMED_ENTITIES["amp"]                   # ('&', False)
```

## Why this exists

Python's `html.unescape` decodes *all* HTML5 entities but offers no way to decode a single reference at a known position, and its behaviour for legacy no-semicolon entities is tied to the full HTML5 tokenizer state machine. This library gives you a small, explicit table and two functions: `decode` for whole-string decoding and `decode_one` for decoding exactly one reference starting at a given index. Numeric references (`&#39;`, `&#x27;`) are deliberately **not** decoded — they belong to a separate concern.

## Edge cases

The tricky part is the greedy longest-match rule. `&not` is the legacy form of `¬`; `&notin;` is `∉`. The decoder picks the longest name that matches starting at the `&`, so `&notin;` yields `∉`, not `¬in;`. Unknown names (e.g. `&foo;`) are left untouched. A bare `&` with no matching name is also left as-is. The library covers the full HTML5 named-entity table as generated from the spec; the module-level `NAMED_ENTITIES` dict maps every accepted name (with and without semicolon where applicable) to a `(decoded_value, has_semicolon)` tuple.

## Exports

- `decode(text: str) -> str` — decode all named references in the string.
- `decode_one(text: str, pos: int = 0) -> tuple[str, int]` — decode a single reference at `pos`; returns `(decoded, consumed)` or `("", 0)`.
- `NAMED_ENTITIES` — dict mapping accepted names to `(value, has_semicolon)` tuples.
