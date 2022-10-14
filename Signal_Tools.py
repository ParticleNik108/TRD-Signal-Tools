


# These are functions to assist with the extraction of TRD signals 
#-----------------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelextrema

def start_stop(det_batch):
    
    # compute the counts of the detectors in the adc batch 
    det_count = np.unique(det_batch, return_counts=True)
    
    # get the cumulative counts of the detectors
    det_cum_count = det_count[1].cumsum()
    
    # get the length
    length_det_count = len(det_count[0])
    
    # initialize empty start and end lists 
    s = []
    e = []
    
    
    for i in range(0, length_det_count):
        
        # if theres less than 4 instances then ignore 
        if det_count[1][i] < 4:
            continue
            
        # if its the first index ie. zero then ...
        if i==0:
            s.append(0)
            e.append(det_cum_count[0])
            
            
        else:
            s.append(det_cum_count[i-1])
            e.append(det_cum_count[i])
            
    return s, e



def get_imgs(det_batch, adc_batch):
    
    
    # initialize empty lists to store info
    imgs = []
    img_dets = []
    #chan = []
    
    # get the start_stop range of the detector instances 
    
    s, e = start_stop(det_batch)
    
    for i in range(len(s)):
        
        # compute the indices that are a local maxima within a particular det instance range
        
        indices = argrelextrema(adc_batch[s[i]:e[i]].sum(axis=1), np.greater, order=3)[0]
        
        # if theres no maxima for the det instance then skip and move to next s[i] and e[i]
        if len(indices)==0:
            continue
        
        # then get the imgs 
        else:
            for j in range(len(indices)):
            
                imgs.append(adc_batch[s[i]:e[i]][indices[j]-1:indices[j]+2].flatten())
                img_dets.append(det_batch[s[i]])
                #chan.append(chan_batch[s[i]:e[i]][indices[j]-1:indices[j]+2])
                #img_dets.append(det_count[0][i])
            
    return imgs, img_dets





def tracklet_range(tracklets_fentry):
    
    t_start = []
    t_end = []
    
    L = len(tracklets_fentry)
    
    for t in range(1,L):
        
        #if t==0:
         #   t_start.append(0)
          #  t_end.append(tracklets_fentry[1])
            
        #now fill up the lists 
        #else:
            #if (tracklets_fentry[t-1] == tracklets_fentry[t]):
                #continue
                
        if (tracklets_fentry[t]-tracklets_fentry[t-1])<50:
            continue
        else:        
            t_start.append(tracklets_fentry[t-1])
            t_end.append(tracklets_fentry[t])
            
    return t_start, t_end




def extract_sigs(trackranges, det, adcs_np):
    
    SIGS = []
    DETS = []
    
    t_s, t_e = tracklet_range(trackranges)
    
    
    for r in range(len(t_s)):
        
        images, detectors = get_imgs(det[t_s[r]:t_e[r]], adcs_np[t_s[r]:t_e[r]])
        SIGS = SIGS + images
        DETS = DETS + detectors
            
        #SIGS.append(images)
        #DETS.append(detectors)
                                                                    
    
    return SIGS, DETS




def viz(adc_array):
    
    fig, ax = plt.subplots(figsize=(10, 7))
    im=ax.imshow(adc_array)
    ax.set_aspect(aspect=4.0)
    #ax.set_yticks(ticks=[], labels=[""])
    #ax.set_ylabel("Pads")
    ax.set_xlabel("Time bin (100ns)")
    cbar = ax.figure.colorbar(im, ax=ax, shrink=0.56)
    cbar.ax.set_title("ADC")


