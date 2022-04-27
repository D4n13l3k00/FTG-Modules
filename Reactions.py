# .------.------.------.------.------.------.------.------.------.------.
# |D.--. |4.--. |N.--. |1.--. |3.--. |L.--. |3.--. |K.--. |0.--. |0.--. |
# | :/\: | :/\: | :(): | :/\: | :(): | :/\: | :(): | :/\: | :/\: | :/\: |
# | (__) | :\/: | ()() | (__) | ()() | (__) | ()() | :\/: | :\/: | :\/: |
# | '--'D| '--'4| '--'N| '--'1| '--'3| '--'L| '--'3| '--'K| '--'0| '--'0|
# `------`------`------`------`------`------`------`------`------`------'
#
#                     Copyright 2022 t.me/D4n13l3k00
#           Licensed under the Creative Commons CC BY-NC-ND 4.0
#
#                    Full license text can be found at:
#       https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode
#
#                           Human-friendly one:
#            https://creativecommons.org/licenses/by-nc-nd/4.0

# meta developer: @D4n13l3k00


import contextlib
from .. import loader
from telethon import functions


@loader.tds
class ReactionsMod(loader.Module):
    "Telegram reactions"

    strings = {"name": __doc__}

    async def client_ready(self, client, _):
        self.client = client

    def reaction(func):
        async def wrapper(self, *args):
            "<reply>"
            message = args[0]
            emoji = await func(self)
            if reply := await message.get_reply_message():
                with contextlib.suppress(Exception):
                    await self.client(
                        functions.messages.SendReactionRequest(
                            reply.peer_id, reply.id, reaction=emoji
                        )
                    )
            if message.out:
                await message.delete()

        return wrapper

    @reaction
    async def lovecmd(self):
        return "❤"

    @reaction
    async def sadcmd(self):
        return "😢"

    @reaction
    async def nastycmd(self):
        return "🤮"

    @reaction
    async def cutecmd(self):
        return "🥰"

    @reaction
    async def clapcmd(self):
        return "👏"

    @reaction
    async def fuckcmd(self):
        return "🤬"

    @reaction
    async def wtfcmd(self):
        return "🤯"

    @reaction
    async def hmmcmd(self):
        return "🤔"

    @reaction
    async def hooraycmd(self):
        return "🎉"

    @reaction
    async def likecmd(self):
        return "👍"

    @reaction
    async def dislikecmd(self):
        return "👎"

    @reaction
    async def firecmd(self):
        return "🔥"

    @reaction
    async def omgcmd(self):
        return "😱"

    @reaction
    async def wowcmd(self):
        return "🤩"

    @reaction
    async def hehecmd(self):
        return "😁"

    @reaction
    async def shitcmd(self):
        return "💩"
