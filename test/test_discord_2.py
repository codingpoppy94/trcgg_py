from fastapi import FastAPI
import discord
from discord.ext import commands
import asyncio
import uvicorn

TOKEN = 'mytoken'
CHANNEL_ID = '1221998721693388851'

# FastAPI 인스턴스 생성
app = FastAPI()

# Intents 설정
intents = discord.Intents.default()
intents.message_content = True  # message_content intent가 필요합니다.

# Discord 봇 설정
bot = commands.Bot(command_prefix='!', intents=intents)

# 봇이 준비되었을 때 실행되는 코드
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# !ping 명령어에 대한 응답 코드
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

# FastAPI 엔드포인트 추가
@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.post("/send-message/")
async def send_message(channel_id: int, message: str):
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(message)
        return {"status": "success", "message": f"Message sent to channel {channel_id}"}
    else:
        return {"status": "error", "message": "Channel not found"}

# 디스코드 봇과 FastAPI 서버를 동시에 실행하기 위한 코드
def start_bot():
    loop = asyncio.get_event_loop()
    loop.create_task(bot.start('mytoken'))
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    start_bot()


# bot.run('mytoken')