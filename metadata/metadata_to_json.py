""""The script below showing simple way of getting metadata and saving it into json file close to collected image.
Metadata tags can be very various depend on device and user preferences."""

import os
import cv2
import exif
import json
import datetime
import argparse

from data_collection.data_recording import run_cap_video


def argument_parsing() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("--output", type=str, required=False,
                        help="Path where to save the metadata jsons."
                             "Note that collected images will be saved in the same place",
                        default=os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                             f'{str(datetime.date.today())}_rec_output'))

    args = parser.parse_args()
    return args


def collect_opencv_metadata(sourse: str) -> dict:

    """extract image resolution using opencv"""

    opencv_metada = {}
    im_cv = cv2.imread(sourse)
    opencv_metada['image_height'] = im_cv.shape[0]
    opencv_metada['image_width'] = im_cv.shape[1]

    return opencv_metada


def collect_exif_metadata(sourse: str) -> dict:

    """"extract camera details using exif"""

    exif_metadata = {}
    im_exif = exif.Image(sourse)
    exif_metadata['timestamp'] = im_exif.datetime_original
    exif_metadata['camera_owner_name'] = im_exif.get('user')
    exif_metadata['camera_model'] = im_exif.get('model')
    exif_metadata['lens_type'] = im_exif.get('lens_make')

    return exif_metadata


def write_metadata_to_json(opencv_metada: dict, exif_metadata: dict, output: str) -> None:

    metadata = {**opencv_metada, **exif_metadata}

    json_file_path = os.path.join(output, 'merged_data.json')
    with open(json_file_path, 'w') as json_file:
        json.dump(metadata, json_file, indent=4)

    print('Metadata file saved to ', json_file_path)
    return None

def run_metada_to_jsons(output: str):
    source = run_cap_video(cam_index=0,
                        video_length=10,
                        output=output)

    opencv_metada = collect_opencv_metadata(sourse=source)
    exif_metadata = collect_exif_metadata(sourse=source)
    write_metadata_to_json(opencv_metada, exif_metadata, output)


if __name__ == '__main__':
    args = argument_parsing()
    output = args.output
    run_metada_to_jsons(output=output)
