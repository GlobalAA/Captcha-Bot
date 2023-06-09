import asyncio

from aiogram import types
from random_word import RandomWords

from dispatcher import bot, dp

captchas = {}

@dp.message_handler(content_types=[types.ContentType.NEW_CHAT_MEMBERS, types.ContentType.LEFT_CHAT_MEMBER])
async def start_captcha(message: types.Message):
	await message.delete()

	if message.content_type == types.ContentType.NEW_CHAT_MEMBERS:
		for user in message.new_chat_members:
			captcha_text = generate_captcha()
			captchas[user.id] = captcha_text

			await message.answer(f"{user.first_name}, введите капчу: {captcha_text}")
			await asyncio.sleep(10)
			if user.id in captchas:
				del captchas[user.id]
				await bot.kick_chat_member(message.chat.id, user.id)
				await message.answer(f"{user.first_name}, был исключен за не введенною капчу!")


@dp.message_handler()
async def verify_captcha(message: types.Message):
	if message.from_user.id in captchas:
		if message.text == captchas[message.from_user.id]:
			del captchas[message.from_user.id]
			await message.reply("Капча пройдена! Рады видеть вас, сеньор!")
		else:
			await message.reply("Неверно!")
	

def generate_captcha():
	captcha_text = RandomWords().get_random_word()
	return captcha_text