import requests
import urllib.parse
import logging
import time

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# URL сайта или сайтов, который нужно проверять
urls = [
    'https://site.com/',
    'https://site2.com/',
]

# Токен вашего бота и chat_id группы
bot_token = "Токен вашего бота Телеграм"
chat_id = "Chat Id вашей группы в Телеграм"

# Функция проверки доступности сайта
def check_site_availability(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.head(url, timeout=10, headers=headers)
        return response.status_code
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при проверке {url}: {e}")
        return None

# Функция отправки уведомления в Telegram-группу
def send_telegram_notification(bot_token, chat_id, message):
    try:
        encoded_message = urllib.parse.quote_plus(message)
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={encoded_message}"
        response = requests.get(url)
        response.raise_for_status() # Проверка статуса ответа от Telegram API
        logging.info(f"Сообщение отправлено в Telegram: {message}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при отправке сообщения в Telegram: {e}")

# Основная логика для проверки всех сайтов
for url in urls:
    http_code = check_site_availability(url)

    # Проверяем, чтобы HTTP-код не был 200 (успех), 301 (редирект) или 302 (временный редирект)
    if http_code is None or (http_code != 200 and http_code != 301 and http_code != 302):
        message = f"Сайт {url} недоступен! Код ошибки: {http_code}"
        send_telegram_notification(bot_token, chat_id, message)
        print(message)
    else:
        print(f"Сайт {url} доступен или перенаправляет. Код: {http_code}")

    time.sleep(5) # Задержка между проверками сайтов
