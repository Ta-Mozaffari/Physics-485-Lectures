#!/usr/bin/env python3
"""Render an animated Bloch-sphere illustration of the Pauli-Z gate.

Requires Pillow (PIL). The qubit's Bloch vector is rotated by pi around the
z-axis; R_z(pi) equals Pauli-Z up to an unobservable global phase.
"""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "figures" / "bloch-sphere-pauli-z.gif"
PDF_FRAMES = ROOT / "figures" / "pauli-z-frames"

WIDTH, HEIGHT = 1300, 850
SCALE = 2  # Supersample for smooth circles and curves.
CX, CY, RADIUS = 430, 435, 265
CAMERA_AZIMUTH = math.radians(38)
CAMERA_ELEVATION = math.radians(24)
POLAR_ANGLE = math.radians(55)
START_AZIMUTH = CAMERA_AZIMUTH + math.pi / 2
ROTATION = math.pi
FRAME_COUNT = 48
FRAME_DURATION_MS = 75

NAVY = (37, 72, 120)
BLUE = (51, 119, 190)
LIGHT_BLUE = (169, 198, 222)
PALE_BLUE = (222, 235, 246)
PURPLE = (124, 83, 171)
GOLD = (218, 151, 45)
INK = (35, 47, 62)
MUTED = (102, 116, 132)
GRID_BACK = (201, 211, 221)
WHITE = (255, 255, 255)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "Arial Bold.ttf" if bold else "Arial.ttf"
    candidates = (
        Path("/System/Library/Fonts/Supplemental") / name,
        Path("/Library/Fonts") / name,
    )
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size * SCALE)
    return ImageFont.load_default(size=size * SCALE)


def project(point: tuple[float, float, float]) -> tuple[float, float, float]:
    """Project a unit-sphere point into screen coordinates and camera depth."""
    x, y, z = point
    ca, sa = math.cos(CAMERA_AZIMUTH), math.sin(CAMERA_AZIMUTH)
    ce, se = math.cos(CAMERA_ELEVATION), math.sin(CAMERA_ELEVATION)
    right = -sa * x + ca * y
    up = -se * ca * x - se * sa * y + ce * z
    depth = ce * ca * x + ce * sa * y + se * z
    return CX + RADIUS * right, CY - RADIUS * up, depth


def sphere_point(theta: float, phi: float) -> tuple[float, float, float]:
    return (
        math.sin(theta) * math.cos(phi),
        math.sin(theta) * math.sin(phi),
        math.cos(theta),
    )


def px(point: tuple[float, float]) -> tuple[int, int]:
    return round(point[0] * SCALE), round(point[1] * SCALE)


def draw_segment(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    color: tuple[int, int, int],
    width: int,
    dashed: bool = False,
) -> None:
    a, b = px(start), px(end)
    if not dashed:
        draw.line((a, b), fill=color, width=width * SCALE)
        return
    count = 8
    for part in range(0, count, 2):
        t0, t1 = part / count, (part + 1) / count
        p0 = (start[0] + (end[0] - start[0]) * t0,
              start[1] + (end[1] - start[1]) * t0)
        p1 = (start[0] + (end[0] - start[0]) * t1,
              start[1] + (end[1] - start[1]) * t1)
        draw.line((px(p0), px(p1)), fill=color, width=width * SCALE)


def draw_curve(
    draw: ImageDraw.ImageDraw,
    points: list[tuple[float, float, float]],
    front_color: tuple[int, int, int],
    back_color: tuple[int, int, int],
    width: int,
) -> None:
    for first, second in zip(points, points[1:]):
        p0, p1 = project(first), project(second)
        front = (p0[2] + p1[2]) / 2 >= 0
        draw_segment(draw, p0[:2], p1[:2], front_color if front else back_color,
                     width if front else max(1, width - 1), dashed=not front)


def draw_arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    color: tuple[int, int, int],
    width: int = 5,
) -> None:
    draw_segment(draw, start, end, color, width)
    dx, dy = end[0] - start[0], end[1] - start[1]
    length = math.hypot(dx, dy)
    if length == 0:
        return
    ux, uy = dx / length, dy / length
    head_len, half_width = 18, 8
    base = (end[0] - ux * head_len, end[1] - uy * head_len)
    perp = (-uy * half_width, ux * half_width)
    tip = px(end)
    left = px((base[0] + perp[0], base[1] + perp[1]))
    right = px((base[0] - perp[0], base[1] - perp[1]))
    draw.polygon((tip, left, right), fill=color)


def draw_label(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str,
               face: ImageFont.FreeTypeFont, fill: tuple[int, int, int]) -> None:
    draw.text((xy[0] * SCALE, xy[1] * SCALE), text, font=face, fill=fill)


def add_wrapped_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    xy: tuple[int, int],
    max_width: int,
    face: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int],
    line_gap: int = 8,
) -> int:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if draw.textbbox((0, 0), candidate, font=face)[2] <= max_width * SCALE:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    y = xy[1]
    for line in lines:
        draw_label(draw, (xy[0], y), line, face, fill)
        y += round(face.size / SCALE) + line_gap
    return y


def make_frame(progress: float) -> Image.Image:
    image = Image.new("RGB", (WIDTH * SCALE, HEIGHT * SCALE), WHITE)
    draw = ImageDraw.Draw(image)

    # Header and two compact explanatory panels.
    draw_label(draw, (70, 43), "Pauli-Z as a Bloch-sphere rotation", font(34, True), INK)
    draw_label(draw, (72, 96), "Watch a qubit state turn halfway around the z-axis", font(20), MUTED)
    draw.rounded_rectangle((790 * SCALE, 185 * SCALE, 1230 * SCALE, 670 * SCALE),
                           radius=18 * SCALE, fill=(246, 249, 252),
                           outline=(222, 230, 238), width=2 * SCALE)

    draw_label(draw, (825, 220), "Bloch vector", font(24, True), NAVY)
    draw_label(draw, (825, 272), "r = (sin θ cos φ, sin θ sin φ, cos θ)", font(18), INK)
    draw_label(draw, (825, 330), "Pauli-Z action", font(24, True), NAVY)
    draw_label(draw, (825, 378), "φ → φ + π", font(27, True), PURPLE)
    draw_label(draw, (825, 430), "(x, y, z) → (−x, −y, z)", font(22), INK)
    add_wrapped_text(
        draw,
        "The z component stays fixed; the x and y components change sign.",
        (825, 490), 365, font(20), MUTED, line_gap=9,
    )
    draw_label(draw, (825, 590), "Rz(π) = Z up to global phase", font(17, True), GOLD)

    # Sphere outline and latitude/longitude grid, with hidden arcs dashed.
    cx, cy, radius = CX, CY, RADIUS
    draw.ellipse(((cx - radius) * SCALE, (cy - radius) * SCALE,
                  (cx + radius) * SCALE, (cy + radius) * SCALE),
                 fill=(250, 252, 254), outline=LIGHT_BLUE, width=3 * SCALE)

    for theta_deg in (30, 60, 90, 120, 150):
        points = [sphere_point(math.radians(theta_deg), i * 2 * math.pi / 180)
                  for i in range(181)]
        draw_curve(draw, points, LIGHT_BLUE, GRID_BACK, 1)
    for phi_deg in range(0, 180, 30):
        points = [sphere_point(i * math.pi / 180, math.radians(phi_deg))
                  for i in range(181)]
        draw_curve(draw, points, LIGHT_BLUE, GRID_BACK, 1)

    # Draw coordinate axes through the sphere and label the positive ends.
    axes = (
        ((-1.17, 0, 0), (1.17, 0, 0), "x"),
        ((0, -1.17, 0), (0, 1.17, 0), "y"),
        ((0, 0, -1.17), (0, 0, 1.17), "z"),
    )
    for start3, end3, label in axes:
        start, end = project(start3), project(end3)
        draw_segment(draw, start[:2], end[:2], (117, 132, 149), 1)
        ex, ey = end[0], end[1]
        draw_label(draw, (round(ex + 9), round(ey - 12)), label, font(18, True), MUTED)
    z_tip = project((0, 0, 1.12))[:2]
    z_bottom = project((0, 0, -1.08))[:2]
    draw_arrow(draw, z_bottom, z_tip, (91, 107, 126), width=2)

    # The state follows a fixed-latitude path as its azimuth increases by pi.
    start_point = sphere_point(POLAR_ANGLE, START_AZIMUTH)
    end_point = sphere_point(POLAR_ANGLE, START_AZIMUTH + ROTATION)
    full_path = [sphere_point(POLAR_ANGLE,
                              START_AZIMUTH + ROTATION * i / 180)
                 for i in range(181)]
    trace_count = max(2, round(progress * (len(full_path) - 1)) + 1)
    draw_curve(draw, full_path[:trace_count], PURPLE, (199, 184, 217), 4)

    start_screen = project(start_point)
    end_screen = project(end_point)
    # Mark the initial and final state locations on the sphere.
    for point, color in ((start_screen, BLUE), (end_screen, GOLD)):
        r = 7 * SCALE
        draw.ellipse((round(point[0] * SCALE) - r, round(point[1] * SCALE) - r,
                      round(point[0] * SCALE) + r, round(point[1] * SCALE) + r),
                     fill=color, outline=WHITE, width=2 * SCALE)
    draw_label(draw, (round(start_screen[0] - 72), round(start_screen[1] - 42)),
               "|ψ>", font(20, True), BLUE)
    draw_label(draw, (round(end_screen[0] + 13), round(end_screen[1] - 25)),
               "Z|ψ>", font(20, True), GOLD)

    current_phi = START_AZIMUTH + ROTATION * progress
    current = project(sphere_point(POLAR_ANGLE, current_phi))
    origin = project((0, 0, 0))
    draw_arrow(draw, origin[:2], current[:2], NAVY, width=5)
    dot_r = 8 * SCALE
    draw.ellipse((round(current[0] * SCALE) - dot_r,
                  round(current[1] * SCALE) - dot_r,
                  round(current[0] * SCALE) + dot_r,
                  round(current[1] * SCALE) + dot_r), fill=NAVY, outline=WHITE,
                 width=2 * SCALE)

    draw_label(draw, (760, 714), "Pauli-Z: a π rotation about z", font(22, True), NAVY)
    draw_label(draw, (760, 750), "(global phase does not affect the qubit state)", font(17), MUTED)

    return image.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def main() -> None:
    frames = [make_frame(index / (FRAME_COUNT - 1)) for index in range(FRAME_COUNT)]
    PDF_FRAMES.mkdir(parents=True, exist_ok=True)
    for index, frame in enumerate(frames):
        # The slide uses the sphere-only crop as an embedded PDF animation.
        crop = frame.crop((120, 130, 740, 750)).resize((620, 620), Image.Resampling.LANCZOS)
        crop.save(PDF_FRAMES / f"pauli-z-{index}.png", optimize=True)

    palette = frames[0].quantize(colors=128, method=Image.Quantize.MEDIANCUT)
    indexed = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    indexed[0].save(
        OUTPUT,
        save_all=True,
        append_images=indexed[1:],
        duration=FRAME_DURATION_MS,
        loop=0,
        disposal=2,
        optimize=True,
    )
    print(f"Wrote {OUTPUT} ({OUTPUT.stat().st_size / 1024:.1f} KiB)")


if __name__ == "__main__":
    main()
