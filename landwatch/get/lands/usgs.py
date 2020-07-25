import os

from warnings import warn
from ..util import _download_file

from tempfile import TemporaryDirectory

from subprocess import Popen

import requests


"""
usgs.py
Tony Cannistra

Manages the data access of USGS datasets, including:
    * Protected Areas Database (PAD-US) 2.0

"""

UNZIP_CMD = "unzip -u -o {zipfile} -d {outdir}"

class USGSProtectedLands(object):
    """Access USGS Protected Lands data"""
    ZIP_SHP_DATA_URL = "https://www.sciencebase.gov/catalog/file/get/5b030c7ae4b0da30c1c1d6de?f=__disk__97%2F0a%2F32%2F970a32899eb4389aaf8b3abf61b6bc7fde229df8"
    DATA_FILENAME = "USGSPAD.shp.zip"
    def __init__(self, local_loc=None, alternate_src=None):
        self.local_loc = local_loc
        self.alternate_src = alternate_src

    def unzip(self, destination, zipfile=None):
        """Unzip USGS Protected Lands database file. Uses local_loc if zipfile is not specified"""
        if zipfile is None:
            zipfile = self.local_loc

        if not os.path.exists(destination):
            warn(f"Directory {destination} does not exist; creating...")
            os.makedirs(destination)

        Popen(UNZIP_CMD.format(
            zipfile = zipfile,
            outdir = os.path.join(destination, "usgs_pad.shp")
        ), shell=True).communicate()

    def download(self, destination):

        """
        Download and unzip PAD-US data into destination.

        Throws warning if local_loc was given at class initialization,
        re-downloading may be unnecessary in this case.
        """
        if self.local_loc:
            warn("Local location of dataset already provided."
                 "Re-running download in this case will result"
                 "in extra bandwidth usage and download times.")

        print("Downloading...")
        srcpath = self.alternate_src if self.alternate_src else ZIP_SHP_DATA_URL
        with TemporaryDirectory() as td:
            tmpfile = os.path.join(td, "pad-us.zip")

            _download_file(srcpath, tmpfile)

            print("Unzipping file...")


            Popen(UNZIP_CMD.format(
                zipfile = tmpfile,
                outdir = os.path.join(destination, "usgs_pad.shp")
            ), shell=True).communicate()

            self.local_loc = outdir

    def savedb(self, destination=None, layers=["PADUS2_0Fee"], fed_only=True):
        """
        Filters the original data and writes a Spatialite database
        containing PADUS2_0Fee layer. Provide `layers` as a list
        to specify alternative layers.

        Fed_only only keeps lands under federal management (default true)

        Reprojects to EPSG:4326.
        """
        destination = self.local_loc if not destination else destination
        destination = os.path.join(destination, "usgspad.sqlite")

        if os.path.exists(destination):
            print(f"warning: {destination} exists! It will be appended to.")

        filter = "SELECT * FROM PADUS2_0Fee"
        filter = filter + " WHERE Mang_Type = 'FED'" if fed_only else filter


        for layer in layers:
            SAVECMD = (
                f"ogr2ogr -progress -f \"SQLite\" {destination} -nlt MULTIPOLYGON -nln {layer} "
                f"-dsco SPATIALITE=YES -dialect sqlite -append -t_srs EPSG:4326 -sql \"" + filter + "\" "
                f"{self.local_loc} "
            )
            print(SAVECMD)
            Popen(SAVECMD, shell=True).communicate()
