# Three.js r180 (0.180.0)

Vendored from the official [Three.js r180 source](https://github.com/mrdoob/three.js/tree/r180) under the MIT license in `LICENSE.txt`.

- `build/three.module.min.js` → `three.module.min.mjs`
- `build/three.core.min.js` → `three.core.min.mjs`
- `examples/jsm/controls/OrbitControls.js` → `OrbitControls.mjs`

Only module filenames/import specifiers were changed: the module imports its matching `.mjs` core; controls import the local `.mjs` module instead of bare `three`. Jupyter Book automatically loads every `.js` under `_static` as a classic script, so these ESM dependencies use `.mjs` and are loaded by dynamic import only when the projection explorer is present. No CDN or runtime download is needed.
