import discord
import random
from discord.ext import commands
from discord import app_commands
from typing import Optional
import operator
from discord.app_commands import Choice
import re
import sympy as sp
operators = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}
# 定義名為 Main 的 Cog
class Main(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.guessed_number=random.randint(1,100)

    # 前綴指令
    @commands.command()
    async def Hello(self, ctx: commands.Context):
        await ctx.send("Hello, world!")

    # 關鍵字觸發
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        if message.author.id==1262855821256032460:
            return
        if message.content == "Hello":
            await message.channel.send("Hello")
        if message.content == "hello":
            await message.channel.send("hello")
        if message.content == "ez":
            await message.channel.send("哈哈真簡單")
        if message.content == "晚安":
            await message.channel.send("睡什麼 起來嗨!!!!!!!")
        if message.content == "早安":
            await message.channel.send("早安阿 傻逼")
        # Regular expression to find simple math expressions
        pattern = r'[0-9+\-*/().]+'
        match = re.fullmatch(pattern, message.content.replace(" ", ""))
        
        if match:
            expression = match.group()
            try:
                # Evaluate the expression using sympy
                result = sp.sympify(expression)
                await message.channel.send(f'答案= {result}')
            except (sp.SympifyError, ZeroDivisionError):
                await message.channel.send("無效的數學表達式或除以零錯誤")
    #/觸發
    @app_commands.command(name = "hello", description = "Hello, world!")
    async def hello(self, interaction: discord.Interaction):
        # 回覆使用者的訊息
        await interaction.response.send_message("Hello, world!")
    @app_commands.command(name = "awa", description = "awa")
    async def awa(self, interaction: discord.Interaction):
        await interaction.response.send_message("awa")
    @app_commands.command(name = "awawa", description = "awa")
    async def awawa(self, interaction: discord.Interaction):
        await interaction.response.send_message("awawa")
    @app_commands.command(name = "say", description = "大聲說出來")
    @app_commands.describe(name = "輸入人名", text = "輸入要說的話")
    async def say(self, interaction: discord.Interaction, name: str, text: Optional[str] = None):
        if text == None:
            text = "。。。"
        await interaction.response.send_message(f"{name} 說 「{text}」")
    @app_commands.command(name="about", description="機器人資訊")
    async def about(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="機器人資訊",
            description="80$製作機器人二代\n\n點擊下方的連結以查看詳細資訊。",
            color=0xFFC0CB
        )

        # Add a field with the link
        embed.add_field(name="詳情連結", value="[點此查看](https://github.com/hexin0101/discord_bot_bot)", inline=False)

        # Send the embed
        await interaction.response.send_message(embed=embed)

    
    

# Cog 載入 Bot 中
async def setup(bot: commands.Bot):
    await bot.add_cog(Main(bot))