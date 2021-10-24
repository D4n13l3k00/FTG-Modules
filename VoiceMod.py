#   Coded by D4n13l3k00    #
#     t.me/D4n13l3k00      #
# This code under AGPL-3.0 #

# requires: ffmpeg-python pytgcalls[telethon] youtube-dl

import io
import os
import re

import ffmpeg
import pytgcalls
from youtube_dl import YoutubeDL
from pytgcalls import GroupCallFactory
from pytgcalls.implementation.group_call_file import GroupCallFile
from telethon import types
from typing import *

from .. import loader, utils


@loader.tds
class VoiceMod(loader.Module):
    """Module for working with voicechat"""
    strings = {
        "name": "VoiceMod",
        "downloading": "<b>[VoiceMod]</b> Downloading...",
        "converting": "<b>[VoiceMod]</b> Converting...",
        "playing": "<b>[VoiceMod]</b> Playing...",
        "plsjoin": "<b>[VoiceMod]</b> You are not joined (type .vjoin)",
        "stop": "<b>[VoiceMod]</b> Playing stopped!",
        "join": "<b>[VoiceMod]</b> Joined!",
        "leave": "<b>[VoiceMod]</b> Leaved!",
        "pause": "<b>[VoiceMod]</b> Paused!",
        "resume": "<b>[VoiceMod]</b> Resumed!",
        "mute": "<b>[VoiceMod]</b> Muted!",
        "unmute": "<b>[VoiceMod]</b> Unmuted!",
        "replay": "<b>[VoiceMod]</b> Replaying...",
        "error": "<b>[VoiceMod]</b> Error: <code>{}</code>",
    }
    ytdlopts = {
            'format': 'bestaudio',
            'addmetadata': True,
            'key': 'FFmpegMetadata',
            'writethumbnail': True,
            'prefer_ffmpeg': True,
            'geo_bypass': True,
            'nocheckcertificate': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'outtmpl': 'ytdl_out.mp3',
            'quiet': True,
            'logtostderr': False
        }
    group_calls: Dict[int, GroupCallFile] = {}

    async def get_chat(self, m: types.Message):
        args = utils.get_args_raw(m)
        if not args:
            chat = m.chat.id
        else:
            try:
                chat = int(args)
            except:
                chat = args
            try:
                chat = (await m.client.get_entity(chat)).id
            except Exception as e:
                await utils.answer(m, self.strings('error').format(str(e)))
                return None
        return chat

    def _call(self, m: types.Message, chat: int):
        if str(chat) not in self.group_calls:
            self.group_calls[str(chat)] = GroupCallFactory(
                m.client, pytgcalls.GroupCallFactory.MTPROTO_CLIENT_TYPE.TELETHON).get_file_group_call()

    async def vplaycmd(self, m: types.Message):
        """.vplay [chat (optional)] <link/reply_to_audio>
        Play audio in VC"""
        args = utils.get_args_raw(m)
        r = await m.get_reply_message()
        chat = from_file = link = None
        if args:
            _ = re.match(r'(-?\d+|@[A-Za-z0-9_]{5,})\s+(.*)', args)
            __ = re.match(r'(-?\d+|@[A-Za-z0-9_]{5,})', args)
            if _:
                chat = _.group(1)
                link = _.group(2)
            elif __:
                chat = __.group(1)
            else:
                chat = m.chat.id
                link = args or None
            try:
                chat = int(chat)
            except:
                chat = chat
            try:
                chat = (await m.client.get_entity(chat)).id
            except Exception as e:
                return await utils.answer(m, self.strings('error').format(str(e)))
        else:
            chat = m.chat.id
        if r and r.audio and not link:
            from_file = True
        if not link and (not r or not r.audio):
            return utils.answer(m, 'no audio/link')
        if str(chat) not in self.group_calls:
            return await utils.answer(m, self.strings('plsjoin'))
        self._call(m, chat)
        input_file = f'{chat}.raw'
        m = await utils.answer(m, self.strings('downloading'))
        if from_file:
            audio_original = await r.download_media()
        else:
            try:
                with YoutubeDL(self.ytdlopts) as rip:
                    rip.extract_info(link)
            except Exception as e:
                return await utils.answer(m, self.strings('error').format(str(e)))
            audio_original = 'ytdl_out.mp3'
        m = await utils.answer(m, self.strings('converting'))
        ffmpeg.input(audio_original).output(
            input_file, format='s16le', acodec='pcm_s16le', ac=2, ar='48k'
        ).overwrite_output().run()
        os.remove(audio_original)
        await utils.answer(m, self.strings('playing'))
        self.group_calls[str(chat)].input_filename = input_file

    async def vjoincmd(self, m: types.Message):
        """.vjoin
        Join to the VC"""
        chat = await self.get_chat(m)
        if not chat:
            return
        self._call(m, chat)
        await self.group_calls[str(chat)].start(chat)
        await utils.answer(m, self.strings('join'))

    async def vleavecmd(self, m: types.Message):
        """.vleave
        Leave from the VC"""
        chat = await self.get_chat(m)
        if not chat:
            return
        self._call(m, chat)
        await self.group_calls[str(chat)].stop()
        del self.group_calls[str(chat)]
        try:
            os.remove(f'{chat}.raw')
        except:
            pass
        await utils.answer(m, self.strings('leave'))

    async def vreplaycmd(self, m: types.Message):
        """.vreplay
        Replay audio in VC"""
        chat = await self.get_chat(m)
        if not chat:
            return
        self._call(m, chat)
        self.group_calls[str(chat)].restart_playout()
        await utils.answer(m, self.strings('replay'))

    async def vstopcmd(self, m: types.Message):
        """.vstop
        Stop play in VC"""
        chat = await self.get_chat(m)
        if not chat:
            return
        self._call(m, chat)
        self.group_calls[str(chat)].stop_playout()
        await utils.answer(m, self.strings('stop'))

    async def vmutecmd(self, m: types.Message):
        """.vmute
        Mute player in VC"""
        chat = await self.get_chat(m)
        if not chat:
            return
        self._call(m, chat)
        self.group_calls[str(chat)].set_is_mute(True)
        await utils.answer(m, self.strings('unmute'))

    async def vunmutecmd(self, m: types.Message):
        """.vmute
        Unmute player in VC"""
        chat = await self.get_chat(m)
        if not chat:
            return
        self._call(m, chat)
        self.group_calls[str(chat)].set_is_mute(False)
        await utils.answer(m, self.strings('mute'))

    async def vpausecmd(self, m: types.Message):
        """.vpause
        Pause player in VC"""
        chat = await self.get_chat(m)
        if not chat:
            return
        self._call(m, chat)
        self.group_calls[str(chat)].pause_playout()
        await utils.answer(m, self.strings('pause'))

    async def vresumecmd(self, m: types.Message):
        """.vresume
        Resume player in VC"""
        chat = await self.get_chat(m)
        if not chat:
            return
        self._call(m, chat)
        self.group_calls[str(chat)].resume_playout()
        await utils.answer(m, self.strings('resume'))
    
    async def vdebugcmd(self, m: types.Message):
        await utils.answer(m, f'DEBUG : {str(self.group_calls)}')
