# .------.------.------.------.------.------.------.------.------.------.
# |D.--. |4.--. |N.--. |1.--. |3.--. |L.--. |3.--. |K.--. |0.--. |0.--. |
# | :/\: | :/\: | :(): | :/\: | :(): | :/\: | :(): | :/\: | :/\: | :/\: |
# | (__) | :\/: | ()() | (__) | ()() | (__) | ()() | :\/: | :\/: | :\/: |
# | '--'D| '--'4| '--'N| '--'1| '--'3| '--'L| '--'3| '--'K| '--'0| '--'0|
# `------`------`------`------`------`------`------`------`------`------'
#
#                     Copyright 2023 t.me/D4n13l3k00
#           Licensed under the Creative Commons CC BY-NC-ND 4.0
#
#                    Full license text can be found at:
#       https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode
#
#                           Human-friendly one:
#            https://creativecommons.org/licenses/by-nc-nd/4.0

# meta developer: @D4n13l3k00

import os

from .. import loader  # type: ignore


@loader.tds
class TesseractMod(loader.Module):
    strings = {"name": "Tesseract"}

    @loader.owner
    async def ocrcmd(self, m):
        "Распознать текст с картинки"
        reply = await m.get_reply_message()
        if not reply:
            return await m.edit("[OCR] Реплай на пикчу")
        await m.edit("[OCR] Распознаём")
        file = await reply.download_media()
        rec = os.popen(f"tesseract -l rus+eng {file} stdout").read()
        await m.edit(
            "[OCR]\n" + (("<code>" + rec + "</code>") if rec != "" else "НЕ_РАСПОЗНАНО")
        )
        os.remove(file)
