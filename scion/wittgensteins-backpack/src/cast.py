"""The cast: engraved dignitary rig + album-art fragments (substitution objects)."""
import math
from engine import *
from engine import _hatch, _src, _ac
from constraints import REST, two_bone

DARK = (205, 196, 176)    # far-side limbs are printed a shade darker
COAT = (58, 54, 60)
SKIN = (238, 214, 186)

# ------------------------------------------------------------------ engraved dignitary parts
# authored facing RIGHT; limb parts authored pointing DOWN with pivot at the top joint.

def limb(sid, length, w0, w1, fill, hatch_ang=80, gap=4.2, cuff=None, shade=True):
    pts = [(-w0 / 2, 0), (w0 / 2, 0), (w1 / 2, length), (-w1 / 2, length)]
    shapes = [dict(pts=pts, fill=fill, hatch=(hatch_ang, gap, 1.1), outline=2.2)]
    if shade:
        shapes.append(dict(pts=[(w0 / 2 - w0 * 0.38, 0), (w0 / 2, 0), (w1 / 2, length), (w1 / 2 - w1 * 0.38, length)],
                           fill=fill, hatch=(hatch_ang, gap * 0.6, 1.1), cross=(hatch_ang - 70, 4.5, 1.0), outline=0))
    if cuff:
        shapes.append(dict(pts=[(-w1 / 2 - 1, length - 9), (w1 / 2 + 1, length - 9), (w1 / 2 + 1, length), (-w1 / 2 - 1, length)],
                           fill=(250, 246, 236), hatch=(0, 4, 0.8), outline=1.6))
    # round joint caps so card joints read as pivots, not breaks
    shapes.append(dict(ellipse=(-w0 / 2, -w0 / 2, w0 / 2, w0 / 2), fill=fill, hatch=(hatch_ang, gap, 1.1), outline=2.2))
    return engrave(shapes, (0, 0), sid, f"engraved limb segment ({sid})")


def make_dignitary(prefix="dig", coat=COAT, far=False):
    f = DARK if far else PAPER
    P = {}
    P["thigh"] = limb(prefix + "_thigh", REST["thigh"], 30, 24, (90, 86, 92) if not far else (70, 66, 72), 75, 3.6)
    P["shin"] = limb(prefix + "_shin", REST["shin"], 24, 20, (90, 86, 92) if not far else (70, 66, 72), 75, 3.6)
    P["upper"] = limb(prefix + "_upper", REST["upper"], 24, 21, coat if not far else (44, 40, 46), 70, 3.4)
    P["fore"] = limb(prefix + "_fore", REST["fore"], 21, 18, coat if not far else (44, 40, 46), 70, 3.4, cuff=True)
    # boot: pivot at ankle, toe to the right
    P["foot"] = engrave([dict(pts=[(-10, -8), (10, -8), (14, 4), (36, 6), (40, 14), (-12, 14)], fill=(40, 34, 30),
                              hatch=(20, 3, 1), outline=2),
                         dict(pts=[(-12, 11), (40, 11), (40, 14), (-12, 14)], fill=(20, 16, 14), outline=0)],
                        (0, 0), prefix + "_foot", "engraved boot")
    # gloved hand: pivot at wrist
    P["hand"] = engrave([dict(ellipse=(-10, -2, 12, 20), fill=(250, 246, 236), hatch=(30, 4, 0.8), outline=2,
                              lines=[[(2, 10), (8, 16)], [(-2, 12), (2, 19)]])], (0, 0), prefix + "_hand", "engraved glove")
    # frock coat torso, pivot at pelvis; neck at (0,-150)
    K = 1.38  # stockier coat
    X = lambda pts: [(x * K, y) for x, y in pts]
    coat_pts = [(-34, 34), (-40, -40), (-36, -120), (-24, -146), (24, -146), (34, -118), (36, -50), (30, 0), (46, 40), (8, 36), (-10, 24)]
    vest = [(4, -140), (22, -138), (26, -60), (12, -40), (2, -60)]
    P["torso"] = engrave([
        dict(pts=X(coat_pts), fill=coat, hatch=(70, 3.2, 1.1), outline=2.5),
        dict(pts=X([(-34, 34), (-40, -40), (-36, -120), (-24, -146), (-10, -146), (-16, -40), (-12, 26)]), fill=coat,
             hatch=(70, 2.2, 1.1), cross=(10, 3.6, 1), outline=0),
        dict(pts=X(vest), fill=(232, 222, 196), hatch=(90, 3.0, 0.8), outline=1.8),
        dict(pts=[(-12, -150), (18, -150), (24, -138), (4, -132), (-14, -138)], fill=(252, 250, 244), outline=1.8,
             lines=[[(4, -136), (4, -120)]]),
        dict(pts=[(0, -134), (10, -134), (6, -118)], fill=(30, 26, 40), outline=1),  # cravat
        dict(lines=[[(19, -110), (19, -109)], [(22, -92), (22, -91)], [(23, -74), (23, -73)]], lw=4),
        dict(lines=[[(5, -138), (-5, -70)], [(30, -138), (41, -100)]], lw=1.8),
    ], (0, 0), prefix + "_torso", "engraved frock-coat torso")
    # head in profile with top hat & mutton chops; pivot at neck base
    face = [(-16, 0), (-22, -24), (-20, -52), (0, -60), (16, -54), (20, -42), (34, -34), (22, -28), (24, -20),
            (20, -14), (24, -10), (14, -2), (6, 6)]
    HK = 1.45
    HS = lambda pts: [(x * HK, y * HK) for x, y in pts]
    HE = lambda e: tuple(v * HK for v in e)
    P["head"] = engrave([
        dict(pts=HS(face), fill=SKIN, hatch=(60, 4.6, 0.7), outline=2.2),
        dict(pts=HS([(-16, 0), (-22, -24), (-20, -44), (-6, -44), (-2, -26), (6, -8), (6, 6)]), fill=(110, 100, 96),
             hatch=(80, 2.0, 1.1), cross=(20, 3, 1), outline=1.5),  # mutton chops
        dict(pts=HS([(-26, -54), (30, -54), (30, -60), (-26, -60)]), fill=(26, 22, 24), outline=1.5),          # brim
        dict(pts=HS([(-18, -58), (22, -58), (20, -128), (-16, -128)]), fill=(36, 32, 36), hatch=(88, 2.2, 1), cross=(0, 6, 1), outline=2),
        dict(pts=HS([(-17, -72), (21, -72), (21, -80), (-17, -80)]), fill=(120, 30, 30), outline=1),             # hat band
        dict(ellipse=HE((9, -44, 15, -38)), fill=(255, 255, 255), outline=1.5),
        dict(lines=[HS(l) for l in [[(6, -48), (18, -50)], [(16, -16), (22, -15)]]], lw=2),
    ], (0, 0), prefix + "_head", "engraved dignitary head (generic Victorian type; not a portrait)")
    return P


# ------------------------------------------------------------------ small engraved props
def make_beetle(k=1.0):
    shapes = [dict(ellipse=(-22, -14, 18, 14), fill=(70, 56, 40), hatch=(30, 2.4, 1), cross=(120, 3.5, 0.8), outline=2,
                   lines=[[(-2, -14), (-2, 14)]]),
              dict(ellipse=(16, -9, 32, 9), fill=(40, 32, 26), hatch=(90, 2, 1), outline=2),
              dict(lines=[[(30, -4), (42, -14)], [(30, 4), (42, 14)]], lw=1.6)]
    for i, x in enumerate((-14, -2, 10)):
        shapes.append(dict(lines=[[(x, -12), (x - 6, -22), (x - 12, -24)], [(x, 12), (x - 6, 22), (x - 12, 24)]], lw=2))
    if k != 1.0:
        import copy
        def S(v): return [(x * k, y * k) for x, y in v]
        for sh in shapes:
            if "pts" in sh: sh["pts"] = S(sh["pts"])
            if "ellipse" in sh: sh["ellipse"] = tuple(v * k for v in sh["ellipse"])
            if "lines" in sh: sh["lines"] = [S(l) for l in sh["lines"]]
            for key in ("hatch", "cross"):
                if key in sh: a_, g_, w_ = sh[key]; sh[key] = (a_, g_ * k * 0.6, w_ * k * 0.6)
            sh["outline"] = sh.get("outline", 2) * k * 0.6; sh["lw"] = sh.get("lw", 1.5) * k * 0.6
    return engrave(shapes, (0, 0), "beetle" if k == 1.0 else "beetle_big", "engraved beetle (top view)", edge=3 if k == 1 else 10)


def make_duckrabbit():
    """Ambiguous head: read with bill to the left = duck; rotated so 'bill' points up = rabbit ears."""
    shapes = [
        dict(pts=[(-10, -6), (-80, -22), (-96, -14), (-82, -4), (-96, 4), (-80, 12), (-10, 8)], fill=(232, 220, 190),
             hatch=(10, 3.8, 0.9), outline=2.4, lines=[[(-80, -4), (-30, 0)]]),          # bill / ears
        dict(ellipse=(-24, -36, 46, 34), fill=(232, 220, 190), hatch=(50, 4.2, 0.9), outline=2.6),  # skull
        dict(ellipse=(-8, -16, 4, -4), fill=(20, 18, 16), outline=1),                           # eye
        dict(pts=[(30, 20), (46, 14), (48, 26), (36, 30)], fill=(200, 180, 150), outline=1.8),   # rabbit mouth / duck nape
        dict(pts=[(0, 30), (30, 30), (24, 60), (-6, 60)], fill=(232, 220, 190), hatch=(50, 4.2, 0.9), outline=2.4),  # neck
    ]
    return engrave(shapes, (10, 60), "duckrabbit", "original ambiguous duck/rabbit head drawn for this video")


def make_bottle():
    pts = [(-16, -150), (16, -150), (18, -110), (70, -60), (78, 0), (78, 120), (-78, 120), (-78, 0), (-70, -60), (-18, -110)]
    return engrave([dict(pts=pts, fill=(214, 232, 226), hatch=(100, 7, 0.7), outline=3,
                         lines=[[(-60, -30), (-60, 90)], [(-48, -40), (-48, 60)]], lw=3, line_color=(250, 255, 250)),
                    dict(pts=[(-20, -160), (20, -160), (18, -146), (-18, -146)], fill=(150, 110, 70), hatch=(0, 2, 1), outline=2)],
                   (0, 120), "bottle", "engraved fly-bottle")


def make_fly(k=1.0):
    E = lambda *v: tuple(x * k for x in v)
    return engrave([dict(ellipse=E(-8, -14, 2, -2), fill=(230, 240, 250), outline=1 * k, hatch=(0, 2 * k, 0.5 * k),
                         lines=[[E(-6, -12)[:2], E(0, -4)[:2]]], lw=0.6 * k),
                    dict(ellipse=E(-2, -14, 8, -2), fill=(230, 240, 250), outline=1 * k, hatch=(0, 2 * k, 0.5 * k)),
                    dict(ellipse=E(-6, -4, 6, 4), fill=(20, 20, 20), outline=1 * k, hatch=(80, 1.2 * k, 0.4 * k), ink=(70, 70, 60)),
                    dict(ellipse=E(4, -3, 9, 3), fill=(120, 20, 20), outline=0.8 * k)],
                   (0, 0), "fly" if k == 1 else "fly_big", "engraved fly", edge=2 if k == 1 else 12, ss=2 if k == 1 else 1)


def make_doorway(w, h, sid):
    return engrave([dict(pts=[(0, 0), (w, 0), (w, h), (0, h)], fill=(14, 10, 8), hatch=(45, 3, 1), outline=2),
                    dict(pts=[(-5, -5), (w + 5, -5), (w + 5, 0), (-5, 0)], fill=(240, 230, 205), outline=1.5),
                    dict(pts=[(w, -5), (w + 5, -5), (w + 5, h), (w, h)], fill=(240, 230, 205), outline=1.5),
                    dict(pts=[(-5, -5), (0, -5), (0, h), (-5, h)], fill=(240, 230, 205), outline=1.5),
                    dict(pts=[(0, h - 10), (w, h - 10), (w, h), (0, h)], fill=(60, 50, 40), hatch=(0, 2, 1), outline=1)],
                   (0, 0), sid, "dark doorway cut")


def make_hand_giant():
    pts = [(-60, -400), (60, -400), (64, -40), (90, -20), (96, 10), (70, 40), (-40, 50), (-66, 10), (-64, -40)]
    return engrave([dict(pts=pts, fill=(250, 246, 236), hatch=(80, 5, 0.8), outline=3,
                         lines=[[(-30, 40), (-30, 0)], [(0, 46), (0, 0)], [(30, 44), (30, 0)]], lw=2),
                    dict(pts=[(-62, -400), (62, -400), (62, -330), (-62, -330)], fill=(58, 54, 60), hatch=(70, 3, 1), outline=2)],
                   (0, 50), "giant_hand", "engraved giant hand from above (interrupt operator)")


# ------------------------------------------------------------------ album-art fragments
CLIMB = "Boxback climb under sodium light.png"
FROGDJ = "Neon Frog on the Back Porch.png"
MASK = "Corrugated Mask With Shipping Boxes.png"
LUMBAR = "Boxback lumbar brace flat-lay.png"
MOUNTAIN = "Boxback Mountain Frog Warehouse.png"
REFUGEE = "Refugee of the Boxback.png"

STACK_ROWS = [("BOX", 202, 262), ("KNOX", 262, 326), ("FOX", 326, 392), ("SOCKS", 392, 460), ("CLOCKS", 460, 528),
              ("BLOCKS", 528, 598), ("ROCKS", 598, 672), ("LOCKS", 672, 742), ("KNOCKS", 742, 812)]


def make_fragments():
    F = {}
    F["backpack"] = cut_photo(MASK, (38, 252, 236, 452), "backpack_box", height=118, pivot="center", rough=2.5)
    F["boxhead"] = cut_photo(MASK, [(512, 20), (1000, 18), (1004, 100), (950, 460), (930, 720), (560, 730), (520, 470), (500, 110)],
                             "boxhead_fragile", height=200, pivot=(740, 720), rough=0)
    F["smallbox"] = cut_photo(MASK, (175, 455, 370, 640), "small_box", height=56, pivot="bottom", rough=2)
    F["door_panel"] = engrave([dict(pts=[(0, 0), (76, 0), (76, 78), (0, 78)], fill=(214, 176, 120), hatch=(90, 4, 1), outline=3),
                               dict(pts=[(8, 8), (68, 8), (68, 36), (8, 36)], fill=(196, 156, 100), hatch=(0, 3, 0.8), outline=2),
                               dict(pts=[(8, 44), (68, 44), (68, 70), (8, 70)], fill=(196, 156, 100), hatch=(0, 3, 0.8), outline=2),
                               dict(ellipse=(60, 36, 70, 46), fill=(240, 200, 80), outline=2)],
                              (0, 0), "door_panel", "engraved panel door (two panels, brass knob)", edge=2)
    F["frog_dj"] = cut_photo(FROGDJ, [(300, 520), (420, 470), (560, 500), (690, 600), (700, 720), (640, 800), (560, 900),
                                      (380, 940), (250, 900), (240, 720)], "frog_dj", height=170, pivot="bottom", rough=0)
    F["frog_boxed"] = cut_photo(LUMBAR, [(870, 800), (1010, 770), (1170, 830), (1190, 960), (1220, 1170), (850, 1175), (880, 960)],
                                "frog_boxedin", height=120, pivot="bottom", rough=0)
    F["logo"] = cut_photo(CLIMB, (700, 140, 1245, 312), "boxback_logo", height=170, rough=3)
    F["coolradio"] = cut_photo(CLIMB, (760, 55, 1195, 122), "coolradio_label", height=56, rough=2)
    F["etubrute"] = cut_photo(LUMBAR, (300, 14, 975, 190), "etubrute_sticker", height=120, rough=2)
    F["boxscore"] = cut_photo(LUMBAR, [(30, 900), (250, 870), (290, 1100), (60, 1170)], "boxscore_sticker", height=150)
    F["packanimal"] = cut_photo(LUMBAR, [(50, 160), (200, 110), (320, 200), (300, 400), (90, 440)], "packanimal_sticker", height=160)
    F["cassette"] = cut_photo(LUMBAR, (615, 950, 870, 1110), "cassette", height=90, rough=1)
    F["handlecare"] = cut_photo(LUMBAR, (470, 470, 800, 650), "handle_with_care", height=120, rough=2)
    F["labels"] = []
    for i, (word, y0, y1) in enumerate(STACK_ROWS):
        x1 = 690 + i * 9
        F["labels"].append(cut_photo(CLIMB, (505 + i * 3, y0, x1, y1), "label_" + word.lower(), height=None, pivot="bottom",
                                     rough=1.5, seed=20 + i))
    F["fragile_box"] = cut_photo(CLIMB, (520, 812, 830, 965), "label_fragile", pivot="bottom", rough=2)
    return F


def backgrounds():
    """Backgrounds: procedural engraved paper stage + toned album-art plates."""
    B = {}
    rnd = np.random.default_rng(7)
    paper = np.ones((H, W, 3), np.float32) * np.array(PAPER, np.float32)
    grain = rnd.normal(0, 6, (H, W, 1)).astype(np.float32)
    yy, xx = np.mgrid[0:H, 0:W]
    vig = 1 - 0.28 * (((xx - W / 2) / (W * 0.7)) ** 2 + ((yy - H / 2) / (H * 0.8)) ** 2)
    paper = np.clip(paper * vig[..., None] + grain, 0, 255).astype(np.uint8)
    base = Image.fromarray(paper).convert("RGBA")
    stage = base.copy()
    sky = _hatch((W, 600), 0, 7, 1, (120, 104, 84, 60), jitter=0.8, seed=3)
    stage.alpha_composite(sky, (0, 0))
    floor = Image.new("RGBA", (W, H - 600), (210, 196, 166, 255))
    floor.alpha_composite(_hatch((W, H - 600), 0, 4, 1, (90, 74, 56, 120), seed=5))
    stage.alpha_composite(floor, (0, 600))
    d = ImageDraw.Draw(stage)
    d.line([(0, 600), (W, 600)], fill=INK + (255,), width=3)
    # engraved proscenium curtains
    for side in (0, 1):
        x0 = 0 if side == 0 else W - 120
        cur = Image.new("RGBA", (120, 600), (120, 30, 34, 255))
        cur.alpha_composite(_hatch((120, 600), 88, 5, 2, (40, 8, 10, 200), seed=8 + side))
        stage.alpha_composite(cur, (x0, 0))
        d.line([(x0 + (120 if side == 0 else 0), 0), (x0 + (120 if side == 0 else 0), 600)], fill=INK + (255,), width=3)
    B["paper"] = base
    B["stage"] = stage

    def plate(src, box, sat=0.6, dark=0.75):
        im = _src(src).crop(box).resize((W, H), Image.LANCZOS)
        im = print_tone(im, sat=sat, contrast=1.05)
        im = ImageEnhance.Brightness(im).enhance(dark).convert("RGBA")
        im.alpha_composite(_hatch((W, H), 30, 6, 1, (0, 0, 0, 26), seed=4))
        return im
    B["mountain"] = plate(MOUNTAIN, (0, 140, 1254, 845), 0.75, 0.8)
    B["pallets"] = plate(LUMBAR, (0, 400, 1254, 1105), 0.55, 0.62)
    B["stairs"] = plate(CLIMB, (760, 560, 1254, 838), 0.6, 0.6)
    B["truck"] = plate(REFUGEE, (0, 250, 1254, 955), 0.6, 0.7)
    for k in ("mountain", "pallets", "truck", "stairs"):
        B[k + "_soft"] = ImageEnhance.Brightness(B[k].filter(ImageFilter.GaussianBlur(3))).enhance(0.55)
    B["stairs"] = ImageEnhance.Brightness(B["stairs"]).enhance(1.35)
    LEDGER["bg_stage"] = {"kind": "procedural", "note": "engraved paper stage", "rights": "original"}
    for k, (s, bx) in {"bg_mountain": (MOUNTAIN, (0, 140, 1254, 845)), "bg_pallets": (LUMBAR, (0, 400, 1254, 1105)),
                       "bg_stairs": (CLIMB, (760, 560, 1254, 838)), "bg_truck": (REFUGEE, (0, 250, 1254, 955))}.items():
        LEDGER[k] = {"kind": "album-art-plate", "source": "Et tu, Brute (BOXBACK)/" + s, "crop_box_px": list(bx),
                     "rights": "producer's own BOXBACK album artwork in this repository (hartswf0/moto)"}
    return B


# ------------------------------------------------------------------ rig: pose -> joints -> draw
class Figure:
    """Pivot/card-joint rig. Pose angles are FORWARD-positive degrees from hanging straight down
    (forward = facing direction). draw() renders far limbs, backpack, torso, head, near limbs."""

    def __init__(self, near, far):
        self.near, self.far = near, far

    @staticmethod
    def fk(pelvis, face=1, lean=0.0, hip=(0, 0), knee=(0, 0), sh=(0, 0), el=(0, 0), head=0.0):
        """hip/knee/sh/el = (near, far) local angles. Returns joint dict."""
        cw = lambda fwd: -fwd * face  # forward-positive -> clockwise screen angle
        J = {"pelvis": pelvis, "lean": lean, "face": face, "head_rot": head}
        torso_cw = lean * face
        J["neck"] = add(pelvis, rot((0, -REST["torso"]), torso_cw))
        J["shoulder"] = add(pelvis, rot((REST["sh_off"][0] * face, REST["sh_off"][1]), torso_cw))
        J["back"] = add(pelvis, rot((-62 * face, -92), torso_cw))
        for i, side in enumerate(("n", "f")):
            a_th = cw(hip[i]) + 0; k = add(pelvis, down_vec(a_th, REST["thigh"]))
            a_sh = a_th + cw(knee[i]); an = add(k, down_vec(a_sh, REST["shin"]))
            J["knee_" + side], J["ankle_" + side] = k, an
            J["foot_rot_" + side] = 0.0
            a_up = torso_cw + cw(sh[i]); e = add(J["shoulder"], down_vec(a_up, REST["upper"]))
            a_fo = a_up + cw(el[i]); h = add(e, down_vec(a_fo, REST["fore"]))
            J["elbow_" + side], J["hand_" + side] = e, h
        return J

    @staticmethod
    def from_solver(b, face=1, far_arm=None):
        J = {"pelvis": b["pelvis"], "lean": b["lean"] * face if False else b["lean"], "face": face, "head_rot": 0.0}
        J["neck"], J["shoulder"] = b["neck"], b["shoulder"]
        torso_cw = b["lean"]
        J["back"] = add(b["pelvis"], rot((-62 * face, -92), torso_cw))
        J["knee_n"], J["ankle_n"], J["knee_f"], J["ankle_f"] = b["knee_n"], b["ankle_n"], b["knee_f"], b["ankle_f"]
        J["foot_rot_n"] = J["foot_rot_f"] = 0.0
        J["elbow_n"], J["hand_n"] = b["elbow"], b["hand"]
        e = add(J["shoulder"], down_vec(torso_cw + 8 * face, REST["upper"]))
        J["elbow_f"], J["hand_f"] = e, add(e, down_vec(torso_cw - 20 * face, REST["fore"]))
        J["lean_cw"] = torso_cw
        return J

    def draw(self, dst, J, scale=1.0, head_sprite=None, head_scale=1.0, head_offset=(0, 0), backpack=None,
             backpack_scale=1.0, draw_head=True, after_torso=None, alpha=1.0, extra_head_rot=0.0, hide=(), strap=True):
        face = J["face"]
        P0 = J["pelvis"]
        S = lambda p: add(P0, mul(sub(p, P0), scale))
        torso_cw = J.get("lean_cw", J["lean"] * face)
        fx = 1 if face > 0 else -1

        def seg(spr, a, b, part):
            if part in hide: return
            blit(dst, spr, S(a), seg_angle(a, b), fx * scale, scale, alpha)

        # far side first
        seg(self.far["upper"], J["shoulder"], J["elbow_f"], "far_arm")
        seg(self.far["fore"], J["elbow_f"], J["hand_f"], "far_arm")
        if "far_arm" not in hide:
            blit(dst, self.far["hand"], S(J["hand_f"]), seg_angle(J["elbow_f"], J["hand_f"]), fx * scale, scale, alpha)
        seg(self.far["thigh"], J["pelvis"], J["knee_f"], "far_leg")
        seg(self.far["shin"], J["knee_f"], J["ankle_f"], "far_leg")
        if "far_leg" not in hide:
            blit(dst, self.far["foot"], S(J["ankle_f"]), J["foot_rot_f"] * fx, fx * scale, scale, alpha)
        if backpack is not None and "backpack" not in hide:
            blit(dst, backpack, S(J["back"]), torso_cw, scale * backpack_scale, None, alpha)
        if "torso" not in hide:
            blit(dst, self.near["torso"], S(J["pelvis"]), torso_cw, fx * scale, scale, alpha)
        if backpack is not None and "backpack" not in hide and strap:
            a = S(add(J["pelvis"], rot((14 * fx, -140), torso_cw))); b = S(add(J["pelvis"], rot((-8 * fx, -64), torso_cw)))
            ImageDraw.Draw(dst).line([a, b], fill=(30, 26, 22, int(255 * alpha)), width=max(2, int(9 * scale)))
        if after_torso:
            after_torso(S)
        if draw_head and "head" not in hide:
            hs = head_sprite or self.near["head"]
            hpos = add(S(J["neck"]), mul(head_offset, scale))
            hr = torso_cw + J.get("head_rot", 0.0) * fx + extra_head_rot
            blit(dst, hs, hpos, hr, fx * scale * head_scale, scale * head_scale, alpha)
        seg(self.near["thigh"], J["pelvis"], J["knee_n"], "near_leg")
        seg(self.near["shin"], J["knee_n"], J["ankle_n"], "near_leg")
        if "near_leg" not in hide:
            blit(dst, self.near["foot"], S(J["ankle_n"]), J["foot_rot_n"] * fx, fx * scale, scale, alpha)
        seg(self.near["upper"], J["shoulder"], J["elbow_n"], "near_arm")
        seg(self.near["fore"], J["elbow_n"], J["hand_n"], "near_arm")
        if "near_arm" not in hide:
            blit(dst, self.near["hand"], S(J["hand_n"]), seg_angle(J["elbow_n"], J["hand_n"]), fx * scale, scale, alpha)


def stand_pelvis_y(floor_y):
    return floor_y - REST["thigh"] - REST["shin"] - 6


def walk_pose(pelvis_x, floor_y, phase, face=1, stride=24, arms=True, lean=4):
    """Cutout walk: stepped card swings (Gilliam walks are blunt and readable, not smooth)."""
    s = math.sin(phase)
    hip_n, hip_f = stride * s, -stride * s
    knee_n = -max(0, 30 * math.sin(phase + 1.3)); knee_f = -max(0, 30 * math.sin(phase + 1.3 + math.pi))
    bob = abs(math.cos(phase)) * 5
    py = stand_pelvis_y(floor_y) - bob + 4
    sh = (-18 * s, 18 * s) if arms else (0, 0)
    return Figure.fk((pelvis_x, py), face, lean, (hip_n, hip_f), (knee_n, knee_f), sh, (14, 14))


def stand_pose(px, floor_y, face=1, lean=0, sh=(6, -4), el=(10, 10), head=0, crouch=0.0):
    k = crouch * 50
    J = Figure.fk((px, stand_pelvis_y(floor_y) + crouch * 12), face, lean, (k * 0.5 + 4, k * 0.5 - 6),
                  (-k, -k), sh, el, head)
    # re-plant feet on the floor exactly after crouch (vertical card slide)
    dy = floor_y - 6 - max(J["ankle_n"][1], J["ankle_f"][1])
    for key in list(J):
        if isinstance(J[key], tuple) and key not in ("pelvis",):
            pass
    if abs(dy) > 0.01:
        J = Figure.fk((px, J["pelvis"][1] + dy), face, lean, (k * 0.5 + 4, k * 0.5 - 6), (-k, -k), sh, el, head)
    return J
