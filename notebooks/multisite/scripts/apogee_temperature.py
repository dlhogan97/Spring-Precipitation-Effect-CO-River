from metpy.units import units
def apogee2temp(dat,tower):
# hard-coded sensor-specific calibrations
    Vref = 2.5
    ID = dat[f"IDir_{tower}"].values
    sns = [136, 137, 138, 139]
    im = [ sns.index(x) if x in sns else None for x in ID ][0]
# unclear if we want these, or scaled up versions
    mC0 = [57508.575,56653.007,58756.588,58605.7861][im]
    mC1 = [289.12189,280.03380,287.12487,285.00285][im]
    mC2 = [2.16807,2.11478,2.11822,2.08932][im]
    bC0 = [-168.3687,-319.9362,-214.5312,-329.6453][im]
    bC1 = [-0.22672,-1.23812,-0.59308,-1.24657][im]
    bC2 = [0.08927,0.08612,0.10936,0.09234][im]
# read data
    Vtherm = dat[f"Vtherm_{tower}"].values
    Vpile = dat[f"Vpile_{tower}"].values*1000
# calculation of detector temperature from Steinhart-Hart
    Rt = 24900.0/((Vref/Vtherm) - 1)
    Ac = 1.129241e-3
    Bc = 2.341077e-4
    Cc = 8.775468e-8
    TDk = 1/(Ac + Bc*np.log(Rt) + Cc*(np.log(Rt)**3))
    TDc = TDk - 273.15
# finally, calculation of "target" temperature including thermopile measurement
    m = mC2*TDc**2 + mC1*TDc + mC0
    b = bC2*TDc**2 + bC1*TDc + bC0
    TTc = (TDk**4 + m*Vpile + b)**0.25 - 273.15
    # sufs = suffixes(TTc,leadch='') # get suffixes
    # dimnames(TTc)[[2]] = paste0("Tsfc.Ap.",sufs)
    TTc = TTc * units('celsius')
    return TTc