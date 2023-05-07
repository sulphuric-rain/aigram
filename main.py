import asyncio
from pyrogram import Client
from pyrogram.errors import Unauthorized, SessionPasswordNeeded, BadRequest
from pyrogram.types import User, TermsOfService

from tgconfig import api_id, api_hash

# TODO: * Resolve User by id or username
# TODO: * Add Resolved User to Set of Resolved Users
# TODO: * Set message handler for each in Resolved Users Set as Resolved User
# TODO: * On new Message from Resolved User send request to ChatGPT with Message text data
# TODO: * When response from ChatGPT is not yet fulfilled and it not fail/error set Typing status to Resolved User
# TODO: * When response return from ChatGPT send response.text as Message to Resolved User



async def init_client(session_name, api_id, api_hash):
    client = Client(session_name, api_id, api_hash)
    await client.connect()
    await client.initialize()
    return client


async def is_user_auth(client):
    try:
        await client.get_me()
        return True
    except Unauthorized:
        return False



async def send_code(phone_number, client):
    sent_code_info = await client.send_code(phone_number)
    return sent_code_info


async def password_auth_step(client):
    while (True):
        try:
            password = input("Password needed type here: ")
            response = await client.check_password(password)
            if type(response) is not User:
                raise RuntimeError("Something went wrong")
            return response
        except BadRequest:
            continue


async def sign_in(phone_number, phone_code_hash, phone_code, client):
    try:
        client = await client.sign_in(phone_number, phone_code_hash, phone_code)
        if type(client) is not User:
            raise TypeError("You need to signup first in off telegram app...")
    except SessionPasswordNeeded:
        await password_auth_step(client)


async def auth(client):
    if await is_user_auth(client) is not True:
        phone_number = input("Type you phone number: ")
        response = await send_code(phone_number, client)
        phone_code_hash = response.phone_code_hash
        phone_code = input("Type code sent by telegram here: ")
        await sign_in(phone_number, phone_code_hash, phone_code, client)
        print("You authorized!\n")
        return True
    print("auth is not needed next...")


async def main():
    client = await init_client("aigram", api_id, api_hash)
    await auth(client)
    # async with Client("my_account", api_id, api_hash) as app:
    #     await app.send_message("me", "Hello World")


asyncio.run(main())