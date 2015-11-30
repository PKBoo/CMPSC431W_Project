from bs4 import BeautifulSoup
import requests
import shutil
import os

url = 'https://wrapbootstrap.com'
request = requests.get('https://wrapbootstrap.com/themes/page.1/sort.rank/order.asc')
data = request.text
soup = BeautifulSoup(data, 'html.parser')
i = 1
for theme_link in soup.find_all('a', {'class': 'image'}):
    print(url + theme_link.get('href'))
    theme_request = requests.get(url+theme_link.get('href'))
    theme_request_data = theme_request.text
    soup = BeautifulSoup(theme_request_data, 'html.parser')
    img_url = soup.find('img', {'id': 'thing_image'}).get('src')
    print('downloading image')
    print(img_url)
    img_download_req = requests.get('http:' + img_url, stream=True)
    if img_download_req.status_code == 200:
        if not os.path.exists('templatesandmoe/static/templates_data/' + str(i)):
            os.makedirs('templatesandmoe/static/templates_data/' + str(i))
        with open('templatesandmoe/static/templates_data/' + str(i) + '/preview_' + str(i) + '.jpg', 'wb') as f:
            img_download_req.raw.decode_content = True
            shutil.copyfileobj(img_download_req.raw, f)

    i += 1

