'''
Data scrapping is one of the pioneer's data collection techniques and still wide useful.
The following script navigates to Google search and download image by its url.
'''

import io
import os.path
import argparse
import requests
import datetime
from PIL import Image
from bs4 import BeautifulSoup


def argument_parsing() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("--prompt", type=str, required=True,
                        help="Short prompt to search",
                        default=0)
    parser.add_argument("--output", type=str, required=False,
                        help="Path where to save the scraped images",
                        default=os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                             f'{str(datetime.date.today())}_scrap_output'))

    args = parser.parse_args()
    return args


def save_url_image(link: str, id: int, output: str):
    r = requests.get(link, stream=True)
    if r.status_code == 200:
        img = Image.open(io.BytesIO(r.content))
        img.save(os.path.join(output, f'{id}.png'))


def scrape_image_url(url: str, output: str):

    page = requests.get(url).text
    bs = BeautifulSoup(page, 'html.parser')

    os.makedirs(output, exist_ok=True)

    '''added enumerate to save image with unique id'''
    for id, raw_img in enumerate(bs.find_all('img')):
        link = raw_img.get('src')
        if link == r'/images/branding/searchlogo/1x/googlelogo_desk_heirloom_color_150x55dp.gif':
            continue
        else:
            save_url_image(link=link, id=id, output=output)


if __name__ == "__main__":

    args = argument_parsing()

    prompt = args.prompt
    output = args.output

    scrape_image_url(url = rf'https://www.google.com/search?q={prompt}&sxsrf=ALeKk00uvzQYZFJo03cukIcMS-pcmmbuRQ:1589501547816&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjEm4LZyrTpAhWjhHIEHewPD1MQ_AUoAXoECBAQAw&biw=1440&bih=740',
                     output=output)