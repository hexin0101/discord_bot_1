import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
import json
import os
import matplotlib.pyplot as plt
import matplotlib

class Vote(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.vote_data = self.load_vote_data()
        
        # 設定 matplotlib 使用中文字體
        matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 使用系統上已安裝的字體
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

    def load_vote_data(self):
        if os.path.exists('votes.json'):
            with open('votes.json', 'r') as f:
                return json.load(f)
        return {}

    def save_vote_data(self):
        with open('votes.json', 'w') as f:
            json.dump(self.vote_data, f, indent=4)

    @app_commands.command(name="create_vote", description="Create a new vote")
    @app_commands.describe(question="The question to vote on")
    @app_commands.describe(option1="First option")
    @app_commands.describe(option2="Second option")
    @app_commands.describe(option3="Third option (optional)")
    async def create_vote(self, interaction: discord.Interaction, question: str, option1: str, option2: str, option3: Optional[str] = None):
        await interaction.response.defer()
        vote_id = len(self.vote_data) + 1
        options = [option1, option2]
        if option3:
            options.append(option3)

        self.vote_data[vote_id] = {
            "question": question,
            "options": options,
            "votes": {opt: 0 for opt in options}
        }
        self.save_vote_data()

        options_text = "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(options)])
        
        view = VoteView(vote_id, options, self)
        
        await interaction.followup.send(f"Vote #{vote_id} created!\n**{question}**\n{options_text}", view=view)

    @app_commands.command(name="results", description="View results of a poll")
    @app_commands.describe(vote_id="The ID of the vote")
    async def results(self, interaction: discord.Interaction, vote_id: int):
        await interaction.response.defer()
        if vote_id not in self.vote_data:
            await interaction.followup.send("Vote ID not found.")
            return

        results = self.vote_data[vote_id]["votes"]
        options = list(results.keys())
        votes = list(results.values())

        # Generate pie chart
        fig, ax = plt.subplots()
        ax.pie(votes, labels=options, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Save the pie chart to a file
        chart_filename = f'vote_{vote_id}_results.png'
        plt.savefig(chart_filename)
        plt.close()

        # Create embed message
        embed = discord.Embed(title=f"Results for Vote #{vote_id}", description=self.vote_data[vote_id]["question"])
        for opt, count in results.items():
            embed.add_field(name=opt, value=f"{count} votes", inline=False)
        
        # Attach the pie chart image to the embed
        file = discord.File(chart_filename, filename=chart_filename)
        embed.set_image(url=f"attachment://{chart_filename}")

        await interaction.followup.send(embed=embed, file=file)

        # Clean up the file after sending the message
        os.remove(chart_filename)

class VoteButton(discord.ui.Button):
    def __init__(self, vote_id, option, cog):
        super().__init__(label=option, style=discord.ButtonStyle.primary)
        self.vote_id = vote_id
        self.option = option
        self.cog = cog

    async def callback(self, interaction: discord.Interaction):
        if self.vote_id not in self.cog.vote_data:
            await interaction.response.send_message("Vote ID not found.", ephemeral=True)
            return

        if self.option not in self.cog.vote_data[self.vote_id]["options"]:
            await interaction.response.send_message("Invalid option.", ephemeral=True)
            return

        # 票數增加
        self.cog.vote_data[self.vote_id]["votes"][self.option] += 1
        self.cog.save_vote_data()

        await interaction.response.send_message(f"Your vote for '{self.option}' has been counted.", ephemeral=True)

class VoteView(discord.ui.View):
    def __init__(self, vote_id, options, cog):
        super().__init__(timeout=None)
        for option in options:
            self.add_item(VoteButton(vote_id, option, cog))

async def setup(bot: commands.Bot):
    await bot.add_cog(Vote(bot))