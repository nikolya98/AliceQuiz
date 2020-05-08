import requests as req
from bs4 import BeautifulSoup as bs


def get_category():
    url = 'https://viquiz.ru/theme/'
    session = req.session()
    request = session.get(url)

    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        themes = {}
        div_container = soup.find('div', class_='themes_cats')
        blocks = div_container.find_all('div', class_='themes_catblock')

        for block in blocks:
            theme = block.find('h2')
            theme_title = theme.text
            link = block.find('a', class_='themes_cat')
            link = link.attrs.get('href')
            themes.update({theme_title: link.replace('/theme/', '')})

        return themes

    else:
        print("Возникла непредвиденная ошибка... Приносим искренние извинения!")


