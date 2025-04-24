from tierra import Target
from tierra.transmission import TransmissionSpectroscopy
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import ascii
import os





dataRead = ascii.read('data/TOI270d_Photochem_COgrid_100xSolar_CO10.txt')

print(dataRead.columns)
'''
plt.figure(figsize=(10, 6))
plt.plot(dataRead['temperature'], dataRead['pressure'], "ko")
plt.gca().invert_yaxis()
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Temperature (K)', fontsize=20)
plt.ylabel('Pressure (bar)', fontsize=20)
plt.title('TOI-270d', fontsize=20)
plt.tight_layout()
plt.show()


plt.figure(figsize=(10, 6))
plt.plot(dataRead['H2O'], dataRead['pressure'], "k-",label="H2O")
plt.plot(dataRead['CO'], dataRead['pressure'], "b-",label="CO")
plt.plot(dataRead['CH4'], dataRead['pressure'], "r-", label="CH4")
plt.gca().invert_yaxis()
plt.legend(loc=1)
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Temperature (K)', fontsize=20)
plt.ylabel('Pressure (bar)', fontsize=20)
plt.title('TOI-270d', fontsize=20)
plt.tight_layout()
plt.show()'''




print("Now plot the data.")

def ParsePlanetFile():
    '''
    This function parses the planetary file
    '''
    PlanetParams = {}
    if os.path.exists("data/PlanetParam.ini"):
        FileContent = open("data/PlanetParam.ini", "r").readlines()
        for Line in FileContent:
            Item = Line.split("#")[0].replace(" ","")
            key, Value = Item.split(":")
            PlanetParams[key]=float(Value)
    else:
        print("PlanetParam.ini does not exist in the local dictionary")
    return PlanetParams


def ParseStarFile():
    '''
    This function parses the star file i.e StelarParam.ini
    '''
    StellarParams = {}
    if os.path.exists("data/StellarParam.ini"):
        FileContent = open("data/StellarParam.ini", "r").readlines()
        for Line in FileContent:
            Item = Line.split("#")[0].replace(" ","")
            key, Value = Item.split(":")
            StellarParams[key]=float(Value)
    else:
        print("StellarParam.HJ.ini does not exist in the local dictionary")
    return StellarParams







PlanetParamsDict = ParsePlanetFile()
StellarParamsDict = ParseStarFile()
print(PlanetParamsDict)
print(StellarParamsDict)



BaseLocation =  "/media/prajwal/LaCie1/TierraCrossSections/Nature_CrossSections"


for CSType in ["CS_1", "CS_5", "CS_6", "CS_7"]:
        
    CurrentSystem = Target.System(PlanetParamsDict, StellarParamsDict, LoadFromFile=False)
    CurrentSystem.LoadCrossSection(BaseLocation, SubFolder=CSType, CIA=True)
    CurrentSystem.InitiateSystem()
    CurrentSystem.PT_Profile(zStep=0.25, ShowPlot=False)
    print("The mean molecular mass of the atmosphere is given by:", CurrentSystem.mu)
    T1 = TransmissionSpectroscopy(CurrentSystem)
    T1.CalculateTransmission(CurrentSystem)

    print("Saved the text.")
    np.savetxt(f"models/{CSType}_TransmissionModel.txt",np.transpose((CurrentSystem.WavelengthArray, T1.Spectrum)), header='Wavelength (nm) Transmission', comments='')
    #Save the cross-section based on this


plt.figure(figsize=(10, 6))
plt.plot(CurrentSystem.WavelengthArray, T1.Spectrum, "ko")
plt.xlabel('Wavelength (nm)', fontsize=20)
plt.ylabel('Transmission', fontsize=20)
plt.tight_layout()
plt.show()




#Use first cross-section to generate the model

#Use the second cross-section to generate the model

