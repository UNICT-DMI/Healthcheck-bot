#!/usr/bin/python3

import httpx # Yes, we could use requests but httpx supports async tasks and HTTP/2!
from os import getenv
from asyncio import run

def get_users() -> list[str]:
    #print(getenv('QDBotIDs'))
    return getenv('QDBotIDs').split(';')

def check_ok(url: str) -> bool:
    r = httpx.get(url)
    #there are various status codes, duckduckgo returns 301; is there a keyword only for errors?
    #return r.status_code == httpx.codes.OK
    return r.status_code == 301

async def make_request_to_telegram(service_name: str) -> dict:
    #TODO: implement check with ping
    if check_ok(service_name) == False:
        #print("async")
        message = f'⚠️ The service {service_name} results offline!'

        #print("getusers: ")
        #print(get_users())

        for chat_id in get_users():
            print("id: " + chat_id)
            url = f'https://api.telegram.org/bot{getenv("QDBotToken")}/sendMessage?chat_id={chat_id}&text={message}'

            async with httpx.AsyncClient(http2=True) as client:
                res = await client.post(url)
                return res.json()


if __name__ == '__main__':
    run(make_request_to_telegram('http://duckduckgo.com/'))