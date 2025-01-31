import os
import datetime
import argparse

import numpy as np
import pandas as pd

from data_collection.data_generation import run_flux


def argument_parsing() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("--output", type=str, required=False,
                        help="Path where to save the metadata csvs."
                             "Note that collected images will be saved in the same place",
                        default=os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                             f'{str(datetime.date.today())}_gen_output'))

    args = parser.parse_args()
    return args

def write_metadata_to_csv(image_path: str,
                          image: np.array,
                          prompt: str,
                          seed: int,
                          output: str):

    # to do: read image with opencv or pillow

    df = pd.DataFrame()
    df['image_path'] = image_path
    df['weight'] = image.weight
    df['height'] = image.height
    df['prompt'] = prompt
    df['seed'] = seed

    df.to_csv(os.path.join(output, image_path.replace('.png', '.csv')))


def run_metadata_to_csv(output: str):
    image_path, image, prompt, rand_seed = run_flux(prompt='yellow road sign of wild pig',
                                        output=output)
    write_metadata_to_csv(image_path=image_path,
                          image=image,
                          prompt=prompt,
                          seed = rand_seed,
                          output=output)


if __name__ == '__main__':
    args = argument_parsing()
    output = args.output
    run_metadata_to_csv(output=output)
