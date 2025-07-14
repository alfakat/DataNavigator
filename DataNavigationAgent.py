import os
import mimetypes
import json
import h5py
import argparse
from PIL import Image


def detect_file_type(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type:
        if mime_type.startswith('image'):
            return 'image'
        elif mime_type.startswith('video'):
            return 'video'
        elif mime_type == 'application/json':
            return 'json'
        elif mime_type in ('text/csv', 'application/vnd.ms-excel'):
            return 'csv'
    if file_path.endswith(".h5") or file_path.endswith(".hdf5"):
        return 'hdf5'
    return 'unknown'


def process_file(file_path):
    file_type = detect_file_type(file_path)
    print(f"Detected file type: {file_type}")

    if file_type == 'image':
        return process_image(file_path)
    elif file_type == 'video':
        return f"Video file '{file_path}' detected. Consider using 'data_video_scrapping.py'."
    elif file_type == 'csv':
        return f"CSV file '{file_path}' detected. Process with 'metadata_to_csv.py'."
    elif file_type == 'json':
        return f"JSON file '{file_path}' detected. Process with 'metadata_to_json.py'."
    elif file_type == 'hdf5':
        return inspect_hdf5(file_path)
    else:
        return f"Unsupported or unknown file type: {file_path}"


def process_image(file_path):
    try:
        with Image.open(file_path) as img:
            return {
                "filename": os.path.basename(file_path),
                "format": img.format,
                "mode": img.mode,
                "size": img.size,  # (width, height)
            }
    except Exception as e:
        return {"error": str(e)}


def inspect_hdf5(file_path):
    result = {"file": file_path, "groups": []}
    try:
        with h5py.File(file_path, 'r') as hf:
            def visit(name, node):
                result["groups"].append(name)
            hf.visititems(visit)
    except Exception as e:
        result["error"] = str(e)
    return result


def analyze_path(path):
    if os.path.isdir(path):
        results = []
        for root, _, files in os.walk(path):
            for file in files:
                full_path = os.path.join(root, file)
                results.append(process_file(full_path))
        return results
    elif os.path.isfile(path):
        return [process_file(path)]
    else:
        return [f"Invalid path: {path}"]

def main():
    parser = argparse.ArgumentParser(description="DataNavigator CLI Agent")
    parser.add_argument("path", help="Path to file or directory to analyze")
    parser.add_argument("--output", help="Optional output JSON file")
    args = parser.parse_args()

    result = analyze_path(args.path)

    print("\n=== Analysis Result ===")
    print(json.dumps(result, indent=2))

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\nResult saved to: {args.output}")


if __name__ == "__main__":
    main()
