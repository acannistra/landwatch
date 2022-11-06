import os
import sqlite3

from datetime import datetime

from .billdb import BillDB
from .congress import ProPublicaAPI

from loguru import logger
from tqdm import tqdm


def get_parcel_names(
    parceldb_path, table_name="padus2_0fee", col_name="unit_nm"
):
    """
    Open spatialite database containing parcels and
    extract unique parcel names.
    """
    db = sqlite3.connect(parceldb_path)
    _query = f"""SELECT distinct {col_name} FROM {table_name}"""
    c = db.cursor()
    c.execute(_query)
    return [_[0] for _ in c.fetchall()]


def process_parcel(parcel, api, billdb):
    """Queries the api for bills containing parcel names
    and writes each result to billsdb."""

    bills = api.bills_search(parcel)
    for bill in bills:
        billdb.write(bill, parcel_id=parcel)


def process_all_parcels(parcels, api, billdb, journalpath=os.getcwd()):
    """
    Queries the propublic api for all parcel names in parcels. Writes all
    bills associated with each parcel to billdb.

    Maintains a file of failed parcel names.
    If an exception is raised, the file of failed parcel names is saved
    to disk and can be used to resume the processing.
    """

    failed_parcels = []
    journal_failed = os.path.join(journalpath, "failed_parcels_{time}.journal")
    parcels_tqdm = tqdm(parcels)
    description_str = "Parcel {}:"
    for parcel in parcels_tqdm:
        parcels_tqdm.set_description(description_str.format(parcel[:20]))
        try:
            process_parcel(parcel, api, billdb)
        except Exception as e:
            logger.error(e)
            failed_parcels.append(parcel)

    if len(failed_parcels) > 0:
        timenow = datetime.now()
        this_journal = journal_failed.format(
            time=timenow.strftime("%Y%m%d_%H%M%S")
        )
        with open(this_journal, "w") as j:
            j.write("\n".join(failed_parcels))
