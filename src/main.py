#!/usr/bin/python3

import httpx # Yes, we could use requests but httpx supports async tasks and HTTP/2!
from os import getenv
from asyncio import run
import platform    # For getting the operating system name
import subprocess  # For executing a shell command


def get_users() -> list[str]:
    #print(getenv('QDBotIDs'))
    return getenv('QDBotIDs').split(';')

 
def check_ok(url: str) -> bool:
    r = httpx.get(url)
    #there are various status codes, duckduckgo returns 301; is there a keyword only for errors?
    #return r.status_code == httpx.codes.OK
    return r.status_code < 400


def check_ok(url: str) -> bool:
    r = httpx.get(url)
    #there are various status codes, duckduckgo returns 301; is there a keyword only for errors?
    #return r.status_code == httpx.codes.OK
    return r.status_code < 400

  
def my_ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """


    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    return subprocess.call(command) == 0


async def make_request_to_telegram(service_name: str,hostname: str) -> dict:
    
    if check_ok(service_name) == False or my_ping(hostname) == False:
        
        message = f'⚠️ The service {service_name} results offline!'

        #print("getusers: ")
        #print(get_users())

        for chat_id in get_users():
            print("id: " + chat_id)
            url = f'https://api.telegram.org/bot{getenv("QDBotToken")}/sendMessage?chat_id={chat_id}&text={message}'

            async with httpx.AsyncClient(http2=True) as client:
                res = await client.post(url)
                return res.json()


async def main() -> None:
    await make_request_to_telegram('https://duckduckgo.com/')


async def init() -> None:
    if __name__ == '__main__':
        await main() 


run(init())