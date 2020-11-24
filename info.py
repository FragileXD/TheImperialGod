import discord
from discord.ext import commands
import traceback
import random
import datetime
import json

class Information(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Information is ready")
    
    @commands.command(aliases = ["guild", "guildinfo", "si"])
    async def serverinfo(self, ctx):
        findbots = sum(1 for member in ctx.guild.members if member.bot)
        roles = sum(1 for role in ctx.guild.roles)
        
        embed = discord.Embed(title = 'Infomation about ' + ctx.guild.name + '.', colour = ctx.author.color)
        embed.set_thumbnail(url = str(ctx.guild.icon_url))
        embed.add_field(name = "Guild's name: ", value = ctx.guild.name)
        embed.add_field(name = "Guild's owner: ", value = str(ctx.guild.owner))
        embed.add_field(name = "Guild's verification level: ", value = str(ctx.guild.verification_level))
        embed.add_field(name = "Guild's id: ", value = str(ctx.guild.id))
        embed.add_field(name = "Guild's member count: ", value = str(ctx.guild.member_count))
        embed.add_field(name="Bots", value=findbots, inline=True)
        embed.add_field(name = "Guild created at: ", value = str(ctx.guild.created_at.strftime("%a, %d %B %Y, %I:%M %p UTC")))
        embed.add_field(name = "Number of Roles:", value = f"`{roles}`")
        await ctx.send(embed =  embed)
    
    @commands.command(aliases = ["ci"])
    async def channelinfo(self, ctx, channel : discord.TextChannel = None):
        if channel == None:
            channel = ctx.channel
        nsfw = self.bot.get_channel(channel.id).is_nsfw()
        news = self.bot.get_channel(channel.id).is_news()
        embed = discord.Embed(title = 'Channel Infromation: ' + str(channel),
        colour = discord.Colour.from_rgb(54, 151, 255))
        embed.add_field(name = 'Channel Name: ', value = str(channel.name))
        embed.add_field(name = "Channel's NSFW Status: ", value = str(nsfw))
        embed.add_field(name = "Channel's id: " , value = str(channel.id))
        embed.add_field(name = 'Channel Created At: ', value = str(channel.created_at.strftime("%a, %d %B %Y, %I:%M %p UTC")))
        embed.add_field(name = 'Channel Type: ', value = str(channel.type))
        embed.add_field(name = "Channel's Announcement Status: ", value = str(news))
        await ctx.send(embed = embed)
    
    @commands.command()
    async def userinfo(self, ctx, member : discord.Member = None):
        if member == None:
            member = ctx.author
        pos = sum(m.joined_at < member.joined_at for m in ctx.guild.members if m.joined_at is not None)
        roles = [role for role in member.roles]
        embed = discord.Embed(color=member.color, timestamp=datetime.datetime.utcnow())
        embed.set_author(name=f"{member}", icon_url=member.avatar_url)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Joined at:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p"))
        embed.add_field(name='Registered at:', value=member.created_at.strftime('%a, %#d %B %Y, %I:%M %p'))
        embed.add_field(name='Bot?', value=f'{member.bot}')
        embed.add_field(name='Status?', value=f'{member.status}')
        embed.add_field(name='Top Role?', value=f'{member.top_role}')
        embed.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles[:1]]))
        embed.add_field(name='Join position', value=pos)
        embed.set_footer(icon_url=member.avatar_url, text=f'Requested By: {ctx.author.name}')
        await ctx.send(embed=embed)

    @commands.command()
    async def whois(ctx, member : discord.Member = None):
        if member == None:
            member = ctx.author
        em = discord.Embed(title = member.name, color = member.color)
        em.add_field(name = "ID:", value = member.id)
        em.set_thumbnail(url = member.avatar_url)
        await ctx.send(embed = em)
    
    
    @commands.command()
    async def botinfo(ctx):
        with open("./data/emojis.json", "r") as f:
            emojis = json.load(f)
        embed = discord.Embed(title = "Botinfo", color = ctx.author.color,
        description = "TheImperialGod, is an awesome customizable discord bot with awesome features. Check some information about the bot below!"
        )
        embed.add_field(name = "First went live on:", value = "1 / 10 / 2020")
        embed.add_field(name = "Started coding on:", value = "26 / 9 / 2020")
        embed.add_field(name = f"Creator", value = f"NightZan999#0194 {emojis["fun"]}")
        embed.add_field(name = 'Hosting', value = f"DanBot Hosting {emojis["success"]}")
        embed.add_field(name = "Servers:", value = f'`{len(client.guilds)}` {emojis["fail"]} ')
        embed.add_field(name = 'Customizable Settings:', value = f"Automoderation and utilities! {emojis["success"]}")
        embed.add_field(name = "Database:", value = "SQLite3")
        try:
            embed.add_field(name = "Users:", value = f'`{len(client.users)}`')
        except:
            pass
        finally:
            embed.add_field(name = "Website:", value = "https://theimperialgod.herokuapp.com\nNOTE: not hosted yet!")
            embed.add_field(name = "Number of Commands:", value = f"`62` (including special owner commands)")
            embed.add_field(name = "**Tech:**", value = "```+ Library : discord.py\n+ Database : SQLite3\n+ Hosting Services : DanBot Hosting!\n```", inline = False)
            await ctx.send(embed = embed)


def setup(client):
    client.add_cog(Information(client))