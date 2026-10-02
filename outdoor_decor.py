"""
KathaStudio v7 — Outdoor Decor & Props
Thick outline cartoon style props for outdoor scenes (park, street, tapri, 
village, beach, station, mountain). Integrates with background_draw.py.
"""

from PIL import ImageDraw
import math
import random

# Outline color (dark brown-black for cartoon style)
OL = (46, 32, 38)

def _dk(c, a):
    """Darken color."""
    return tuple(max(0, x - a) for x in c)

def _lt(c, a):
    """Lighten color."""
    return tuple(min(255, x + a) for x in c)

def box(d, x0, y0, x1, y1, fill, r=0, w=3):
    """Draw rectangle with optional rounded corners and outline."""
    if r:
        d.rounded_rectangle([(x0, y0), (x1, y1)], radius=r, fill=fill, outline=OL, width=w)
    else:
        d.rectangle([(x0, y0), (x1, y1)], fill=fill, outline=OL, width=w)

def ell(d, x0, y0, x1, y1, fill, w=3):
    """Draw ellipse with outline."""
    d.ellipse([(x0, y0), (x1, y1)], fill=fill, outline=OL, width=w)

def poly(d, pts, fill, w=3):
    """Draw polygon with outline."""
    d.polygon(pts, fill=fill)
    d.line(pts + [pts[0]], fill=OL, width=w, joint="curve")

def line(d, x0, y0, x1, y1, color=OL, w=3):
    """Draw thick line."""
    d.line([(x0, y0), (x1, y1)], fill=color, width=w, joint="curve")

# ═══════════════════════════════════════════════════════════════════════
# NATURE & SKY ELEMENTS
# ══════════════════════════════════════════════════════════════════════
def draw_tree(d, x, y, scale=1.0, tree_type="normal", tod="day"):
    """
    Draw a tree. 
    tree_type: "normal", "palm", "neem", "pine"
    (x, y) is the base of the trunk.
    """
    s = scale
    if tree_type == "palm":
        # Trunk (curved)
        pts = [(x - 8*s, y), (x + 8*s, y), (x + 4*s, y - 160*s), (x - 4*s, y - 160*s)]
        poly(d, pts, (160, 110, 60), w=2)
        # Coconuts
        ell(d, x - 12*s, y - 165*s, x - 2*s, y - 155*s, (80, 50, 30), w=1)
        ell(d, x + 2*s, y - 165*s, x + 12*s, y - 155*s, (80, 50, 30), w=1)
        # Leaves
        leaf_c = (60, 140, 60) if tod != "night" else (30, 70, 30)
        for ang in [-60, -30, 0, 30, 60, 120, -120]:
            rad = math.radians(ang)
            lx = x + math.cos(rad) * 70*s
            ly = (y - 160*s) + math.sin(rad) * 40*s
            poly(d, [(x, y - 160*s), (lx - 10*s, ly), (lx, ly + 10*s)], leaf_c, w=2)
    elif tree_type == "pine":
        # Trunk
        box(d, x - 6*s, y - 40*s, x + 6*s, y, (120, 80, 40), w=2)
        # Layers
        leaf_c = (40, 100, 50) if tod != "night" else (20, 50, 25)
        for i in range(3):
            ly = y - 40*s - (i * 45*s)
            lw = 50*s - (i * 10*s)
            poly(d, [(x - lw, ly), (x + lw, ly), (x, ly - 60*s)], leaf_c, w=2)
    elif tree_type == "neem":
        # Trunk
        box(d, x - 8*s, y - 80*s, x + 8*s, y, (130, 90, 50), w=2)
        # Bushy top
        leaf_c = (50, 120, 40) if tod != "night" else (25, 60, 20)
        ell(d, x - 50*s, y - 140*s, x + 50*s, y - 60*s, leaf_c, w=2)
        ell(d, x - 35*s, y - 170*s, x + 35*s, y - 110*s, _lt(leaf_c, 15), w=2)
    else:  # normal
        # Trunk
        box(d, x - 10*s, y - 100*s, x + 10*s, y, (110, 75, 45), w=2)
        # Crown
        leaf_c = (70, 150, 80) if tod != "night" else (35, 75, 40)
        ell(d, x - 60*s, y - 160*s, x + 60*s, y - 80*s, leaf_c, w=2)
        ell(d, x - 40*s, y - 190*s, x + 40*s, y - 130*s, _lt(leaf_c, 20), w=2)

def draw_cloud(d, x, y, scale=1.0):
    """Draw a fluffy cartoon cloud."""
    s = scale
    c = (255, 255, 255)
    ell(d, x - 40*s, y - 20*s, x + 20*s, y + 20*s, c, w=2)
    ell(d, x - 10*s, y - 40*s, x + 50*s, y + 10*s, c, w=2)
    ell(d, x + 20*s, y - 20*s, x + 80*s, y + 20*s, c, w=2)
    box(d, x - 30*s, y - 10*s, x + 70*s, y + 20*s, c, w=0)

def draw_sun_moon(d, x, y, scale=1.0, tod="day"):
    """Draw sun or moon based on time of day."""
    s = scale
    if tod == "night":
        # Moon
        ell(d, x - 30*s, y - 30*s, x + 30*s, y + 30*s, (240, 240, 210), w=2)
        # Craters
        ell(d, x - 10*s, y - 10*s, x, y, (210, 210, 180), w=0)
        ell(d, x + 5*s, y + 5*s, x + 15*s, y + 15*s, (210, 210, 180), w=0)
    else:
        # Sun
        ell(d, x - 35*s, y - 35*s, x + 35*s, y + 35*s, (255, 220, 100), w=2)
        # Rays
        for ang in range(0, 360, 45):
            rad = math.radians(ang)
            x1 = x + math.cos(rad) * 45*s
            y1 = y + math.sin(rad) * 45*s
            x2 = x + math.cos(rad) * 60*s
            y2 = y + math.sin(rad) * 60*s
            line(d, x1, y1, x2, y2, (255, 220, 100), w=3)

def draw_bird(d, x, y, scale=1.0):
    """Draw a simple flying bird (V-shape)."""
    s = scale
    line(d, x - 15*s, y, x, y + 8*s, OL, w=2)
    line(d, x, y + 8*s, x + 15*s, y, OL, w=2)

# ═══════════════════════════════════════════════════════════════════════
# STREET & PARK PROPS
# ═══════════════════════════════════════════════════════════════════════
def draw_bench(d, x, y, scale=1.0):
    """Draw a park/street bench."""
    s = scale
    # Legs
    box(d, x + 10*s, y - 30*s, x + 18*s, y, (60, 60, 60), w=2)
    box(d, x + 110*s, y - 30*s, x + 118*s, y, (60, 60, 60), w=2)
    # Seat
    box(d, x, y - 40*s, x + 130*s, y - 25*s, (160, 110, 60), w=2)
    # Backrest
    box(d, x + 5*s, y - 70*s, x + 125*s, y - 45*s, (160, 110, 60), w=2)
    # Slats
    line(d, x + 5*s, y - 60*s, x + 125*s, y - 60*s, OL, w=2)
    line(d, x + 5*s, y - 50*s, x + 125*s, y - 50*s, OL, w=2)

def draw_street_lamp(d, x, y, scale=1.0, tod="day"):
    """Draw a street lamp. Glows at night."""
    s = scale
    # Pole
    box(d, x - 6*s, y - 180*s, x + 6*s, y, (80, 80, 85), w=2)
    # Base
    box(d, x - 15*s, y - 10*s, x + 15*s, y + 5*s, (60, 60, 65), w=2)
    # Lamp head
    poly(d, [(x - 25*s, y - 180*s), (x + 25*s, y - 180*s), (x + 15*s, y - 210*s), (x - 15*s, y - 210*s)], (60, 60, 65), w=2)
    # Bulb
    bulb_c = (255, 240, 150) if tod == "night" else (220, 220, 200)
    ell(d, x - 10*s, y - 175*s, x + 10*s, y - 160*s, bulb_c, w=2)
    # Glow effect at night
    if tod == "night":
        ell(d, x - 40*s, y - 160*s, x + 40*s, y - 100*s, (255, 240, 150, 60), w=0)

def draw_car(d, x, y, scale=1.0, color=(200, 60, 60)):
    """Draw a basic cartoon car."""
    s = scale
    # Body bottom
    box(d, x, y - 50*s, x + 180*s, y - 10*s, color, r=10, w=3)
    # Body top (cabin)
    poly(d, [(x + 30*s, y - 50*s), (x + 60*s, y - 90*s), (x + 130*s, y - 90*s), (x + 150*s, y - 50*s)], _dk(color, 20), w=3)
    # Windows
    poly(d, [(x + 40*s, y - 50*s), (x + 65*s, y - 85*s), (x + 90*s, y - 85*s), (x + 90*s, y - 50*s)], (180, 220, 240), w=2)
    poly(d, [(x + 95*s, y - 50*s), (x + 95*s, y - 85*s), (x + 125*s, y - 85*s), (x + 140*s, y - 50*s)], (180, 220, 240), w=2)
    # Wheels
    ell(d, x + 25*s, y - 15*s, x + 55*s, y + 15*s, (30, 30, 35), w=2)
    ell(d, x + 125*s, y - 15*s, x + 155*s, y + 15*s, (30, 30, 35), w=2)
    # Rims
    ell(d, x + 35*s, y - 5*s, x + 45*s, y + 5*s, (180, 180, 190), w=1)
    ell(d, x + 135*s, y - 5*s, x + 145*s, y + 5*s, (180, 180, 190), w=1)

def draw_auto_rickshaw(d, x, y, scale=1.0):
    """Draw an Indian auto-rickshaw (Green/Yellow)."""
    s = scale
    # Bottom body (black/dark green)
    box(d, x, y - 40*s, x + 120*s, y - 5*s, (30, 30, 35), r=8, w=3)
    # Top roof (yellow/green)
    poly(d, [(x + 10*s, y - 40*s), (x + 30*s, y - 90*s), (x + 110*s, y - 90*s), (x + 115*s, y - 40*s)], (220, 190, 50), w=3)
    # Front windshield
    poly(d, [(x + 15*s, y - 40*s), (x + 30*s, y - 85*s), (x + 50*s, y - 85*s), (x + 50*s, y - 40*s)], (180, 220, 240), w=2)
    # Wheels
    ell(d, x + 15*s, y - 10*s, x + 35*s, y + 10*s, (30, 30, 35), w=2)
    ell(d, x + 85*s, y - 10*s, x + 105*s, y + 10*s, (30, 30, 35), w=2)

def draw_road_markings(d, x, y, width, scale=1.0):
    """Draw dashed road center line."""
    s = scale
    dash_len = 40 * s
    gap = 30 * s
    cx = x
    while cx < x + width:
        box(d, cx, y, cx + dash_len, y + 8*s, (240, 220, 100), w=0)
        cx += dash_len + gap

# ═══════════════════════════════════════════════════════════════════════
# ANIMALS (Street/Village)
# ═══════════════════════════════════════════════════════════════════════
def draw_cow(d, x, y, scale=1.0):
    """Draw a cartoon cow standing."""
    s = scale
    # Body
    box(d, x, y - 70*s, x + 140*s, y - 20*s, (240, 240, 235), r=20, w=3)
    # Spots
    ell(d, x + 20*s, y - 60*s, x + 50*s, y - 30*s, (40, 40, 45), w=0)
    ell(d, x + 80*s, y - 50*s, x + 110*s, y - 25*s, (40, 40, 45), w=0)
    # Head
    box(d, x + 130*s, y - 90*s, x + 180*s, y - 40*s, (240, 240, 235), r=15, w=3)
    # Horns
    poly(d, [(x + 140*s, y - 90*s), (x + 135*s, y - 110*s), (x + 145*s, y - 90*s)], (200, 180, 150), w=2)
    poly(d, [(x + 170*s, y - 90*s), (x + 175*s, y - 110*s), (x + 165*s, y - 90*s)], (200, 180, 150), w=2)
    # Legs
    box(d, x + 15*s, y - 20*s, x + 30*s, y + 10*s, (240, 240, 235), w=3)
    box(d, x + 45*s, y - 20*s, x + 60*s, y + 10*s, (240, 240, 235), w=3)
    box(d, x + 90*s, y - 20*s, x + 105*s, y + 10*s, (240, 240, 235), w=3)
    box(d, x + 120*s, y - 20*s, x + 135*s, y + 10*s, (240, 240, 235), w=3)
    # Tail
    line(d, x, y - 50*s, x - 20*s, y - 30*s, OL, w=3)
    ell(d, x - 25*s, y - 35*s, x - 15*s, y - 25*s, (40, 40, 45), w=1)

def draw_dog(d, x, y, scale=1.0):
    """Draw a cartoon street dog."""
    s = scale
    # Body
    box(d, x, y - 40*s, x + 90*s, y - 10*s, (180, 130, 80), r=15, w=3)
    # Head
    ell(d, x + 80*s, y - 60*s, x + 120*s, y - 20*s, (180, 130, 80), w=3)
    # Ears
    poly(d, [(x + 85*s, y - 55*s), (x + 75*s, y - 75*s), (x + 95*s, y - 50*s)], (140, 90, 50), w=2)
    # Legs
    box(d, x + 10*s, y - 10*s, x + 20*s, y + 15*s, (180, 130, 80), w=3)
    box(d, x + 30*s, y - 10*s, x + 40*s, y + 15*s, (180, 130, 80), w=3)
    box(d, x + 60*s, y - 10*s, x + 70*s, y + 15*s, (180, 130, 80), w=3)
    box(d, x + 75*s, y - 10*s, x + 85*s, y + 15*s, (180, 130, 80), w=3)
    # Tail (wagging up)
    line(d, x, y - 30*s, x - 20*s, y - 60*s, (180, 130, 80), w=4)

# ══════════════════════════════════════════════════════════════════════
# TAPRI (Chai Stall) PROPS
# ══════════════════════════════════════════════════════════════════════
def draw_kettle(d, x, y, scale=1.0):
    """Draw a steel chai kettle."""
    s = scale
    # Body
    box(d, x, y - 40*s, x + 50*s, y, (200, 205, 212), r=10, w=3)
    # Lid
    box(d, x + 5*s, y - 45*s, x + 45*s, y - 38*s, (180, 185, 192), r=4, w=2)
    # Spout
    poly(d, [(x + 50*s, y - 20*s), (x + 70*s, y - 30*s), (x + 70*s, y - 20*s), (x + 50*s, y - 10*s)], (190, 195, 202), w=2)
    # Handle
    line(d, x + 10*s, y - 30*s, x + 10*s, y - 10*s, (60, 60, 65), w=3)

def draw_kulhad(d, x, y, scale=1.0):
    """Draw a clay cup (kulhad)."""
    s = scale
    poly(d, [(x, y - 20*s), (x + 20*s, y - 20*s), (x + 15*s, y), (x + 5*s, y)], (180, 120, 80), w=2)
    # Tea inside
    ell(d, x + 2*s, y - 20*s, x + 18*s, y - 15*s, (140, 80, 40), w=0)

def draw_stove(d, x, y, scale=1.0):
    """Draw a gas stove with flame."""
    s = scale
    # Base
    box(d, x, y - 15*s, x + 60*s, y, (60, 60, 66), w=2)
    # Burner
    ell(d, x + 20*s, y - 18*s, x + 40*s, y - 10*s, (40, 40, 45), w=2)
    # Flame
    poly(d, [(x + 25*s, y - 18*s), (x + 30*s, y - 35*s), (x + 35*s, y - 18*s)], (255, 150, 40), w=1)
    poly(d, [(x + 28*s, y - 18*s), (x + 30*s, y - 28*s), (x + 32*s, y - 18*s)], (255, 220, 90), w=0)

# ══════════════════════════════════════════════════════════════════════
# VILLAGE PROPS
# ═══════════════════════════════════════════════════════════════════════
def draw_well(d, x, y, scale=1.0):
    """Draw a village well (kuan)."""
    s = scale
    # Base cylinder
    box(d, x, y - 40*s, x + 100*s, y, (160, 150, 140), r=10, w=3)
    # Water inside
    ell(d, x + 10*s, y - 40*s, x + 90*s, y - 20*s, (60, 100, 140), w=2)
    # Roof supports
    box(d, x + 10*s, y - 100*s, x + 20*s, y - 40*s, (110, 80, 50), w=2)
    box(d, x + 80*s, y - 100*s, x + 90*s, y - 40*s, (110, 80, 50), w=2)
    # Roof
    poly(d, [(x - 10*s, y - 100*s), (x + 110*s, y - 100*s), (x + 50*s, y - 140*s)], (180, 100, 50), w=3)
    # Rope and bucket
    line(d, x + 50*s, y - 120*s, x + 50*s, y - 30*s, (100, 80, 60), w=2)
    box(d, x + 40*s, y - 30*s, x + 60*s, y - 10*s, (140, 100, 60), w=2)

def draw_mud_house(d, x, y, scale=1.0):
    """Draw a simple village mud house (jhopdi)."""
    s = scale
    # Walls
    box(d, x, y - 100*s, x + 150*s, y, (190, 150, 105), w=3)
    # Roof (thatched)
    poly(d, [(x - 20*s, y - 100*s), (x + 170*s, y - 100*s), (x + 75*s, y - 160*s)], (150, 110, 50), w=3)
    # Thatch lines
    for i in range(5):
        line(d, x + 10*s + i*25*s, y - 100*s, x + 75*s, y - 150*s, (120, 85, 35), w=2)
    # Door
    box(d, x + 55*s, y - 60*s, x + 95*s, y, (90, 60, 40), w=2)

# ═══════════════════════════════════════════════════════════════════════
# BEACH & WATER PROPS
# ═══════════════════════════════════════════════════════════════════════
def draw_beach_umbrella(d, x, y, scale=1.0, color=(210, 60, 70)):
    """Draw a beach umbrella."""
    s = scale
    # Pole
    line(d, x, y, x, y - 150*s, (120, 80, 40), w=4)
    # Canopy
    poly(d, [(x - 60*s, y - 140*s), (x + 60*s, y - 140*s), (x, y - 180*s)], color, w=3)
    # Stripes
    poly(d, [(x - 20*s, y - 140*s), (x + 20*s, y - 140*s), (x, y - 180*s)], _lt(color, 40), w=0)

def draw_wave(d, x, y, width, scale=1.0):
    """Draw a simple cartoon wave line."""
    s = scale
    pts = []
    for i in range(0, int(width), 10):
        px = x + i
        py = y + math.sin(i * 0.1) * 10 * s
        pts.append((px, py))
    if len(pts) > 1:
        d.line(pts, fill=(255, 255, 255), width=int(3 * s), joint="curve")

# ═══════════════════════════════════════════════════════════════════════
# STATION PROPS
# ═══════════════════════════════════════════════════════════════════════
def draw_train_coach(d, x, y, scale=1.0, color=(60, 110, 190)):
    """Draw a single train coach."""
    s = scale
    # Body
    box(d, x, y - 120*s, x + 200*s, y, color, r=15, w=3)
    # Stripe
    box(d, x, y - 60*s, x + 200*s, y - 50*s, (240, 200, 60), w=0)
    # Windows
    for i in range(4):
        wx = x + 15*s + i * 45*s
        box(d, wx, y - 100*s, wx + 30*s, y - 70*s, (200, 228, 245), w=2)
    # Wheels
    ell(d, x + 20*s, y - 10*s, x + 50*s, y + 10*s, (30, 30, 35), w=2)
    ell(d, x + 150*s, y - 10*s, x + 180*s, y + 10*s, (30, 30, 35), w=2)
    # Connector
    box(d, x - 10*s, y - 40*s, x, y - 20*s, (60, 60, 65), w=2)

def draw_platform_bench(d, x, y, scale=1.0):
    """Draw a metal station bench."""
    s = scale
    # Legs
    box(d, x + 10*s, y - 30*s, x + 15*s, y, (80, 80, 85), w=2)
    box(d, x + 105*s, y - 30*s, x + 110*s, y, (80, 80, 85), w=2)
    # Seat
    box(d, x, y - 35*s, x + 120*s, y - 25*s, (100, 100, 105), w=2)
    # Backrest
    box(d, x + 5*s, y - 60*s, x + 115*s, y - 50*s, (100, 100, 105), w=2)

# ═══════════════════════════════════════════════════════════════════════
# MOUNTAIN PROPS
# ═══════════════════════════════════════════════════════════════════════
def draw_snow_peak(d, x, y, width, height, scale=1.0):
    """Draw a mountain with a snow cap."""
    s = scale
    # Mountain body
    poly(d, [(x, y), (x + width*s, y), (x + (width/2)*s, y - height*s)], (120, 140, 160), w=3)
    # Snow cap
    snow_y = y - height*s + (height * 0.3)*s
    poly(d, [(x + (width*0.3)*s, snow_y), (x + (width*0.7)*s, snow_y), (x + (width/2)*s, y - height*s)], (245, 248, 252), w=2)
    # Snow drips
    line(d, x + (width*0.4)*s, snow_y, x + (width*0.4)*s, snow_y + 20*s, (245, 248, 252), w=4)
    line(d, x + (width*0.6)*s, snow_y, x + (width*0.6)*s, snow_y + 15*s, (245, 248, 252), w=4)

# ═══════════════════════════════════════════════════════════════════════
# UTILITY: Apply props based on category
# ═══════════════════════════════════════════════════════════════════════
def apply_outdoor_props(img, category, tod, width, height, rng=None):
    """
    Automatically scatter props based on outdoor category.
    Called by background_draw.py after base background is drawn.
    """
    if rng is None:
        rng = random.Random(42)
    
    d = ImageDraw.Draw(img)
    ground_y = int(height * 0.75)
    
    if category == "park":
        draw_tree(d, 100, ground_y, 1.2, "normal", tod)
        draw_tree(d, width - 150, ground_y, 1.0, "neem", tod)
        draw_bench(d, width // 2 - 60, ground_y + 20, 1.0)
        draw_cloud(d, 200, 80, 1.0)
        draw_cloud(d, width - 250, 120, 0.8)
        draw_sun_moon(d, width - 100, 80, 1.0, tod)
        
    elif category == "street":
        draw_street_lamp(d, 150, ground_y, 1.0, tod)
        draw_street_lamp(d, width - 150, ground_y, 1.0, tod)
        draw_road_markings(d, 0, int(height * 0.85), width, 1.0)
        if rng.random() > 0.5:
            draw_auto_rickshaw(d, rng.randint(100, width - 300), ground_y + 10, 0.9)
        draw_cloud(d, 300, 100, 1.2)
        
    elif category == "village":
        draw_mud_house(d, 50, ground_y, 1.0)
        draw_well(d, width - 200, ground_y, 1.0)
        draw_tree(d, width // 2, ground_y, 1.1, "neem", tod)
        if rng.random() > 0.6:
            draw_cow(d, rng.randint(200, width - 200), ground_y + 10, 0.8)
        draw_sun_moon(d, 100, 80, 1.0, tod)
        
    elif category == "tapri":
        draw_stove(d, 150, ground_y - 40, 1.0)
        draw_kettle(d, 120, ground_y - 80, 1.0)
        draw_kulhad(d, 220, ground_y - 20, 1.0)
        draw_kulhad(d, 250, ground_y - 20, 1.0)
        draw_kulhad(d, 280, ground_y - 20, 1.0)
        draw_street_lamp(d, width - 100, ground_y, 0.8, tod)
        
    elif category == "beach":
        draw_beach_umbrella(d, 200, ground_y, 1.0, (210, 60, 70))
        draw_beach_umbrella(d, width - 250, ground_y, 1.0, (60, 150, 210))
        draw_wave(d, 0, int(height * 0.65), width, 1.0)
        draw_wave(d, 0, int(height * 0.70), width, 1.0)
        draw_sun_moon(d, width - 120, 100, 1.2, tod)
        
    elif category == "station":
        draw_platform_bench(d, 100, ground_y, 1.0)
        draw_platform_bench(d, width - 220, ground_y, 1.0)
        draw_train_coach(d, 0, ground_y + 20, 1.0)
        draw_street_lamp(d, width // 2, ground_y, 1.0, tod)
        
    elif category == "mountain":
        draw_snow_peak(d, 100, ground_y, 400, 300, 1.0)
        draw_snow_peak(d, width - 500, ground_y, 500, 400, 0.9)
        draw_tree(d, 50, ground_y, 0.8, "pine", tod)
        draw_tree(d, width - 80, ground_y, 0.9, "pine", tod)
        draw_bird(d, 300, 150, 1.0)
        draw_bird(d, 350, 130, 0.8)
        draw_bird(d, 320, 170, 0.9)
        
    return img
    
