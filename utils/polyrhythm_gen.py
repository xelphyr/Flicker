import time

from .math_utils import lcm_from_array
from PIL import Image, ImageDraw
from io import BytesIO
import random

square_side = 8

def polyrhythm_gen(requested_polyrhthyms, bpm):
    mspf_raw = (1/(bpm/60))*1000
    mspf = (mspf_raw//10) * 10

    random.seed(time.time())
    total_frames = lcm_from_array(requested_polyrhthyms)
    if total_frames > 2000:
        print("Too many frames to generate")
        return
    total_length = square_side * len(requested_polyrhthyms)
    total_height = square_side
    images = []
    color_squares = [(random.randint(10,255), random.randint(10,255), random.randint(10,255)) for _ in range(len(requested_polyrhthyms))]
    for frame in range(total_frames):
        im = Image.new("RGB", (total_length, total_height), (0,0,0))
        draw = ImageDraw.Draw(im)
        for j in range(len(requested_polyrhthyms)):
            if frame%requested_polyrhthyms[j] == 0:
                draw.rectangle([
                    square_side*j,
                    0,
                    square_side*j+square_side,
                    square_side
                ], fill=(color_squares[j]))
        images.append(im)
    out = BytesIO()
    images[0].save(out, format="GIF", save_all=True, append_images=images[1:], optimize = False, duration=mspf, loop = 0)
    out.seek(0)
    return out

polyrhythm_gen([2,3], 120)
