# .------.------.------.------.------.------.------.------.------.------.
# |D.--. |4.--. |N.--. |1.--. |3.--. |L.--. |3.--. |K.--. |0.--. |0.--. |
# | :/\: | :/\: | :(): | :/\: | :(): | :/\: | :(): | :/\: | :/\: | :/\: |
# | (__) | :\/: | ()() | (__) | ()() | (__) | ()() | :\/: | :\/: | :\/: |
# | '--'D| '--'4| '--'N| '--'1| '--'3| '--'L| '--'3| '--'K| '--'0| '--'0|
# `------`------`------`------`------`------`------`------`------`------'
#
#                     Copyright 2022 t.me/D4n13l3k00
#           Licensed under the Creative Commons CC BY-NC-ND 4.0
#
#                    Full license text can be found at:
#       https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode
#
#                           Human-friendly one:
#            https://creativecommons.org/licenses/by-nc-nd/4.0

# meta developer: @D4n13l3k00

# require httpx

import json

import httpx
from telethon import types

from .. import loader, utils


@loader.tds
class OpenAIGPTMod(loader.Module):
    "OpenAI GPT"
    strings = {
        "name": "GPT",
        "pref": "<b>[GPT]</b> {}",
        "result": "<b>Result:</b> {text}\n\n"
        "<b>Used tokens:</b> {prompt_tokens}+{completion_tokens}={total_tokens}",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            *("MODEL", "text-davinci-003", "Model name"),
            *(
                "COMPLETION_ENDPOINT",
                "https://api.openai.com/v1/completions",
                "Completions API endpoint",
            ),
            *("MAX_TOKENS", 512, "Completions API endpoint"),
            *("TEMPERATURE", 0.7, "Completions API endpoint"),
            *("DEBUG", False, "Debug mode for answers"),
        )

    async def client_ready(self, _, db):
        self._db = db
        self._db_name = "OpenAI_GPT"

    @loader.owner
    async def setgptcmd(self, m: types.Message):
        "<token> - set OpenAI access Token"
        token: str or None = utils.get_args_raw(m)
        if not token:
            return await utils.answer(m, self.strings("pref", m).format("No token"))
        self._db.set(self._db_name, "token", token)
        await utils.answer(m, self.strings("pref", m).format("Token set"))

    @loader.owner
    async def gptcmd(self, m: types.Message):
        "<text/reply_to_text> - generate text"
        text = utils.get_args_raw(m)
        reply = await m.get_reply_message()
        if reply:
            text = text or reply.raw_text

        if not text:
            return await utils.answer(m, self.strings("pref", m).format("No text"))

        m = await utils.answer(m, self.strings("pref", m).format("Generating..."))
        async with httpx.AsyncClient(timeout=300) as client:
            response = await client.post(
                self.config["COMPLETION_ENDPOINT"],
                headers={
                    "Authorization": f"Bearer {self._db.get(self._db_name, 'token')}",
                },
                json={
                    "model": self.config["MODEL"],
                    "prompt": text,
                    "max_tokens": self.config["MAX_TOKENS"],
                    "temperature": self.config["TEMPERATURE"],
                },
            )
            if response.status_code != 200:
                if self.config["DEBUG"]:
                    return await utils.answer(
                        m, "<code>{}</code>".format(str(json.dumps(j, indent=2)))
                    )
                return await utils.answer(
                    m,
                    self.strings("pref", m).format(
                        f"<b>Error:</b> {response.status_code} {response.reason_phrase}"
                    ),
                )
            j = response.json()
            if self.config["DEBUG"]:
                return await utils.answer(
                    m, "<code>{}</code>".format(str(json.dumps(j, indent=2)))
                )
            text = j["choices"][0]["text"].strip("\n").strip(" ")
            if j["choices"][0]["finish_reason"] == "length":
                text += "\n<code>TOKEN_LIMIT. Use .config to change them.</code>"
            await utils.answer(
                m,
                self.strings("pref", m).format(
                    self.strings("result", m).format(text=text, **j["usage"])
                ),
            )
