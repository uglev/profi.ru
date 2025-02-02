# profi.ru
Bot for parsing orders from Profi.ru

# profi.ru bot
Бот для парсинга заказов с профи.ру по ключевым словам.
Может отправлять сообщения в группу телеграмм (по умолчанию) и по электронной почте.
В связи с вводом капчи её необходимо вводить вручную после автоматического логина (время ввода по умолчанию — 30 секунд).
Автоматически скроллит заказы, подгружая новые, если их много.
Для работы требуются логин, пароль, ID бота и имя группы со знаком "@".

Установка зависимостей: python -m pip install -r requirements.txt

Обратите внимание, что использование ботов для автоматического отклика на заказы может нарушать правила платформы Profi.ru. Поэтому перед использованием данного кода рекомендуется ознакомиться с правилами Profi.ru и получить разрешение на использование бота от администрации платформы.

P. S. Для тех, кто использует FreeBSD, необходимо использование таких параметров chromedriver, где переменная service - искомый путь после установки sudo pkg install chromium:

import selenium

from selenium import webdriver

from selenium.webdriver.chrome.options import Options

from selenium.webdriver.chrome.service import Service

from bs4 import BeautifulSoup as bs

...

service = Service("/usr/local/bin/chromedriver")

chrome_options = Options()

chrome_options.add_argument("--headless")

chrome_options.add_argument("--user-agent=Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)")

chrome_options.add_argument("--headless")  # Запуск в фоновом режиме

chrome_options.add_argument("--no-sandbox")  # Для FreeBSD

chrome_options.add_argument("--disable-dev-shm-usage")  # Для FreeBSD

driver = webdriver.Chrome(service=service, options=chrome_options)
