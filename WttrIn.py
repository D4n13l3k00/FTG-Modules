#   Coded by D4n13l3k00    #
#     t.me/D4n13l3k00      #
# This code under AGPL-3.0 #

import aiohttp

from .. import loader, utils


@loader.tds
class WttrInMod(loader.Module):
    """WttrIn"""
    strings = {'name': 'WttrIn'}

    @loader.owner
    async def wthrcmd(self, m):
        """.wthr <Город если надо>
        Получить текущую погоду
        """
        rr = utils.get_args_raw(m)
        
        await m.edit("<code>{}</code>".format(await (await aiohttp.ClientSession().get(f"https://wttr.in/{rr if rr != None else ''}?0Tq&lang=ru")).text()))
