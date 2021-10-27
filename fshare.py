#   Coded by D4n13l3k00    #
#     t.me/D4n13l3k00      #
# This code under AGPL-3.0 #

import asyncio

from .. import loader, utils


def register(cb):
    cb(HosttMod())


class HosttMod(loader.Module):
    """Загрузить файл через @freehosttgbot"""
    strings = {'name': 'FileShare'}

    def __init__(self):
        self.name = self.strings['name']

    async def dupcmd(self, m):
        'Загрузить файл через @freehosttgbot'
        reply = await m.get_reply_message()
        if reply and reply.file:
            a = (await m.client.send_file("freehosttgbot", reply)).id
            await asyncio.sleep(1)
            lnk = (await m.client.get_messages("freehosttgbot", ids=a+1)).entities[0].url
            await m.edit(f"[Link:]({lnk}) `{lnk}`", parse_mode='markdown')
        else:
            await m.edit("shit...")
