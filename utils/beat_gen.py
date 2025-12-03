import time

from .math_utils import lcm_from_array
from PIL import Image, ImageDraw
from io import BytesIO
import random

square_side = 32

def beat_gen(beatmap, grouping, bpm, kind):
    frames_per_beat = 3
    mspf_raw = (1/((bpm/60)*grouping*frames_per_beat))*1000
    mspf = int((mspf_raw//10) * 10)

    random.seed(time.time())
    total_frames = frames_per_beat * len(beatmap)
    print(bpm, " ", grouping, " ",len(beatmap), " ", total_frames)
    if total_frames > 2000:
        print("Too many frames to generate")
        return None

    total_length = square_side * len(beatmap)
    total_height = square_side
    images = []
    color_squares = [(random.randint(10,255), random.randint(10,255), random.randint(10,255)) for _ in range(len(beatmap))]
    for frame in range(total_frames):
        im = Image.new("RGB", (total_length, total_height), (0,0,0))
        draw = ImageDraw.Draw(im)
        square_idx = frame//frames_per_beat
        square_mod = frame%frames_per_beat
        if beatmap[square_idx] != '-':
            draw.rectangle([
                square_side*square_idx,
                0,
                square_side*square_idx+square_side,
                square_side
            ], fill=(tuple(map(lambda x: int(x*(1/(square_mod+1))), color_squares[square_idx]))))
        else:
            draw.rectangle([
                square_side*square_idx,
                0,
                square_side*square_idx+square_side,
                square_side
            ], fill=(tuple(map(lambda x: int(x*(1/(square_mod+1))), (15, 15, 15)))))
        images.append(im)
    out = BytesIO()
    images[0].save(out, format="GIF", save_all=True, append_images=images[1:], optimize = False, duration=mspf, loop = 0)
    out.seek(0)
    return out
