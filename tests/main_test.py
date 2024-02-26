import pytest
from pytest_mock import MockerFixture
from unittest.mock import AsyncMock
import src.main as main


tests = [
    {
        'func': main.check_ok,
        'expected_res': True,
        'arg': ('http://example.org/',),
        'is_async': True
    },
    {
        'func': main.check_ok,
        'expected_res': False,
        'arg': ('https://github.com/IDontThinkThisPageWillEverExist',),
        'is_async': True
    },
    {
        'func': main.check_ping,
        'expected_res': False,
        'arg': ('wrongurlpage.com',)
    }, 
    {
        'func': main.obtain_hostname,
        'expected_res': 'example.com',
        'arg': ('http://example.com',)
    },
    {
        'func': main.get_users,
        'expected_res': [],
        'arg': tuple(),
    },
    {
        'func': main.check_ping,
        'expected_res': True,
        'arg': ('example.org',),
        'mock_obj': [main.subprocess],
        'mock_func': ['call'],
        'mock_ret': [0]
    },
    {
        'func': main.make_request_to_telegram,
        'expected_res': {"ok":False,"error_code":401,"description":"Unauthorized"},
        'arg': ('http://example.com', 'get', '0'),
        'mock_obj': [main],
        'mock_func': ['get_token'],
        'mock_ret': ['123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11'],
        'is_async': True  
    },
    {
        'func': main.handle_urls,
        'expected_res': None,
        'arg': ('http://example.com', 'get'),
        'mock_obj': [main],
        'mock_func': ['run'],
        'mock_ret': [AsyncMock(return_value=True)]
    },
    {
        'func': main.handle_urls,
        'expected_res': None,
        'arg': ('http://example.com', 'get'),
        'mock_obj': [main, main],
        'mock_func': ['run', 'handle_communication'],
        'mock_ret': [AsyncMock(return_value=False), None]
    },
    {
        'func': main.handle_urls,
        'expected_res': None,
        'arg': ('http://example.com', 'ping'),
        'mock_obj': [main, main],
        'mock_func': ['obtain_hostname', 'check_ping'],
        'mock_ret': ['example.com', True]
    },
    {
        'func': main.handle_urls,
        'expected_res': None,
        'arg': ('http://example.com', 'ping'),
        'mock_obj': [main, main, main],
        'mock_func': ['obtain_hostname', 'check_ping', 'handle_communication'],
        'mock_ret': ['example.com', False, None]
    },
    {
        'func': main.handle_communication,
        'expected_res': None,
        'arg': ('http://example.com', 'get'),
        'mock_obj': [main, main, main],
        'mock_func': ['get_users', 'run', 'sleep'],
        'mock_ret': [['12345678'], {"ok":False,"error_code":429,"description":"Unauthorized"}, None]
    },
    {
        'func': main.handle_communication,
        'expected_res': None,
        'arg': ('http://example.com', 'get'),
        'mock_obj': [main, main],
        'mock_func': ['get_users', 'run'],
        'mock_ret': [['12345678'], {"ok":True,"error_code":429,"description":"Fine"}]
    },
    {
        'func': main.handle_communication,
        'expected_res': None,
        'arg': ('http://example.com', 'get'),
        'mock_obj': [main, main],
        'mock_func': ['get_users', 'run'],
        'mock_ret': [[], None]
    },
    {
        'func': main.main,
        'expected_res': None,
        'arg': tuple(),
        'mock_obj': [main, main],
        'mock_func': ['handle_urls', 'bot_checker'],
        'mock_ret': [None, None]
    },
    {
        'func': main.get_token,
        'expected_res': '',
        'arg': tuple(),
    },
    {
        'func': main.get_users,
        'expected_res': [],
        'arg': tuple(),  
    }
]

@pytest.mark.asyncio
@pytest.mark.parametrize('test', tests)
async def test_generic(mocker: MockerFixture, test: dict) -> None:
    spyed_objs = []
    if test.get('mock_obj') is not None:
        for index, obj in enumerate(test['mock_obj']):
            mocker.patch.object(obj, test['mock_func'][index], return_value=test['mock_ret'][index])
            spyed_objs.append(mocker.spy(obj, test['mock_func'][index]))

    if test.get('is_async'):
        res = await test['func'](*test['arg'])
    else:
        res = test['func'](*test['arg'])       

    assert res == test['expected_res']
    for index, spy in enumerate(spyed_objs):
        assert spy.spy_return == test['mock_ret'][index]


def test_init(mocker: MockerFixture) -> None:
    mocker.patch.object(main, "__name__", "__main__")
    mocker.patch.object(main, 'main', return_value=None)

    assert main.init() == None