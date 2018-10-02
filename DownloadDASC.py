#!/usr/bin/env python
import dascutils as du
from argparse import ArgumentParser


def main():
    p = ArgumentParser()
    p.add_argument('startend', help='start/end times UTC e.g. 2012-11-03T06:23Z', nargs=2)
    p.add_argument('-o', '--odir', help='directory to write downloaded FITS to', default='')
    p.add_argument('-c', '--overwrite', help='overwrite existing files', action='store_true')
    p.add_argument('-host', default='ftp://optics.gi.alaska.edu')
    p.add_argument('-s', '--site', help='EAA FYU KAK PKR TOO VEE', default='PKR')
    p.add_argument('-w', '--wl', help='Choose the wavelength', default=None)
    p = p.parse_args()

    # host = "ftp://mirrors.arsc.edu/AMISR/PKR/DASC/RAW/"
    du.download(p.startend, p.host, p.site, p.odir,p.wl)


if __name__ == '__main__':
    main()
