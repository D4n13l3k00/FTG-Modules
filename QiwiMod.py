"""
.------.------.------.------.------.------.------.------.------.------.
|D.--. |4.--. |N.--. |1.--. |3.--. |L.--. |3.--. |K.--. |0.--. |0.--. |
| :/\: | :/\: | :(): | :/\: | :(): | :/\: | :(): | :/\: | :/\: | :/\: |
| (__) | :\/: | ()() | (__) | ()() | (__) | ()() | :\/: | :\/: | :\/: |
| '--'D| '--'4| '--'N| '--'1| '--'3| '--'L| '--'3| '--'K| '--'0| '--'0|
`------`------`------`------`------`------`------`------`------`------'

                    Copyright 2022 t.me/D4n13l3k00                     
          Licensed under the Creative Commons CC BY-NC-ND 4.0          
  
                   Full license text can be found at:                  
      https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode      
    
                          Human-friendly one:                          
           https://creativecommons.org/licenses/by-nc-nd/4.0           
"""
# meta developer: @D4n13l3k00


# requires: glQiwiApi pycryptodome

import asyncio
import hashlib

from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
from glQiwiApi import QiwiWrapper
from telethon import types

from .. import loader, utils


@loader.tds
class QiwiMod(loader.Module):
    "Модуль для работы с Qiwi кошельком"

    strings = {
        "name": "Qiwi",
        "pref": "<b>[Qiwi]</b> ",
        "need_arg": "{}need args...",
        "phone_setted_successfully": "{}Номер и токен установлены!",
        "p2p_setted_successfully": "{}Секретный P2P токен установлен!",
        "bal": "{}Баланс: {}",
        "commission": "{}Итоговая сумма: {}\nКомиссия Qiwi: {}\nСумма к зачислению: {}",
        "sent": "{}Средства отправлены!\nID: <code>{}</code>",
        "bill_created": "{}Счёт создан!\n{}\nСтатус счёта: <code>{}</code>",
        "bill_payed": "Оплачен",
        "bill_notpayed": "Не оплачен",
        "bill_disabled": "Автопроверка отключена после 5 минут",
        "bill_link_exp": "Ссылка истекла по причине оплаты",
    }
    _db = "QiwiMod"

    async def client_ready(self, _, db):
        self.db = db
        self.me = await _.get_me()

    def __pad(self, text: bytes):
        return text[:8] if len(text) > 8 else text

    def __get_enc(self, key: str) -> str:
        c = DES.new(
            self.__pad(
                hashlib.md5((self.me.phone + str(self.me.id)).encode("utf-8"))
                .hexdigest()
                .encode("utf-8")
            ),
            DES.MODE_ECB,
        )
        return unpad(c.decrypt(self.db.get(self._db, key, b"")), 8).decode("utf-8")

    def __set_enc(self, key: str, value: str):
        c = DES.new(
            self.__pad(
                hashlib.md5((self.me.phone + str(self.me.id)).encode("utf-8"))
                .hexdigest()
                .encode("utf-8")
            ),
            DES.MODE_ECB,
        )
        self.db.set(self._db, key, c.encrypt(pad(value.encode("utf-8"), 8)))

    async def qsetp2pcmd(self, m: types.Message):
        """.qsetp2p <TOKEN>
        Установить секретный p2p ключ"""
        args = utils.get_args(m)
        if args:
            self.__set_enc("p2p", args[0])
            return await utils.answer(
                m, self.strings("p2p_setted_successfully").format(self.strings("pref"))
            )
        await utils.answer(m, self.strings("need_arg").format(self.strings("pref")))

    async def qsetcmd(self, m: types.Message):
        """.qset <phone> <TOKEN>
        Установить номер и токен"""
        args = utils.get_args(m)
        if args:
            self.__set_enc("phone", args[0])
            self.__set_enc("token", args[1])
            return await utils.answer(
                m,
                self.strings("phone_setted_successfully").format(self.strings("pref")),
            )
        await utils.answer(m, self.strings("need_arg").format(self.strings("pref")))

    async def qbalcmd(self, m: types.Message):
        ".qbal - Получить баланс"
        async with QiwiWrapper(self.__get_enc("token"), self.__get_enc("phone")) as w:
            w: QiwiWrapper
            bal = await w.get_balance()
            await utils.answer(
                m,
                self.strings("bal").format(
                    self.strings("pref"), str(bal.amount) + bal.currency.symbol
                ),
            )

    async def qswalcmd(self, m: types.Message):
        ".qswal <phone> <amount> <?comment> - Отправить средства по номеру"
        async with QiwiWrapper(self.__get_enc("token"), self.__get_enc("phone")) as w:
            w: QiwiWrapper
            args = utils.get_args(m)
            args_raw = utils.get_args_raw(m)
            trans_id = await w.to_wallet(
                to_number=args[0],
                amount=int(args[1]),
                comment=args_raw.split(args[1])[1].strip() if len(args) > 2 else None,
            )
            await utils.answer(
                m,
                self.strings("sent").format(
                    self.strings("pref"), str(trans_id.payment_id)
                ),
            )

    async def qscardcmd(self, m: types.Message):
        ".qscard <card_num[no_spaces]> <amount> - Отправить средства на карту"
        async with QiwiWrapper(self.__get_enc("token"), self.__get_enc("phone")) as w:
            w: QiwiWrapper
            args = utils.get_args(m)
            trans_id = await w.to_card(
                to_card=args[0],
                trans_sum=float(args[1]),
            )
            await utils.answer(
                m,
                self.strings("sent").format(
                    self.strings("pref"), str(trans_id.payment_id)
                ),
            )

    async def qcmscmd(self, m: types.Message):
        ".qcms <card_num/phone> <amount> - Посчитать комиссию"
        async with QiwiWrapper(self.__get_enc("token"), self.__get_enc("phone")) as w:
            w: QiwiWrapper
            args = utils.get_args(m)
            commission = await w.calc_commission(args[0], float(args[1]))
            await utils.answer(
                m,
                self.strings("commission").format(
                    self.strings("pref"),
                    str(commission.withdraw_sum.amount)
                    + commission.withdraw_sum.currency.symbol,
                    str(commission.qiwi_commission.amount)
                    + commission.qiwi_commission.currency.symbol,
                    str(commission.enrollment_sum.amount)
                    + commission.enrollment_sum.currency.symbol,
                ),
            )

    async def qp2pcmd(self, m: types.Message):
        ".qp2p <amount> <?comment> - Создать счёт для оплаты"
        async with QiwiWrapper(secret_p2p=self.__get_enc("p2p")) as w:
            w: QiwiWrapper
            args = utils.get_args(m)
            args_raw = utils.get_args_raw(m)
            bill = await w.create_p2p_bill(
                amount=args[0],
                comment=args_raw.split(args[0])[1].strip() if len(args) > 1 else None,
            )
            last_status = None
            url = bill.pay_url
            n = 0
            while True:
                if n >= 72:
                    await utils.answer(
                        m,
                        self.strings("bill_created").format(
                            self.strings("pref"),
                            self.strings("bill_link_exp"),
                            self.strings("bill_disabled"),
                        ),
                    )
                    break
                status = await bill.check()
                if status != last_status:
                    last_status = status
                    await utils.answer(
                        m,
                        self.strings("bill_created").format(
                            self.strings("pref"),
                            url,
                            self.strings("bill_payed" if status else "bill_notpayed"),
                        ),
                    )
                    if status:
                        break
                n += 1
                await asyncio.sleep(5)
