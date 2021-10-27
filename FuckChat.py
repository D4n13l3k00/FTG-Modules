#   Coded by D4n13l3k00    #
#     t.me/D4n13l3k00      #
# This code under AGPL-3.0 #

import re
from asyncio import sleep

from .. import loader, utils


@loader.tds
class ChatFuckerMod(loader.Module):
    """Чатоёб"""
    strings = {'name': 'Чатоёб'}

    @loader.owner
    async def fccmd(self, message):
        """.fc <Количество заёба> <reply to text/text>
                Заебать чат (СРЁТ В ЛОГИ)
        """
        reply = await message.get_reply_message()
        repeat = 0
        text = ""
        if reply:
            if utils.get_args_raw(message):
                try:
                    if(reply.text):
                        text = reply.text
                        repeat = int(utils.get_args_raw(message))
                    else:
                        await message.edit("Текста нет!")
                        return
                except:
                    await message.edit("<b>Err</b>")
                    return
            else:
                await message.edit("А скольо раз надо?")
                return
        elif utils.get_args_raw(message):
            try:
                repeat = int(utils.get_args_raw(message).split(" ")[0])
                text = re.split(r".[a-z-0-9]{1,} [0-9]{1,} ", message.text)[1]
            except:
                await message.edit("<b>Err</b>")
                return
        else:
            await message.edit("А как же текст/реплай на текст?")
            return
        await message.delete()
        for _ in range(repeat):
            m = await message.client.send_message(message.to_id, text)
            await sleep(0.5)
            await m.delete()
            await sleep(0.1)
