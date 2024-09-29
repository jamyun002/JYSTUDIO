import discord

from discord.ext import commands

from discord import app_commands

import random

import json

import os

intents = discord.Intents.default()

intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 유저 잔고 파일 경로

BALANCE_FILE = "balance.json"

# 최소 베팅 금액 설정

MIN_BET_AMOUNT = 1000

# 잔고 데이터를 파일로 저장하는 함수

def save_balance():

    with open(BALANCE_FILE, "w") as f:

        json.dump(user_balance, f)

# 잔고 데이터를 파일에서 불러오는 함수

def load_balance():

    global user_balance

    if os.path.exists(BALANCE_FILE):

        with open(BALANCE_FILE, "r") as f:

            user_balance = json.load(f)

    else:

        user_balance = {}

# 잔고 확인 함수

def get_balance(user_id):

    return user_balance.get(str(user_id), 0)

# 잔고 추가 함수

def add_balance(user_id, amount):

    user_balance[str(user_id)] = get_balance(user_id) + amount

    save_balance()

# 베팅 금액 차감 함수

def deduct_balance(user_id, amount):

    if get_balance(user_id) >= amount:

        user_balance[str(user_id)] -= amount

        save_balance()

        return True

    return False

# 봇 준비 이벤트

@bot.event

async def on_ready():

    print(f'Logged in as {bot.user}')

    load_balance()  # 봇이 시작될 때 잔고 데이터 로드

    await bot.tree.sync()

    print("슬래시 명령어가 동기화되었습니다.")

# 잔고 확인 슬래시 명령어 (비밀 메시지로 응답)

@bot.tree.command(name="잔액", description="소유하고 있는 돈을 보여줍니다")

async def balance(interaction: discord.Interaction):

    user_id = interaction.user.id

    balance = get_balance(user_id)

    embed = discord.Embed(title="잔액", description=f"{interaction.user.name}님의 잔액 : {balance}", color=discord.Color.blue())

    await interaction.response.send_message(embed=embed, ephemeral=True)

# 돈 추가 슬래시 명령어 (비밀 메시지로 응답, 관리자 전용)

@bot.tree.command(name="돈추가", description="특정 유저에게 돈을 추가합니다. [ 관리자 전용 ]")

@app_commands.checks.has_permissions(administrator=True)

async def add_money(interaction: discord.Interaction, 유저: discord.Member, 금액: int):

    add_balance(유저.id, 금액)  # 'member' 대신 '유저'로 수정

    embed = discord.Embed(title="돈 추가", description=f"{유저.name}님의 잔고에 {금액}원이 추가되었습니다.", color=discord.Color.green())

    await interaction.response.send_message(embed=embed, ephemeral=True)

# 돈 차감 슬래시 명령어 (비밀 메시지로 응답, 관리자 전용)

@bot.tree.command(name="돈차감", description="특정 유저의 돈을 차감합니다. [ 관리자 전용 ]")

@app_commands.checks.has_permissions(administrator=True)

async def deduct_money(interaction: discord.Interaction, 유저: discord.Member, 금액: int):

    if deduct_balance(유저.id, 금액):  # 'member' 대신 '유저'로 수정

        embed = discord.Embed(title="돈 차감", description=f"{유저.name}님의 잔고에서 {금액}원이 차감되었습니다.", color=discord.Color.red())

    else:

        embed = discord.Embed(title="오류", description=f"{유저.name}님의 잔고가 부족하여 차감할 수 없습니다.", color=discord.Color.red())

    await interaction.response.send_message(embed=embed, ephemeral=True)

# 복권 슬래시 명령어 (결과는 일반 메시지로 전송)

@bot.tree.command(name="복권", description="복권에 참여하여 돈을 걸고 베팅합니다")

async def lottery(interaction: discord.Interaction, 금액: int, 선택: int):

    user_id = interaction.user.id

    # 선택 범위 확인

    if 선택 not in [1, 2, 3]:

        await interaction.response.send_message("선택할 수 있는 값은 1, 2 또는 3입니다.", ephemeral=True)

        return

    if 금액 < MIN_BET_AMOUNT:

        await interaction.response.send_message(f"최소 베팅 금액은 {MIN_BET_AMOUNT}입니다.", ephemeral=True)

        return

    # 잔고 확인 및 베팅 금액 차감

    if get_balance(user_id) < 금액:

        await interaction.response.send_message("잔액이 부족합니다.", ephemeral=True)

        return

    if not deduct_balance(user_id, 금액):

        await interaction.response.send_message("베팅 금액이 부족합니다.", ephemeral=True)

        return

    # 복권 결과 생성 (1~3 중 하나가 정답)

    correct_choice = random.randint(1, 3)

    # 결과 메시지 작성

    embed = discord.Embed(title="복권 결과", color=discord.Color.green())

    embed.add_field(name="당신의 선택", value=str(선택), inline=True)

    embed.add_field(name="정답", value=str(correct_choice), inline=True)

    # 사용자가 이겼는지 확인

    if 선택 == correct_choice:

        winnings = 금액 * 2

        add_balance(user_id, winnings)

        balance = get_balance(user_id)  # 잔액 업데이트

        embed.add_field(name="결과", value=f"축하합니다! 돈을 2배로 얻으셨습니다. [ 현재 잔액 : {balance} ]", inline=False)

    else:

        balance = get_balance(user_id)  # 잔액 업데이트

        embed.add_field(name="결과", value=f"아쉽게도 배팅한 금액을 다 잃었습니다... [ 현재 잔액 : {balance} ]", inline=False)

    # 결과 임베드 전송

    await interaction.response.send_message(embed=embed)

# 봇 실행

bot.run("")  # 실제 토큰으로 교체하세요.