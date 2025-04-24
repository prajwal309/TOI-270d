import numpy as np
import matplotlib.pyplot as plt
import glob
from scipy.ndimage import filters
from scipy.signal import gaussian
from bisect import bisect


import matplotlib as mpl
mpl.rc('font', family='sans-serif', size=25)
mpl.rc('font', serif='Helvetica Neue')
mpl.rc('font', serif='Skia')
mpl.rc('text', usetex='True')
mpl.rc('ytick',**{'major.pad':5, 'color':'black', 'major.size':11,'major.width':1.5, 'minor.size':5,'minor.width':0.75})
mpl.rc('xtick',**{'major.pad':5, 'color':'black',  'major.size':11,'major.width':1.5, 'minor.size':5,'minor.width':0.75})
#mpl.rc('mathtext',**{'default':'regular','fontset':'cm','bf':'monospace:bold'})
mpl.rc('axes',**{'linewidth':1.0,'edgecolor':'black'})



def binSpectrum(Wavelength, Spectrum):
    binningData = np.loadtxt("tierra/Combined.R100.txt", skiprows=1)
    newWavelength = binningData[:,2]

    Model = np.empty((len(newWavelength)))

    for counter, (WLower, WUpper) in enumerate(zip(binningData[:,0], binningData[:,1])):
        
        WLowerIndex = bisect(Wavelength, WLower)
        WUpperIndex = bisect(Wavelength, WUpper)
        #print("WLower, WUpper", WLower, WUpper)
        #print("WLowerIndex, WUpperIndex", WLowerIndex, WUpperIndex)
        #input("Wait here...")
        Model[counter] = np.mean(Spectrum[WLowerIndex:WUpperIndex])

    return newWavelength, Model


def moving_average(series, sigma=3):
    b = gaussian(300, sigma)
    average = filters.convolve1d(series, b/b.sum())
    var = filters.convolve1d(np.power(series-average,2), b/b.sum())
    return average, var


allFiles = np.array(glob.glob("models/*.txt"))


fig, ax = plt.subplots(figsize=(12, 8), nrows=2, ncols=1, sharex=True, gridspec_kw={'height_ratios': [2, 1]})

for filecounter, fileName in enumerate(allFiles):
    currentColor = plt.cm.hot(filecounter/len(allFiles))
    dataContent = np.loadtxt(fileName, skiprows=1)
    currentWavelength = dataContent[:,0]*1e4
    currentSpectrum = dataContent[:,1]*1e6
    NewWavelength, NewModel = binSpectrum(currentWavelength, currentSpectrum) 

    ax[0].plot(NewWavelength, NewModel, label=fileName.split("/")[-1].split("_")[0], color=currentColor)
    if "CS1" in fileName:
        refSpectrum = NewModel
ax[0].legend(loc=1, fontsize=8)       
ax[0].set_xlabel("Wavelength (microns)")   
ax[0].set_ylabel("Transit Depth [ppm]")

for filecounter, fileName in enumerate(allFiles):
    if "CS1" in fileName:
        continue
    currentColor = plt.cm.hot(filecounter/len(allFiles))
    dataContent = np.loadtxt(fileName, skiprows=1)
    currentWavelength = dataContent[:,0]*1e4
    currentSpectrum = dataContent[:,1]*1e6
    NewWavelength, NewModel = binSpectrum(currentWavelength, currentSpectrum) 
       
    ax[1].plot(NewWavelength, NewModel-refSpectrum, color=currentColor)
ax[1].set_xlim(min(dataContent[:,0]*1e4), max(dataContent[:,0]*1e4))
ax[1].set_xlabel("Wavelength (microns)")
ax[1].set_ylabel("Model Difference [ppm]")
ax[1].axhline(0, color='black', linestyle='--', linewidth=3)

plt.tight_layout()
plt.show()