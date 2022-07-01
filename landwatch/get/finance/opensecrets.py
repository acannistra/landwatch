from prefect import task, Flow, Parameter

import requests
import os
from glob import glob
import sqlalchemy as sa

API_DATA_TYPES = {
    "contrib": "candContrib",
    "industry": 'candIndustry',
    "sector": "candSector"
}

DATA_TYPE_NAMES = list(API_DATA_TYPES.keys())
OPEN_SECRETS_API = "http://www.opensecrets.org/api/"

"""
opensecrets.py

"""

@task
def _glob_one(pattern):
    return glob(pattern)[0]

@task
def _insert_file_to_table_with_schema(dbpath, file, schema):
    dbeng = sa.create_engine(f"sqlite:///{dbpath}")
    with open(file, 'r') as f:
        for line in f:
            data = {
                col.name: val.replace("|", "")
                for col, val in zip(schema.c, line.strip().split(","))
            }
            dbeng.execute(
                schema.insert(),
                data
            )


class OSBulkData(object):
    """Facilities for importing OpenSecrets Bulk Data
    to sqlite database.
    """
    meta = sa.MetaData()

    candidates_schema = sa.Table(
        'candidates', meta,
        sa.Column('cycle', sa.String(4), nullable=False),
        sa.Column('feccandid', sa.String(4), nullable=False),
        sa.Column('cid', sa.String(9), nullable=True),
        sa.Column('firstlastp', sa.String(50), nullable=True),
        sa.Column('party', sa.String(1), nullable=True),
        sa.Column('distidrunfor', sa.String(4), nullable=True),
        sa.Column('distidcurr', sa.String(4), nullable=True),
        sa.Column('currcand', sa.String(1), nullable=True),
        sa.Column('cyclecand', sa.String(1), nullable=True),
        sa.Column('crpico', sa.String(1), nullable=True),
        sa.Column('recipcode', sa.String(2), nullable=True),
        sa.Column('nopacs', sa.String(1), nullable=True)
    )

    commitees_schema =  sa.Table(
        'committees', meta,
        sa.Column('cycle', sa.String(4), nullable=False),
        sa.Column('cmteid', sa.String(9), nullable=False),
        sa.Column('pacshort', sa.String(50), nullable=True),
        sa.Column('affiliate', sa.String(50), nullable=True),
        sa.Column('ultorg', sa.String(50), nullable=True),
        sa.Column('recipid', sa.String(9), nullable=True),
        sa.Column('recipcode', sa.String(2), nullable=True),
        sa.Column('feccandid', sa.String(9), nullable=True),
        sa.Column('party', sa.String(1), nullable=True),
        sa.Column('primcode', sa.String(5), nullable=True),
        sa.Column('source', sa.String(10), nullable=True),
        sa.Column('sensitive', sa.String(1), nullable=True),
        sa.Column('foreign', sa.String(1), nullable=False),
        sa.Column('active', sa.Integer(), nullable=True)
    )

    pacs_schema = sa.Table(
        'pacs', meta,
        sa.Column('cycle', sa.String(4), nullable=False),
        sa.Column('fecrecno', sa.String(19), nullable=False),
        sa.Column('pacid', sa.String(9), nullable=False),
        sa.Column('cid', sa.String(9), nullable=False),
        sa.Column('amount', sa.Integer(), default=0),
        sa.Column('date', sa.String(50), nullable=True),
        sa.Column('realcode', sa.String(5), nullable=True),
        sa.Column('type', sa.String(3), nullable=True),
        sa.Column('di', sa.String(1), nullable=True),
        sa.Column('feccandid', sa.String(9), nullable=True)
    )


    def __init__(self, datadir, dbpath):
        self.datadir = datadir
        self.dbpath = os.path.abspath(dbpath)


    def load(self):
        """Imports candidates, committees, and pacs to sqlite db"""
        # create tables
        engine = sa.create_engine(f"sqlite:///{self.dbpath}")
        OSBulkData.meta.create_all(engine)
        # import candidates

        try:
            candfile = _glob_one(os.path.join(self.datadir, "cand*.txt"))
            _insert_file_to_table_with_schema(
                f"sqlite:///{self.dbpath}",
                candfile,
                OSBulkData.candidates_schema
            )
        except IndexError:
            print("Cannot find candidates")
        # import committees
        try:
            committeefile = _glob_one(os.path.join(self.datadir, "cmtes*.txt"))
            _insert_file_to_table_with_schema(
                f"sqlite:///{self.dbpath}",
                committeefile,
                OSBulkData.commitees_schema
            )
        except IndexError:
            print("Cannot find committees")
        # import PACs
        try:
            pacfile = _glob_one(os.path.join(self.datadir, "pacs*.txt"))
            _insert_file_to_table_with_schema(
                f"sqlite:///{self.dbpath}",
                pacfile,
                OSBulkData.pacs_schema
            )
        except IndexError:
            print("cannot find pacs")

        
