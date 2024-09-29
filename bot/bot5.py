import nextcord

from nextcord.ext import commands

import random

# 봇 설정

bot = commands.Bot(command_prefix="!", intents=nextcord.Intents.all())

# 봇이 준비되었을 때 호출되는 이벤트

@bot.event

async def on_ready():

    print(f'{bot.user}로 로그인했습니다.')

# 뽑기 명령어

@bot.command(name="뽑기")

async def tokenboopgi(ctx):

    winning_number = random.randint(1, 1000)  # 1부터 1000까지 무작위 숫자 뽑기

    # 역할 ID와 당첨 번호를 딕셔너리로 정의

    roles = {

        65: [1286854389847560242],

        815: [1286853926519308401],

        921: [1286853817614471218],

        111: [1286853727231283201],

        813: [1286853570045411348],

        416: [1286853436452638753],

        625: [1286853201630330900],

        722: [1286852915578933319],

        666: [1286852669603844207, 1286852669603844208],  # 중복된 역할 ID 리스트로 추가

        444: [1286852669603844207],  # 중복 역할

        888: [1286852569288802367],

        999: [1286657022212837409],

        123: [1286657022212837410],

        777: [1286657022212837411],

    }

    # 각 번호에 따라 역할 부여

    assigned_roles = roles.get(winning_number, [])

    if assigned_roles:

        for role_id in assigned_roles:

            role = nextcord.utils.get(ctx.guild.roles, id=role_id)

            if role:

                await ctx.author.add_roles(role)

        await ctx.send(f"축하합니다! {ctx.author.mention}님이 {', '.join([role.name for role in ctx.author.roles if role.id in assigned_roles])} 역할을 받으셨습니다! [ 뽑은 번호: {winning_number} ]")

    else:

        # 당첨되지 않았을 때 뽑은 숫자 알려주기

        await ctx.send(f"아쉽게도 역할을 뽑지 못하셨네요! [ 당첨 번호 : {winning_number} ]")

# 봇 실행

bot.run("")