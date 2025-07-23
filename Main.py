import discord, os
from discord.ext import commands
from discord import Intents
from dotenv import load_dotenv



class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="/",
            intents = discord.Intents.all()
        )
        
    async def startup(self):
        await self.wait_until_ready()
        await self.tree.sync() 
        print('Sucessfully synced applications commands')
        print(f'Connected as {bot.user}')
    
    async def setup_hook(self):
        print("A")
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")
        
        self.loop.create_task(self.startup())
    
    
    async def send(self, channel_id:int, message=False, embed=False):
        channel = self.get_channel(channel_id)
        if message:
            await channel.send(message)
        if embed:
            await channel.send(embed=embed)
            
            
    #이벤트
    async def on_ready(self):
        print(f"{self.user.name}으로 로그인")

        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Game("봇 테스트")
        )
        
    #async def on_member_join(self, ctx):
    #    print(ctx.avatar)
    #    embed = discord.Embed(title=f"{ctx.name} 입장", colour=0x00ff00)
    #    embed.add_field(name="계정 생성 날짜", value=f"{ctx.created_at}", inline=False)
    #    embed.set_thumbnail(url=ctx.avatar_url)
    #    await self.send(1222165949667606548, message=ctx.mention)
    #    await self.send(1222165949667606548, embed=embed)
    
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    
intents = Intents()
bot = Bot()
bot.run(DISCORD_TOKEN)

