# Changelog

## [0.9] - 2026-03-13
### Fixed
- **All face normals now correct** — zero blue faces in Blender, slicer sees a perfect solid
- Ring top winding order fixed: `[e4,e5,it1,it0]` instead of `[e4,it0,it1,e5]`
- Top plate central face correct: `[it0,it1,it2,it3]` (CCW from above = normal UP)
- Outer walls, inner walls, bottom ring all verified analytically
- Manifold confirmed: 0 open edges

## [0.8] - 2026-03-13
### Changed
- Top plate rebuilt as solid box (6 faces, shared vertices with shell)
- Studs start at H+0.01 to avoid coplanar faces with top plate
- Removed all `recalc_face_normals` calls (unreliable on non-manifold meshes)
- Shared vertices between shell ring and top plate box

### Fixed
- Manifold mesh: 0 open edges
- Top plate now visible to slicer (was missing in v0.7)

## [0.7] - 2026-03-12
### Added
- Multi-height bricks (altezza_mattoni parameter)
- Stackable: H = altezza × 9.6 mm
- Tubes and ribs scale with height

### Fixed
- Hollow shell with correct wall thickness
- Anti-stud tubes capped on both ends

## [0.6] - 2026-03-12
### Added
- Tolerance parameters exposed in F9 panel
- Outer expand, tube expand, stud expand

## [0.5] - 2026-03-12
### Added
- Internal ribs between anti-stud tubes
- Ribs split around tubes to avoid intersection

## [0.4] - 2026-03-12
### Added
- Anti-stud tubes (hollow cylinders at stud intersections)
- Tube outer/inner radius from LEGO spec

## [0.3] - 2026-03-12
### Added
- Hollow shell (outer + inner walls + bottom ring)
- Wall thickness: 1.2 mm

## [0.2] - 2026-03-12
### Added
- Parametric width × length in studs
- Closed cylindrical studs (base cap + top cap + mantle)

## [0.1] - 2026-03-12
### Added
- Initial release: basic box with LEGO dimensions
- Blender operator with REGISTER/UNDO
- Menu entry under Add → Mesh
