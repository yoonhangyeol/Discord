import discord, datetime, sys
sys.path.append("./")
from discord.ext import commands
from discord.app_commands import Group
import Main

class money(commands.Cog):
    util_group = Group(name="money", description="돈에 관련된 명령어들을 지원합니다.")
    def __init__(self, bot: Main.Bot):
        self.Dbcord = bot.DB
        
    @util_group.command(description="마치 노숙자처럼 바닥에 돈이 있는지 살펴봅니다.")
    async def search(self, interaction: discord.Interaction):
        collection = self.Dbcord.Discord["User"]
        user_id = interaction.user.id
        if collection.count_documents({"name" : user_id}):
            if (datetime.datetime.now() - collection.find_one({"name" : user_id})["cooltime"]).total_seconds() >= 300:
                collection.update_one({"name" : user_id}, {"$set" :
                    {"money" : collection.find_one({"name" : user_id})["money"] + 50, "cooltime" : datetime.datetime.now()}
                })
            else:
                cooltime = collection.find_one({"name" : user_id})["cooltime"]
                now = datetime.datetime.now()
                delta = datetime.timedelta(seconds=300)
                seconds_remaining = cooltime - now + delta
                minutes, seconds = divmod(seconds_remaining.total_seconds(), 60)
                await interaction.response.send_message(f'땅바닥에서 돈을 찾지 못했습니다... (잔여 쿨타임 : {int(minutes)}.{int(seconds)})')
                return
        else:
            collection.insert_one({"name" : user_id, "money" : 50, "cooltime" : datetime.datetime.now()})
        await interaction.response.send_message('땅바닥에서 돈을 발견했습니다! (+50원)')

class status(commands.Cog):
    util_group = Group(name="status", description="자신의 정보를 확인합니다.")
    def __init__(self, bot: Main.Bot):
        self.Dbcord = bot.DB
        
    @util_group.command(description="전체적인 정보를 확인합니다.")
    async def all(self, interaction: discord.Interaction):
        collection = self.Dbcord.Discord["User"]
        user = interaction.user
        embed = discord.Embed(title=f"{user.name}", colour=0x00ff00)
        embed.add_field(name="계정 생성 날짜", value=f"{user.created_at.year}.{user.created_at.month}.{user.created_at.day}", inline=False)
        embed.add_field(name="서버 참가 날짜", value=f"{user.joined_at.year}.{user.joined_at.month}.{user.joined_at.day}", inline=False)
        if collection.count_documents({"name" : user.id}):
            embed.add_field(name="돈", value=f"{collection.find_one({'name' : user.id})['money']}", inline=False)
        embed.set_thumbnail(url=user.avatar.url)
        await interaction.response.send_message(embed=embed)
            
class reload(commands.Cog):
    util_group = Group(name="reload", description="Cog 파일을 재로딩합니다.")
    def __init__(self, bot: commands.bot):
        self.bot = bot
        
    @util_group.command(description="Cog 파일을 재로딩합니다.")
    async def reload(self, interaction: discord.Interaction):
        print("Reloading....")
        try:
            await self.bot.reload_extension("cogs.cog")
            print("Complete!")
            await interaction.response.send_message('재로드에 성공했습니다~!')
        except Exception as e:
            await interaction.response.send_message("재로드에 실패했습니다..")
            await interaction.response.send_message(f"오류 내용 : {e}")
            print("Fail..")

async def setup(bot: Main.Bot):
    await bot.add_cog(money(bot))
    await bot.add_cog(status(bot))
    await bot.add_cog(reload(bot))