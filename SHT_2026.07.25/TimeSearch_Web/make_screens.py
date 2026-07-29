#!/usr/bin/env python3
"""
Generate the instruction screens for the Simplified Horizons Task.

Text is rendered here rather than exported from PowerPoint so the wording can be
edited in one place. Illustrations are cropped from the original slides, and the
paint-can diagrams are composed from the same stim images the task itself uses.

Edit TEXT below and re-run:  python3 make_screens.py
"""
from PIL import Image, ImageDraw, ImageFont
import textwrap, os

W, H = 1000, 600
OUT = "stim"
ILLUS = "/tmp/illus"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# --------------------------------------------------------------------------
# WORDING  — edit here
# --------------------------------------------------------------------------
TEXT = {
"welcome1": [
    "This is Ralphie. He is a painter.",
    "Ralphie needs paint for a big picture.",
    "Let's help him get as much paint as we can!",
],
"welcome2": [
    "We will go to lots of paint stores.",
    "Each store has four paint cans.",
    "You can't see what is inside them yet.",
    "When you pick a can, you get the paint inside, and you keep it.",
    "",
    "Let's try picking some cans!",
],
"fixed_choice_intro": [
    "At every store, the art store helper shows you some cans first.",
    "A hand points to the can he wants you to see.",
    "Pick the can the hand points to.",
    "",
    "Let's try it!",
],
"free_choice_intro": [
    "After that, you can pick any can you want.",
    "Every time you pick the same can, you get the same paint.",
    "",
    "Remember, pick the biggest splashes of paint you can!",
],
"horizons_intro": [
    "The store helper is busy, so you only get a few picks.",
    "You will see hands in the middle of the screen.",
    "They show how many picks you have.",
    "Sometimes you get 4 picks. Sometimes you get 1 pick.",
    "Sometimes you will see a cloud.",
    "That means you don't know how many picks you have.",
    "",
    "When your picks are gone, you go on to the next store.",
    "",
    "Let's try it!",
],
# same screen with the ambiguous sentences removed, used when the cloud
# condition is switched off in the setup panel
"horizons_intro_ls": [
    "The store helper is busy, so you only get a few picks.",
    "You will see hands in the middle of the screen.",
    "They show how many picks you have.",
    "Sometimes you get 4 picks. Sometimes you get 1 pick.",
    "",
    "When your picks are gone, you go on to the next store.",
    "",
    "Let's try it!",
],
"practice_intro": [
    "Now let's practice at a few stores.",
    "These ones are just for practice.",
],
"comprehension": [
    "Comprehension questions",
    "",
    "(experimenter: ask now, record on your sheet)",
],
"ready": [
    "Great! Now let's help Ralphie for real.",
    "Remember, pick the biggest splashes of paint you can.",
    "Ralphie is counting on you. Are you ready?",
],
"break1": [
    "You are getting so much paint!",
    "Here's Ralphie hard at work.",
],
"break2": [
    "You are getting so much paint!",
    "Keep going — Ralphie needs just a little more.",
],
"end": [
    "Good job!",
    "Thank you for helping Ralphie get paint!",
],
}

# which cropped illustration sits on each screen, and how tall it is drawn
ART = {
    "welcome1":  ("ralphie_easel",   230),
    "ready":     ("ralphie_ready",   210),
    "break1":    ("ralphie_working", 250),
    "break2":    ("palette",         200),
    "end":       ("ralphie_done",    250),
}

# --------------------------------------------------------------------------

def draw_text(d, lines, font, top, wrap=62, lh=36):
    """Left-aligned inside a centred block. Centred text forces the eye to find a
    new left edge on every line, which is slower to read."""
    segs = []
    for ln in lines:
        segs.append(None) if not ln else segs.extend(textwrap.wrap(ln, width=wrap))
    widest = max((d.textlength(t, font=font) for t in segs if t), default=0)
    x = (W - widest) / 2
    y = top
    for t in segs:
        if t is None:
            y += lh // 2
            continue
        d.text((x, y), t, font=font, fill="black")
        y += lh
    return y


def text_height(d, lines, font, wrap=62, lh=36):
    n = 0
    for ln in lines:
        n += 0.5 if not ln else len(textwrap.wrap(ln, width=wrap))
    return int(n * lh)


def can_row(img, centres, splashes, hand_on=None, cy=None, can_h=150):
    """Draw a row of paint cans, optionally with splashes or a pointing hand."""
    can = Image.open(os.path.join(OUT, "circle_gray.png")).convert("RGBA")
    ratio = can.size[0] / can.size[1]
    ch = can_h
    cw = int(ch * ratio)
    for i, cx in enumerate(centres):
        img.alpha_composite(can.resize((cw, ch)), (int(cx - cw / 2), int(cy - ch / 2)))
        s = splashes[i]
        if s == "?":
            d = ImageDraw.Draw(img)
            f = ImageFont.truetype(FONT, int(ch * 0.34))
            t = "?"
            w = d.textlength(t, font=f)
            d.text((cx - w / 2, cy - ch * 0.24), t, font=f, fill="black")
        elif isinstance(s, float):
            sp = Image.open(os.path.join(OUT, "paint_yellow.png")).convert("RGBA")
            sw = int(ch * s)
            img.alpha_composite(sp.resize((sw, sw)), (int(cx - sw / 2), int(cy - sw / 2)))
        if hand_on == i:
            hd = Image.open(os.path.join(OUT, "choices.png")).convert("RGBA")
            hh = int(ch * 0.52)
            hw = int(hh * hd.size[0] / hd.size[1])
            img.alpha_composite(hd.resize((hw, hh)), (int(cx - hw / 2), int(cy - hh / 2)))


def build(name, lines):
    img = Image.new("RGBA", (W, H), "white")
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT, 22)

    th = text_height(d, lines, font)

    if name in ART:
        art_name, art_h = ART[name]
        art = Image.open(os.path.join(ILLUS, art_name + ".png")).convert("RGBA")
        aw = int(art_h * art.size[0] / art.size[1])
        block = th + 24 + art_h
        top = (H - block) // 2
        y = draw_text(d, lines, font, top)
        img.alpha_composite(art.resize((aw, art_h)), ((W - aw) // 2, int(y + 24)))

    elif name == "welcome2":
        block = th + 30 + 150
        top = (H - block) // 2
        y = draw_text(d, lines, font, top)
        can_row(img, [330, 500, 670], ["?", "?", "?"], cy=y + 30 + 75)

    elif name == "fixed_choice_intro":
        block = th + 30 + 150
        top = (H - block) // 2
        y = draw_text(d, lines, font, top)
        can_row(img, [400, 600], ["?", "?"], hand_on=1, cy=y + 30 + 75)

    elif name == "free_choice_intro":
        block = th + 30 + 150
        top = (H - block) // 2
        y = draw_text(d, lines, font, top)
        can_row(img, [330, 500, 670], ["?", 0.62, 0.26], cy=y + 30 + 75)

    else:
        draw_text(d, lines, font, (H - th) // 2)

    out = os.path.join(OUT, name + "_screen.png")
    img.convert("RGB").save(out, optimize=True)
    return out


if __name__ == "__main__":
    for name, lines in TEXT.items():
        p = build(name, lines)
        print("wrote", p)
