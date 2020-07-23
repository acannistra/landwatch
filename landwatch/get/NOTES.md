# `get` Design

**Purpose**: This module provides programmatic access to four primary data types in service of the landwatch project. The data types and associated sources are enumerated below. It is intended to be run via a CLI, but can be imported. The output of each of the data type submodules are flatfiles/csv files. Another associated module will organize the data into a relational or network structure.

## Data Types

This module enables the acquisition of four primary data types:

1. Federal public lands (*location, name, congressional district, and other related metadata*): `lands`
1. Congressional legislation that references US Public Lands (*bill name, introduction date, legislator sponsors, and other related metadata*): `bills`
1. Congressional sponsors of aforementioned legislation: `sponsors`
1. Campaign finance contributors for legislators sponsoring / associated with legislation (*corporate sponsors, contribution amounts, associated industry, and other related metadata*): `finance`

## Data Sources

Some of these data types are derived from a single source (e.g. both legislation and sponsors will likely derive from the same source) and others will depend on multiple APIs or data sources. The data sources I intend to use are below. A working database of possible data sources to choose from is [here](https://docs.google.com/spreadsheets/d/14oKvM8lpXP2JJRqUJ-B8zCPoL7HsF0rSlVgbeUFug_M/edit#gid=0).


| Category | Data Source | Type | Organization | URL | Notes |
|:-:|:-:|:-:|:-:|:-:|:-:|
| Campaign Finance | OpenSecrets Open Data | Data Download | OpenSecrets | https://www.opensecrets.org/resources/create/data_doc.php | Candidates, PACs to Candidates, PACs to PACs.  |
| Campaign Finance | OpenSecrets API | API | OpenSecrets | https://www.opensecrets.org/resources/create/api_doc.php | Top contributors to candidate, top industry to candidate. SEEMS VALUABLE |
| Legislation | Congress API | API | ProPublica | https://projects.propublica.org/api-docs/congress-api/ | Member data, bill data, floor actions, committee data |
| Public Lands | Protected Areas Database | Data Download | USGS | https://www.usgs.gov/core-science-systems/science-analytics-and-synthesis/gap/science/pad-us-data-download?qt-science_center_objects=0#qt-science_center_objects | From the Gap Analysis Project  |

Other Notes:
* [WDPA Documentation / Manual](http://wdpa.s3.amazonaws.com/WDPA_Manual/English/WDPA_Manual_1_4_EN_FINAL.pdf)

## Implementation Strategy

The implementation of each data type will be as a sub-module (`.py`) within this `get` directory. Each type (`lands`, `bills`, `sponsors`, and `finance`) will have its own file. These modules will contain a class implementing various domain-specific functions. These are not yet enumerated. All will eventually have a `save` or similar command which writes final output to a flatfile/csv.
