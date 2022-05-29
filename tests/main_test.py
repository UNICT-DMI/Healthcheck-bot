import httpx
import pytest
from pytest_mock import MockerFixture
import src.main as main


tests = [
    {
        'func': main.get_users,
        'expected_res': ['12345678'],
        'arg': tuple(),
        'mock_obj': [main],
        'mock_func': ['getenv'],
        'mock_ret': ['12345678'],
        'is_async': False
    },
    {
        'func': main.get_users,
        'expected_res': ['12345678', '23456789'],
        'arg': tuple(),
        'mock_obj': [main],
        'mock_func': ['getenv'],
        'mock_ret': ['12345678;23456789'],
        'is_async': False
    },
    {
        'func': main.check_ok,
        'expected_res': [True],
        'arg': ('http://example.org/',),
        'is_async': False
    },
    {
        'func': main.check_ok,
        'expected_res': [False],
        'arg': ('garbage',),
        'is_async': False
    },
    {
        'func': main.check_ping,
        'expected_res': [True],
        'arg': ('example.org',),
        'is_async': False
    },
    {
        'func': main.check_ping,
        'expected_res': [False],
        'arg': ('garbage',),
        'is_async': False
    }
]

@pytest.mark.parametrize('test', tests)
async def test_generic(mocker: MockerFixture, test: dict) -> None:
    spyed_objs = []
    if test.get('mock_obj') is not None:
        for index, obj in enumerate(test['mock_obj']):
            mocker.patch.object(obj, test['mock_func'][index], return_value=test['mock_ret'][index])
            spyed_objs.append(mocker.spy(obj, test['mock_func'][index]))

    if test['is_async']:
        res = await test['func'](*test['arg'])
    else:
        res = test['func'](*test['arg'])

    assert res == test['expected_res']
    for index, spy in enumerate(spyed_objs):
        assert spy.spy_return == test['mock_ret'][index]

async def test_init(mocker: MockerFixture) -> None:
    mocker.patch.object(main, "__name__", "__main__")
    mocker.patch.object(main, 'main', return_value=None)

    #this is broken
    assert await main.init() == None
    
