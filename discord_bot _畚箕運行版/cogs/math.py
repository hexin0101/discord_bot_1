import discord
import random
from discord.ext import commands
from discord import app_commands
from typing import Optional
from discord.app_commands import Choice
import sympy as sp

class Math(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="calculator", description="是計算機歐")
    async def calculator(self, interaction: discord.Interaction, expression: str):
        # 解析表达式
        parsed_expression = sp.sympify(expression)

        # 计算表达式的值
        result = parsed_expression.evalf()
        # 格式化结果为小数点后两位
        formatted_result = f"{result:.2f}"
        await interaction.response.send_message(f"{expression}={formatted_result}") 


# Cog 載入 Bot 中
async def setup(bot: commands.Bot):
    await bot.add_cog(Math(bot)) 
