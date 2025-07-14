import pandas as pd
from pathlib import Path
from validate_csv_metadata import validate_csv_metadata

def insert_csv_metadata(conn, csv_dir):
    cursor = conn.cursor()
    for csv_file in Path(csv_dir).glob("*.csv"):
        df = pd.read_csv(csv_file)
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO csv_metadata (image_path, weight, height, prompt, seed)
                VALUES (?, ?, ?, ?, ?)
            """, (row.image_path, row.weight, row.height, row.prompt, row.seed))
    conn.commit()

def validate_csv_data(csv_dir):
    return validate_csv_metadata(csv_dir)
