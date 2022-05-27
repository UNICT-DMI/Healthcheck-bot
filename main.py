#!/usr/bin/python3

import httpx # Yes, we could use requests but httpx supports async tasks and HTTP/2!
from os import getenv
from asyncio import run

async def make_request_to_telegram(service_name: str) -> dict:
    message = f'⚠️ The service {service_name} results offline!'
    url = f'https://api.telegram.org/bot{getenv("QDBotToken")}/sendMessage?chat_id={getenv("QDBotIDs")}&text={message}'

    async with httpx.AsyncClient(http2=True) as client:
        res = await client.post(url)
        print(res)
        return res


if __name__ == '__main__':
    run(make_request_to_telegram('test'))