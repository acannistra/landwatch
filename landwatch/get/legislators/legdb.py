import os

import sqlalchemy as sa
from loguru import logger

from prefect import task

class LegislatorDB(object):
    """Interface to a sqlite database that contains
    metadata about individual legislators and connections
    between legislators and bills, parameterized on the connection
    type (sponsor or cosponsor).

    """

    legtable_name = 'legislators'
    linkstable_name = 'leg_bill_links'

    def __init__(self, dbpath, overwrite=False):
        """Define tables in dbpath database"""


        self.engine = sa.create_engine(f"sqlite:///{dbpath}")
        self.meta = sa.MetaData(self.engine)
        self.meta.reflect()

        existing_tables =  sa.engine.reflection.Inspector(self.engine).get_table_names()
        if ((LegislatorDB.legtable_name in existing_tables) or (LegislatorDB.linkstable_name in existing_tables)) and overwrite:
            sa.Table(LegislatorDB.legtable_name, self.meta).drop(self.engine)
            sa.Table(LegislatorDB.linkstable_name, self.meta).drop(self.engine)



        self.legtable = sa.Table(
            LegislatorDB.legtable_name,
            self.meta,
            sa.Column('id', sa.String, primary_key=True),
            sa.Column('first_name', sa.String, nullable=True),
            sa.Column('middle_name', sa.String, nullable=True),
            sa.Column('last_name', sa.String, nullable=True),
            sa.Column('gender', sa.String, nullable=True),
            sa.Column('govtrack_id', sa.String, nullable=True),
            sa.Column('twitter_account', sa.String, nullable=True),
            sa.Column('facebook_account', sa.String, nullable=True),
            sa.Column('in_office', sa.String, nullable=True),
            sa.Column('current_party', sa.String, nullable=True),
            sa.Column('fec_candidate_ids', sa.String, nullable=True),
            extend_existing=True
        )
        self.legtable.colnames = [c.name for c in self.legtable.columns]
        self.legtable.create(checkfirst=True)

        self.linktable = sa.Table(
            LegislatorDB.linkstable_name,
            self.meta,
            sa.Column('leg_id', sa.Integer),
            sa.Column('bill_id', sa.Integer),
            sa.Column('link_type', sa.String),
            extend_existing=True
        )
        self.linktable.colnames = [c.name for c in self.linktable.columns]
        self.linktable.create(checkfirst=True)

    def write(self,leg_data, bill_id = None, sponsor_type = None):
        """Write a single legislator to the db. If given, associate
        the legislator with a bill via bill_id and sponsor_type."""

        unknown_keys = set(leg_data.keys()) - set(self.legtable.colnames)
        [leg_data.pop(k, None) for k in unknown_keys]

        with self.engine.connect() as con:
            i = self.legtable.insert().values(**leg_data)
            try:
                con.execute(i)
            except sa.exc.IntegrityError as e:
                if 'UNIQUE' in str(e):
                    logger.warning(f"Legislator id {leg_data['id']} already in db.")
                else:
                    raise e

            if bill_id and sponsor_type:
                i = self.linktable.insert().values(
                    leg_id = leg_data['id'],
                    bill_id = bill_id,
                    link_type = sponsor_type
                )
                con.execute(i)
