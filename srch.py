#   Coded by D4n13l3k00    #
#     t.me/D4n13l3k00      #
# This code under AGPL-3.0 #

from .. import loader, utils


def register(cb):
    cb(SearcherMod())


class SearcherMod(loader.Module):
    strings = {'name': 'Searcher'}

    def __init__(self):
        self.name = self.strings['name']

    async def srchcmd(self, m):
        """.srch <канал/чат> <запрос>
        Найти пост в канале/чате сообщение и переслать
        """
        args = utils.get_args_raw(m)
        if not args:
            return await m.edit("[Search] Укажите аргументы!")
        if len(args.split(" ")) == 1:
            return await m.edit("[Search] Укажите запрос!")
        ch = args.split(" ")[0]
        req = args.split(" ", 1)[1]
        try:
            ms = await m.client.get_messages(ch, search=req, limit=100)
        except Exception as e:
            return await m.edit("[Searcher] " + str(e.args))
        if ms.total == 0:
            return await m.edit("[Searcher] Данных по запросу нет")
        for i in ms:
            await i.forward_to(m.to_id)
        await m.delete()
