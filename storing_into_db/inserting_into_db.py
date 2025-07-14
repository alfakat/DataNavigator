# main.py
import argparse
import sqlite3
from csv_handler import insert_csv_metadata, validate_csv_data
from json_handler import insert_json_metadata, validate_json_data
from hdf5_handler import insert_hdf5_metadata, validate_hdf5_data
from db_schema import create_tables, insert_validation_results


def argument_parsing() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_dir", required=True, help="Directory with CSV metadata files")
    parser.add_argument("--json_file", required=True, help="Path to JSON metadata file")
    parser.add_argument("--hdf5_file", required=True, help="Path to HDF5 metadata file")
    parser.add_argument("--db_file", default="metadata.db", help="Path to SQLite DB file")
    args = parser.parse_args()
    return args


def main():
    args = argument_parsing()

    conn = sqlite3.connect(args.db_file)
    create_tables(conn)

    insert_csv_metadata(conn, args.csv_dir)
    insert_json_metadata(conn, args.json_file)
    insert_hdf5_metadata(conn, args.hdf5_file)

    insert_validation_results(conn, validate_csv_data(args.csv_dir), "csv")
    insert_validation_results(conn, validate_json_data(args.json_file), "json")
    insert_validation_results(conn, validate_hdf5_data(args.hdf5_file), "hdf5")

    print(f"All metadata and validation results stored in: {args.db_file}")
    conn.close()

if __name__ == '__main__':
    main()
