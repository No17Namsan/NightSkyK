import asyncio
import discord
import random
import re
import urllib.request
import urllib.parse
from urllib.parse import quote
import json
from datetime import datetime, timedelta

client = discord.Client()

# 봇이 구동되었을 때 동작되는 코드입니다.
@client.event
async def on_ready():
    print("Logged in as ")  # 화면에 봇의 아이디, 닉네임이 출력됩니다.
    print(client.user.name)
    # print(client.user.id)
    print(datetime.now())
    print("===========")

@client.event
async def on_message(message):
    if message.author.bot:  # 만약 메시지를 보낸사람이 봇일 경우에는
        return None  # 동작하지 않고 무시합니다.

    guild = message.author.guild  # id라는 변수에는 메시지를 보낸사람의 ID를 담습니다.
    textchannel = message.channel  # textchannel이라는 변수에는 메시지를 받은 채널의 ID를 담습니다.
    member = message.author
    memberid = message.author.mention
    channel = message.channel.id
    now = datetime.now()


    if message.channel.id==867411166572314624:
        if message.content.startswith('!모집'):
            print(member,guild,now,'!모집')
            print('==========')
            ##EmojiReaction = await textchannel.send(memberid + '님이 레이드 모집중!')
            await message.add_reaction('☑')

        elif message.content.startswith('!까만콩'):  # 인사
            print(member, guild, now, channel, '!까만콩')
            print('==========')
            await textchannel.send(embed=discord.Embed(title='Ver.1.0.0',
                                                   description='파티 모집용 디스코드 봇입니다.\n'
                                                               '모집 채널에서의 모든 잡담은 자동으로 제거합니다.\n'
                                                               '\'!모집 (원하는 활동)\'만 남깁니다.'
                                                               '까만콩은 위험하지 않아요 ._.',
                                                   colour=0xe3da13))

        else:
            print(member, guild, now, '잡담제거')
            print('==========')
            await message.delete()


client.run("Discord_API")
