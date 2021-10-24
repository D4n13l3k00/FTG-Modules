#   Coded by D4n13l3k00    #
#     t.me/D4n13l3k00      #
# This code under AGPL-3.0 #

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from .. import loader, utils


@loader.tds
class dmt228Mod(loader.Module):
    """Демотиватор 228 @super_rjaka_demotivator_bot"""
    strings = {'name': 'Демотиватор 228'}

    @loader.owner
    async def dmtcmd(self, message):
        """ .dmt [текст по желанию] <reply to video, photo or gif>"""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if not reply:
            return await message.edit("<b>Reply to media</b>")
        try:
            media = reply.media
        except:
            return await message.edit("<b>Only media</b>")
        chat = '@super_rjaka_demotivator_bot'
        await message.edit('<b>Демотивируем...</b>')
        async with message.client.conversation(chat) as conv:
            try:
                response = conv.wait_event(events.NewMessage(
                    incoming=True, from_users=1016409811))
                mm = await message.client.send_file(chat, media, caption=args)
                response = await response
                await mm.delete()
            except YouBlockedUserError:
                return await message.reply('<b>Разблокируй @super_rjaka_demotivator_bot</b>')
            await message.delete()
            await response.delete()
            await message.client.send_file(message.to_id, response.media, reply_to=await message.get_reply_message())
