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


from .. import loader
from telethon import functions


@loader.tds
class ReactionsMod(loader.Module):
    "Telegram reactions"

    strings = {"name": __doc__}

    async def client_ready(self, client, _):
        self.client = client

    def reaction(func):
        async def wrapper(self, *args, **kwargs):
            "<reply>"
            message, emoji = await func(self, *args, **kwargs)
            if reply := await message.get_reply_message():
                await self.client(
                    functions.messages.SendReactionRequest(
                        reply.peer_id, reply.id, reaction=emoji
                    )
                )
            if message.out:
                await message.delete()

        return wrapper

    @reaction
    async def lovecmd(self, m):
        return m, "❤"

    @reaction
    async def sadcmd(self, m):
        return m, "😢"

    @reaction
    async def nastycmd(self, m):
        return m, "🤮"

    @reaction
    async def cutecmd(self, m):
        return m, "🥰"

    @reaction
    async def clapcmd(self, m):
        return m, "👏"

    @reaction
    async def fuckcmd(self, m):
        return m, "🤬"

    @reaction
    async def wtfcmd(self, m):
        return m, "🤯"

    @reaction
    async def hmmcmd(self, m):
        return m, "🤔"

    @reaction
    async def hooraycmd(self, m):
        return m, "🎉"

    @reaction
    async def likecmd(self, m):
        return m, "👍"

    @reaction
    async def dislikecmd(self, m):
        return m, "👎"

    @reaction
    async def firecmd(self, m):
        return m, "🔥"

    @reaction
    async def omgcmd(self, m):
        return m, "😱"

    @reaction
    async def wowcmd(self, m):
        return m, "🤩"

    @reaction
    async def hehecmd(self, m):
        return m, "😁"

    @reaction
    async def shitcmd(self, m):
        return m, "💩"
