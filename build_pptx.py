#!/usr/bin/env python3
"""Assemble captured screenshots into a PPTX presentation.

Each screenshot becomes a full-slide background image.
Animation frames appear as consecutive slides, creating
a frame-by-frame animation effect when clicking through.
"""

import os
import glob
import re

from pptx import Presentation
from pptx.util import Inches, Pt, Emu


# --- config ---
SCREENSHOTS_DIR = r"D:\TOYCLAUDE\Teaching class\screenshots"
OUT_PATH = r"D:\TOYCLAUDE\Teaching class\二叉树遍历_教学课件.pptx"

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)

# Regular slides to skip (handled as animation frames)
ANIMATION_SLIDES = {9, 10, 11, 14}


def get_image_files():
    """Build ordered list of (display_order, filepath) tuples."""
    files = glob.glob(os.path.join(SCREENSHOTS_DIR, "*.png"))
    if not files:
        raise FileNotFoundError(f"No screenshots found in {SCREENSHOTS_DIR}")

    regular = {}  # slide_num -> path
    anim_frames = []  # (slide_num, prefix, step_num, path)

    for f in files:
        basename = os.path.basename(f)
        # Animation frame pattern: slide_NN_pp_SS_stepS.png or slide_NN_pp_00_initial.png
        m = re.match(r"slide_(\d+)_(\w+)_(\d+)_(?:step\d*|initial)\.png", basename)
        if m:
            anim_frames.append((int(m.group(1)), m.group(2), int(m.group(3)), f))
            continue
        # Regular slide pattern: slide_NN.png
        m = re.match(r"slide_(\d+)\.png", basename)
        if m:
            regular[int(m.group(1))] = f

    return regular, anim_frames


def build_slide_order(regular, anim_frames):
    """Build the final ordered list of image paths."""
    # Group animation frames by (slide_num, prefix)
    anim_groups = {}
    for slide_num, prefix, step_num, path in anim_frames:
        key = (slide_num, prefix)
        if key not in anim_groups:
            anim_groups[key] = {}
        anim_groups[key][step_num] = path

    # Sort each group by step_num and flatten
    anim_sequences = {}
    for key, steps in anim_groups.items():
        anim_sequences[key] = [steps[k] for k in sorted(steps.keys())]

    ordered = []
    for n in range(1, 23):  # slides 1-22
        if n in ANIMATION_SLIDES:
            # Add all animation frame sequences for this slide
            # Sort by prefix to keep pre -> in -> post consistent
            for prefix in sorted(
                set(k[1] for k in anim_sequences if k[0] == n)
            ):
                ordered.extend(anim_sequences.get((n, prefix), []))
        else:
            if n in regular:
                ordered.append(regular[n])

    return ordered


def add_slide_from_image(prs, image_path):
    """Add a slide with the image as full-slide background."""
    slide_layout = prs.slide_layouts[6]  # blank
    slide = prs.slides.add_slide(slide_layout)

    # Add picture filling entire slide
    slide.shapes.add_picture(
        image_path,
        Inches(0), Inches(0),
        SLIDE_W, SLIDE_H
    )


def main():
    print("Gathering screenshots...")
    regular, anim_frames = get_image_files()
    print(f"  Regular slides: {len(regular)}")
    print(f"  Animation frames: {len(anim_frames)}")

    ordered = build_slide_order(regular, anim_frames)
    print(f"  Total slides in PPT: {len(ordered)}")

    print("Building PPTX...")
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    for i, path in enumerate(ordered, 1):
        add_slide_from_image(prs, path)
        print(f"  [{i}/{len(ordered)}] {os.path.basename(path)}")

    prs.save(OUT_PATH)
    print(f"\nDone → {OUT_PATH}")
    print(f"Total: {len(ordered)} slides")


if __name__ == "__main__":
    main()
