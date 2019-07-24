
URL = "https://archive.scryfall.com/json/scryfall-oracle-cards.json"

# 17 = CMC
# 18 = type line
# 19 = oracle text
# 20 = colors
# 21 = color identity
# 22 = 
TARGET_COLUMN = 17

from pandas import read_json
import numpy as np
import matplotlib.pyplot as plt

try:
    # [OPTIONAL] Seaborn makes plots nicer
    import seaborn
except ImportError:
    pass

def download_data():

    frame = read_json(
        URL
        )

    return frame[[156, 157, 158, TARGET_COLUMN]]