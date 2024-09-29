import nextcord

from nextcord.ext import commands

import random

import asyncio

# 봇 설정

bot = commands.Bot(command_prefix="!", intents=nextcord.Intents.all())

# 봇이 준비되었을 때 호출되는 이벤트

@bot.event

async def on_ready():

    print(f'{bot.user}로 로그인했습니다.')

# 뽑기 명령어

@bot.command(name="뽑기")

async def tokenboopgi(ctx):

    # 1부터 1000까지 순차적으로 돌아가는 롤렛 휠처럼 출력

    winning_number = random.randint(1, 1000)

    # 롤렛 휠 애니메이션처럼 1초 간격으로 숫자가 출력됨

    embed = nextcord.Embed(title="🎰 뽑기 진행 중...", description="숫자를 뽑고 있습니다!", color=0xFFFF00)  # 노란색

    message = await ctx.send(embed=embed)

    for i in range(5):  # 5번 돌아가는 것처럼 보이게

        fake_number = random.randint(1, 1000)

        embed.description = f"🎰 {fake_number}..."

        await message.edit(embed=embed)

        await asyncio.sleep(0.5)

    # 최종 결과 출력

    embed.title = "🎉 뽑기 결과"

    embed.description = f"최종 번호: **{winning_number}**!"

    await message.edit(embed=embed)

    # 역할 ID와 당첨 번호를 딕셔너리로 정의

    roles = {

        777: [1286292190649126995],

        444: [1286302307302117499],

        666: [1286302307302117499],

        888: [1286623476047679572],

        333: [1286611820555014197],

        222: [1286622858243604480],

    }

    # 각 번호에 따라 역할 부여

    assigned_roles = roles.get(winning_number, [])

    if assigned_roles:

        for role_id in assigned_roles:

            role = nextcord.utils.get(ctx.guild.roles, id=role_id)

            if role:

                await ctx.author.add_roles(role)

        embed.add_field(

            name="🎉 축하합니다!",

            value=f"{ctx.author.mention}님이 {', '.join([role.name for role in ctx.author.roles if role.id in assigned_roles])} 역할을 받으셨습니다!"

        )

    else:

        embed.add_field(name="😢 아쉽게도...", value="아쉽게도 역할을 뽑지 못하셨네요!")

    await message.edit(embed=embed)

# 봇 실행

bot.run("")