#!/usr/bin/python3

import httpx # Yes, we could use requests but httpx supports async tasks and HTTP/2!
from os import getenv
from asyncio import run
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
from urllib import parse
from time import sleep


def get_users() -> list[str]:
    return getenv('QDBotIDs').split(';')


def check_ok(url: str) -> bool:
    r = httpx.get(url)
    #may want to use a keyword instead
    return r.status_code < 400

  
def check_ping(host: str) -> bool:

    param = '-n' if platform.system().lower() == 'windows' else '-c'

    command = ['ping', param, '1', host]

    return subprocess.call(command) == 0


async def make_request_to_telegram(service_name: str, method_used: str) -> list:
    tg_responses = []
    message = f'⚠️ The service {service_name} contacted via {method_used} results offline!'

    users_list = get_users()
    
    for chat_id in users_list:
        url = f'https://api.telegram.org/bot{getenv("QDBotToken")}/sendMessage?chat_id={chat_id}&text={message}'

        async with httpx.AsyncClient(http2=True) as client:
            res = await client.post(url)
            """
            #TODO: limit number of append
            if not (handle_responses(res)):
                users_list.append(chat_id)
            """
            tg_responses.append(res.json())
    
    return tg_responses


def obtain_hostname(url: str) -> str:
    url_obj = parse.urlparse(url)
    return url_obj.netloc.replace('www.', '')


def handle_urls(url: str, method: str) -> None:
    match method:
        case 'get':
            check_result = check_ok(url)
        case 'ping':
            hostname = obtain_hostname(url)
            check_result = check_ping(hostname)
    
    if not check_result:
        tg_res = run(make_request_to_telegram(url, method))
        #handle_retries(url, method, 5)
    else:
        print(f'✅ Execution of {method} with address {url} succeeded')

"""
def handle_responses(res) -> bool:
   
    if not res['ok']:
        print(f"Error {str(res['error_code'])}: {res['description']}")

        if res['error_code'] == 429:
            #too many requests
            sleep(30)
            print("Error 429")

        return False
    else:
        print("Message sent succesfully")
        return True
"""  


def main() -> None:
    urls_list = { # This should be loaded from a json
        'get': ['https://duckduckgo.com/', 'https://google.com/'], 
        'ping': ['https://duckduckgo.com/', 'https://google.com/']
    }

    for method, urls in urls_list.items():
        for url in urls:
            handle_urls(url, method)
        


def init() -> None:
    if __name__ == '__main__':
        main() 


init()