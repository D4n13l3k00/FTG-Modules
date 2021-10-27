#   Coded by D4n13l3k00    #
#     t.me/D4n13l3k00      #
# This code under AGPL-3.0 #

import re

from telethon.errors import ChannelInvalidError

from .. import loader, utils


@loader.tds
class SenderMod(loader.Module):
    strings = {'name': 'Sender'}

    @loader.owner
    async def sndcmd(self, m):
        """.snd <канал/чат/id> <reply>
        Отпрпвить сообшение в чат/канал(без авторства)
        """
        args = utils.get_args_raw(m)
        reply = await m.get_reply_message()
        if not args:
            return await m.edit("[Sender] Укажите канал/чат")
        try:
            this = await m.client.get_input_entity(int(args) if re.match(r'-{0,1}\d+', args) else args)
        except ChannelInvalidError as e:
            return await m.edit("[Sender] Такого канала/чата не существует!")
        except Exception as e:
            return await m.edit("[Sender] Неизвестная мне ошибка:\n"+" ".join(e.args))
        ok = await m.client.send_message(this, reply)
        await m.edit("[Sender] Сообщение отправлено!")
