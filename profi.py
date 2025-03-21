from bs4 import BeautifulSoup as bs
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
import re
import telebot

# Settings
myLogin = 'yourlogin'  # login
myPassword = 'pass'  # password
main_key = {'Психоло', 'оби', 'ремон', 'труб'}  # Needed parts of words here
bad_key = {'врач'} # Needed parts of words here

token = '6489483666jkhkjjkhkjsdfhjkdshfjkhdskfjhdsh--yourtoken'
chat_id = '@blablabla'
profi = []

url = 'https://profi.ru/backoffice/n.php'
url_site = 'https://spb.profi.ru'

def send_email(task):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    me = '<your email (from)>'
    you = '<your email (to)>'
    server.login(me, '<your_email_password(from)>')
    msg = MIMEText(task + url)
    msg['Subject'] = 'Новое задание!'
    msg['From'] = me
    msg['To'] = you
    server.sendmail(me, [you], msg.as_string())
    server.quit()

def refreshPage():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("End of scroll")
            break
        last_height = new_height
        print("New content!")
    return

def word_check(full_text, good, bad):
    for key in full_text:
        for i in good:
            if i.lower() in key.lower():
                for j in bad:
                    if j.lower() in key.lower():
                        return False
                return True
    return False

service = Service("/usr/local/bin/chromedriver") # For FreeBSD, install chromedriver: sudo pkg install chromium
bot = telebot.TeleBot(token)
options = webdriver.ChromeOptions()
options.add_argument("--user-agent=Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)")
options.add_argument("--headless") # Execute in background
options.add_argument("--no-sandbox") # For FreeBSD
options.add_argument("--disable-dev-shm-usage") # For FreeBSD
options.add_argument("--dns-prefetch-disable") # Timeout

driver = webdriver.Chrome(service=service, options=options)

# Enter login and password
try:
   driver.get(url);
except TimeoutException as ex:
   print(ex.Message)
   driver.navigate().refresh()
namesLogin = driver.execute_script(
    "return document.getElementsByClassName('ui-input ui-input-bo login-form__input-login ui-input_desktop ui-input_with-placeholder_empty');")
namesLogin[0].clear()
email_input = namesLogin[0].send_keys(myLogin)

time.sleep(1)
namesPassword = driver.execute_script(
    "return document.getElementsByClassName('ui-input ui-input-bo login-form__input-password ui-input_desktop ui-input_with-placeholder_empty');")
namesPassword[0].clear()
password_input = namesPassword[0].send_keys(myPassword)
time.sleep(1)

namesButton = driver.execute_script(
    "return document.getElementsByClassName('ui-button');")
button_input = namesButton[0].click()

# Pause comfortably to enter the captcha
time.sleep(30)

page = driver.page_source

soup = bs(page, 'html.parser')

try:
    while True:
        # Body of the loop after login
        refreshPage()

        arr = driver.execute_script(
            "return document.getElementsByClassName('SnippetBodyStyles__Container-sc-br3c4b-0 dNCmqL');")

        # We get a list of links of all profiles that we found, taking into account scrolling
        # arrayClients = []
        # for i in arr:
        #     arrayClients.append(i.get_attribute('href'))
        # There may be a collection of questionnaires or functionality as desired. arrayClients - list of urls

        for block in soup.find_all(class_=re.compile('SnippetBodyStyles__Container-')):
            task_key = block.find(class_=re.compile('SubjectAndPriceStyles__SubjectsText-'))
            name = block.find(class_=re.compile('SnippetBodyStyles__MainInfo-'))
            my_url = url_site + str(block.attrs['href'])
            task_stack = (str(task_key.get_text()), str(name.get_text()), my_url)
            arr_url = ''.join(filter(lambda x: x.isdigit(), my_url))
            arr_url = str(block.attrs['href']) if len(arr_url) < 8 else arr_url[:8]
            if arr_url not in profi:
                if word_check(task_stack, main_key, bad_key):
                    profi.append(arr_url)
                    bot.send_message(chat_id, str(': '.join(task_stack)))
        if len(profi) > 100:
            profi = profi[-10:]
        time.sleep(60)
        try:
            driver.get(url);
        except TimeoutException as ex:
            print(ex.Message)
            driver.navigate().refresh()
        page = driver.page_source
        soup = bs(page, 'html.parser')

except Exception as ex:
    print(ex)

finally:
    driver.close()
    driver.quit()
