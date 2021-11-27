import json
import os
import logging

import requests
import snoop
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from lxml import etree


formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)


@snoop()
def get_owasp_data(url: str) -> list:
    logger.info(f'Getting OWASP data for {url}')

    response = requests.get(url)
    link_prefixes = [
        'A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10'
    ]

    top_page = BeautifulSoup(response.content, features='html.parser')
    dom = etree.HTML(str(top_page))

    items = []

    for i in range(1, len(link_prefixes) + 1):
        dom_path = dom.xpath(f'/html/body/div[3]/main/div/div[3]/article/ul[1]/li[{i}]/strong/a')
        text = dom_path[0].text
        key = text.split('-')[0]
        href = url + dom_path[0].attrib['href']
        items.append({'key': key, 'text': text, 'href': href})

    return items


@snoop()
def get_reference_links(url: str) -> list:
    logger.info(f'Getting reference links for {url}')

    response = requests.get(url)
    page = BeautifulSoup(response.content, features='html.parser')

    items = []

    links = page.find('h2', attrs={'id': 'references'}).find_next('ul').findAll('a')
    for link in links:
        text = link.text
        href = link.attrs['href']
        items.append({'text': text, 'href': href})

    return items


@snoop()
def get_mapped_cwes(url: str) -> list:
    logger.info(f'Mapping CWEs for {url}')

    response = requests.get(url)
    page = BeautifulSoup(response.content, features='html.parser')

    items = []

    paragraphs = page.find('h2', attrs={'id': 'list-of-mapped-cwes'}).find_next_siblings('p')
    for p in paragraphs:
        link = p.find('a')
        if link:
            text = link.text
            href = link.attrs.get('href', '')
            items.append({'text': text, 'href': href})

    return items


@snoop()
def main(url: str, file: str):

    logger.info('Entered main')
    owasp_data = get_owasp_data(url)

    for page in owasp_data:
        reference_links = get_reference_links(page['href'])
        mapped_cwes = get_mapped_cwes(page['href'])
        page['reference_links'] = reference_links
        page['mapped_cwes'] = mapped_cwes

    data = {
        'data': owasp_data
    }

    logger.info(f'Writing data to {file}')
    with open(file, 'w') as web:
        json.dump(obj=data, fp=web, indent=4)

    logger.info(f'Done...')


if __name__ == '__main__':
    true_values = ['True', 'true', 1]

    load_dotenv()
    url = os.getenv('URL')
    file = os.getenv('FILE')
    is_debug = os.getenv('DEBUG', False)
    if is_debug not in true_values:
        snoop.install(enabled=False)

    logger.info(f'Parsing URL {url}')
    logger.info(f'File: {file}')
    logger.info(f'Debug mode: {is_debug}')

    main(url, file)
