from pathlib import Path
import getpass
import math

import pandas as pd
import mysql.connector


# --------------------------------------------------
# 1. PROJECT CONFIGURATION
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

CSV_DIR = PROJECT_ROOT / "data" / "interim" / "mysql_import"

TABLES = {
    "matches": 1243,
    "innings": 2514,
    "deliveries": 295732,
}

BATCH_SIZE = 2000

BOOLEAN_COLUMNS = {
    "matches": ["city_was_imputed"],
    "innings": ["is_super_over"],
    "deliveries": ["is_legal_delivery"],
}


# --------------------------------------------------
# 2. MYSQL CONNECTION
# --------------------------------------------------

host = "127.0.0.1"
port = 3306
database = "ipl_analytics"

username = input("MySQL username: ")
password = getpass.getpass("MySQL password: ")

connection = mysql.connector.connect(
    host=host,
    port=port,
    user=username,
    password=password,
    database=database,
)

cursor = connection.cursor()

print("\nMYSQL CONNECTION: SUCCESS")


# --------------------------------------------------
# 3. DATA CONVERSION
# --------------------------------------------------


def clean_value(value):

    if pd.isna(value):
        return None

    if hasattr(value, "item"):
        value = value.item()

    if isinstance(value, float) and math.isnan(value):
        return None

    return value


# --------------------------------------------------
# 4. IMPORT EACH TABLE
# --------------------------------------------------

try:

    for table, expected_rows in TABLES.items():

        print("\n" + "=" * 60)
        print(f"IMPORTING: {table.upper()}")
        print("=" * 60)

        csv_path = CSV_DIR / f"{table}.csv"

        if not csv_path.exists():
            raise FileNotFoundError(csv_path)

        df = pd.read_csv(csv_path)

        # Verify CSV columns
        if not df.columns.is_unique:
            raise ValueError(f"Duplicate CSV columns in {table}")

        if len(df) != expected_rows:
            raise ValueError(f"Unexpected row count in {table}: {len(df)}")

        # Convert Boolean values
        for column in BOOLEAN_COLUMNS[table]:

            values = df[column].astype(str).str.strip().str.lower()

            converted = values.map(
                {
                    "true": 1,
                    "false": 0,
                    "1": 1,
                    "0": 0,
                }
            )

            if converted.isna().any():
                raise ValueError(f"Invalid Boolean values: {table}.{column}")

            df[column] = converted.astype("int8")

        # Validate target database columns
        cursor.execute(
            """
            SELECT COLUMN_NAME
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = %s
              AND TABLE_NAME = %s
            ORDER BY ORDINAL_POSITION
            """,
            (database, table),
        )

        database_columns = [row[0] for row in cursor.fetchall()]

        if set(df.columns) != set(database_columns):
            raise ValueError(
                f"Column mismatch in {table}.\n"
                f"CSV only: {set(df.columns) - set(database_columns)}\n"
                f"DB only: {set(database_columns) - set(df.columns)}"
            )

        # Explicit column names prevent duplicate mapping
        column_sql = ", ".join(f"`{column}`" for column in df.columns)

        placeholders = ", ".join(["%s"] * len(df.columns))

        insert_sql = (
            f"INSERT INTO `{table}` " f"({column_sql}) " f"VALUES ({placeholders})"
        )

        # Convert DataFrame to Python records
        records = [
            tuple(clean_value(value) for value in row)
            for row in df.itertuples(
                index=False,
                name=None,
            )
        ]

        inserted = 0

        for start in range(0, len(records), BATCH_SIZE):

            batch = records[start : start + BATCH_SIZE]

            cursor.executemany(
                insert_sql,
                batch,
            )

            connection.commit()

            inserted += len(batch)

            print(f"{table}: {inserted:,} / {expected_rows:,}")

        # Verify actual MySQL count
        cursor.execute(f"SELECT COUNT(*) FROM `{table}`")

        actual_count = cursor.fetchone()[0]

        if actual_count != expected_rows:
            raise RuntimeError(
                f"{table}: expected {expected_rows}, " f"found {actual_count}"
            )

        print(f"{table.upper()} IMPORT: PASS")

    print("\n" + "=" * 60)
    print("ALL THREE TABLES IMPORTED SUCCESSFULLY")
    print("=" * 60)

except Exception:

    connection.rollback()
    raise

finally:

    cursor.close()
    connection.close()
