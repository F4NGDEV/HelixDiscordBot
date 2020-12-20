import discord
from discord.ext import commands



class Moderation(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    #COMMANDS   
    
    @commands.command(aliases=["clear"])
    @commands.guild_only()
    @commands.has_permissions(manage_messages = True)
    async def purge(self,ctx,amount : int):
        await ctx.channel.purge(limit=amount+1)


    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def warn(self,ctx,member : discord.Member,*,reason):
        await ctx.message.delete()
        dm_embed = discord.Embed(title="Warn",colour=discord.Color.gold())
        dm_embed.description = f"You have been warned in {ctx.guild.name} for {reason}"
        try:
            await member.send(embed=dm_embed)
            warn_embed = discord.Embed(title="Moderation",colour=discord.Color.gold())
            warn_embed.add_field(name="Warn",value=f"{member.mention} has been warned, Reason - {reason}")
            await ctx.send(embed=warn_embed)
        
        except:
            await ctx.send("Couldn't send a DM")

        

        


        
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self,ctx,member : discord.Member,*,reason="Not Provided"):
        if member != ctx.author:
            await member.kick(reason=reason)
            kick_embed = discord.Embed(title='Moderation', colour=discord.Colour.red())
            kick_embed.add_field(name="Kick",value=f"{member.mention} has been kicked, Reason - {reason}")
            await ctx.send(embed = kick_embed)
            try:
                dm_kick = discord.Embed(title="Kick",colour=discord.Color.red())
                dm_kick.description = f"You have been kicked from {ctx.guild.name} for {reason}"
                await member.send(embed=dm_kick)
            except:
                pass
        else:
            await ctx.send(f"{ctx.author.mention} You cannot kick yourself")




    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self,ctx,member : discord.Member,*,reason="Not Provided"):
        if member != ctx.author:
            await member.ban(reason=reason)
            ban_embed = discord.Embed(title='Moderation', colour=discord.Colour.red())
            ban_embed.add_field(name="Ban",value=f"{member.mention} has been banned, Reason - {reason}")
            await ctx.send(embed = ban_embed)
            try:
                dm_ban = discord.Embed(title="Ban",colour=discord.Color.red())
                dm_ban.description = f"You have been banned from {ctx.guild.name} for {reason}"
                await member.send(embed=dm_ban)
            except:
                pass
        else:
            await ctx.send(f"{ctx.author.mention} You cannot ban yourself")


    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self,ctx,member):
        banned_users = await ctx.guild.bans()
        found = False
        try:
            member_name,member_id = member.split("#")
        except ValueError:
            id_error = discord.Embed(title='Moderation', colour=discord.Colour.red())
            id_error.add_field(name="Unban",value=f"Please enter a discriminator")
            await ctx.send(embed = id_error)
            return

        if member_id.isnumeric() == False or len(member_id) >4:
            discrimiator_error = discord.Embed(title='Moderation', colour=discord.Colour.red())
            discrimiator_error.add_field(name="Unban",value=f"Please enter a proper discriminator")
            await ctx.send(embed = discrimiator_error)
            return

        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name,user.discriminator) == (member_name,member_id):
                await ctx.guild.unban(user)
                unban_embed = discord.Embed(title='Moderation', colour=discord.Colour.green())
                unban_embed.add_field(name="Unban",value=f"{user.mention} has been unbanned")
                await ctx.send(embed = unban_embed)
                found = True
                return
                    

        if found == False:
            Notfound_embed = discord.Embed(title='Moderation', colour=discord.Colour.red())
            Notfound_embed.add_field(name="Unban",value=f"{member} not found")
            await ctx.send(embed = Notfound_embed)
            return

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages = True) 
    async def mute(self,ctx,member : discord.Member):
        if member != ctx.author:

        

            role = discord.utils.get(ctx.guild.roles, name="Muted")

            if role not in member.roles:

                muted_embed = discord.Embed(title="Moderation",colour=discord.Color.red())
                muted_embed.add_field(name="Mute",value=f"{member.mention} has been muted")

                if role == None:
                    muted = await ctx.guild.create_role(name="Muted")
                    for channel in ctx.guild.channels: 
                        await channel.set_permissions(muted, send_messages=False)
                        await member.add_roles(muted) 

                    await ctx.send(embed=muted_embed)

                else:
                    await member.add_roles(role)
                    await ctx.send(embed=muted_embed)
            else:
                await ctx.send(f"{member.mention} is already muted")
            
        else:
            await ctx.send(f"{ctx.author.mention} You cannot mute yourself")




    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages = True)
    async def unmute(self,ctx,member : discord.Member):

    
        if member != ctx.author:

        

            role = discord.utils.get(ctx.guild.roles, name="Muted")

            if role in member.roles:

                unmuted_embed = discord.Embed(title="Moderation",colour=discord.Color.green())
                unmuted_embed.add_field(name="Mute",value=f"{member.mention} has been unmuted")


                await member.remove_roles(role)
                await ctx.send(embed=unmuted_embed)



            else:
                await ctx.send(f"{member.mention} is already unmuted")
            
        else:
            await ctx.send(f"{ctx.author.mention} You cannot unmute yourself")


        
    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def announce(self,ctx,*,announcement):
        await ctx.message.delete()
        try:
            title = announcement.split("~~")[0]
            message = announcement.split("~~")[1]

        except:
            await ctx.send("Error! Invalid Format | Format : >announce title~~message")
            return

        announcement_embed = discord.Embed(title=title,colour=discord.Colour.blue())
        announcement_embed.description = message
        announcement_embed.set_footer(text=f"Announcement by {ctx.author}")
        msg = await ctx.send(embed = announcement_embed)
        await msg.add_reaction("👍")

def setup(client):
    client.add_cog(Moderation(client))
