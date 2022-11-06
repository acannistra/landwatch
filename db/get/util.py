import requests
from tqdm import tqdm
from subprocess import Popen


def _download_file(url, destination):
    r = requests.get(url, stream=True)
    # Total size in bytes.
    total_size = int(r.headers.get("content-length", 0))

    block_size = 1024  # 1 Kibibyte

    t = tqdm(total=total_size, unit="iB", unit_scale=True)

    with open(destination, "wb") as f:
        for data in r.iter_content(block_size):

            t.update(len(data))
            f.write(data)

    t.close()
    if total_size != 0 and t.n != total_size:
        raise Exception(f"Download error (size: {total_size} != {t.n})")


UNZIP_CMD = "unzip -u -o {zipfile} -d {outdir}"


def _unzip(file, dest):
    Popen(UNZIP_CMD.format(zipfile=file, outdir=dest), shell=True).communicate()
