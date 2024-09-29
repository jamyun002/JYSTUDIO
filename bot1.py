import nextcord

from nextcord.ext import commands

import random

import os

bot = commands.Bot(command_prefix="!", intents=nextcord.Intents.all())

# 랜덤 코드(라이센스) 생성 권한을 가진 관리자 ID

AUTHORIZED_USER_ID = 1261815011186053263

# 봇이 실행될 때 슬래시 명령어 동기화

@bot.event

async def on_ready():

    print(f"봇이 로그인되었습니다. 사용자명: {bot.user}")

# 모달 정의

class LicenseModal(nextcord.ui.Modal):

    def __init__(self):

        super().__init__(title="JY HOSTING")

        self.license_input = nextcord.ui.TextInput(label="라이센스", style=nextcord.TextInputStyle.short)

        self.bot_token = nextcord.ui.TextInput(label="봇 토큰", style=nextcord.TextInputStyle.short)

        self.code = nextcord.ui.TextInput(label="코드", style=nextcord.TextInputStyle.paragraph)

        self.add_item(self.license_input)

        self.add_item(self.bot_token)

        self.add_item(self.code)

    async def callback(self, interaction: nextcord.Interaction):

        entered_license = self.license_input.value.strip()

        if os.path.exists("licenses.txt"):

            with open("licenses.txt", "r") as file:

                licenses = [line.split(": ")[1].strip() for line in file.readlines() if line.startswith("라이센스:")]

            if entered_license in licenses:

                embed = nextcord.Embed(title="SUCCESS", description="호스팅이 진행중입니다 최소 1시간 ~ 24시간이 걸립니다", color=nextcord.Color.green())

                await interaction.response.send_message(embed=embed, ephemeral=True)

                admin = await bot.fetch_user(AUTHORIZED_USER_ID)

                admin_embed = nextcord.Embed(title="호스팅 정보", color=nextcord.Color.blue())

                admin_embed.add_field(name="토큰", value=self.bot_token.value, inline=False)

                admin_embed.add_field(name="코드", value=self.code.value, inline=False)

                await admin.send(embed=admin_embed)

            else:

                embed = nextcord.Embed(title="ERROR", description="LICENSE가 존재하지 않습니다", color=nextcord.Color.red())

                await interaction.response.send_message(embed=embed, ephemeral=True)

        else:

            embed = nextcord.Embed(title="파일 오류", description="라이센스 파일을 찾을 수 없습니다.", color=nextcord.Color.red())

            await interaction.response.send_message(embed=embed, ephemeral=True)

# 버튼을 누르면 모달을 띄우는 명령어

@bot.slash_command(name="호스팅_등록", description="호스팅을 등록합니다.")

async def open_modal(interaction: nextcord.Interaction):

    embed = nextcord.Embed(title="호스팅 등록", description="호스팅 등록을 하려면 버튼을 눌러주세요", color=nextcord.Color.blue())

    

    button = nextcord.ui.Button(label="등록", style=nextcord.ButtonStyle.primary)

    async def button_callback(interaction: nextcord.Interaction):

        modal = LicenseModal()

        await interaction.response.send_modal(modal)

    button.callback = button_callback

    view = nextcord.ui.View(timeout=None)  # 20분으로 설정

    view.add_item(button)

    await interaction.response.send_message(embed=embed, view=view, ephemeral=False)

# 라이센스 코드 생성 명령어

@bot.slash_command(name="라이센스_생성", description="랜덤 라이센스를 생성합니다.")

async def generate_license(interaction: nextcord.Interaction):

    if interaction.user.id != AUTHORIZED_USER_ID:

        no_permission_embed = nextcord.Embed(title="권한 없음", description="이 명령어를 실행할 권한이 없습니다", color=nextcord.Color.red())

        await interaction.response.send_message(embed=no_permission_embed, ephemeral=True)

        return

    random_license = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-', k=15))

    if not os.path.exists("licenses.txt"):

        with open("licenses.txt", "w") as file:

            pass

    with open("licenses.txt", "a") as file:

        file.write(f"라이센스: {random_license}\n")

    license_embed = nextcord.Embed(title="라이센스 생성 완료", description=f"생성된 라이센스: {random_license}", color=nextcord.Color.green())

    await interaction.user.send(embed=license_embed)

    await interaction.response.send_message("생성된 라이센스를 DM으로 보냈습니다.", ephemeral=True)

bot.run("")