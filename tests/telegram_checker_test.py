import pytest
from pytest_mock import MockerFixture
from unittest.mock import AsyncMock
import src.telegram_checker as tg
import src.main as main
from pyrogram.client import Client
import asyncio

tests = [
    {
        'func': tg.bot_checker,
        'expected_res': None,
        'arg': ({'bots_to_check': [{'username':'WebpageBot', 'command':'/start', 'expected_response':'Hello, I\'m the Webpage Bot!\nPlease send me up to 10 links and I will update previews for them.'}]},),
        'is_async': False
    },
    {
        'func': tg.bot_checker,
        'expected_res': None,
        'arg': ({},),
        'is_async': False
    },
    {
        'func': tg.bot_checker,
        'expected_res': None,
        'arg': ({'api_id':'12345', 'api_hash':'0123456789abcdef0123456789abcdef','bots_to_check': [{'username':'WebpageBot', 'command':'/start', 'expected_response':'Hello, I\'m the Webpage Bot!\nPlease send me up to 10 links and I will update previews for them.'}]},),
        'mock_obj': [Client],
        'mock_func': ['run'],
        'mock_ret': [None],
        'is_async': False
    },
    {
        'func': tg.main,
        'expected_res': None,
        'arg': tuple(),
        'mock_obj': [main, Client],
        'mock_func': ['make_request_to_telegram', 'send_message'],
        'mock_ret': [None, None],
        'mock_dict': {'bots_to_check': [{'username':'WebpageBot', 'command':'/start', 'expected_response':'Hello, I\'m the Webpage Bot!\nPlease send me up to 10 links and I will update previews for them.'}]},
        'is_async': True
    },
    {
        'func': tg.main,
        'expected_res': None,
        'arg': tuple(),
        'mock_obj': [main, Client],
        'mock_func': ['make_request_to_telegram', 'send_message'],
        'mock_ret': [None, None],
        'mock_dict': {'bots_to_check': [{'command':'/start'}]},
        'is_async': True
    },
    {
        'func': tg.check_welcome,
        'expected_res': None,
        'arg': (None, {'from_user': {'username': 'username'}, 'text': 'A response'},),
        'mock_dict': {'bots_to_check': [{'username':'WebpageBot', 'command':'/start', 'expected_response':'Hello, I\'m the Webpage Bot!\nPlease send me up to 10 links and I will update previews for them.'}]},
        'is_async': True
    }
]

@pytest.mark.asyncio
@pytest.mark.parametrize('test', tests)
async def test_generic(mocker: MockerFixture, test: dict) -> None:
    spyed_objs = []
    spyed_dicts = []

    if test.get('mock_obj'):
        for index, obj in enumerate(test['mock_obj']):
            mocker.patch.object(obj, test['mock_func'][index], return_value=test['mock_ret'][index])
            spyed_objs.append(mocker.spy(obj, test['mock_func'][index]))
    
    if test.get('mock_dict'):
        mocker.patch.dict(tg.config_map, test['mock_dict'])
        spyed_dicts.append(mocker.spy(tg, 'config_map'))

    if test.get('is_async'):
        res = await test['func'](*test['arg'])
    else:
        res = test['func'](*test['arg'])       

    assert res == test['expected_res']
    for index, spy in enumerate(spyed_objs):
        assert spy.spy_return == test['mock_ret'][index]
