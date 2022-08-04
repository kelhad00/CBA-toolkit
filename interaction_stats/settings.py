import os, sys
script_path = os.path.realpath(os.path.dirname("IBPY_files"))
os.chdir(script_path)
sys.path.append("..")
from IBPY_files.db import *


OHE = True         # One hot encoding option for the datasets.
REC_TSTEP = 20      # Step (in ms) between each sample recovered from the video.
MODEL_TYPE = 'cnn'  # Model type we want to train between rnn, cnn and crf.
FRAME_LEN = 2000    # Length of a frame (in ms) for one sequence
FRAME_TSTEP = 2000  # How many ms the frame move between each record

EAF_FORMATS = {
    'ccdb': form_pairs_ccdb,
    'ifadv': form_pairs_ifadv,
    'ndc': form_pairs_ndc
}