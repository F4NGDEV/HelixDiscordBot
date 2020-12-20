import discord
from discord.ext import commands,tasks
from json import load,dump
import configure
import os

class Commands(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    #COMMANDS
    @commands.command()
    async def ping(self,ctx):
        await ctx.send(f"Pong ! Latency is `{round(self.client.latency*1000 )}` ms")


    @commands.command()
    async def say(self,ctx,*,message):
        await ctx.send(message)


    @commands.command()
    @commands.guild_only()
    async def avatar(self, ctx, *,  avamember : discord.Member =None):
        if avamember == None:
            avamember = ctx.author
        member_embed = discord.Embed(title = f"Avatar of {avamember.display_name}",colour = discord.Color.blue())
        userAvatarUrl = avamember.avatar_url
        member_embed.set_image(url=userAvatarUrl)
        member_embed.set_footer(text=f"Requested by {ctx.author}")
        await ctx.send(embed=member_embed)



    @commands.command()
    @commands.guild_only()
    async def help(self,ctx):
        with open(os.path.join("db","help.json"),encoding="utf8") as f:
            help_json = load(f)
            moderation_embed = discord.Embed(title="Moderation Commands",colour=discord.Color.blue())
            for command,desc in help_json["Moderation Commands"].items():
                moderation_embed.add_field(name=str(command),value=desc,inline=False)

            commands_embed = discord.Embed(title="Commands",colour=discord.Color.blue())
            for command,desc in help_json["Commands"].items():
                commands_embed.add_field(name=str(command),value=desc,inline=False)

            tags_embed = discord.Embed(title="Tags",colour=discord.Color.blue())
            for command,desc in help_json["Tags"].items():
                tags_embed.add_field(name=str(command),value=desc,inline=False)

        try:
            await ctx.author.send(f"Prefixes - {configure.PREFIX}") 
            await ctx.author.send(embed=commands_embed)
            await ctx.author.send(embed=moderation_embed)
            await ctx.author.send(embed=tags_embed)
            await ctx.send("Help sent in DMs")

        except:
            await ctx.author.send(f"Prefixes - {configure.PREFIX}") 
            await ctx.author.send(embed=commands_embed)
            await ctx.author.send(embed=moderation_embed)

    @commands.command()
    async def newmeet(self,ctx):
        await ctx.send("https://meet.google.com/new")


    @commands.command()
    @commands.guild_only()
    async def suggest(self,ctx,*,suggestion):
        suggester = ctx.author
        suggest_embed = discord.Embed(title="Suggestion",colour=discord.Color.blue())
        suggest_embed.description = suggestion
        suggest_embed.set_author(name=suggester.display_name,icon_url=suggester.avatar_url)
        await ctx.message.delete()
        msg = await ctx.send(embed=suggest_embed)
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")
    


    @commands.command()
    async def invite(self,ctx):
        invite = discord.utils.oauth_url(self.client.user.id, discord.Permissions(permissions=2147483639))
        invite_embed= discord.Embed(title="Invite",colour=discord.Color.blue())
        invite_embed.description=f"[Add to your server]({invite})"
        await ctx.send(embed=invite_embed)
    


    @commands.command()
    @commands.is_owner()
    async def log(self,ctx):
        await ctx.send(file=discord.File("log.txt"))

    @commands.command()
    @commands.is_owner()
    async def clrlog(self,ctx):
        with open("log.txt","w") as f:
            f.write("")
            
        await ctx.send("Log cleared")
    
     
    




def setup(client):
    client.add_cog(Commands(client))