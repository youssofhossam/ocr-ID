import os
import json
import gi
import cairo
import cv2
import numpy as np

from PIL import Image

gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")

from gi.repository import Pango, PangoCairo

# ============================================================
# Files
# ============================================================

TEMPLATE = "template.jpg"
OUTPUT_DIR = "output_cards"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# Dataset
# ============================================================

with open("dataset.json", encoding="utf-8") as f:
    dataset = json.load(f)

with open("config.json", encoding="utf-8") as f:
    POS = json.load(f)

# ============================================================
# Load template
# ============================================================

def load_surface(path):

    img = Image.open(path).convert("RGBA")

    w, h = img.size

    data = bytearray(img.tobytes("raw", "BGRA"))

    surface = cairo.ImageSurface.create_for_data(
        data,
        cairo.FORMAT_ARGB32,
        w,
        h
    )

    return surface, data


# ============================================================
# Draw Arabic Text
# ============================================================
def draw_text(
        ctx,
        text,
        x,
        y,
        font="Noto Sans Arabic",
        size=20,
        color=(0.08, 0.08, 0.08)
):

    layout = PangoCairo.create_layout(ctx)

    layout.set_text(str(text), -1)

    desc = Pango.FontDescription()

    desc.set_family(font)

    desc.set_size(size * Pango.SCALE)

    layout.set_font_description(desc)

    layout.set_auto_dir(True)

    layout.set_alignment(Pango.Alignment.RIGHT)

    layout.set_width(-1)

    layout.set_single_paragraph_mode(False)

    layout.set_wrap(Pango.WrapMode.WORD_CHAR)

    layout.set_justify(False)

    layout.set_ellipsize(Pango.EllipsizeMode.NONE)

    _, logical = layout.get_pixel_extents()

    ctx.set_source_rgb(*color)

    ctx.move_to(
        x - logical.width,
        y
    )

    PangoCairo.show_layout(ctx, layout)


# ============================================================
# Generate Cards
# ============================================================

for i, person in enumerate(dataset):

    surface, _ = load_surface(TEMPLATE)

    ctx = cairo.Context(surface)

        # -------------------------------
    # First Name
    # -------------------------------

    draw_text(
        ctx,
        person["name_first"],
        *POS["name_first"],
        font="Noto Sans Arabic",
        size=34
    )

    # -------------------------------
    # Rest of Name
    # -------------------------------

    draw_text(
        ctx,
        person["name_rest"],
        *POS["name_rest"],
        font="Noto Sans Arabic",
        size=29
    )

    # -------------------------------
    # Street
    # -------------------------------

    draw_text(
        ctx,
        person["street"],
        *POS["street"],
        font="Noto Sans Arabic",
        size=26
    )

    # -------------------------------
    # Rest of Address
    # -------------------------------

    draw_text(
        ctx,
        person["address_rest"],
        *POS["address_rest"],
        font="Noto Sans Arabic",
        size=26
    )

    # -------------------------------
    # National ID
    # -------------------------------

    draw_text(
        ctx,
        person["national_id"],
        *POS["nid"],
        font="DejaVu Sans",
        size=40
    )

    # ============================================================
    # Save temporary PNG
    # ============================================================

    tmp = os.path.join(
        OUTPUT_DIR,
        f"tmp_{i}.png"
    )

    surface.write_to_png(tmp)

    # ============================================================
    # OpenCV Post-processing
    # ============================================================

    img = cv2.imread(tmp)

    img = cv2.GaussianBlur(
        img,
        (3, 3),
        0.3
    )

    noise = np.random.normal(
        0,
        2,
        img.shape
    )

    img = img.astype(np.float32)

    img += noise

    img = np.clip(
        img,
        0,
        255
    ).astype(np.uint8)

    output = os.path.join(
        OUTPUT_DIR,
        f"card_{i}.jpg"
    )

    cv2.imwrite(
        output,
        img,
        [
            cv2.IMWRITE_JPEG_QUALITY,
            95
        ]
    )

    os.remove(tmp)

    print(f"Saved: {output}")

print("Done.")