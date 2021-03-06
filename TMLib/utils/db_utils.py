import pandas as pd
import csv
from pathlib import Path
from sqlalchemy import create_engine


def connection_SQLite3_fromStatistics(statistics):
    """
    Creates SQLalchemy engine based on path to sqlite stored in statistics.

    Limited to SQLite db.

    :param statistics: Core.Statistics.Statistics object
    :return: SQLalchemy DB engine
    """
    return create_engine(f'sqlite:///{statistics.path_db}')


def connection_SQLite3_fromPath(file_path):
    """
    Creates SQLalchemy engine based on path to sqlite db.

    Limited to SQLite db.

    :param statistics: String containing path to sqlite db.
    :return: SQLalchemy DB engine
    """
    return create_engine(f'sqlite:///{file_path}')


def extractTables(e):
    """
    Extracts names of all tables in database and returns them in a list.

    Expects SQLalchemy engine or similiar (support of execute and fetchall)

    :param e: SQLAlchemy engine
    :return: List of table names as strings
    """
    return [i[0] for i in e.execute('SELECT name FROM sqlite_master WHERE type=\'table\'').fetchall()]


def exportSQLite3_toCSV(extract, statistics, filepath = '.'):
    """
    Exports SQLite3 database, all its tables, into CSV files.
    Every table is exported into separate CSV file.

    Expects extraction function through SQLAlchemy.

    :param extract: Function that creates (extracts) connection to the SQLite database.
    :param statistics: Core.Statistics.Statistics object
    :param filepath: Path to the directory where CSV files will be written
    """
    connection = extract(statistics)
    table_list = extractTables(connection)
    for table in table_list:
            with ( Path(filepath) / f'{table}.csv' ).open('a') as _handle:
                r = connection.execute(f"select * from {table}")
                _handle.write( ','.join(r.keys()) )
                row = r.fetchone()
                while row != None:
                    _handle.write('\n')
                    _handle.write( ','.join([str(i) for i in row]) )
                    row = r.fetchone()
                # pd.read_sql_table(table, connection).to_csv( str(Path(filepath) / f'{table}.csv') )

def exportSQLite3_toXLSX(extract, statistics, filename, filepath = '.'):
    """
    Exports SQLite3 database, all its tables, into XLSX file.

    Expects extraction function through SQLAlchemy.

    :param extract: Function that creates (extracts) connection to the SQLite database.
    :param statistics: Core.Statistics.Statistics object
    :param filename: XLSX file name without the extension (.xlsx)
    :param filepath: Path to the directory where XLSX file will be written.
    """
    connection = extract(statistics)
    table_list = extractTables(connection)
    xlsx_file = str( Path(filepath) / f'{filename}.xlsx' )
    with pd.ExcelWriter(xlsx_file) as writer:
        for table in table_list:
            pd.read_sql_table(table, connection).to_excel(writer, sheet_name = table)
