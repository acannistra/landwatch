import unittest
import requests
from os import path
from .util import _download_file
from tempfile import TemporaryDirectory


class TestDownloadFile(unittest.TestCase):
    def test_download(self):
        test_url = "https://f001.backblazeb2.com/file/t11a-xyz/20190414_192837-1555520806.jpg"
        tmpdir = TemporaryDirectory()
        outpath_true = path.join(tmpdir.name, "true.html")
        outpath_test = path.join(tmpdir.name, "test.html")

        with open(outpath_true, "wb") as f:
            r = requests.get(test_url)
            f.write(r.content)

        _download_file(test_url, outpath_test)

        true = open(outpath_true, "rb")  # pragma: no cover
        test = open(outpath_test, "rb")

        self.assertEqual(str(true.read()), str(test.read()))

        true.close()
        test.close()
        tmpdir.cleanup()
