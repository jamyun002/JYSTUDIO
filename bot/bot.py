import discord

from discord.ext import commands

from discord import app_commands

import asyncio

import os

import sys

intents = discord.Intents.default()

intents.messages = True

intents.guilds = True

intents.dm_messages = True

intents.members = True

# 토큰 관리 봇 클래스

class TokenManagementBot(commands.Bot):

    def __init__(self, command_prefix, intents, token_management_token):

        super().__init__(command_prefix=command_prefix, intents=intents)

        self.token_management_token = token_management_token

    async def on_ready(self):

        print(f'토큰 관리 봇 로그인: {self.user}')

        await self.tree.sync()

    async def send_dm(self, user: discord.User, message: str):

        try:

            await user.send(message)

        except discord.Forbidden:

            print(f'DM을 보내는 데 실패했습니다: {user.display_name}')

    async def setup_commands(self):

        @self.tree.command(name="토큰추가", description="토큰을 추가합니다.")

        async def add_token(interaction: discord.Interaction, token: str):

            try:

                with open('token/tokens.txt', 'a') as f:

                    f.write(token + '\n')

                await self.send_dm(interaction.user, f"토큰 {token}이 성공적으로 추가되었습니다.")

                await interaction.response.send_message("토큰 추가 성공", ephemeral=True)

                

                # 코드 재실행

                await self.send_dm(interaction.user, "코드가 다시 실행됩니다.")

                await interaction.response.send_message("코드가 다시 실행됩니다.", ephemeral=True)

                await asyncio.sleep(2)  # 잠시 대기 후 코드 재실행

                os.execv(sys.executable, ['python'] + sys.argv)

            except Exception as e:

                await self.send_dm(interaction.user, f"토큰 추가 실패: {e}")

                await interaction.response.send_message(f"토큰 추가 실패: {e}", ephemeral=True)

        @self.tree.command(name="토큰삭제", description="토큰을 삭제합니다.")

        async def remove_token(interaction: discord.Interaction, token: str):

            try:

                with open('token/tokens.txt', 'r') as f:

                    lines = f.readlines()

                with open('token/tokens.txt', 'w') as f:

                    for line in lines:

                        if line.strip() != token:

                            f.write(line)

                await self.send_dm(interaction.user, f"토큰 {token}이 성공적으로 삭제되었습니다.")

                await interaction.response.send_message("토큰 삭제 성공", ephemeral=True)

            except Exception as e:

                await self.send_dm(interaction.user, f"토큰 삭제 실패: {e}")

                await interaction.response.send_message(f"토큰 삭제 실패: {e}", ephemeral=True)

# 메인 봇 클래스

class MainBot(commands.Bot):

    def __init__(self, command_prefix, intents, token):

        super().__init__(command_prefix=command_prefix, intents=intents)

        self.token = token

        self.role_file = f'dm_roles{token[:8]}.txt'

    async def on_ready(self):

        print(f'광고 봇 로그인: {self.user}')

        await self.tree.sync()

    async def is_admin(self, interaction: discord.Interaction):

        guild = interaction.guild

        if guild is None:

            return False

        member = guild.get_member(interaction.user.id)

        return member is not None and member.guild_permissions.administrator

    async def setup_commands(self):

        @self.tree.command(name="광고", description="광고를 보냅니다.")

        @app_commands.check(self.is_admin)

        async def dm(interaction: discord.Interaction, 내용: str):

            guild = interaction.guild

            if not guild:

                await interaction.response.send_message("관리자만 사용 가능한 명령어입니다.", ephemeral=True)

                return

            try:

                with open(f'dmrole/{self.role_file}', 'r') as file:

                    role_ids = file.read().splitlines()

                await interaction.response.send_message('메시지를 보내는 중...', ephemeral=True)

                for role_id in role_ids:

                    role = guild.get_role(int(role_id))

                    if role:

                        for member in role.members:

                            try:

                                await member.send(내용)

                            except discord.Forbidden:

                                print(f'메시지 보내기 실패 {member.display_name}.')

                            except Exception as e:

                                print(f'에러 {member.display_name}: {e}')

                await interaction.followup.send('광고가 보내졌습니다!')

            except FileNotFoundError:

                await interaction.followup.send(f'{self.role_file} 파일을 찾을 수 없습니다!', ephemeral=True)

            except Exception as e:

                await interaction.followup.send(f'에러 {e}', ephemeral=True)

        @self.tree.command(name="광고_역할추가", description="광고 역할 파일에 역할을 추가합니다.")

        @app_commands.check(self.is_admin)

        async def add_role(interaction: discord.Interaction, role: discord.Role):

            try:

                with open(f'dmrole/{self.role_file}', 'a') as file:

                    file.write(f'{role.id}\n')

                await interaction.response.send_message(f'{role.name} 역할이 {self.role_file}에 추가되었습니다.', ephemeral=True)

            except FileNotFoundError:

                with open(f'dmrole/{self.role_file}', 'w') as file:

                    file.write(f'{role.id}\n')

                await interaction.response.send_message(f'{role.name} 역할이 {self.role_file}에 새로 생성되었습니다.', ephemeral=True)

            except Exception as e:

                await interaction.response.send_message(f'에러: {e}', ephemeral=True)

        @self.tree.command(name="광고_역할삭제", description="광고 역할 파일에서 역할을 삭제합니다.")

        @app_commands.check(self.is_admin)

        async def remove_role(interaction: discord.Interaction, role: discord.Role):

            try:

                with open(f'dmrole/{self.role_file}', 'r') as file:

                    lines = file.readlines()

                with open(f'dmrole/{self.role_file}', 'w') as file:

                    for line in lines:

                        if line.strip() != str(role.id):

                            file.write(line)

                await interaction.response.send_message(f'{role.name} 역할이 {self.role_file}에서 삭제되었습니다.', ephemeral=True)

            except Exception as e:

                await interaction.response.send_message(f'에러: {e}', ephemeral=True)

async def main():

    # 토큰 관리 봇

    token_management_token = ""  # 여기에는 토큰 관리 봇의 실제 토큰을 입력하세요

    token_management_bot = TokenManagementBot(command_prefix='/', intents=intents, token_management_token=token_management_token)

    await token_management_bot.setup_commands()

    # 메인 봇들

    with open('token/tokens.txt', 'r') as f:

        TOKENS = f.read().splitlines()

    main_bots = []

    for token in TOKENS:

        bot = MainBot(

            command_prefix='/',

            intents=intents,

            token=token

        )

        await bot.setup_commands()

        main_bots.append(bot)

    await asyncio.gather(

        token_management_bot.start(token_management_token),

        *(bot.start(bot.token) for bot in main_bots)

    )

if __name__ == '__main__':

    asyncio.run(main())
