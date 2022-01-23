#   Coded by D4n13l3k00    #
#     t.me/D4n13l3k00      #
# This code under AGPL-3.0 #

# requires: pornhub-api

from random import choice

from pornhub_api import PornhubApi

from .. import loader, utils


@loader.tds
class PhSrchMod(loader.Module):
    strings = {"name": "PornHub"}

    @loader.owner
    async def sphcmd(self, m):
        "Найти видео на pornhub"
        args = utils.get_args_raw(m)
        if args:
            srch = args
        else:
            return await m.delete()
        api = PornhubApi()
        data = api.search.search(
            srch,
            ordering="mostviewed"
        )
        video = choice(data.videos)
        await m.edit(f"<b>Нашёл кое-что по запросу</b> <code>{srch}</code>: <a href=\"{video.url}\">{video.title}</a>")
