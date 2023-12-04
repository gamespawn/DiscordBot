# music.py
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.MAX_QUEUE = 10

    @commands.command()
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        if channel:
            print(f"\nChannel ID: {channel.id}")
            await channel.connect(reconnect=False)
        else:
            await ctx.send('You are not in a VC right now!')

    @commands.command()
    async def play(self, ctx, url):
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        voice = ctx.voice_client
        
        if(not voice):
            await ctx.send("You are not in a vocie channel right now!")
            return
        
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            player = info['url']
            async with ctx.typing():
                if not voice.is_playing() and not self.queue:
                    self.start_playing(voice, player)
                    await ctx.send(f':mag_right: **Searching for** ``' + url + '``\n<:youtube:763374159567781890> **Now Playing:** ``{}'.format(info["title"]) + "``")

                elif len(self.queue) < self.MAX_QUEUE:
                    self.queue.append((player, info["title"]))
                    await ctx.send(f':mag_right: **Searching for** ``' + url + '``\n<:youtube:763374159567781890> **Added to queue:** ``{}`` \n**Position #{}'.format(info["title"], str(len(self.queue))))
                
                else:
                    await ctx.send(":mag_right: The queue is full right now, please wait for the current song to finish")
    # command to resume voice if it is paused
    @commands.command()
    async def resume(self, ctx):
        voice = ctx.voice_client

        if(not voice):
            await ctx.send("You are not in a vocie channel right now!")
            return

        if not voice.is_playing():
            voice.resume()
            await ctx.send('Bot is resuming')


    # command to pause voice if it is playing
    @commands.command()
    async def pause(self, ctx):
        voice = ctx.voice_client

        if(not voice):
            await ctx.send("You are not in a vocie channel right now!")
            return

        if voice.is_playing():
            voice.pause()
            await ctx.send('Bot has been paused')


    # command to stop voice
    @commands.command()
    async def skip(self, ctx, amount=1):
        voice = ctx.voice_client

        if(not voice):
            await ctx.send("You are not in a vocie channel right now!")
            return

        if voice.is_playing():
            voice.stop()
            await ctx.send(f"Skipping the next {f'{amount} songs' if amount > 1 else 'song'}")
            amount -= 1
        
        if(amount <= len(self.queue)):
            self.queue = [] if amount == len(self.queue) else self.queue[amount:]
            

    @commands.command()
    async def queue(self, ctx):
        if not self.queue:
            await ctx.send("The queue is empty.")
        else:
            queue_info = "\n".join([f"{index + 1}. {title}" for index, (_, title) in enumerate(self.queue)])
            await ctx.send(f"Current Queue:\n{queue_info}")

    def start_playing(self, voice_client, player):
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        voice_client.play(FFmpegPCMAudio(player, **FFMPEG_OPTIONS), after=lambda e: self.play_next())

    def play_next(self):
        if self.queue:
            player = self.queue.pop(0)[0]
            voice_client = self.bot.voice_clients[0]  # Assuming there is only one voice client
            self.start_playing(voice_client, player)

# The setup function remains unchanged
async def setup(bot):
    await bot.add_cog(Music(bot))