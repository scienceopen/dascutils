#!/usr/bin/env python
from pathlib import Path
from time import sleep
import ftplib
from pytz import UTC
from datetime import datetime
from dateutil.parser import parse
from urllib.parse import urlparse
#
from histutils.fortrandates import forceutc

def getdasc(start,end,host,site,odir='',clobber=False):
    """
    year,month,day: integer
    hour, minute:  start,stop integer len == 2
    """
    start = forceutc(start)
    end   = forceutc(end)

    parsed = urlparse(host)
    ftop = parsed[1]
    fpath = parsed[2] + site
    odir = Path(odir).expanduser()
    print(f'downloading to {odir.resolve()}')
#%% get available files for this day
    rpath = f'{fpath}/DASC/RAW/{start.year:4d}/{start.year:4d}{start.month:02d}{start.day:02d}'

    with ftplib.FTP(ftop,'anonymous','guest',timeout=15) as F:
        F.cwd(rpath)
        dlist = F.nlst()
        for f in dlist:
#%% file in time range
            #print (int(round(float(f[27:31]))))
            t = forceutc(datetime.strptime(f[14:-9],'%Y%m%d_%H%M%S'))
            if  start <= t <= end:
#%% download file
                ofn = odir / f
                if not clobber:
                    if ofn.is_file(): #do filesizes match, if so, skip download
                        rsize = F.size(f)
                        if ofn.stat().st_size == rsize:
                            print(f'SKIPPING existing {ofn}')
                            continue

                print(ofn)
                with ofn.open('wb') as h:
                    F.retrbinary(f'RETR {f}', h.write)
                    sleep(1) # anti-leech


if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('start',help='start time UTC e.g. 2012-11-03T06:23Z')
    p.add_argument('end',help='end time UTC e.g. 2012-11-03T06:25Z')
    p.add_argument('-o','--odir',help='directory to write downloaded FITS to',default='')
    p.add_argument('-c','--clobber',help='clobber (overwrite) existing files',action='store_true')
    p.add_argument('--host',default='ftp://optics.gi.alaska.edu')
    p.add_argument('-s','--site',help='EAA FYU KAK PKR TOO VEE',default='PKR')
    p = p.parse_args()

#host = "ftp://mirrors.arsc.edu/AMISR/PKR/DASC/RAW/"
    start = parse(p.start)
    end = parse(p.end)

    getdasc(start,end, p.host,p.site, p.odir, p.clobber)
