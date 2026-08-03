# Namazu 🌍

A Python-based platform for collecting, storing, cleaning, and analyzing earthquake data in Japan.

The project focuses on an ETL workflow:

- **Extract** earthquake data from external sources
- **Transform** and clean raw records
- **Load** processed data into PostgreSQL
- Analyze earthquake data using SQL and Python tools

---

## Tech Stack

- Python
- PostgreSQL
- SQLAlchemy
- Pandas
- BeautifulSoup / Selenium
- unittest

---

## Prerequisites

Before running the project, make sure the following tools are installed:

- Python 3.10+
- PostgreSQL
- `psql` command-line client
- Git

---

## Database Setup

Start PostgreSQL, then open the PostgreSQL shell:

```bash
psql postgres


install postgresql and command and execute the following commands
CREATE USER earthquakes_user WITH PASSWORD '1234';
CREATE DATABASE earthquakes OWNER earthquakes_user;

# create test table for unittest

CREATE DATABASE test_db_earthquakes OWNER earthquakes_user;
```
