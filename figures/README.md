# Figure conventions

The files in this directory are shared by the local checkout, GitHub, and Overleaf.
Final figures are versioned in Git so every environment builds the same slides.

## Formats

- Use PDF for vector diagrams when possible.
- Use PNG for raster artwork, plots, and screenshots.
- Use JPG only for photographs where its smaller size is useful.
- Store editable source files in `source/` when future editing is likely.

## Naming

Use descriptive lowercase kebab-case names without spaces:

```text
bloch-sphere-x-gate.pdf
hadamard-basis-change.png
quantum-platforms-photo.jpg
```

Create a new filename when a figure's subject changes. A revised rendering of the
same figure may replace the existing file so references in the slides stay stable.

## Size and layout

- Prefer files smaller than 5 MB each.
- Crop unused margins before committing.
- Export raster images at sufficient resolution for a 16:9 presentation, usually
  at least 1600 pixels wide for a full-slide image.
- Preserve transparency when the slide background should remain visible.

## Sources and attribution

For an externally sourced or adapted figure, add an entry below with the filename,
creator, source URL or publication, license or permission, and access date.

| Filename | Creator/source | License or permission | Accessed |
| --- | --- | --- | --- |

## Synchronization

Commit figure changes with the related slide changes. Run `scripts/sync-remotes.sh`
from the repository root to fetch both remotes and push `main` to GitHub and
Overleaf. The script stops if the worktree is dirty, the branch is not `main`, or a
remote cannot be fast-forwarded safely.
