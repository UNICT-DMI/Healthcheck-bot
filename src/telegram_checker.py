from pyrogram import Client, filters
from pyrogram.errors import RPCError
from pyrogram.types import Message
from os.path import exists
from asyncio import sleep

config_map = None
app = Client('healthcheck_user_client')
received_answer = []

@app.on_message(filters.text & filters.bot)
async def check_welcome(client: Client, message: Message) -> None:
    global received_answer

    for bots_to_check in config_map['bots_to_check']:
        if message.from_user.username == bots_to_check['username']:
            if message.text == bots_to_check['expected_response']:
                received_answer.insert(0, message.from_user.username)
            return


def bot_checker(config: dict) -> None:
    global config_map
    config_map = config

    # No bots to check
    if 'bots_to_check' not in config_map or not config_map['bots_to_check']:
        return

    # Checking if already exists a session
    if not exists('healthcheck_user_client.session'):
        # We need to check that all the needed parameters are available
        for key in ['api_id', 'api_hash']:
            if key not in config_map:
                print(f'Missing required parameter: {key}')
                return
        
        app.api_id=config_map['api_id']
        app.api_hash=config_map['api_hash']

        print('Starting login, after the client is connected you can exit with CTRL+C')
    
    app.run(main())


async def main() -> None:
    async with app:
        for bot in config_map['bots_to_check']:
            if not all(key in bot for key in ['username', 'command', 'expected_response']):
                print(f'Skipping {bot["username"] if "id" in bot else "a bot without a specified username c:"}')
                continue
            
            try:
                await app.send_message(chat_id=bot['username'], text=bot['command'])
            except RPCError as e:
                print(f'There was a problem communicating with {bot["username"]}:', e)

        await sleep(10) # Just to be sure the bot is not busy
        # To prevent circular imports
        # TODO: in a future refactor we could split the main code in another file only for webpages, 
        #       would improve modularity and reuse of code with an helper file
        print(received_answer)
        from main import make_request_to_telegram
        for bot in config_map['bots_to_check']:
            if bot['username'] not in received_answer:
                for user_to_notify in config_map['chat_ids']:
                    await make_request_to_telegram(f'@{bot["username"]}', 'Telegram', user_to_notify)

