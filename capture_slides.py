#!/usr/bin/env python3
"""Capture binary-tree-lecture slides as screenshots, including traversal animation frames.

Uses Playwright to set location.hash to trigger the runtime's hashchange-driven navigation.
Traversal animation is captured frame-by-frame by calling highlightTrav() stepwise.
"""

import http.server
import socketserver
import threading
import os
import time

from playwright.sync_api import sync_playwright

# --- config ---
HTML_DIR = r"D:\TOYCLAUDE\Teaching class\binary-tree-lecture"
OUT_DIR = r"D:\TOYCLAUDE\Teaching class\screenshots"
PORT = 8765

# Traversal animation definitions
TRAV_ORDERS = {
    "pre": {
        "nodes": [0, 1, 2, 3, 4, 5, 6],
        "steps": [2, 3, 2, 3, 2, 3, 2],
        "slide": 9,
        "label": "先根序",
    },
    "in": {
        "nodes": [2, 1, 3, 0, 5, 4, 6],
        "steps": [1, 3, 1, 3, 1, 3, 1],
        "slide": 10,
        "label": "中根序",
    },
    "post": {
        "nodes": [2, 3, 1, 5, 6, 4, 0],
        "steps": [1, 1, 4, 1, 1, 4, 4],
        "slide": 11,
        "label": "后根序",
    },
}

ZOO_STEPS = {
    "pre":  ["A", "B", "D", "E", "F", "C", "G", "H", "I"],
    "in":   ["E", "D", "B", "F", "A", "H", "G", "C", "I"],
    "post": ["E", "D", "F", "B", "H", "G", "I", "C", "A"],
}

TOTAL_SLIDES = 22


def start_server():
    os.chdir(HTML_DIR)
    handler = http.server.SimpleHTTPRequestHandler

    class QuietHandler(handler):
        def log_message(self, format, *args):
            pass

    with socketserver.TCPServer(("", PORT), QuietHandler) as httpd:
        httpd.serve_forever()


def navigate_to(page, slide_1based):
    """Navigate to a slide by setting location.hash (triggers hashchange → runtime fromHash() → go())."""
    page.evaluate(f"location.hash = '#/{slide_1based}'")
    page.wait_for_timeout(800)


def screenshot(page, filename, wait_ms=600):
    """Take a screenshot after waiting for CSS transitions."""
    page.wait_for_timeout(wait_ms)
    path = os.path.join(OUT_DIR, filename)
    page.screenshot(path=path)
    print(f"  {filename}")
    return path


def capture_traversal_frames(page, prefix, info):
    """Capture each step of a traversal animation."""
    slide_1based = info["slide"]
    label = info["label"]

    # Navigate to the slide
    navigate_to(page, slide_1based)

    # Reset and capture initial state
    page.evaluate(f"resetTrav('{prefix}')")
    screenshot(page, f"slide_{slide_1based:02d}_{prefix}_00_initial.png")

    # Capture each step
    for idx in range(len(info["nodes"])):
        page.evaluate(f"highlightTrav('{prefix}', {idx})")
        screenshot(page, f"slide_{slide_1based:02d}_{prefix}_{idx + 1:02d}_step{idx + 1}.png")


def capture_zoo_frames(page):
    """Capture zoo traversal frames (slide 14)."""
    order_names = {"pre": "先根序", "in": "中根序", "post": "后根序"}

    for order in ["pre", "in", "post"]:
        labels = ZOO_STEPS[order]

        # Navigate to slide 14
        navigate_to(page, 14)

        # Reset
        page.evaluate("resetZooTrav()")
        screenshot(page, f"slide_14_zoo_{order}_00_initial.png")

        # Each step
        for idx in range(len(labels)):
            page.evaluate(f"""() => {{
                highlightZoo({idx}, {labels});
            }}""")
            screenshot(page, f"slide_14_zoo_{order}_{idx + 1:02d}_step{idx + 1}.png")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    # Start HTTP server
    print(f"Starting HTTP server on port {PORT}...")
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    time.sleep(1)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})

        try:
            # Load the page once
            print("Loading page...")
            page.goto(f"http://localhost:{PORT}/index.html", wait_until="networkidle")
            page.wait_for_timeout(2000)
            print("Page ready.\n")

            # ── Regular slides ──
            print("=== Capturing regular slides ===\n")
            animation_slides = {9, 10, 11, 14}

            for n in range(1, TOTAL_SLIDES + 1):
                if n in animation_slides:
                    continue
                navigate_to(page, n)
                screenshot(page, f"slide_{n:02d}.png")

            # ── Traversal animation frames ──
            print("\n=== Capturing traversal animation frames ===\n")
            for prefix, info in TRAV_ORDERS.items():
                capture_traversal_frames(page, prefix, info)

            # ── Zoo traversal frames ──
            print("\n=== Capturing zoo traversal frames ===\n")
            capture_zoo_frames(page)

        finally:
            browser.close()

    print(f"\nDone! All screenshots saved to: {OUT_DIR}")


if __name__ == "__main__":
    main()
