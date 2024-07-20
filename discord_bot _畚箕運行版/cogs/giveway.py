import discord
import random
from discord.ext import commands
from discord import app_commands
import os
import logging

# 添加日誌
logging.basicConfig(level=logging.INFO)
OPTIONS_DIR = 'options'  # 用於存放選項文件的目錄

class Giveaway(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def load_options(self, filename: str):
        """從指定的文件中讀取選項並加載到內存中。"""
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f.readlines()]
        return []

    def save_options(self, filename: str, options: list):
        """將內存中的選項保存到指定的文件中。"""
        with open(filename, 'w', encoding='utf-8') as f:
            for option in options:
                f.write(option + '\n')

    def get_files_list(self) -> list:
        """列出 OPTIONS_DIR 目錄下的所有文件。"""
        if not os.path.exists(OPTIONS_DIR):
            os.makedirs(OPTIONS_DIR)
        return [f for f in os.listdir(OPTIONS_DIR) if os.path.isfile(os.path.join(OPTIONS_DIR, f))]

    @app_commands.command(name='add_option', description='添加一個或多個抽獎選項')
    @app_commands.describe(filename='選項文件名', options='要添加的選項，用空格分隔')
    async def add_option(self, interaction: discord.Interaction, filename: str, options: str):
        filepath = os.path.join(OPTIONS_DIR, filename)
        options_list = options.split()
        current_options = self.load_options(filepath)
        current_options.extend(options_list)
        self.save_options(filepath, current_options)
        await interaction.response.send_message(f'選項 "{", ".join(options_list)}" 已添加到文件 "{filename}"！')

    @app_commands.command(name='list_files', description='列出所有可選擇的選項文件')
    async def list_files(self, interaction: discord.Interaction):
        await interaction.response.defer()
        files = self.get_files_list()
        if not files:
            await interaction.response.send_message("目前沒有可用的選項文件。")
            return

        embed = discord.Embed(title="可選擇的選項文件", description="請使用其他指令來選擇文件。", color=discord.Color.blue())
        
        for file in files:
            embed.add_field(name=file, value="使用 `/view_options filename` 查看內容", inline=False)
        
        try:
            await interaction.followup.send(embed=embed)
        except discord.DiscordException as e:
            await interaction.followup.send(f"發送嵌入消息時出錯：{e}")

    @app_commands.command(name='view_options', description='查看指定文件中的所有選項')
    @app_commands.describe(filename='選項文件名')
    async def view_options(self, interaction: discord.Interaction, filename: str):
        filepath = os.path.join(OPTIONS_DIR, filename)
        options = self.load_options(filepath)
        if options:
            embed = discord.Embed(title=f"文件 \"{filename}\" 的選項", description="\n".join(options), color=discord.Color.green())
        else:
            embed = discord.Embed(title=f"文件 \"{filename}\"", description="此文件中沒有選項。", color=discord.Color.red())

        try:
            await interaction.response.send_message(embed=embed)
        except discord.DiscordException as e:
            await interaction.response.send_message(f"發送嵌入消息時出錯：{e}")

    @app_commands.command(name='draw', description='從指定文件隨機選擇一個選項作為獲獎選項')
    async def draw(self, interaction: discord.Interaction):
        files = self.get_files_list()
        if not files:
            await interaction.response.send_message("目前沒有可選擇的選項文件。")
            return

        # 創建下拉選單
        select = discord.ui.Select(
            placeholder="選擇一個選項文件",
            options=[discord.SelectOption(label=file, value=file) for file in files],
        )

        # 添加選擇器回調
        async def select_callback(interaction: discord.Interaction):
            selected_file = select.values[0]
            filepath = os.path.join(OPTIONS_DIR, selected_file)
            options = self.load_options(filepath)
            if options:
                winner = random.choice(options)
                embed = discord.Embed(title=f"抽獎結果", description=f'恭喜！文件 "{selected_file}" 中選中的選項是："{winner}"', color=discord.Color.gold())
            else:
                embed = discord.Embed(title=f"文件 \"{selected_file}\"", description="此文件中沒有選項可供抽獎。", color=discord.Color.red())

            await interaction.response.send_message(embed=embed)

        select.callback = select_callback

        # 發送消息和下拉選單
        view = discord.ui.View()
        view.add_item(select)

        await interaction.response.send_message(
            content="請選擇一個選項文件進行抽獎：",
            view=view
        )

    @app_commands.command(name='clear_options', description='清除指定文件中的所有選項')
    @app_commands.describe(filename='選項文件名')
    async def clear_options(self, interaction: discord.Interaction, filename: str):
        filepath = os.path.join(OPTIONS_DIR, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            await interaction.response.send_message(f"文件 \"{filename}\" 中的所有選項已清除。")
        else:
            await interaction.response.send_message(f"文件 \"{filename}\" 不存在。")

# Cog 載入 Bot 中
async def setup(bot: commands.Bot):
    await bot.add_cog(Giveaway(bot))
