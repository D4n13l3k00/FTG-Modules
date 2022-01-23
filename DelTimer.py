#   Coded by D4n13l3k00    #
#     t.me/D4n13l3k00      #
# This code under AGPL-3.0 #

import re
from asyncio import sleep

from .. import loader, utils


@loader.tds
class DelTmMod(loader.Module):
    strings = {"name": "Delete Timer"}

    @loader.owner
    async def deltmcmd(self, m):
        ".deltm <реплай> <секунды>\
        \nУдалить сообщение в реплае через указанное время"
        reply = await m.get_reply_message()
        if not reply:
            return await m.edit("reply...")
        a = re.compile(r"^\d+$")
        t = utils.get_args_raw(m)
        if a.match(t):
            await m.delete()
            await sleep(int(t))
            await reply.delete()
        else:
            await m.edit("shit...")
            return
