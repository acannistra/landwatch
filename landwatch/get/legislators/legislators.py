import sqlalchemy as sa
import requests
import requests_cache
import tqdm
from .legdb import LegislatorDB

from prefect import task

import os



def get_single_sponsor(uri, api_key):
    """Use ProPublica Congress API to get a single sponsor metadata
    from URI"""

    header = {
        'x-api-key' : api_key
    }
    return requests.get(uri, headers=header).json()['results'][0]


def get_sponsors(billdb, api_key, table='bills'):
    """Return list of dicts for all sponsors mentioned in billsdb.
    Requires ProPublica Congress API key"""
    requests_cache.install_cache('propub_spon_cache')

    eng = sa.create_engine(f"sqlite:///{billdb}")
    meta = sa.MetaData(eng)
    tab = sa.Table(table, meta, autoload=True)

    uris = []
    with eng.connect() as con:
        # put bills in comma sep list next to each uri.
        s = sa.sql.select(
            [tab.c.sponsor_uri, sa.func.group_concat(tab.c.bill_id, ',')]
        ).group_by(tab.c.sponsor_uri)
        # s = sa.sql.select([tab.c.sponsor_uri])
        rs = con.execute(s)
        uris = rs.fetchall()

    sponsor_data = []

    for s in tqdm.tqdm(uris, desc="Downloading sponsors"):

        sponsor_data.append((
            get_single_sponsor(s[0], api_key),
            s[1]
        ))

    return list(sponsor_data)


@task
def process_legislators(dbpath, api_key, overwrite):
    legdb = LegislatorDB(dbpath, overwrite)

    sponsors = get_sponsors(dbpath,api_key)

    for sponsor, bills in sponsors:
        bills = bills.split(',')
        for bill in bills:
            legdb.write(sponsor, bill_id = bill, sponsor_type = 'sponsor')