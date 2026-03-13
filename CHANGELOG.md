# Changelog

All notable changes to uBrick Generator are documented here.

---

## [0.9.2] - 2026-03-13
### Fixed
- **Zero slicer errors** — "Nessun errore rilevato" in PrusaSlicer ✅
- Eliminated 8 duplicate oriented edges on inner walls
- Root cause: inner wall winding `[ib,im]` → `[im,ib]` makes edges consistent
  with adjacent bottom ring and cavity ceiling faces
- Verified by simulating STL triangulation and checking all oriented edges

---

## [0.9.1] - 2026-03-13
### Fixed
- Eliminated all ngons (n-gons with >4 vertices) from stud caps
- Replaced single 32-vertex polygon caps with fan triangulation
- Each stud cap is now 32 triangles around a center vertex
- PrusaSlicer no longer needs to auto-repair polygon caps

---

## [0.9] - 2026-03-13
### Fixed
- **All face normals now correct** — zero blue faces in Blender
- Ring top winding corrected: `[e4,e5,it1,it0]` instead of `[e4,it0,it1,e5]`
- Top plate central face correct: `[it0,it1,it2,it3]` (CCW from above = UP)
- Outer walls, inner walls, bottom ring all verified analytically
- Manifold confirmed: 0 open edges

---

## [0.8] - 2026-03-13
### Changed
- Top plate rebuilt as solid box (6 faces, shared vertices with shell)
- Studs start at H+0.01 to avoid coplanar faces with top plate
- Removed all `recalc_face_normals` calls (unreliable on non-manifold meshes)

### Fixed
- Manifold mesh: 0 open edges
- Top plate now visible to slicer (was missing/inverted in v0.7)

---

## [0.7] - 2026-03-12
### Added
- Multi-height bricks (`altezza_mattoni` parameter, up to 16)
- Stackable: H = altezza × 9.6 mm
- Tubes and ribs scale correctly with height

### Fixed
- Hollow shell with correct wall thickness throughout

---

## [0.6] - 2026-03-12
### Added
- Tolerance parameters exposed in F9 panel
- `outer_expand`, `tube_expand`, `stud_expand` (mm)
- Default values tuned for Prusa MK3 + PETG:
  outer=0.20, tube=0.30, stud=0.10

---

## [0.5] - 2026-03-12
### Added
- Internal ribs between anti-stud tubes
- Ribs split around each tube to avoid intersection
- Rib thickness: 0.8 mm (LEGO spec)

---

## [0.4] - 2026-03-12
### Added
- Anti-stud tubes (hollow cylinders at stud grid intersections)
- Tube outer radius 3.25 mm, inner radius 2.5 mm (LEGO spec)
- Tubes capped on both ends (bottom and cavity ceiling)

---

## [0.3] - 2026-03-12
### Added
- Hollow shell: outer walls + inner walls + bottom ring
- Wall thickness: 1.2 mm (LEGO spec)
- Cavity open at top for tube and rib integration

---

## [0.2] - 2026-03-12
### Added
- Parametric width × length in studs (1–32 × 1–32)
- Closed cylindrical studs with base cap, top cap, and mantle
- Stud radius 2.4 mm, height 1.6 mm (LEGO spec)

---

## [0.1] - 2026-03-12
### Added
- Initial release: solid box with LEGO grid dimensions
- Blender operator with `REGISTER` / `UNDO` support
- Menu entry under **Add → Mesh → uBrick**
- LEGO constants: unit=8mm, brick height=9.6mm, gap=0.2mm
