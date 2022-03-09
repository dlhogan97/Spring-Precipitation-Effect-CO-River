import act

ftp = ftplib.FTP('ftp.archive.arm.gov') # Connect to NOAA's FTP
ftp.login() # Anonymous login
ftp.cwd('./hogand1/230468')

files = ftp.nlst() # Collect files into vector
ftp.close()

met_files = []
for file in files:
    if 'gucmetM1.b1' in file:
        met_files.append(file)

# used this as reference: https://towardsdatascience.com/an-efficient-way-to-read-data-from-the-web-directly-into-python-a526a0b4f4cb
url = 'ftp://ftp.archive.arm.gov/hogand1/230468/' + met_files[-2]

req = urllib.request.Request(url)
with urllib.request.urlopen(req) as resp:

    act.io.armfiles.read_netcdf(f'{ceil}/*')
