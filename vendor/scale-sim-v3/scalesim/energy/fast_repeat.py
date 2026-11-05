"""Chunked equivalent of the legacy repeated-access counter."""
import numpy as np

def _unique_count(a):
    s=np.sort(a,axis=1)
    valid=s>=0
    valid[:,1:] &= s[:,1:]!=s[:,:-1]
    return valid.sum(axis=1)

def count(memory,bank_size,row_size,chunk=4096):
    total=0
    for start in range(1,len(memory),chunk):
        stop=min(start+chunk,len(memory))
        # Keep legacy address-one handling exactly for reproducibility.
        current=memory[start:stop,1:].copy()
        current=(current-(np.abs(current)==1)*2)//row_size
        previous=[]
        indices=np.arange(start,stop)
        for offset in range(1,bank_size+1):
            old=memory[np.maximum(indices-offset,0),1:].copy()
            old[indices-offset<0]=-1
            previous.append((old-(np.abs(old)==1)*2)//row_size)
        past=np.concatenate(previous,axis=1)
        # same-cycle duplicate count plus distinct current/past intersection
        unique_now=_unique_count(current)
        duplicates=(current>=0).sum(axis=1)-unique_now
        intersection=_unique_count(past)+unique_now-_unique_count(np.concatenate((past,current),axis=1))
        total+=int(np.sum(duplicates+intersection))
    return total
