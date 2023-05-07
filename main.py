import asyncio
from pyrogram import Client

from tgconfig import api_id, api_hash

# TODO: * Resolve User by id or username
# TODO: * Add Resolved User to Set of Resolved Users
# TODO: * Set message handler for each in Resolved Users Set as Resolved User
# TODO: * On new Message from Resolved User send request to ChatGPT with Message text data
# TODO: * When response from ChatGPT is not yet fulfilled and it not fail/error set Typing status to Resolved User
# TODO: * When response return from ChatGPT send response.text as Message to Resolved User
async def main():
    async with Client("my_account", api_id, api_hash) as app:
        await app.send_message("me", "Hello World")


asyncio.run(main())