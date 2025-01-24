'''
Data generation is new way to create data, required GPU to produce high quality content.
The following script geerates images in pool using FLUX model.
'''


import os
import torch
import random
import argparse
import datetime
import numpy as np
from diffusers import FluxPipeline


def argument_parsing() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("--prompt", type=str, required=True,
                        help="Prompt to generate images",
                        default=0)
    parser.add_argument("--output", type=str, required=False,
                        help="Path where to save the generated images",
                        default=os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                             f'{str(datetime.date.today())}_gen_output'))

    args = parser.parse_args()
    return args


def run_flux(prompt: str):

    rand_seed = random.choice(range(100, 1001, 5))

    pipe = FluxPipeline.from_pretrained("black-forest-labs/FLUX.1-dev", torch_dtype=torch.bfloat16, use_fast=False)
    pipe.enable_model_cpu_offload()

    image = pipe(
        prompt=prompt,
        height=600,
        width=600,
        guidance_scale=3.5,
        num_inference_steps=50,
        max_sequence_length=512,
        generator=torch.Generator('cuda').manual_seed(rand_seed)
    ).images[0]
    image.save(os.path.join("flux_out", f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{rand_seed}.png"))


if __name__ == '__main__':

    args = argument_parsing()

    prompt = args.prompt

    while True:
        run_flux(prompt=prompt)