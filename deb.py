#   Coded by D4n13l3k00    #
#     t.me/D4n13l3k00      #
# This code under AGPL-3.0 #

from .. import loader
from PIL import Image
from requests import get
import io


@loader.tds
class DebMod(loader.Module):
    "Дэб"
    strings = {"name": "Дэб"}

    @loader.owner
    async def debcmd(self, m):
        "Дэб"
        reply = await m.get_reply_message()
        image = await get_img_from_msg(reply)
        if not image:
            await m.edit("не дэб...")
            return
        await m.edit("Дэб'им...")
        deb = Image.open(io.BytesIO(get("https://x0.at/Evn.png").content))
        img = Image.open(image)
        deb.thumbnail((img.width//3, img.height//3))
        img.paste(deb, (0, img.height-deb.height), deb)
        out = io.BytesIO()
        iswebp = reply.file.ext == ".webp"
        out.name = "дэб." + ("webp" if iswebp else "png")
        img.save(out)
        out.seek(0)
        await reply.reply(file=out)
        await m.delete()


async def get_img_from_msg(reply):
    if reply and reply.file and reply.file.mime_type != "image":
        return io.BytesIO(await reply.download_media(bytes))
    else:
        return None
