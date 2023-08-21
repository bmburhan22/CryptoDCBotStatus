import os, discord, json
from discord.http import aiohttp
from discord.ext import tasks
from dotenv import load_dotenv

load_dotenv()
# from keep_alive import keep_alive

CRYPTO_TOKEN = '0x088bebef4e371757509e64d3508b6da6f376e2ac'
BOT_TOKEN = os.getenv('BOT_TOKEN')
SERVER_ID = int(os.getenv('SERVER_ID'))
bot = discord.Client()

@bot.event
async def on_ready():
    
    print('Bot started')
    # while True:
    #     try:
    #         pricedata = get('https://api.pancakeswap.info/api/v2/tokens/'+CRYPTO_TOKEN).json()['data']
    #         nick = pricedata['symbol']+' $'+str(round(float(pricedata['price']), 4))
    #         print(nick)


    #         # activity = discord.Activity(type=discord.ActivityType.watching, name='$ '+pricedata['price'])
    #         await bot.change_presence(status=discord.Status.idle)#, activity=activity)
    #         guild = bot.get_guild(int(SERVER_ID))
    #         await guild.me.edit(nick=nick)
    #     except Exception as err:
    #         print(err)
    #     finally:
    #         sleep(60)

@tasks.loop(seconds=60)
async def update_nick():

    try:
        await bot.wait_until_ready()
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://api.pancakeswap.info/api/v2/tokens/'+CRYPTO_TOKEN) as r:
                pricedata = await r.json()
                nick = pricedata['data']['symbol']+' $'+str(round(float(pricedata['data']['price']), 4))
                print(nick)
                # activity = discord.Activity(type=discord.ActivityType.watching, name='$ '+pricedata['price'])
                # await bot.change_presence(status=discord.Status.idle)#, activity=activity)

                guild = bot.get_guild(id=SERVER_ID)

                await guild.me.edit(nick=nick)
    except Exception as err:
        print(err)


# keep_alive()
update_nick.start()

bot.run(BOT_TOKEN)