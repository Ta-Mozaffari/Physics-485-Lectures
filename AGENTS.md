# Repository instructions

## Figures

- Keep every final figure used by the slides under `figures/` and commit it to Git.
- Track presentation assets such as `.png`, `.jpg`, and `.pdf` files. Do not add final image formats to `.gitignore`.
- Prefer PDF for vector diagrams and PNG for raster images or screenshots.
- Use descriptive, lowercase, kebab-case filenames without spaces, for example `bloch-sphere-x-gate.png`.
- Do not reuse an existing filename for unrelated content. Add a new file when the subject changes.
- Keep editable source files in `figures/source/` when they are useful for future revisions.
- Keep individual image files reasonably small, preferably below 5 MB, and crop unused margins.
- Record the origin and required attribution for external figures in `figures/README.md`.
- Treat the local repository as the working copy. Commit figure changes and push the same `main` branch to both `origin` and `overleaf`.
- Before pushing, fetch both remotes. If their histories diverge, stop and reconcile the changes rather than force-pushing.

## Slides

- Keep one Beamer frame per `.tex` file under `slides/`.
- Assemble the ordered frames from the root `main.tex` file with `\input{slides/<name>}`.
