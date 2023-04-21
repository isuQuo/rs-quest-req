import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

BASE_URL = "https://runescape.wiki"
URI = "/w/The_Temple_at_Senntisten"

def get_base_requirements() -> dict:
    url = BASE_URL + URI
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Using the CSS selector to find the nested unordered list
        css_selector = '#mw-content-text > div.mw-parser-output > table.plainlinks.no-parenthesis-style.questdetails.plainlinks > tbody > tr:nth-child(4) > td > table > tbody > tr:nth-child(2) > td > ul > li > ul'
        nested_ul = soup.select_one(css_selector)

        if nested_ul:
            list_items = nested_ul.find_all('li')

            links = {}
            for li in list_items:
                link = li.find('a')
                if link:
                    links[link['title']] = link['href']
        else:
            print('Nested unordered list not found.')
    else:
        print(f'Error: {response.status_code}')

    return links

def get_final_requirements(links: list) -> dict:
    levels = {}

    for title, uri in links.items():
        url = BASE_URL + uri
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Using the CSS selector to find the nested unordered list
            css_selector = '#mw-content-text > div.mw-parser-output > table.plainlinks.no-parenthesis-style.questdetails.plainlinks > tbody > tr:nth-child(4) > td > ul'
            nested_ul = soup.select_one(css_selector)

            if nested_ul:
                list_items = nested_ul.find_all('li')

                for li in list_items:
                    link = li.find('a')
                    if link:
                        levels[title] = li.text
        else:
            print(f'Error: {response.status_code}')

    return levels

def get_highest_level(levels: dict) -> dict:
    highest_levels = {}

    for key, value in levels.items():
        parts = value.split()
        if len(parts) == 2:
            level = int(parts[0])
            skill = parts[1]

            if skill not in highest_levels or level > highest_levels[skill][1]:
                highest_levels[skill] = (key, level)

    return highest_levels

def print_table(d: dict, headers=[]):
    # Convert the dictionary to a list of tuples
    highest_levels_list = [(val[0], f'{key} {val[1]}') for key, val in d.items()]

    # Print the table using tabulate
    print(tabulate(highest_levels_list, headers=headers, tablefmt='pipe'))

if __name__ == "__main__":
    links = get_base_requirements()
    levels = get_final_requirements(links)
    highest_levels = get_highest_level(levels)

    print_table(highest_levels, headers=['Quest', 'Skill & Level'])

