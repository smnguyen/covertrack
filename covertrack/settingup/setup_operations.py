import glob
from os.path import join
import os

# Both functions modify argdict to store the channels (`argdict['channels']`)
# and image frames associated with each channel (`argdict['channeldict']`)

def retrieve_files(argdict, imgdir, holder, channels):
    chdict = {}
    for ch in channels:
        pathset = [join(imgdir, file_name) for file_name in os.listdir(imgdir)
                   if ch in file_name]
        chdict[ch] = sorted(pathset)[argdict['first_frame']:argdict['last_frame']]
    argdict['channeldict'] = chdict
    argdict['channels'] = channels
    return argdict


# glob: associates channels based on a filename pattern, e.g. '*channel000*.png' = 'CFP'
def retrieve_files_glob(argdict, imgdir, holder, channels, patterns):
    chdict = {}
    for ch, pattern in zip(channels, patterns):
        pathset = glob.glob(join(imgdir, pattern))
        chdict[ch] = pathset[argdict['first_frame']:argdict['last_frame']]
    argdict['channeldict'] = chdict
    argdict['channels'] = channels
    return argdict
