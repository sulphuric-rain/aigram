import asyncio
from pyrogram import Client, idle
from pyrogram.errors import Unauthorized, SessionPasswordNeeded, BadRequest
from pyrogram.types import User, TermsOfService
from pyrogram.handlers import MessageHandler
from pyrogram import filters


from tgconfig import api_id, api_hash

# TODO: * Resolve User by id or username
# TODO: * Add Resolved User to Set of Resolved Users
# TODO: * Set message handler for each in Resolved Users Set as Resolved User
# TODO: * On new Message from Resolved User send request to ChatGPT with Message text data
# TODO: * When response from ChatGPT is not yet fulfilled and it not fail/error set Typing status to Resolved User
# TODO: * When response return from ChatGPT send response.text as Message to Resolved User

USER_POOL = []


def filter_message_user_in_pool(filter, client, update):
    print(update)
    return True


user_pool_filter = filters.create(filter_message_user_in_pool, "UserPoolFilter")
app = Client("aigram", api_id, api_hash)


async def init_client(client):
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



def add_to_user_pool(user):
    USER_POOL.append(user)


def remove_from_user_pool(user):
    USER_POOL.remove(user)



async def handle_message(client, message):
    print(f"From: {message.from_user.first_name}\nText: {message.text}")



async def main():
    client = await init_client(app)
    await auth(client)
    app.add_handler(MessageHandler(handle_message))
    await idle()


app.run(main())


