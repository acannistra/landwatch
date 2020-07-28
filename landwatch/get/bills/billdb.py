import os
import sqlite3

from loguru import logger

"""
billdb module

An interface for persistent storage of legislative data.
A loose wrapper around sqlite3.

"""

def create_table(conn, name, schema, logger=logger):
    """Creates a db table with name and schema at conn"""
    logger.info(f"Creating table {name}")
    schema_string = ",".join([f"{col} {type}" for col, type in schema.items()])
    create_query = f"CREATE TABLE IF NOT EXISTS {name} ({schema_string})"
    logger.debug(create_query)
    c = conn.cursor()
    c.execute(create_query)
    conn.commit()
    c.close()



class BillDB(object):
    """
    Interface to sqlite3 database for storing bill information
    linked to protected lands parcels.

    Creates two tables:
        * bills: contains bill information
        * land_bills: links parcel ids to bill ids.


    """
    bills_table_name = 'bills'
    bills_table_schema =  {
        "bill_id": "text PRIMARY KEY",
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
    links_table_name = 'land_bill_links'
    links_table_schema = {
        'land_id' : 'text',
        'bill_id' : 'text'
    }

    def __init__(
        self,
        path,
        bills_table_name = bills_table_name,
        bills_table_schema = bills_table_schema,
        links_table_name = links_table_name,
        links_table_schema = links_table_schema,
        overwrite=True,
        logger=logger):
        """
        Check if db exists at path. If not, create one.

        Add bills table to db. If overwrite, overwrite existing table.
        """

        self.path = path
        self.overwrite = overwrite
        self.logger = logger
        self.bills_table_name = bills_table_name
        self.bills_table_schema = bills_table_schema

        if not os.path.exists(self.path):
            self.logger.warning("Database not found at {self.path}. Creating.")

        self.connection = sqlite3.connect(self.path)

        # check if tables exist
        c = self.connection.cursor()
        tableCount = c.execute(
            'SELECT count(*) from sqlite_master where type=\'table\' and name in (?, ?)',
            (self.bills_table_name, self.links_table_name)
        ).fetchone()
        tableExists = (tableCount[0] == 2)
        c.close()

        if tableExists and not self.overwrite:
            self.logger.info(f"Both {self.bills_table_name} and {self.links_table_name} exist."
            " Appending to it. Add overwrite=True to overwrite.")

        if self.overwrite:
            logger.warning(f"Overwrite: True. Dropping tables.")
            c = self.connection.cursor()
            c.execute(f"DROP TABLE IF EXISTS {self.bills_table_name}")
            c.execute(f"DROP TABLE IF EXISTS {self.links_table_name}")
            self.connection.commit()
            c.close()

        if not tableExists or self.overwrite:
            ## create bills table
            create_table(self.connection, self.bills_table_name, self.bills_table_schema, logger=self.logger)

            ## create links table
            create_table(self.connection, self.links_table_name, self.links_table_schema, logger=self.logger)


        self.connection.close()

    def write(self, billdata, parcel_id=None):
        """Writes billdata (dictionary of key:values) to db. Replaces missing
        columns of schema with null.

        If parcel_id is provided, adds a row to the parcel table."""

        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        # insert bill
        insert_string = [repr(billdata[col]) if col in billdata.keys() else 'null' for col in self.bills_table_schema.keys()]
        query_string = f"INSERT INTO {self.bills_table_name} ({','.join(self.bills_table_schema.keys())}) VALUES ({',' .join(insert_string)})"
        self.logger.debug(query_string)
        try:
            c.execute(query_string)
        except sqlite3.IntegrityError as ie:
            self.logger.warning(f"Bill {billdata['bill_id']} already exists in database.")
            c.close()

        # insert link
        query_string = f"INSERT INTO {self.links_table_name} ('land_id', 'bill_id') VALUES (?, ?)"
        c.execute(query_string, (parcel_id, billdata['bill_id']))
        conn.commit()
        conn.close()
