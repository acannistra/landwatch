import os
import sqlite3

from loguru import logger

class BillDB(object):
    """
    Interface to sqlite3 database for storing bill information
    linked to protected lands parcels.
    """
    table_name = 'bills'
    table_schema =  {
        "bill_id": "text",
        "bill_slug": "text",
        "bill_type": "text",
        "number": "text",
        "bill_uri": "text",
        "title": "text",
        "short_title": "text",
        "sponsor_title": "text",
        "sponsor_id": "text",
        "sponsor_name": "text",
        "sponsor_state": "text",
        "sponsor_party": "text",
        "sponsor_uri": "text",
        "gpo_pdf_uri": "text",
        "congressdotgov_url": "text",
        "govtrack_url": "text",
        "introduced_date": "text",
        "active": "text",
        "last_vote": "text",
        "house_passage": "text",
        "senate_passage": "text",
        "enacted": "text",
        "vetoed": "text",
        "cosponsors": 'integer',
        "cosponsors_by_party": 'blob',
        "committees": "text",
        "committee_codes": 'blob',
        "subcommittee_codes": 'blob',
        "primary_subject": 'text',
        "summary": "text",
        "summary_short": "text",
        "latest_major_action_date": "text",
        "latest_major_action": "text"
    }

    def __init__(
        self,
        path,
        table_name = table_name,
        table_schema = table_schema,
        overwrite=True,
        logger=logger):
        """
        Check if db exists at path. If not, create one.

        Add bills table to db. If overwrite, overwrite existing table.
        """

        self.path = path
        self.overwrite = overwrite
        self.logger = logger
        self.table_name = table_name
        self.table_schema = table_schema

        if not os.path.exists(self.path):
            self.logger.warning("Database not found at {self.path}. Creating.")

        self.connection = sqlite3.connect(self.path)

        # check if table exists
        tableCount = self.connection.cursor().execute(
            'SELECT count(name) from sqlite_master where type=\'table\' and name=?',
            (table_name, )
        ).fetchone()
        tableExists = (tableCount[0] == 1)

        if tableExists and not self.overwrite:
            self.logger.info(f"Table {self.table_name} exists."
            " Appending to it. Add overwrite=True to overwrite.")

        if self.overwrite:
            logger.warning(f"Overwrite: True. Dropping table.")
            self.connection.cursor().execute(f"DROP TABLE IF EXISTS {self.table_name}")
            self.connection.commit()

        if not tableExists or self.overwrite:
            self.logger.info(f"Creating table {self.table_name}")
            schema_string = ",".join([f"{col} {type}" for col, type in self.table_schema.items()])
            create_query = f"CREATE TABLE {self.table_name} ({schema_string})"
            self.logger.debug(create_query)
            self.connection.cursor().execute(create_query)
            self.connection.commit()

    def write(self, billdata):
        """Writes billdata (dictionary of key:values) to db. Replaces missing
        columns of schema with null."""

        c = self.connection.cursor()
        insert_string = [repr(billdata[col]) if col in billdata.keys() else 'null' for col in self.table_schema.keys()]
        query_string = f"INSERT INTO {self.table_name} ({','.join(self.table_schema.keys())}) VALUES ({',' .join(insert_string)})"
        self.logger.debug(query_string)
        c.execute(query_string)
        self.connection.commit()
