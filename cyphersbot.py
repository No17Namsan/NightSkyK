#!/usr/bin/env python3

# cyphersbot.py by.NightSkyK A.K.A MoonSeong Kang

# Library
import asyncio
import discord
import urllib.request
import urllib.parse
from urllib.parse import quote
import json
from datetime import datetime
import random

#client_set
client = discord.Client()
cy_client_id = "A2kZ1re2e0i8a6ge6qAg4CjkYPUMHimq"

#embed setting_Footer&thumbnail
def embed_default(embed):
    embedsetting = embed
    embedsetting.set_footer(text='문의사항은 NightSkyK#0117로 DM주세요.')
    embedsetting.set_thumbnail(
        url="http://pub.cyphers.co.kr/images3/art/2021/06/02/1622596975918.png")

#Data Request
def data_request(url):
    req = urllib.request.Request(url)
    req.add_header("Cyphers-ID", cy_client_id)
    response = urllib.request.urlopen(req)
    response_body = response.read()
    return json.loads(response_body)

#position emoji dictionary
POSITION = {'원거리딜러': '🔫', '근거리딜러': '👊', '탱커': '🛡️', '서포터': '⭐'}

#Default Color
DEFAULT_COLOR = 0xcc9911

@client.event #client Ready
async def on_ready():
        print("Logged in as ") #화면에 봇의 이름, 아이디, 닉네임이 출력됩니다.
        print(client.user.name)
        print(client.user.id)
        print(datetime.now())
        print("===========")
        await client.change_presence(activity=discord.Game(name='Cyphers'))

@client.event #client Active
async def on_message(message):
        if message.author.bot:  # 만약 메시지를 보낸사람이 봇일 경우에는
            return None  # 동작하지 않고 무시합니다.

        guild = message.author.guild
        member = message.author         #메세지를 보낸 사람
        now = datetime.now()            #메세지를 보낸 시각
        textchannel = message.channel   #메세지를 보낸 채널

        if message.content == ("!패치노트"): #PatchNote
            embed = discord.Embed(
                title='V0.0.3B',
                color=DEFAULT_COLOR
            )
            embed_default(embed)
            embed.add_field(name='1.랜덤 선택 기능이 추가되었습니다!',
                            value='```**!랜덤 (1~5까지의 정수)**을 이용하시면 현재 사용 가능한 모든 캐릭터중 원하는 만큼 선택해줍니다.```',
                            inline=False)
            embed.add_field(name='2.전적 검색 결과가 개선되었습니다!',
                            value='```포지션 정보가 캐릭터 레벨 옆에 표시됩니다!```',
                            inline=False)

            print(member, guild, now, '!패치노트')
            print('==========')

            await textchannel.send(embed=embed)

        if message.content == ("!도움말"):  # Help
            embed = discord.Embed(
                title='도움말입니다.',
                color=DEFAULT_COLOR
            )
            embed_default(embed)
            embed.add_field(name='!전적 (이름) (공식, 일반)',
                            value='```최근 6게임의 게임 결과를 불러옵니다.```',inline=False)
            embed.add_field(name='!랜덤',
                            value='```현재 이용 가능한 캐릭터 중 하나를 무작위로 선택합니다.```',inline=False)
            print(member, guild, now, '!도움말')
            print('==========')
            await textchannel.send(embed=embed)

        if message.content.startswith("!전적"):   #Games Result Searching
                msg = message.content.split(" ")

                if len(msg) != 3:           #Case 1 3단어 이상 검색
                        if msg[1]=='도움말':   #Case 1 도움말
                                print(member, guild, now, '!전적 도움말')
                                print('==========')
                                embed = discord.Embed(
                                    title='사용법: !전적 (이름) (공식,일반) ',
                                    description='```이름: 사이퍼즈 인게임 닉네임을 적어주세요.\n공식, 일반: 조회하고 싶은 종류를 적어주세요.\n\n총 6개의 게임을 출력합니다.```',
                                    colour=DEFAULT_COLOR)
                                embed_default(embed)
                                await textchannel.send(embed=embed)

                        else:               #Another Case 도움말 이외의 전체
                                print(member, guild, now, '!전적', 'Error Code: Bad Order')
                                print('==========')
                                embed = discord.Embed(title='오류!',
                                                      description='```명령어를 제대로 작성했는지 확인해주세요.\n 주로 이 오류는 닉네임에 공백이 포함되었거나 일반과 공식을 입력하지 않았을때 출력됩니다.\n도움이 필요하시다면 \'!전적 도움말\'을 이용해주세요.```'
                                                      , colour=DEFAULT_COLOR)
                                embed_default(embed)
                                await  textchannel.send(embed=embed)

                elif msg[2] == '공식'or msg[2]=='일반': #Case 2 공식, 일반 전적 검색
                        if msg[2]=='공식':
                                gameTypeId='rating'
                        else:
                                gameTypeId='normal'

                        url = ("https://api.neople.co.kr/cy/players?nickname=" + msg[1] + "&wordType=match&apikey="+cy_client_id)
                        req = urllib.request.Request(url)
                        req.add_header("Cyphers-ID", cy_client_id)

                        try:
                                response = urllib.request.urlopen(req)

                        except UnicodeEncodeError:
                                url = ("https://api.neople.co.kr/cy/players?nickname=" + quote(msg[1]) + "&wordType=match&apikey="+cy_client_id)
                                req = urllib.request.Request(url)
                                req.add_header("Cyphers-ID", cy_client_id)
                                response = urllib.request.urlopen(req)

                        rescode = response.getcode()

                        if (rescode == 200):
                                response_body = response.read()
                                data = json.loads(response_body)
                                data1 = data.get('rows')
                                try:
                                        playerId = data1[0].get('playerId')
                                        nickname = data1[0].get('nickname')
                                        grade = str(data1[0].get('grade'))

                                        url = (
                                                    'https://api.neople.co.kr/cy/players/' + playerId + '?apikey=' + cy_client_id)  # 자세한 정보 받기
                                        data1 = data_request(url)

                                        if (data1.get('clanName') != None):  # 클랜명 받기
                                            clanname = data1.get('clanName')
                                        else:
                                            clanname = '클랜 없음'
                                        if (data1.get('ratingpoint')) != None:  # 랭크점수받기
                                            ratingpoint = str(data1.get('ratingpoint'))
                                        else:
                                            ratingpoint = 0
                                        if (data1.get('maxRatingPoint')) != None:  # 최대랭크점수받기
                                            maxratingpoint = str(data1.get('maxRatingPoint'))
                                        else:
                                            maxratingpoint = 0
                                        if (data1.get('tierName')) != None:  # 티어 이름받기
                                            tiername = str(data1.get('tierName'))
                                        else:
                                            tiername = '공식 전적 없음'

                                        records = data1.get('records')

                                        if records[0].get('gameTypeId') == 'rating':
                                            rankwin = str(records[0].get('winCount'))
                                            ranklose = str(records[0].get('loseCount'))
                                            rankstop = str(records[0].get('stopCount'))
                                            normwin = str(records[1].get('winCount'))
                                            normlose = str(records[1].get('loseCount'))
                                            normstop = str(records[1].get('stopCount'))
                                        else:
                                            rankwin = 0
                                            ranklose = 0
                                            rankstop = 0
                                            normwin = str(records[0].get('winCount'))
                                            normlose = str(records[0].get('loseCount'))
                                            normstop = str(records[0].get('stopCount'))

                                        url = ('https://api.neople.co.kr/cy/players/' + playerId + '/matches?gameTypeId=' + gameTypeId + '&startDate=&endDate=&limit=6&next=&apikey='+cy_client_id)
                                        data1 = data_request(url)

                                        matches = data1.get('matches')
                                        game = matches.get('rows')

                                        nmb = -1

                                        mdate = []
                                        mmap = []
                                        mmapname = []
                                        mpI = []
                                        mpIres = []
                                        mpIran = []
                                        mpIpUC = []
                                        mpIchN = []
                                        mpIlvl = []
                                        mpIK = []
                                        mpID = []
                                        mpIA = []
                                        mpIatkP = []
                                        mpIdmgP = []
                                        mpIbtlP = []
                                        mpIsigP = []
                                        mpIpT = []
                                        mpIhA = []
                                        mpPos = []

                                        for _ in game:
                                                nmb += 1
                                                mdate.append(game[nmb].get('date'))
                                                mmap.append(game[nmb].get('map'))
                                                mmapname.append(mmap[nmb].get('name'))
                                                mpI.append(game[nmb].get('playInfo'))
                                                mpPos.append(game[nmb].get('position').get('name'))

                                                if mpI[nmb].get('result') == 'lose':
                                                        mpIres.append('패배')

                                                elif mpI[nmb].get('result') == 'win':
                                                        mpIres.append('승리')

                                                else:
                                                        mpIres.append('탈주')

                                                if mpI[nmb].get('random') == 'False':
                                                        mpIran.append('O')

                                                else:
                                                        mpIran.append('X')

                                                if mpI[nmb].get('partyUserCount') == 0:
                                                        mpIpUC.append(1)

                                                else:
                                                        mpIpUC.append(mpI[nmb].get('partyUserCount'))

                                                mpIchN.append(mpI[nmb].get('characterName'))
                                                mpIlvl.append(mpI[nmb].get('level'))
                                                mpIK.append(mpI[nmb].get('killCount'))
                                                mpID.append(mpI[nmb].get('deathCount'))
                                                mpIA.append(mpI[nmb].get('assistCount'))
                                                mpIatkP.append(mpI[nmb].get('attackPoint'))
                                                mpIdmgP.append(mpI[nmb].get('damagePoint'))
                                                mpIbtlP.append(mpI[nmb].get('battlePoint'))
                                                mpIsigP.append(mpI[nmb].get('sightPoint'))
                                                mpIpT.append(mpI[nmb].get('playTime'))
                                                mpIhA.append(mpI[nmb].get('healAmount'))

                                        print(member, guild, now, '!전적', msg[2], rescode)
                                        print('==========')

                                        if nmb != -1:
                                                nmb = -1
                                                for _ in game:
                                                        nmb += 1
                                                        if nmb == 0:
                                                            embed = discord.Embed(title=nickname + ' 정보',
                                                                                  description='등급: {}\n클랜 이름: {}\n공식 티어: {}\n현재/최고 점수: {}/{}\n공식 전적(승-패-탈주): {}-{}-{}\n일반 전적(승-패-탈주): {}-{}-{}'.format(
                                                                                      grade, clanname, tiername,
                                                                                      ratingpoint, maxratingpoint,
                                                                                      rankwin, ranklose, rankstop,
                                                                                      normwin, normlose, normstop
                                                                                  )
                                                                                  , colour=DEFAULT_COLOR)

                                                        embed.add_field(
                                                            name='{} {}'.format(mmapname[nmb], mpIres[nmb]),
                                                            value='\n[{}]\n'
                                                                  '```무작위 캐릭터:{}\n'
                                                                  '{}({}){}\n'
                                                                  '{}인팟\n'
                                                                  'K/D/A: {}/{}/{}\n'
                                                                  '가한/받은데미지\n{}/{}\n'
                                                                  '치유량: {}\n'
                                                                  '전투 참여: {}\n'
                                                                  '시야 확보: {}\n```'.format(
                                                                mdate[nmb], mpIran[nmb],
                                                                mpIchN[nmb],
                                                                mpIlvl[nmb], POSITION[mpPos[nmb]],
                                                                mpIpUC[nmb], mpIK[nmb], mpID[nmb], mpIA[nmb],
                                                                mpIatkP[nmb], mpIdmgP[nmb], mpIhA[nmb], mpIbtlP[nmb],
                                                                mpIsigP[nmb]),
                                                            inline=True)


                                                embed_default(embed)
                                                await textchannel.send(embed=embed)

                                        else:
                                            embed = discord.Embed(title=nickname + ' 정보',
                                                                  description='등급: {}\n클랜 이름: {}\n공식 티어: {}\n현재/최고 점수: {}/{}\n공식 전적(승-패-탈주): {}-{}-{}\n일반 전적(승-패-탈주): {}-{}-{}'.format(
                                                                      grade, clanname, tiername,
                                                                      ratingpoint, maxratingpoint,
                                                                      rankwin, ranklose, rankstop,
                                                                      normwin, normlose, normstop
                                                                  )
                                                                  , colour=DEFAULT_COLOR)
                                            embed.add_field(name='전적이 없습니다.',value='```최근 게임이 끝난지 1시간이 안되었거나 30일 전에 진행되었습니다.```')
                                            embed.set_footer(text='문의사항은 NightSkyK#0117로 DM주세요.')
                                            embed.set_thumbnail(
                                                url="http://pub.cyphers.co.kr/images3/art/2021/06/02/1622596975918.png")
                                            await textchannel.send(embed=embed)

                                except IndexError:
                                        print(member, guild, now, '!전적', "Error Code: 이름 없음")
                                        print('==========')
                                        embed = discord.Embed(title='오류', description='이름을 확인한 후 다시 시도해주세요.',
                                                              colour=0xcc9911, timestamp=now)
                                        embed_default(embed)
                                        await textchannel.send(embed=embed)

                else:
                    embed = discord.Embed(title='오류!',
                                          description='```명령어를 제대로 작성했는지 확인해주세요.\n 주로 이 오류는 닉네임에 공백이 포함되었거나 일반과 공식을 입력하지 않았을때 출력됩니다.\n도움이 필요하시다면 \'!전적 도움말\'을 이용해주세요.```'
                                          , colour=DEFAULT_COLOR)
                    embed_default(embed)
                    await  textchannel.send(embed=embed)

        if message.content.startswith("!랜덤"): #Random Choice

            msg = message.content.split(" ")

            if len(msg) !=2 : #Case 0
                embed = discord.Embed(
                    title='오류!',
                    description='```\'!랜덤\'의 올바른 사용법은 \'!랜덤 (1~5 사이의 정수)\'입니다.```',
                    color=DEFAULT_COLOR
                )
                embed_default(embed)
                print(member, guild, now, '!랜덤', 'Bad Request')
                print('==========')
                await textchannel.send(embed=embed)

            elif msg[1]=='1' or msg[1]=='2' or msg[1]=='3' or msg[1]=='4' or msg[1]=='5': #Case 1 1~5

                require = int(msg[1])
                url = ("https://api.neople.co.kr/cy/characters?apikey=" + cy_client_id)
                data = data_request(url)

                chardata = data.get('rows')
                charID = []
                charName = []
                charNum = -1

                for _ in chardata:
                    charNum += 1
                    charID.append(chardata[charNum].get('characterId'))
                    charName.append(chardata[charNum].get('characterName'))

                nmb = list(range(0,charNum+1))
                randomchoice = random.sample(nmb, require)

                embed = discord.Embed(
                    title='사이퍼즈 봇의 선택은!!',
                    description='총 {}개 선택되었습니다!'.format(require),
                    colour=DEFAULT_COLOR)
                nmb = 0
                for i in randomchoice:
                    nmb += 1
                    embed.add_field(name='{}번째 선택!'.format(nmb),
                                    value='**{}**입니다!'.format(charName[i]),
                                    inline=False)

                print(member, guild, now, '!랜덤', require)
                print('==========')
                await textchannel.send(embed=embed)

            else: #Another Case Bad Requests
                embed = discord.Embed(
                    title='오류!',
                    description='```\'!랜덤\'의 올바른 사용법은 \'!랜덤 (1~5 사이의 정수)\'입니다.```',
                    color=DEFAULT_COLOR
                )
                embed_default(embed)
                print(member, guild, now, '!랜덤', 'Bad Request')
                print('==========')
                await textchannel.send(embed=embed)

#Discord API_Keys
client.run('Njg0NzA0MzIwMTEyOTUxMzQ3.Xl9-lw.FK0vOHX7xPiVW48z72LD1dKUnYw')
