import numpy as np
import random
from relaxed import run
from config import PATH, PLOT, VARIATIONS, SEED, VISUALIZE

if __name__ == '__main__':
    if SEED >= 0:
        np.random.seed(SEED)
        random.seed(SEED)

    run(VARIATIONS, PATH, PLOT, vis = VISUALIZE, quiet = False)