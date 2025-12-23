from wand.image import Image
import random

from globals import GEN_DIR

def recolor(img: str, targs: list[str]):
    # thanks hexose
    with Image(filename=f"{GEN_DIR}{img}-base.png") as im:
        for targ in targs:
            im.opaque_paint(targ, f"#{random.randrange(0x1000000):06x}", 0.05)

        fn = f"{GEN_DIR}{img}-colored.png"
        im.save(filename=fn)
    return fn