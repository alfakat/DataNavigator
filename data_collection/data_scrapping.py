'''
Data scrapping is one of the pioneer's data collection techniques and still wide useful.
The following script navigates to Google search and download image by its url.
'''
import os.path

from PIL import Image
import requests
import io
from bs4 import BeautifulSoup


def save_url_image(link: str, id: int, output: str):
    r = requests.get(link, stream=True)
    if r.status_code == 200:
        img = Image.open(io.BytesIO(r.content))
        img.save(os.path.join(output, f'{id}.png'))


def scrape_image_url(url: str, output: str):
    '''navigate to Google search line'''
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
    # to do: make search_key as list, add pages to search
    search_key = 'cat'
    output = r'C:\Users\KATE\Downloads\DataNavigator-main\data_collection\test'
    scrape_image_url(url = rf'https://www.google.com/search?q={search_key}&sxsrf=ALeKk00uvzQYZFJo03cukIcMS-pcmmbuRQ:1589501547816&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjEm4LZyrTpAhWjhHIEHewPD1MQ_AUoAXoECBAQAw&biw=1440&bih=740',
                     output=output)
