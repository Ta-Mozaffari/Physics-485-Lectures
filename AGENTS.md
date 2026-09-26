# Repository instructions

## Git workflow

- Handle routine Git operations for the user, including fetching, synchronizing, committing, pushing, pull requests, merges, conflict resolution, and branch cleanup.
- Use `main` as the normal working branch. Check out `main` before editing and do not leave the repository on another branch when a task is complete.
- Commit completed, verified work directly to `main` unless a pull request or an explicit user request requires a temporary branch.
- Before starting work, fetch both `origin/main` and `overleaf/main` when network access is available. Reconcile upstream changes while preserving the user's work.
- After completing work, create a focused commit and push the resulting `main` history to both `origin` and `overleaf`. Verify that local `main`, `origin/main`, and `overleaf/main` resolve to the intended commit.
- Never force-push or rewrite `main`. Resolve divergent histories with a normal merge or another history-preserving method.
- Handle the full pull-request lifecycle when a pull request is required: create the temporary branch, push it, create or update the PR, address conflicts or review feedback, merge it, update local `main`, and synchronize both remotes.
- Delete temporary work branches after they are merged, both locally and on the applicable remote. Delete only branches whose changes are confirmed merged or otherwise preserved.
- Never delete `main`, an unmerged branch, or a branch with unique work unless the user explicitly requests that exact deletion.
- Remove stale merged work branches during Git cleanup. Do not remove branches that belong to an active pull request or ongoing task.
- If a merge conflict cannot be resolved without choosing between materially different user changes, preserve both sides and ask for direction.

## Figures

- Keep every final figure used by the slides under `figures/` and commit it to Git.
- Track presentation assets such as `.png`, `.jpg`, and `.pdf` files. Do not add final image formats to `.gitignore`.
- Prefer PDF for vector diagrams and PNG for raster images or screenshots.
- Use descriptive, lowercase, kebab-case filenames without spaces, for example `bloch-sphere-x-gate.png`.
- Do not reuse an existing filename for unrelated content. Add a new file when the subject changes.
- Keep editable source files in `figures/source/` when they are useful for future revisions.
- Keep individual image files reasonably small, preferably below 5 MB, and crop unused margins.
- Record the origin and required attribution for external figures in `figures/README.md`.
- Treat the local repository as the working copy and follow the Git workflow above for figure changes.

## Slides

- Keep one Beamer frame per `.tex` file under `slides/`.
- Name slide files with a zero-padded numeric prefix followed by a lowercase, kebab-case topic, for example `01-title.tex` and `02-qubit-bloch-sphere.tex`.
- The numeric prefix defines deck order. Keep the `slides/` filenames and the `\input{slides/<name>}` entries in root `main.tex` in ascending numeric order.
- Assign the next available prefix to new slides. Renumber only when the intended deck sequence changes.
- Build slide source locally and let the user review the rendered deck in Overleaf. Do not open, compile, or inspect the Overleaf browser preview during routine slide work unless the user explicitly asks for remote review or troubleshooting.
