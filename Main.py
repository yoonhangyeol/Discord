import discord, os, certifi
from discord.ext import commands
from discord import Intents
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

class DB:
    Discord = None
    def __init__(self, MONGO_URI):
        try:
            self.Discord = MongoClient(MONGO_URI, server_api=ServerApi('1'), tlsCAFile=certifi.where())["Discord"]
            print(self.Discord.list_database_names())
        except Exception as e:
            print(f"DB 연결 실패: {e}")
    
    def whlog(self):
        '''
        유저가 등록과정을 거쳤는지 확인합니다.
        즉, 해당 id를 가진 사람이 DB에 속해있는지 확인합니다.
        반환 값은 그 id를 가진 플레이어의 DB입니다.
        '''

class Bot(commands.Bot):
    DB = None
    def __init__(self, MONGO_URI):
        super().__init__(
            command_prefix="/",
            intents = discord.Intents.all()
        )
        self.DB = DB(MONGO_URI)
        
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
MONGO_URI = os.getenv("MONGO_URI")
intents = Intents()
bot = Bot(MONGO_URI)
bot.run(DISCORD_TOKEN)

