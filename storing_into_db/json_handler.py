import json
from validate_json_metadata import validate_json_metadata

def insert_json_metadata(conn, json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO json_metadata (image_height, image_width, timestamp, camera_owner_name, camera_model, lens_type)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (data.get("image_height"), data.get("image_width"), data.get("timestamp"),
          data.get("camera_owner_name"), data.get("camera_model"), data.get("lens_type")))
    conn.commit()

def validate_json_data(json_path):
    return validate_json_metadata(json_path)
