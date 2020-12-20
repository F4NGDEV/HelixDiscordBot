import discord
from discord.ext import commands
import configure
import os
import traceback
import datetime


class Client:


        def __init__(self,token,prefix):
                        
                self.intents = discord.Intents.all()

                self.token = token
                self.prefix = prefix
                self.client = commands.Bot(command_prefix = self.prefix,
                case_insensitive=True, 
                intents=self.intents,
                activity=discord.Game(name=f"Hello there | {self.prefix[0]}help"),
                status=discord.Status.online)

                self.on_ready = self.client.event(self.on_ready)
                self.on_message = self.client.event(self.on_message)
                self.on_command_error = self.client.event(self.on_command_error)


 
             


        async def on_ready(self):

                

                #cogs loads
                for filename in os.listdir("cogs"):
                        if filename.endswith(".py"):
                                try:
                                        bot.client.load_extension(f"cogs.{filename[:-3]}")

                                        
                                except commands.ExtensionAlreadyLoaded:
                                        with open("log.txt","a") as f:
                                                f.write(f"INFO:BOT RESTARTED AT {datetime.datetime.now().strftime('%d %b %Y %H:%M')} LATENCY - {round(bot.client.latency*1000)} ms\n")
                                                break
                else:
                        with open("log.txt","a") as f:
                                f.write(f"INFO:BOT STARTED AT {datetime.datetime.now().strftime('%d %b %Y %H:%M')} LATENCY - {round(bot.client.latency*1000)} ms\n") 

 

        async def on_message(self,message):
                await self.client.process_commands(message)
                        
                if message.content.startswith(f"<@!{self.client.user.id}>"):
                        await message.channel.send(f"Prefixes - {self.prefix}")



        async def on_command_error(self,ctx,error):

                error = getattr(error, 'original', error)

                if isinstance(error,commands.MissingRequiredArgument):
                        missing_argument_embed = discord.Embed(title='Error', colour=discord.Colour.red())
                        missing_argument_embed.description=f"Required arguments not entered. Please pass all required arguments"
                        await ctx.send(embed = missing_argument_embed)


                elif isinstance(error,commands.CommandNotFound):
                        commandnotfound_embed = discord.Embed(title='Error', colour=discord.Colour.red())
                        commandnotfound_embed.description=f"The command you entered does not exist"
                        await ctx.send(embed = commandnotfound_embed)   


                elif isinstance(error,commands.MissingPermissions):
                        missing_permissions_embed = discord.Embed(title='Error', colour=discord.Colour.red())
                        missing_permissions_embed.description=f"You do not have permission to use that command"
                        await ctx.send(embed=missing_permissions_embed)


                elif isinstance(error,commands.MissingRole):
                        missing_role_embed = discord.Embed(title='Error', colour=discord.Colour.red())
                        missing_role_embed.description=f"You do not have permission to use that command"
                        await ctx.send(embed=missing_role_embed)
                        
                elif isinstance(error,discord.Forbidden):
                        missing_role_bot_embed = discord.Embed(title='Error', colour=discord.Colour.red())
                        missing_role_bot_embed.description=f"I do not have permission to perform the action"
                        await ctx.send(embed=missing_role_bot_embed)

                elif isinstance(error,commands.NoPrivateMessage):
                        await ctx.send("Direct Message is not supported for this command")

                elif isinstance(error,commands.BadArgument):
                        bad_argument_embed = discord.Embed(title='Error', colour=discord.Colour.red())
                        bad_argument_embed.description=f"Please enter a proper argument"
                        await ctx.send(embed=bad_argument_embed)

                elif isinstance(error,commands.NotOwner):
                        not_owner_embed = discord.Embed(title='Error', colour=discord.Colour.red())
                        not_owner_embed.description=f"You do not have permission to use that command"
                        await ctx.send(embed=not_owner_embed)
                
                else:
                        with open("log.txt","a") as f:
                                f.write(f"ERROR:EXCEPTION IN COMMAND {ctx.command}\n")
                                traceback.print_exception(type(error), error, error.__traceback__,file=f)

        

        def connect(self):
                print("Logging")
                self.client.remove_command("help")
                self.client.run(self.token,reconnect=True)     
                
bot = Client(prefix=configure.PREFIX,token=configure.TOKEN)
bot.connect()