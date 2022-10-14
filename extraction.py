
# This contains code to open a root tree and get the trd signals and corresponding detectors
# this uses Signal_Tools.py



from Signal_Tools import *
import matplotlib.pyplot as plt
import numpy as np
import uproot
import pandas as pd
from scipy.signal import argrelextrema
import awkward as ak

#----------------------------------------------------------------------------------
# open the root files and get the o2sim branch
file_d = uproot.open("trddigits.root")["o2sim"]
file_t = uproot.open("trdtracklets.root")["o2sim"]

# Get the adc arrays of each timeframe as numpy array 

adcs_np = file_d['TRDDigit/TRDDigit.mADC[30]'].array(library='np')[0]

# Get the detectors as an awkward array
det = ak.flatten(file_d['TRDDigit/TRDDigit.mDetector'].arrays(), axis=None)

# Get the first entries of the tracklets 

tracklet_r = np.unique(ak.flatten(file_t['TrackTrg/TrackTrg.mTrackletDataRange.mFirstEntry'].arrays(), axis=None))


# Now get the signals 

trdsigs = extract_sigs(tracklet_r, det, adcs_np)


# Make columns names for the adc arrays 
names = ['HN00', 'HN01', 'HN02', 'HN03', 'HN04', 'HN05', 'HN06', 'HN07', 'HN08', 'HN09', 'HN10',
'HN11', 'HN12', 'HN13', 'HN14', 'HN15', 'HN16', 'HN17', 'HN18', 'HN19', 'HN20',
'HN21', 'HN22', 'HN23', 'HN24', 'HN25', 'HN26', 'HN27', 'HN28', 'HN29',
'M00', 'M01', 'M02', 'M03', 'M04', 'M05', 'M06', 'M07', 'M08', 'M09', 'M10', 
'M11', 'M12', 'M13', 'M14', 'M15', 'M16', 'M17', 'M18', 'M19', 'M20', 'M21', 'M22', 'M23', 
'M24', 'M25', 'M26', 'M27', 'M28', 'M29',
'LN00', 'LN01', 'LN02', 'LN03', 'LN04', 'LN05', 'LN06', 'LN07', 'LN08', 'LN09', 'LN10',
'LN11', 'LN12', 'LN13', 'LN14', 'LN15', 'LN16', 'LN17', 'LN18', 'LN19', 'LN20', 'LN21', 
'LN22', 'LN23', 'LN24', 'LN25', 'LN26', 'LN27', 'LN28', 'LN29']

# Convert to a pandas dataframe and save as csv 

df1 = pd.DataFrame(trdsigs[0], columns=names)
df2 = pd.DataFrame(trdsigs[1], columns=["Detector"])

df = pd.concat([df1, df2], axis=1)

# save to a csv file 

df.to_csv("signals.csv", index=False)

