from bs4 import BeautifulSoup, NavigableString, Tag
from selenium import webdriver

BASE_URL = 'https://www.letras.com/'
DEBUG = False


def prepare_for_url(text: str) -> str:
    """
    Prepare the text for passing in a url

    :param text:
    :return: prepared text
    """
    return str.replace(text, ' ', '%20')


def process_result(browser, title, link):
    """
    Get the result of scraping in the link passed as a parameter

    :param browser: WebBrowser for do the web scrapping
    :param title: Song's title shown in the main screen
    :param link: Link to the song's lyric
    :return: Dictionary with the scrapped data
    """

    data = {
        'title': ' '.join(title.split(' - ')[:-1]),
        'link': link
    }
    browser.get(link)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # check if it is a song
    cnt_letra = soup.find('div', 'cnt-letra')
    if cnt_letra:
        data['type'] = 'song'
        paragraphs = cnt_letra.find_all('p')
        lyric = ''
        for p in paragraphs:
            for element in p.contents:
                if type(element) == NavigableString or type(element) == str:
                    lyric = lyric + element
                elif type(element) == Tag:
                    if element.name == 'br':
                        lyric = lyric + '\n'
                else:
                    print(type(element))
            lyric = lyric + '\n\n'

        data['lyric'] = lyric
        return data

    # check if it is an artist
    artist_top_songs = soup.find('div', 'artista-top')
    if artist_top_songs:
        data['type'] = 'artist'
        return data

    data['type'] = 'unknown'
    return data


def main():
    name = 'astronaut in the ocean '
    url = '{}?q={}'.format(BASE_URL, prepare_for_url(name))
    browser = webdriver.Chrome()
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    result_links = soup.find('div', 'gsc-resultsbox-visible').find_all('a', 'gs-title')
    results = []
    for i in range(0, len(result_links), 2):
        result_link = result_links[i]
        results.append(process_result(browser, result_link.text, result_link['href']))

    print('Select the lyric number:\n')
    for i in range(0, len(results)):
        print('{}) {}\n'.format(i + 1, results[i]['title']))

    number = int(input('Selected number: '))
    while number <= 0 or number > len(results):
        number = int(input('Invalid number, please select a valid one: '))

    print(results[number - 1])
    # Type can be song, album, etc. For now the program only songs are processed
    pass


if __name__ == '__main__':
    main()
