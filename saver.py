#   Coded by D4n13l3k00    #
#     t.me/D4n13l3k00      #
# This code under AGPL-3.0 #
import io

from .. import loader, utils


@loader.tds
class SaverMod(loader.Module):
    strings = {"name": "Saver"}

    async def client_ready(self, client, db):
        self.db = db

    @loader.owner
    async def бляcmd(self, m):
        ".бля <reply> - скачать самоуничтожающееся фото"
        reply = await m.get_reply_message()
        if not reply or not reply.media or not reply.media.ttl_seconds:
            return await m.edit("бля")
        await m.delete()
        new = io.BytesIO(await reply.download_media(bytes))
        new.name = reply.file.name
        await m.client.send_file("me", new)

    @loader.owner
    async def swбляcmd(self, m):
        "Переключить режим автозагрузки фото в лс"
        new_val = not self.db.get("Saver", "state", False)
        self.db.set("Saver", "state", new_val)
        await utils.answer(m, f"<b>[Saver]</b> <pre>{new_val}</pre>")

    async def watcher(self, m):
        if m and m.media and m.media.ttl_seconds and self.db.get("Saver", "state", False):
            new = io.BytesIO(await m.download_media(bytes))
            new.name = m.file.name
            await m.client.send_file("me", new, caption=f"<b>[Saver] Фото от</b> {'@'+m.sender.username if m.sender.username else m.sender.first_name} | <code>{m.sender.id}</code>\nttl_seconds: {m.media.ttl_seconds}")
