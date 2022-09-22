import asyncio
from io import BytesIO
from pyrogram.types import Message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import MessageNotModified
from HOKAGE import aiohttpsession as aiosession
from HOKAGE import pgram
from pyrogram import Client, filters
from HOKAGE.utils.errors import capture_err



REPO_TEXT = """
❂ ʜᴏᴋᴀɢᴇ ɪs ᴀɴ ᴀɴɪᴍᴇ ᴄʜᴀʀᴀᴄᴛᴇʀ ғʀᴏᴍ ᴄʜᴀɪɴsᴀᴡ ᴍᴀɴ ᴀɴɪᴍᴇ.

❂ ᴡᴇ ᴍᴀᴅᴇ ᴛʜɪs ʜᴏᴋᴀɢᴇ  ʙᴇᴄᴀᴜsᴇ ᴀʟʀᴇᴀᴅʏ ᴀ ʜᴏᴋᴀɢᴇ ᴏɴ ᴛᴇʟᴇɢʀᴀᴍ ɪs ᴀʟʀᴇᴀᴅʏ ᴘᴏᴘᴜʟᴀʀ ᴀɴᴅ sʜᴇ ɪs ᴏɴᴇ ᴏғ ᴛʜᴇ ʙᴇsᴛ ᴀɴɪᴍᴇ ᴛʜᴇᴍᴇᴅ ᴛᴇʟᴇɢʀᴀᴍ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ ᴛʜᴏᴜɢʜ ʜᴇʀ ʀᴇᴘᴏ ɪs ɴᴏᴛ ᴘᴜʙʟɪᴄ sᴏ ᴀɴʏᴏɴᴇ ᴄᴀɴ'ᴛ ᴍᴀᴋᴇ ᴏᴡɴ ʜᴏᴋᴀɢᴇ ᴀɴᴅ ᴅᴇᴘʟᴏʏ ɪᴛ.

❂ sᴏ ᴡᴇ ᴛʜᴏᴜɢʜᴛ ʟᴇᴛs ɢɪᴠᴇ ɪᴛ ᴀ ᴛʀʏ ᴀɴᴅ ᴍᴀᴋᴇ ᴏᴡɴ ʜᴏᴋᴀɢᴇ ᴀɴᴅ ᴡᴇ ᴋɴᴏᴡ ᴛʜᴀᴛ ᴡᴇ ᴀʀᴇ ɴᴏᴛ sᴜᴄᴄᴇssғᴜʟʟ ɪɴ ᴄᴏᴘʏɪɴɢ ᴛʜᴇ ᴏʀɪɢɪɴᴀʟ ɢᴏᴅᴅᴇss ʜᴏᴋᴀɢᴇ ʙᴜᴛ ᴡᴇ ᴀᴛʟᴇᴀsᴛ ɢɪᴠᴇ ɪᴛ ᴀ ᴛʀʏ
ᴀɴᴅ ʜᴏᴋᴀɢᴇ ʀᴇᴘᴏ ɪs ɴᴏᴡ ᴘᴜʙʟɪᴄ ʙʏ ᴄʟɪᴄᴋɪɴɢ ᴏɴ ᴛʜᴇ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ ʏᴏᴜ ᴄᴀɴ ᴅᴇᴘʟᴏʏ ʏᴏᴜʀ ᴏᴡɴ ʜᴏᴋᴀɢᴇ.

⚠️ ɴᴏᴛᴇ :- 2.0 ɪs ɪɴ ᴘʀᴏᴄᴇss ᴡᴇ ᴡɪʟʟ ʀᴇʟᴇᴀsᴇ ɪᴛ sᴏᴏɴ ʙᴜᴛ ʜᴏᴋᴀɢᴇ 2.0 ʀᴇᴘᴏ ᴡɪʟʟ ʙᴇ ᴘʀɪᴠᴀᴛᴇ sᴏ ɪғ ᴡᴀɴᴛ ᴛᴏ ʙᴜʏ ᴛʜᴀᴛ ʀᴇᴘᴏ ᴛʜᴀɴ ʏᴏᴜ ᴄᴀɴ ᴄᴏɴᴛᴀᴄᴛ.
"""

async def make_carbon(code):
    url = "https://carbonara.vercel.app/api/cook"
    async with aiosession.post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "carbon.png"
    return image


@pgram.on_message(filters.command("carbon"))
@capture_err
async def carbon_func(_, message):
    if not message.reply_to_message:
        return await message.reply_text("`ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴇxᴛ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ᴄᴀʀʙᴏɴ`")
    if not message.reply_to_message.text:
        return await message.reply_text("`ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴇxᴛ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ᴄᴀʀʙᴏɴ`")
    m = await message.reply_text("`ɢᴇɴᴇʀᴀᴛɪɴɢ ᴄᴀʀʙᴏɴ...`")
    carbon = await make_carbon(message.reply_to_message.text)
    await m.edit("`waitoo...`")
    await pgram.send_photo(message.chat.id, carbon)
    await m.delete()
    carbon.close()



@pgram.on_message(filters.command("repo"))
@capture_err
async def help(client: Client, message: Message):
    get_me = await client.get_me()
    self.username = get_me.username
    buttons =  [
           [
        InlineKeyboardButton(text="🐙 ʀᴇᴘᴏsɪᴛᴏʀʏ", url="https://github.com/Sumit9969/HokageRobot"),
        InlineKeyboardButton(
            text="🎓 ᴅᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/Mr_DiSasTer_XD"
        ),
    ],
    [
        InlineKeyboardButton(text="⛽ sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/TechQuardSupport"),
        InlineKeyboardButton(
            text="📣 ᴜᴘᴅᴀᴛᴇs", url=f"https://t.me/TechQuard"
        ),
    ],
           ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_photo(photo=f"https://te.legra.ph/file/501c5315150b4f27daf9f.mp4", caption=f"{REPO_TEXT}", reply_markup=reply_markup)


__mod_name__ = "𝙲ᴀʀʙᴏɴ"

__help__ = """

/carbon *:* ᴍᴀᴋᴇs ᴄᴀʀʙᴏɴ ғᴏʀ ʀᴇᴘʟɪᴇᴅ ᴛᴇxᴛ
/repo *:*🌟
 """
