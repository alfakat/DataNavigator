import os
import h5py
from PIL import Image
import numpy as np
from pathlib import Path
import argparse
from data_collection.data_scrapping import scrape_image_url


def argument_parsing() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("--output", required=False, help="Path where to save the output HDF5 file")

    args = parser.parse_args()
    return args

def extract_image_metadata(image_path):
    with Image.open(image_path) as img:
        metadata = {
            "path": str(image_path),
            "format": img.format,
            "mode": img.mode,
            "width": img.width,
            "height": img.height}
        return metadata, np.array(img)


def write_images_and_metadata_to_hdf5(image_dir: str, hdf5_path: str):
    image_paths = sorted([p for ext in ('*.png', '*.jpg', '*.jpeg', '*.webp', '*.bmp', '*.tiff')
        for p in Path(image_dir).glob(ext)])
    if not image_paths:
        print(f"No images found in {image_dir}")
        return

    with h5py.File(hdf5_path, "w") as hdf5_file:
        meta_group = hdf5_file.create_group("metadata")
        img_group = hdf5_file.create_group("images")

        for idx, img_path in enumerate(image_paths):
            meta, img_array = extract_image_metadata(img_path)
            img_group.create_dataset(str(idx), data=img_array, compression="gzip")
            for key, value in meta.items():
                meta_group.attrs[f"{idx}/{key}"] = str(value)


def run_metadata_to_hdf5(output: str):
    prompt = "yellow road sign of wild pig"
    scrape_image_url(
        url=rf'https://www.google.com/search?q={prompt}&sxsrf=ALeKk00uvzQYZFJo03cukIcMS-pcmmbuRQ:1589501547816&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjEm4LZyrTpAhWjhHIEHewPD1MQ_AUoAXoECBAQAw&biw=1440&bih=740',
        output=output)

    hdf5_path = os.path.join(output, "metadata.h5")
    write_images_and_metadata_to_hdf5(output, hdf5_path)


if __name__ == "__main__":
    args = argument_parsing()
    output = args.output
    os.makedirs(output)
    run_metadata_to_hdf5(output=output)

