#!/usr/bin/python3

from httpx import AsyncClient, codes # Yes, we could use requests but httpx supports async tasks and HTTP/2!
from src.telegram_checker import bot_checker
from asyncio import run
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
from urllib import parse
from time import sleep
from json import load
import yaml

#try to open settings.yaml otherwise use settings.yaml.dist as config file
try:
    with open('config/settings.yaml', 'r', encoding='utf-8') as yaml_config:
        config_map = yaml.load(yaml_config, Loader=yaml.SafeLoader)
except FileNotFoundError:
    with open('config/settings.yaml.dist', 'r', encoding='utf-8') as yaml_config:
        config_map = yaml.load(yaml_config, Loader=yaml.SafeLoader)

def get_token() -> str:
    return config_map['token']

def get_users() -> list[str]:
    return config_map['chat_ids']


async def check_ok(url: str) -> bool:
    async with AsyncClient(http2=True, follow_redirects=True) as client:
        try:
            r = await client.get(url)
            return codes.is_success(r.status_code)
        except:
            return codes.is_success(404)
  
def check_ping(host: str) -> bool:
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]

    return subprocess.call(command) == 0


async def make_request_to_telegram(service_name: str, method_used: str, chat_id: str) -> list:
    message = f'⚠️ The service {service_name} contacted via {method_used} results offline!'
    url = f'https://api.telegram.org/bot{get_token()}/sendMessage?chat_id={chat_id}&text={message}'

    async with AsyncClient(http2=True) as client:
        res = await client.post(url)
        return res.json()


def obtain_hostname(url: str) -> str:
    url_obj = parse.urlparse(url)
    return url_obj.netloc.replace('www.', '')


def handle_urls(url: str, method: str) -> None:
    match method:
        case 'get':
            check_result = run(check_ok(url))
        case 'ping':
            hostname = obtain_hostname(url)
            check_result = check_ping(hostname)
    
    if not check_result:
        handle_communication(url, method)
    else:
        print(f'✅ Execution of {method} with address {url} succeeded')


def handle_communication(url: str, method: str) -> None:
    obtained_ids = get_users()

    for _ in range(5):
        if obtained_ids == []:
            return

        for id in obtained_ids:
            tg_res = run(make_request_to_telegram(url, method, id))

            if tg_res['ok']:
                print(f'Message sent successfully to {id}')
                obtained_ids.remove(id)
            elif tg_res['error_code'] == 429:
                sleep(30)
                print('Error 429, aka too many requests')


def main() -> None:
    with open('src/urls.json', 'r') as f:
        urls_list = load(f)

    for method, urls in urls_list.items():
        for url in urls:
            handle_urls(url, method)
    
    bot_checker(config_map)
        


def init() -> None:
    if __name__ == '__main__':
        main() 


init()
