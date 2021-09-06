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
    print(client.user.id)
    print(datetime.now())
    print("===========")


# 봇이 새로운 메시지를 수신했을때 동작되는 코드입니다.
@client.event
async def on_message(message):
    if message.author.bot:  # 만약 메시지를 보낸사람이 봇일 경우에는
        return None  # 동작하지 않고 무시합니다.

    dice = ['<:d1:683941256711241744>', '<:d2:683941257000910869>', '<:d3:683941256606253068>',
            '<:d4:683941256937734203>', '<:d5:683941256862105620>', '<:d6:683941256891858964>']
    food = ['워..... 워.... 네 체중을 생각해!', '너구리 순한맛! (그후 봇을 볼 수 없었다고 한다)', '굶어ㅋㅋ', '피자사주세요!', '오늘은 치느님을 영접할 시간입니다!',
            '갓스터치가 있는데 버거킹이 없을리가 없잖아! 버거킹?',
            '밥버거', '집밥이 최고!', '빵야! 빵야! 빵!', '루나랑 라면먹고 가실래요?',
            '수르스트뢰밍 https://namu.wiki/w/%EC%88%98%EB%A5%B4%EC%8A%A4%ED%8A%B8%EB%A2%B0%EB%B0%8D',
            '진리 콩 까네~ 진리 콩 까네~ 칠리 콘 카르네~', '김밥말아서 소풍가요!', '스시....? 라고 불리는 초밥!',
            '이봐, 친구! 그거 알아? 레몬 한 개엔 자그마치 레몬 한 개 분량의 비타민 C가 있다는 놀라운 사실을!', '일단 3D안경을 쓰고..:popcorn:',
            '부어라! 마셔라! 죽어라! :beer:', '도넛!',
            '커피는 좋은 도핑제입니다.', '넌... 아직... 준비가... 안되었다..!:baby_bottle: ', '후헤헤헷 숙제(일)을 머거랑 헤헷', '까까먹어', '빵과 계란후라이!',
            ':pig2: 족발! 돼지고기! 보쌈!', ':fish: 회?', '술에 부대찌개먹고싶... 아니 부대찌개에 술마시고싶다.', '어제도 오늘도 내일도 마라탕. 당연한거잖아요?',
            '떡뽀끼? 떡뽁이? 알게뭐람, 떡볶이 주세요!', '버거킹이 있는데 갓스터치가 없을리가 없잖아! 갓스터치!', '워워... 진정해..! 빡친 당신을 위한 엽떡을 가져왔다구!',
            '발은 역시 닭발이지!:chicken:', '말해 뭐해 곱창이 최고 아니야?', '삶은 감자.... Life is Egg... Egg...?', '아야어여오요**우유** :milk:',
            '쌀국수 뚝배기!', '아... 시리얼에 우유부어먹고싶다... ... ...?', '풀리와 웰시가 맛나게 먹는 밀웜 한번 먹어보실?', '민트초코가 치약맛일까 치약이 민트초코맛일까?']
    do = ['잠만보처럼 잠만 자던가! :zzz:', '톰 아저씨의 무지개 여섯 공성할래?', '데스티니 가디언즈는 죽었지만 우리 케이드는 마음 속에 살아있어!',
          '생존마 낚으러 희생제갈까나~ 살인마 괴롭히러 희생제갈까나~',
          'WINNER WINNER CHICKEN DINNER!', '느껴지지않아..? 우리의 심장에 뛰고있는 이 뜨거운 :cy:가!', '역시 힐링은 마인크래프트', '나만 없어 모동숲...ㅠ',
          '오늘도 싱글벙글 롤 협곡생활!',
          '우리집에서 넷플릭스보고갈래?(으브븝)', '밥머겅 많이머겅', '저 오늘떠나요~ 공항으로~ :airplane:', 'TFT 모바일 ㄷㄷㄷㅈ, ㅇㅍㄷㄷ', '타르코프에서 도망쳐! 도망치라구!']
    fates = [':spades:', ':clubs:', ':diamonds:', ':hearts:']
    fatecall = ['!합기', '!gkqrl', '!GKQRL']
    num = [':regional_indicator_a:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:',
           ':keycap_ten:', ':regional_indicator_j:', ':regional_indicator_q:', ':regional_indicator_k:']
    result = []
    eat = ['!뭐먹지', '!뭐먹지?', '!머먹지?', '!머먹지', '!멀먹징?', '!멀먹징', '!뭐먹징?', '!뭐먹징', '!뭐먹제?', '!뭐먹지?', '!뭐먹']
    doing = ['!뭐하지?', '!뭐하지', '!뭐할까?', '!뭐할까']
    up = ['!업', '!djq', '!DJQ', '!up', '!UP']
    meow = ['애옹', '야옹', '먀옹', 'meow', 'moew', '냐오', '냐옹', '냥', '미야옹', '마오', '앩옹', '이얏호응', '애-옹', '야-옹']
    meowe = ['<:meow1:682071155943014415>', '<:meow2:682071408540647563>', '<:meow3:684983336178810888>',
             '<:meow4:684983336824733697>', '<:meow5:684984172963692545>']

    blackcow = ['음머', '살고시퍼여ㅠㅠㅠ', '음머어어어어어엉']

    guild = message.author.guild  # id라는 변수에는 메시지를 보낸사람의 ID를 담습니다.
    textchannel = message.channel  # textchannel이라는 변수에는 메시지를 받은 채널의 ID를 담습니다.
    member = message.author
    now = datetime.now()

    if message.content == ('!패치노트'):
        print(member, guild, now, '!패치노트')
        print('==========')
        await textchannel.send(embed=discord.Embed(title='Ver.1.0.3a',
                                                   description='0.재구동 시작했습니다.\n',
                                                   colour=0xe3da13))

    if message.content == ("!도움말"):
        print(member, now, guild, '!도움말')
        print('==========')
        await textchannel.send(embed=discord.Embed(title='도움말',
                                                   description='1. !루나리스: 봇이 인사를 합니다.\n2. !뭐먹지?, !머먹지?, !멀먹징?, !뭐먹징?, !뭐먹제?: 봇이 음식을 추천합니다.\n3. 야옹, 애옹, 냥 등등: 고양이 이모지를 가져옵니다!\n'
                                                               '4. !n(dDㅇ)N: N면체 주사위를 n개 던집니다. (N=1~6,n=1~9)',
                                                   colour=0xe3da13))

    if message.content.startswith('!루나리스'):  # 인사
        print(member, guild, now, '!루나리스')
        print('==========')
        await textchannel.send('안녕하세요. 여러분!')
        return None

    if message.content in doing:
        print(member, guild, now, '!뭐하지?')
        print('==========')
        await textchannel.send(do[random.randint(0, len(do) - 1)])

    if message.content in eat:
        print(member, guild, now, '!뭐먹지?')
        print('==========')
        await textchannel.send(food[random.randint(0, len(food) - 1)])

    if message.content in meow:
        print(member, guild, now, '야옹')
        print('==========')
        await textchannel.send(meowe[random.randint(0, len(meowe) - 1)])

    if message.content.startswith("!갈고리"):
        print(member, guild, now, '!갈고리')
        print('==========')
        await textchannel.send(
            '<:QuestionSpam:767992761491259443><:QuestionSpam:767992761491259443><:QuestionSpam:767992761491259443><:QuestionSpam:767992761491259443><:QuestionSpam:767992761491259443>')

    if message.content == ("!나스"):
        print(member, guild, now, '!나스')
        print('==========')
        await textchannel.send("<:NBSB:766596746762649621> sp? 잠깐만요. 아니, 잠깐만 sp?")

    if message.content == ("!나스바보"):
        print(member, guild, now, '!나스바보')
        print('==========')
        await textchannel.send(
            "<:NBSB:766596746762649621> ㄴ <:UnIm:684328036065476613> ㄱ <:NBSB:766596746762649621>")

    if message.content == ("!나바스보"):
        print(member, guild, now, '!나바스보')
        print('==========')
        await textchannel.send(
            "<:NBSB:766596746762649621><:NBSB:766596746762649621>\n<:NBSB:766596746762649621><:NBSB:766596746762649621>")

    if message.content.startswith("!멜라"):
        print(member, guild, now, '!멜라')
        print('==========')
        await textchannel.send('<:D2Ghost:685817640366768174> **현실**을 사세요, 수호자!!')

    if message.content.startswith("!흑우"):
        print(member, guild, now, '!흑우')
        print('==========')
        await textchannel.send(blackcow[random.randint(0, len(blackcow) - 1)])

    if message.content.startswith("!힐카"):
        print(member, guild, now, '!힐카')
        print('==========')
        await textchannel.send('힐카는 힝해')

    dice_set = re.findall('^!([0-9]+)[dDㅇ]([1-6])$', message.content)
    if len(dice_set) != 0:
        dice_set = dice_set[0]
        for _ in range(int(dice_set[0])):
            result.append(dice[random.randint(0, int(dice_set[1]) - 1)])
        print(member, now, guild, '!주사위', result)
        print('==========')
        await textchannel.send(result)

    # if message.content in fatecall:
    #   result = (fates[random.randint(0, 3)]), (num[random.randint(0, 12)])
    #  print(member, guild, now, '!합기', result)
    # print('==========')
    # await textchannel.send(result)

    # if message.content in up:
    #   result = (dice[random.randint(0, 5)])
    #  print(member, guild, now, '!업', result)
    # print('==========')
    # await textchannel.send(result)

    if message.content.startswith("!이스포츠"):
        print(member, guild, now, '!이스포츠')
        print('==========')
        await textchannel.send(embed=discord.Embed(title='이스포츠 일정 정리 21년 07월 4주차'
                                                   , colour=0xe3da13))


client.run("Discord_API")
