import h5py
from validate_hdf5_metadata import validate_hdf5_metadata

def insert_hdf5_metadata(conn, hdf5_path):
    with h5py.File(hdf5_path, "r") as f:
        attrs = f["metadata"].attrs
        grouped = {}
        for key in attrs:
            if "/" not in key:
                continue
            idx, field = key.split("/")
            grouped.setdefault(idx, {})[field] = attrs[key]

        cursor = conn.cursor()
        for record in grouped.values():
            cursor.execute("""
                INSERT INTO hdf5_metadata (path, format, mode, width, height)
                VALUES (?, ?, ?, ?, ?)
            """, (record.get("path"), record.get("format"), record.get("mode"),
                  int(record.get("width")), int(record.get("height"))))
    conn.commit()

def validate_hdf5_data(hdf5_path):
    return validate_hdf5_metadata(hdf5_path)
