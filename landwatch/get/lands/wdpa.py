import os

from warnings import warn
from ..util import _download_file, _unzip

from tempfile import TemporaryDirectory

from subprocess import Popen

import requests

from glob import glob

"""
wdpa.py
Tony Cannistra

Manages the data access of the World Database of Protected Areas.
"""

class WDPA(object):
    """
    Access WDPA protected areas dataset
    https://www.protectedplanet.net/
    """

    ZIP_SHP_DATA_URL = "https://www.protectedplanet.net/downloads/WDPA_Jun2020?type=shapefile"
    DATA_FILENAME = "WDPA_Jun2020.shp"

    def __init__(self, local_loc=None):
        self.local_loc = local_loc

    def unzip(self, destination, zipfile=None):
        """
        Unzip WDPA database file.

        WDPA Monthly extracts have several sub-files, which we also extract.

        Uses local_loc as zipfile root if zipfile is not specified.
        """
        if zipfile is None:
            zipfile = self.local_loc

        if not os.path.exists(destination):
            warn(f"Directory {destination} does not exist; creating...")
            os.makedirs(destination)

        zipdest = os.path.join(destination, WDPA.DATA_FILENAME)
        _unzip(zipfile, zipdest)

        result_zipfiles = glob(
            os.path.join(
                zipdest,
                "*.zip"
            )
        )

        for file in result_zipfiles:
            rootname = os.path.splitext(file)[0]
            _unzip(file, rootname)


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
        with TemporaryDirectory() as td:
            tmpfile = os.path.join(td, WDPA.DATA_FILENAME+'.zip')

            _download_file(WDPA.ZIP_SHP_DATA_URL, tmpfile)

            print("Unzipping file...")
            self.unzip(destination, tmpfile)
