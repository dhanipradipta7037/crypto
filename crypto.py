from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
import time
import requests

url = 'https://coinmarketcap.com/'

def running(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, timeout=120000)
        for x in range (1, 11):
            print(x)
            page.mouse.wheel(0, 1000)
            time.sleep(10)
        html = page.inner_html('table.sc-66133f36-3.etbEmy.cmc-table')
    return html

def save_html():
    html = running(url)
    with open("HTML/coincrypto.html", "+w", encoding="utf-8") as f:
        f.write(html)

def parser_data():
    data_coin =[]
    with open("HTML/coincrypto.html", encoding="utf-8") as f:
        page = f.read()
        soup = BeautifulSoup(page, "html.parser")
        coins = soup.find('tbody')
        all_coins = coins.find_all('tr')
        for coin in all_coins:
            id = coin.find('p', {'class':'sc-4984dd93-0 iWSjWE'}).text.strip()
            name = coin.find('p', {'class':'sc-4984dd93-0 kKpPOn'}).text.strip()
            kode = coin.find('p', {'class':'sc-4984dd93-0 iqdbQL coin-item-symbol'}).text.strip()
            list_price = coin.find('div', {'class':'sc-a0353bbc-0 gDrtaY'})
            price = list_price.find('span').text.strip()
            market_cap = coin.find('span', {'class':'sc-7bc56c81-1 bCdPBp'}).text.strip()
            logo = coin.find('img', {'class':'coin-logo'}).get('src')
            supply = coin.find('p', {'class':'sc-4984dd93-0 WfVLk'}).text.strip()
            list_data ={
                'ID':id,
                'Name':name,
                'Code':kode,
                'Price':price,
                'Market Cap':market_cap,
                'Supply':supply,
                'Logo':logo
            }
            data_coin.append(list_data)
    return data_coin

def save_csv():
    data_crypto = parser_data()
    df =pd.DataFrame(data_crypto)
    print(df)
    df.to_csv('Data crypto.csv', index=False)

def download_logo():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
    df = pd.read_csv('Data crypto.csv')
    for img in df['Logo']:
        data_img = img.split('/')[-1].replace('.png', '')
        respon = requests.get(img, headers=headers)
        if respon.status_code == 200:
            with open('IMAGES/{}.png'.format(data_img), 'wb') as fp:
                fp.write(respon.content)
                print("Download finish")
        else:
            print("Gagal mendownload gambar. Status code:", respon.status_code)



if __name__ == '__main__':
    #save_html()
    #save_csv()
    download_logo()
