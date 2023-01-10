# ----------------------------------
# Import Python modules
# ----------------------------------
import numpy as np

merra_collection = 'MERRA2_MONTHLY'
shortname = 'M2TMNXLND'
version = '5.12.4'

longname = 'tavgM_2d_lnd_Nx'
product = 'GWETPROF'
years = np.arange(2004,2023,1)
months = np.arange(1,13,1)
urls = []
for year in years:
    for mo in months: 
        if mo < 10:
            mo = '0'+str(mo)
        if year < 2012:
            col_num = 'MERRA2_300'
        else: 
            col_num = 'MERRA2_400'
        urls.append(f'https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2_MONTHLY/{shortname}.{version}/{year}/{col_num}.{longname}.{year}{mo}.nc4.nc4?{product}[0:0][254:260][115:120],time,lat[254:260],lon[115:120]')
with open(r'merra2_urls.txt','w') as fp:
    for url in urls:
        fp.write(f"{url}\n")
    print('Done!')
# use this to get files 
# wget --load-cookies ~/.urs_cookies --save-cookies ~/.urs_cookies --auth-no-challenge=on --keep-session-cookies --content-disposition -i subset_M2TMNXLND_5.12.4_20221219_203407_.txt