from PIL import Image, ImageFilter, ImageEnhance
import os

# ============================================================
# SETTINGS
# ============================================================

INPUT = "hiking_base.png"
OUTPUT = "assets/hiking.gif"

WIDTH = 1200
HEIGHT = 220

FRAMES = 40
FPS = 18

# ============================================================
# LOAD BASE IMAGE
# ============================================================

if not os.path.exists(INPUT):
    raise FileNotFoundError(
        f"{INPUT} not found.\n"
        "Place your realistic hiking landscape image next to this script."
    )

base = Image.open(INPUT).convert("RGB")
base = base.resize((WIDTH, HEIGHT))

# Slight cinematic adjustment
base = ImageEnhance.Contrast(base).enhance(1.08)
base = ImageEnhance.Color(base).enhance(1.08)

# ============================================================
# CREATE PARALLAX LAYERS
# ============================================================

# Distant scenery
far = base.filter(ImageFilter.GaussianBlur(0.4))

# Middle scenery
middle = base.filter(ImageFilter.GaussianBlur(0.15))

# Foreground
foreground = base

frames = []

# ============================================================
# CREATE MOVING FRAMES
# ============================================================

for frame in range(FRAMES):

    progress = frame / (FRAMES - 1)

    # Continuous horizontal movement
    far_shift = int(progress * 70)
    middle_shift = int(progress * 180)
    foreground_shift = int(progress * 360)

    canvas = Image.new(
        "RGB",
        (WIDTH, HEIGHT),
        (10, 15, 13)
    )

    # --------------------------------------------------------
    # FAR BACKGROUND
    # --------------------------------------------------------

    far_extended = Image.new(
        "RGB",
        (WIDTH + 100, HEIGHT)
    )

    far_extended.paste(far, (0, 0))
    far_extended.paste(far.crop((0, 0, 100, HEIGHT)),
                       (WIDTH, 0))

    far_crop = far_extended.crop(
        (far_shift, 0,
         far_shift + WIDTH, HEIGHT)
    )

    canvas.paste(far_crop, (0, 0))

    # --------------------------------------------------------
    # MIDDLE LAYER
    # --------------------------------------------------------

    middle_extended = Image.new(
        "RGB",
        (WIDTH + 250, HEIGHT)
    )

    middle_extended.paste(middle, (0, 0))

    middle_extended.paste(
        middle.crop((0, 0, 250, HEIGHT)),
        (WIDTH, 0)
    )

    middle_crop = middle_extended.crop(
        (middle_shift, 0,
         middle_shift + WIDTH, HEIGHT)
    )

    # Blend middle layer
    canvas = Image.blend(
        canvas,
        middle_crop,
        0.28
    )

    # --------------------------------------------------------
    # FOREGROUND PARALLAX
    # --------------------------------------------------------

    foreground_extended = Image.new(
        "RGB",
        (WIDTH + 500, HEIGHT)
    )

    foreground_extended.paste(
        foreground,
        (0, 0)
    )

    foreground_extended.paste(
        foreground.crop((0, 0, 500, HEIGHT)),
        (WIDTH, 0)
    )

    foreground_crop = foreground_extended.crop(
        (foreground_shift, 0,
         foreground_shift + WIDTH, HEIGHT)
    )

    # Very subtle foreground movement
    canvas = Image.blend(
        canvas,
        foreground_crop,
        0.16
    )

    # --------------------------------------------------------
    # CINEMATIC VIGNETTE
    # --------------------------------------------------------

    vignette = Image.new(
        "RGBA",
        (WIDTH, HEIGHT),
        (0, 0, 0, 0)
    )

    pixels = vignette.load()

    for y in range(HEIGHT):
        for x in range(WIDTH):

            dx = abs(x - WIDTH / 2) / (WIDTH / 2)
            dy = abs(y - HEIGHT / 2) / (HEIGHT / 2)

            darkness = int(
                min(90, (dx ** 2 + dy ** 2) * 35)
            )

            pixels[x, y] = (
                0,
                0,
                0,
                darkness
            )

    canvas = Image.alpha_composite(
        canvas.convert("RGBA"),
        vignette
    ).convert("RGB")

    frames.append(canvas)

# ============================================================
# SAVE GIF
# ============================================================

os.makedirs(
    os.path.dirname(OUTPUT),
    exist_ok=True
)

frames[0].save(
    OUTPUT,
    save_all=True,
    append_images=frames[1:],
    duration=int(1000 / FPS),
    loop=0,
    optimize=True,
    disposal=2
)

print()
print("========================================")
print(" Hiking animation created successfully")
print("========================================")
print()
print(f"Output: {OUTPUT}")
print(f"Frames: {FRAMES}")
print(f"FPS:    {FPS}")
print()
