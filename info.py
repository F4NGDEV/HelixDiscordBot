import discord

from discord.ext import commands,tasks
from datetime import datetime,timedelta
start_time = datetime.now()
start_time = start_time.strftime('%H:%M:%S')

class Info(commands.Cog):
    def __init__(self,client):
        self.client = client
     
    #COMMANDS
    @commands.command()
    @commands.guild_only()
    async def serverinfo(self,ctx):
        member_count=0
        guild = self.client.get_guild(ctx.guild.id)
        text = [channel for channel in guild.channels if channel.type == discord.ChannelType.text]
        voice = [channel for channel in guild.channels if channel.type == discord.ChannelType.voice]


        server_info_embed = discord.Embed(title=guild.name,colour=discord.Color.blue())
        server_info_embed.add_field(name="Created on",value=guild.created_at.strftime("%d %b %Y %H:%M"))
        server_info_embed.add_field(name="Server Region",value=str(guild.region).title())
        if "COMMUNITY" in guild.features:

            server_info_embed.add_field(name="Type",value="Community")
        else:
            server_info_embed.add_field(name="Type",value="Personal")
        server_info_embed.add_field(name="Server Owner",value=str(guild.owner.mention).title())
        server_info_embed.add_field(name="Members",value=guild.member_count)
        server_info_embed.add_field(name="Role Count",value=len(guild.roles)-1)
        server_info_embed.add_field(name="Categories",value=len(guild.categories)) 
        server_info_embed.add_field(name="Text Channels",value=len(text))
        server_info_embed.add_field(name="Voice Channels ",value=len(voice))

        
        role_list = []
        roles = guild.roles[::-1]
        for role in roles[:-1]:
            role_list.append(f"{role.mention} ")

        server_info_embed.add_field(name="Roles",value="".join(role_list))

        
        try:
            
            invite = await ctx.channel.create_invite(max_age = 1000)
            server_info_embed.add_field(name="Invite",value=invite,inline=False)


        except:
            pass
        


        server_info_embed.set_footer(text=f"Requested by {ctx.author} | Server ID : {ctx.guild.id}")
        server_info_embed.set_thumbnail(url=guild.icon_url)

        await ctx.send(embed=server_info_embed)


 
    @commands.command()
    async def info(self,ctx):
        name = ctx.me.name
        command_time = datetime.now()
        command_time = command_time.strftime('%H:%M:%S')
        FMT = '%H:%M:%S'
        uptime = datetime.strptime(command_time, FMT) - datetime.strptime(start_time, FMT)

        if uptime.days < 0:
            tdelta = timedelta(days=0,
                seconds=uptime.seconds, microseconds=uptime.microseconds)

        invite = discord.utils.oauth_url(self.client.user.id, discord.Permissions(permissions=2147483639))
        
       
        info_embed = discord.Embed(title=name,colour=discord.Color.blue())
        info_embed.set_thumbnail(url=ctx.me.avatar_url)
        info_embed.add_field(name="Creator",value="[Fang](https://www.youtube.com/channel/UCjnf3KoodS1gFb0IXB-jK1A)") #add git link
        info_embed.add_field(name="Source",value="[Github](https://github.com/F4NGDEV/helix)")
        info_embed.add_field(name="Servers",value=str(len(self.client.guilds)))
        info_embed.add_field(name="Uptime",value=uptime)
        info_embed.add_field(name="Library",value="[Discord.py](https://github.com/Rapptz/discord.py)")
        info_embed.add_field(name="Invite",value=f"[Add to your server]({invite})",inline=False)
        info_embed.set_footer(text=f"Requested by {ctx.author}")

        await ctx.send(embed=info_embed)


    @commands.command() 
    @commands.guild_only()
    async def userinfo(self,ctx,member : discord.Member=None):
        if member == None:
            member=ctx.author

        user_info_embed = discord.Embed(title=str(member),colour=discord.Color.blue())
        user_info_embed.set_thumbnail(url=member.avatar_url)



        user_info_embed.add_field(name="Joined Discord on",value=member.created_at.strftime("%d %b %Y %H:%M"))
        user_info_embed.add_field(name="Joined Server on",value=member.joined_at.strftime("%d %b %Y %H:%M"))

        if member.bot:
            user_info_embed.add_field(name="Type",value="Bot",inline=False)
        else:
            user_info_embed.add_field(name="Type",value="User",inline=False)
        
        user_info_embed.add_field(name="Status",value=str(member.status).title())

        try:
            user_info_embed.add_field(name="Activity",value=member.activities[0].name)
        except:
            pass
        


        
        if len(member.roles)>1:
            role_list = []
            roles = member.roles[::-1]
            for role in roles[:-1]:
                role_list.append(f"{role.mention} ")

            user_info_embed.add_field(name=f"Roles ({len(member.roles)-1})",value="".join(role_list),inline=False)

        user_info_embed.set_footer(text=f"Requested by {ctx.author} | Member ID : {member.id}")

        await ctx.send(embed=user_info_embed)
    


def setup(client):
    client.add_cog(Info(client))