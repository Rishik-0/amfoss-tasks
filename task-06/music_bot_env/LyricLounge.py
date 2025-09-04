import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import requests
from discord import File

userplaylist = {}

load_dotenv()
token = os.getenv('DISCORD_BOT_TOKEN')


handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ')

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server, {member.name}!") 


@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")




@bot.command()
async def lyrics(ctx,*,query:str):
    try:
        song, artist = [s.strip() for s in query.split('-')]
        song = song.replace(' ','+')
        artist = artist.replace(' ','+')
    except ValueError:
        return await ctx.send("Use format: /lyrics <song> - <artist>")
    
    url = f"https://lrclib.net/api/search?track_name={song}&artist_name={artist}"
    
    response = requests.get(url)
    if response.status_code != 200:
        return await ctx.send("Failed to fetch lyrics.")
    data = response.json()
    if not data:
        return await ctx.send("No lyrics found for that track.")
    lyrics = data[0].get('plainLyrics',"Lyrics not found")
    if len(lyrics) <= 1900:
        await ctx.send(lyrics)
    else:
        file_name = "lyrics.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(lyrics)
        await ctx.send(file=File(file_name))
        os.remove(file_name)

@bot.command()
async def track(ctx,*,query:str):
    try:
        song,artist = [s.strip() for s in query.split('-')]
        song = song.replace(' ','+')
        artist = artist.replace(' ','+')
    except ValueError:
        return await ctx.send("Use format: /track <song> - <artist>")
    
    url = f"https://musicbrainz.org/ws/2/recording/?query=recording:{song}+AND+artist:{artist}&inc=releases+tags&fmt=json"
    response = requests.get(url)
    if response.status_code != 200:
        return await ctx.send("Failed to fetch data.")
    data = response.json()
    if not data:
        return await ctx.send("No track found")
    recording =  data.get('recordings') 
        
    track = recording[0]
    print(track)
    title = track.get('title','None')
    await ctx.send(f"Title: {title}")
    length_ms = track.get('length',0)
    if length_ms != 0:
        track_length = length_ms//1000
    else:
        track_length =0
    await ctx.send(f"Duration: {track_length} seconds")
    artist_credit = track.get('artist-credit')
    artist_name = artist_credit[0]['name']
    await ctx.send(f"Artist: {artist_name}")
    
    release_date = track.get('first-release-date','unknown')
    await ctx.send(f"Release date: {release_date}")
    
    
    albums = track.get('releases', [])
    if albums:
        for album in albums:
            album_title = album.get('title', 'Unknown Album')
            
    else:
        await ctx.send("No album information available")
    await ctx.send(f"Album: {album_title}")



@bot.command()
async def playlist(ctx,action: str ,*, song: str = None):
    user_id = str(ctx.author.id)
    playlist = userplaylist.setdefault(user_id,[])

    if action == "add":
        if not song:
            return await ctx.send("Mention a song to be added.")
        playlist.append(song)
        await ctx.send(f"Added {song} to playlist..")

    elif action == "remove":
        if not song:
            return await ctx.send("Mention the song to be removed.")
        if song in playlist:
            playlist.remove(song)
            await ctx.send(f"Removed {song} from the playlist..")
        else:
            await ctx.send(f"{song} not in playlist..")
    elif action == "view":
        await ctx.send("...YOUR PLAYLIST...")
        n=1
        for i in playlist:
            await ctx.send(f"{n}. {i}")
            n+=1

    elif action == "clear":
        playlist.clear()
        await ctx.send("You playlist has been cleared..")

    else:
        await ctx.send("Use format: /playlist [add/remove/view/clear] [song]")



@bot.command()
async def help(ctx):

        
    await ctx.send("/lyrics <song> - <artist> ==> Fetches and displays song lyrics")
    await ctx.send("/track <song> - <artist> ==> Gets detailed track information including album, duration, and tags")
    await ctx.send("/playlist [add/remove/view/clear] [song] ==> Manage your personal playlist")
    await ctx.send("/help ==> for getting a list of the commands along with their description.")




    




bot.run(token, log_handler=handler, log_level=logging.DEBUG)