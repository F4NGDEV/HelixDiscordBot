import discord
from discord.ext import commands
import configure
from json import load,dump
from datetime import date
import os

class Tags(commands.Cog):
    def __init__(self,client):
        self.client = client



    @commands.command()
    @commands.guild_only()
    async def tag(self,ctx,name):
        with open(os.path.join("db","tags.json"),encoding="utf8") as f:
            data = load(f)

        try:
            content = data[str(ctx.guild.id)][name]["content"]
            await ctx.send(content)
        except KeyError:
            await ctx.send(f"Tag named `{name}` not found")

        

    @commands.command()
    @commands.guild_only()
    async def newtag(self,ctx,name,*,content):
        with open(os.path.join("db","tags.json"),encoding="utf8") as f:
            data = load(f)
            new_server = True
            for server in data.keys():
                if str(ctx.guild.id) == server:
                    new_server = False
                    break
        
        if new_server:

            data[ctx.guild.id] = {
                name:{

                    "content" : content,
                    "author" : str(ctx.author),
                    "date" : date.today().strftime("%B %d, %Y")

                }

            }


            with open(os.path.join("db","tags.json"),"w",encoding="utf8") as f:
                dump(data,f,indent=4)
                await ctx.send("Tag created successfully")
        else:
            with open(os.path.join("db","tags.json"),encoding="utf8") as f:
                data = load(f)

                if name in data[str(ctx.guild.id)].keys():
                    await ctx.send(f"Tag named `{name}` already exists")
                else:
                    data[str(ctx.guild.id)][name] = {
                        
                        "content" : content,
                        "author" : str(ctx.author),
                        "date" : date.today().strftime("%B %d, %Y")




                    }
                    with open(os.path.join("db","tags.json"),"w",encoding="utf8") as f:
                        dump(data,f,indent=4)
                        await ctx.send("Tag created successfully")
    
                
                    

    @commands.command()
    @commands.guild_only()
    async def deltag(self,ctx,name):
        with open(os.path.join("db","tags.json"),encoding="utf8") as f:
            data = load(f)
            try:
                if data[str(ctx.guild.id)][name]["author"] == str(ctx.author) or ctx.author.guild_permissions.manage_messages == True:

                    try:
                        del data[str(ctx.guild.id)][name]

                        await ctx.send("Tag deleted successfully")

                        with open(os.path.join("db","tags.json"),"w",encoding="utf8") as f:
                            dump(data,f,indent=4)
                    except KeyError:

                        await ctx.send(f"Tag named `{name}` not found")

                else:
                    missing_permissions_embed = discord.Embed(title='Error', colour=discord.Colour.red())
                    missing_permissions_embed.description=f"You do not have permission to use that command"
                    await ctx.send(embed=missing_permissions_embed)
            except KeyError:
                await ctx.send("There are no tags for this server")
                    
            


    @commands.command()
    @commands.guild_only()
    async def taginfo(self,ctx,name):
        with open(os.path.join("db","tags.json"),encoding="utf8") as f:
            data = load(f)
        try:
            author = data[str(ctx.guild.id)][name]["author"]
            date = data[str(ctx.guild.id)][name]["date"]

            tag_info_embed = discord.Embed(title=name,colour=discord.Color.blue())
            tag_info_embed.add_field(name="Author",value=author)
            tag_info_embed.add_field(name="Created on",value=date)
            await ctx.send(embed=tag_info_embed)
        except KeyError:
            await ctx.send("Tag not found")
                    
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def cleartags(self,ctx):
            with open(os.path.join("db","tags.json"),encoding="utf8") as f:
                data = load(f)

                try:
                    data[str(ctx.guild.id)] = {}
                    with open(os.path.join("db","tags.json"),"w",encoding="utf8") as f:
                            dump(data,f,indent=4)
                except KeyError:
                    await ctx.send("There are no tags for this server")
def setup(client):
    client.add_cog(Tags(client))
