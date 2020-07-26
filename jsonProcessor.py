import discord
from discord.ext import commands
import json
import logging, sys, re, time, asyncio

from BotMakerExceptions import *

class cake:
    def __init__(self, ctx, command, this, guild=None, channel=None, message=None):
        self.this = this
        self.message = None
        self.guild = None
        self.channel = None
        if ctx is not None:
            self.guild = ctx.guild
            self.channel = ctx.channel
            self.message = ctx.message
            self.view = ctx.view
            self.ctx = ctx

        if guild is not None:
            self.guild = guild
        if channel is not None:
            self.channel = channel
        if message is not None:
            self.message = message
            self.guild = message.guild
            self.channel = message.channel

        self.client = this.client

        self.command = self.this.commands[command]
        self.commandsVar = {"client.user": self.this.client.user,
                            "message": self.message, "guild": self.guild,
                            "channel": self.channel, "time": time.time()}
        self.commandsArgs = {}
        try:
            self.args = str(ctx.message.content).split(" ")
            self.args.pop(0)
        except Exception:
            self.args = None

        self.events = {
            'on_ready': "",
            'on_message_delete': "",
            'on_message': ""
        }

        self.callbacks = {
            'getRole': self.getRole,  # Gets a role from name or id in the current guild
            'getGuild': self.getGuild,  # Gets a guild from id or name
            "getArgument": self.getArgument,  # Get an argument from the message
            'getChannel': self.getChannel,  # Gets a channel from id or name
            'sendMessage': self.sendMessage,  # Sends a message to a channel
            'setVariable': self.set_var,  # Sets a variable in in self.commandsVar
            "ifStatement": self.if_statement,  # An if statement
            "getMember": self.getMember,  # Get a member from the current guild
            'forLoop': self.forLoop,  # A for loop of stuff
            'print': self.print_function,  # Prints something
            'setGuild': self.setGuild,  # Sets the current guild
            'setChannel': self.setChannel,  # Sets the current channel
            'setPressence': self.setPressence,  # Sets the presence
            'purge': self.purge,  # Deletes x amount of messages in a channel
            'withTyping': self.withTyping,
            # Returns a context manager that allows you to type for an indefinite period of time.
            'wait': self.wait,  # Waits x amount of seconds
            'append_to_list': self.append_to_list,  # Appends a value to a list
            'create_list': self.create_list,  # Creates a list and stores it in self.commandsVar
            'pop_from_list': self.pop_from_list,  # Pops from a list and saves it as a variable
            'try_catch': self.try_catch,  # List of actions inside a try/except
            'wait_for': "",
            "pin_message": self.pin_message,  # Pins a message from a variable or a message from id in the current channel
            "unpin_message": self.unpin_message,  # Same as Pin just unpin
            'get_message': self.get_message,  # Gets a message from the current channel and saves it in self.commandsVar
            "check_for_key_perms": self.check_for_key_perms,  # Checks for specified perms if they have them go in true else go in false Supports or and and
            'raise_exception': self.raise_exception,  # Raises an exception (Useful with the try_catch action)
            'add_roles': self.add_roles,  # Adds a role from the roles key for the target, which can be set to author. can set the reason which will show up in audit log
            'remove_roles': self.remove_roles,  # Same as add_roles just removes instead
            'set_category': self.set_category  # Sets a category as the main category
        }
        self.type_functions = {
            'int': int,
            "str": str,
            'dict': dict,
            'list': list,
            'tuple': tuple
        }
        self.conditions = {
            '==': lambda a, b: a == b,
            '<': lambda a, b: a < b,
            '!=': lambda a, b: a != b,
            '>': lambda a, b: a > b,
            '>=': lambda a, b: a >= b,
            '<=': lambda a, b: a <= b
        }
        self.exceptions = {
            'Exception': Exception,
            'ValueError': ValueError
        }

    async def set_category(self, action):
        for channel in self.guild.channels:
            if type(channel) is discord.CategoryChannel:
                if channel.id == await self.get_variable(action, "id"):
                    self.category = channel
                    if "var" in action:
                        self.commandsVar[action["var"]] = channel


    async def add_roles(self, action):
        if type(action["target"]) is str:
            target = await self.get_variable(action, "target")
            if type(target) is int:
                target = self.guild.get_member(target)
        else:
            target = self.guild.get_member(action["target"])
        if action["target"] == "author":
            target = self.message.author
        if type(action["roles"]) is str:
            roles = await self.get_variable(action, "roles")
            if type(roles) is int:
                roles = self.guild.get_role(roles)
        else:
            roles = self.guild.get_role(action["roles"])
        await target.add_roles(roles, reason=action["reason"])

    async def remove_roles(self, action):
        if type(action["target"]) is str:
            target = await self.get_variable(action, "target")
            if type(target) is int:
                target = self.guild.get_member(target)
        else:
            target = self.guild.get_member(action["target"])
        if action["target"] == "author":
            target = self.message.author
        if type(action["roles"]) is str:
            roles = await self.get_variable(action, "roles")
            if type(roles) is int:
                roles = self.guild.get_role(roles)
        else:
            roles = self.guild.get_role(action["roles"])
        await target.remove_roles(roles, reason=action["reason"])

    async def raise_exception(self, action):
        raise self.exceptions[action["exception"]]

    async def check_for_key_perms(self, action):
        """ Checks if they have perms for a certain action Supports 'or' and 'and' """
        perms = []
        for x in self.message.author.guild_permissions:
            if x[1] is True:
                perms.append(x[0])

        if action["type"] == "and":
            for perm in await self.get_variable(action, "perms"):
                if perm not in perms:
                    return await self.check_perms(action, False)
            return await self.check_perms(action, True)
        elif action["type"] == "or":
            for perm in await self.get_variable(action, "perms"):
                if perm in perms:
                    return await self.check_perms(action, True)
            return await self.check_perms(action, False)



    async def check_perms(self, action, perms):
        if perms is True:
            for new_actions in action["true"]:
                for new_action in new_actions:
                    await self.callbacks[new_action](new_actions[new_action])
        else:
            for new_actions in action["false"]:
                for new_action in new_actions:
                    await self.callbacks[new_action](new_actions[new_action])

    async def get_message(self, action):
        id = await self.get_variable(action, "id")
        msg = await self.channel.fetch_message(id)
        if "var" in action:
            self.commandsVar[action["var"]] = msg
        else:
            self.commandsVar["msg"] = msg

    async def pin_message(self, action):
        if type(action["message"]) == str:
            msg = await self.get_variable(action, "message")
            await msg.pin()
        else:
            msg = await self.channel.fetch_message(action["message"])
            await msg.pin()
    async def unpin_message(self, action):
        if type(action["message"]) == str:
            msg = await self.get_variable(action, "message")
            await msg.unpin()
        else:
            msg = await self.channel.fetch_message(action["message"])
            await msg.unpin()


    async def wait(self, action):
        await asyncio.sleep(action["delay"])

    async def try_catch(self, action):
        try:
            for new_actions in action["actions"]:
                for new_action in new_actions:
                    await self.callbacks[new_action](new_actions[new_action])
        except self.exceptions[action["exception"]] as error:
            self.commandsVar["error"] = error, error.__class__
            for new_actions in action["error"]:
                for new_action in new_actions:
                    await self.callbacks[new_action](new_actions[new_action])

    async def withTyping(self, action):
        if self.channel is None: raise ChannelNotSet(action)
        async with self.channel.typing():
            for new_actions in action["actions"]:
                for new_action in new_actions:
                    await self.callbacks[new_action](new_actions[new_action])

    async def purge(self, action):
        if "limit" in action:
            delete = await self.channel.purge(limit=action["limit"])
            if "var" in action:
                self.commandsVar[action["var"]] = len(delete)

    async def setPressence(self, action):
        game = discord.Game(await self.parseMessage(action["game"]))
        statuses = {
            'dnd': discord.Status.dnd,
            'idle': discord.Status.idle,
            'offline': discord.Status.offline,
            'online': discord.Status.online,
            '': None
        }
        await self.client.change_presence(status=statuses[action["status"]], activity=game)

    async def process_var(self, action, target):
        """Convert str to a self.commandsVar variable"""
        if type(action[target]) is str:
            var = await self.parseMessage(action[target])
            if "type" in action:
                if action["type"] in self.type_functions:
                    var = self.type_functions[action["type"]](var)
        else:
            var = action[target]
        return var

    async def set_var(self, action):
        """Set a variable in self.commandsVar"""
        var = await self.process_var(action, "content")
        if "discord" in action["type"]:
            var = await self.get_discord_object(var, action["type"])
        self.commandsVar[action["var"]] = var

    async def if_statement(self, action):
        var1 = await self.get_variable(action, "var1")
        var2 = await self.get_variable(action, "var2")
        operator = await self.get_variable(action, "operator")
        if self.conditions[operator](var1, var2):
            for new_actions in action["true"]:
                for new_action in new_actions:
                    await self.callbacks[new_action](new_actions[new_action])
        else:
            for new_actions in action["false"]:
                for new_action in new_actions:
                    await self.callbacks[new_action](new_actions[new_action])

    async def setGuild(self, action):
        guild = await self.get_variable(action, "id")
        self.guild = self.client.get_guild(guild)
        self.commandsVar["guild"] = self.guild
        if "print" in action:
            print(await self.parseMessage(action["print"]))

    async def setChannel(self, action):
        channel = await self.get_variable(action, "id")
        self.channel = self.client.get_channel(channel)
        self.commandsVar["channel"] = self.channel
        if "print" in action:
            print(await self.parseMessage(action["print"]))

    async def getRole(self, action):
        """Requires action class with id, name and var"""
        if "id" in action:
            id = await self.get_variable(action, "id")
            role = self.guild.get_role(id)
            if role is None:
                raise RoleIdNotFound(id)
            self.commandsVar[action["var"]] = role
        elif "name" in action:
            name = await self.get_variable(action, "name")
            for role in self.guild.roles:
                if role.name == name:
                    self.commandsVar[action["var"]] = role
                    return
            raise RoleNameNotFound(name)

    async def getMember(self, action):
        """Requires action class with id, name and var"""
        if "id" in action:
            id = await self.get_variable(action, "id")
            member = self.guild.get_member(id)
            if member is None:
                raise MemberIdNotFound(id)
            self.commandsVar[action["var"]] = member
        elif "name" in action:
            name = await self.get_variable(action, "name")
            for member in self.guild.members:
                if member.name == name:
                    self.commandsVar[action["var"]] = member
                    return
            raise MemberNameNotFound(name)

    async def getGuild(self, action):
        """Requires action class with id and var"""
        if "id" in action:
            id = await self.get_variable(action, "id")
            guild = self.client.get_guild(id)
            if guild is None:
                raise GuildIdNotFound(action)
            self.commandsVar[action["var"]] = guild

        elif "name" in action:
            name = await self.get_variable(action, "name")
            for guild in self.client.guilds:
                if guild.name == name:
                    self.commandsVar[action["var"]] = guild
                    return
            raise GuildNameNotFound(name)

    async def get_discord_object(self, id, target):
        if target == "discord.Member":
            return self.guild.get_member(id)
        if target == "discord.Role":
            return self.guild.get_role(id)
        if target == "discord.Channel":
            return self.guild.get_channel(id)

    async def convert_var(self, action):
        """Requires action class with type and index"""
        if not self.args: return
        if 'discord' in action["type"]:
            strings_to_remove = ["@", "#", "<", ">", "&"]
            id = self.args[action["index"]]
            for x in strings_to_remove:
                id = re.sub(x, "", id)
            id = int(id)
            return await self.get_discord_object(id, action["type"])
        else:
            return self.type_functions[action["type"]](self.args[action["index"]])

    async def getArgument(self, action):
        """Requires action class with var"""
        self.commandsVar[action["var"]] = await self.convert_var(action)

    async def getChannel(self, action):
        """Requires action class with var, id and name"""
        if "id" in action:
            id = await self.process_var(action, "id")
            self.commandsVar[action["var"]] = self.ctx.message.guild.get_channel(id)
        if "name" in action:
            name = await self.process_var(action, "name")
            for channel in self.ctx.message.guild.channels:
                if channel.name == name:
                    self.commandsVar[action["var"]] = channel

    async def get_variable(self, action, target):
        """Gets a variable from self.commandsVar using the key"""
        for key in self.commandsVar:
            if f"{{{key}}}" == action[target]:
                return self.commandsVar[key]
        return action[target]

    async def print_function(self, action):
        print(await self.parseMessage(action["message"]))

    async def forLoop(self, action):
        if "stop" not in action:
            for var in await self.get_variable(action, "var"):
                self.commandsVar["var"] = var
                for new_actions in action["actions"]:
                    for new_action in new_actions:
                        await self.callbacks[new_action](new_actions[new_action])
        else:
            if "start" in action:
                for var in range(action["start"], action["stop"]):
                    self.commandsVar["var"] = var
                    for new_actions in action["actions"]:
                        for new_action in new_actions:
                            await self.callbacks[new_action](new_actions[new_action])
            else:
                for var in range(action["stop"]):
                    self.commandsVar["var"] = var
                    for new_actions in action["actions"]:
                        for new_action in new_actions:
                            await self.callbacks[new_action](new_actions[new_action])

    async def parseMessage(self, message: str):
        """Requires String"""
        for variable in self.commandsVar:
            for attribute in [attribute for attribute in dir(self.commandsVar[variable]) if
                              not attribute.startswith('__')]:
                try:
                    stringtoreplace = f'{{{variable}.{attribute}}}'
                    message = re.sub(stringtoreplace, str(getattr(self.commandsVar[variable], attribute)), message)
                except Exception:
                    pass
        for variable in self.commandsVar:
            message = re.sub(f"{{{variable}}}", str(self.commandsVar[variable]), message)
        return message

    async def create_list(self, action):
        if "var" in action:
            self.commandsVar[action["var"]] = []

    async def append_to_list(self, action):
        if "value" and "target" in action:
            self.commandsVar[action["target"]].append(await self.get_variable(action, "value"))

    async def pop_from_list(self, action):
        if "target" and "var" and "index" in action:
            self.commandsVar[action["var"]] = self.commandsVar[await self.get_variable(action, "target")].pop(action["index"])

    async def sendMessage(self, action):
        if self.channel is None:
            raise ChannelNotSet(action)
        """Requires action class with message, channel, target and var"""
        message = await self.parseMessage(action["message"])

        if not "delete_after" in action:
            delete_after = None
        else:
            delete_after = action["delete_after"]
        msg = None
        if action["channel"] == "channel":
            msg = await self.channel.send(message, delete_after=delete_after)
        elif action["channel"] == "ctx.author":
            msg = await self.message.author.send(message, delete_after=delete_after)
        elif action["channel"] == "var":
            msg = await self.commandsVar[action["target"]].send(message, delete_after=delete_after)
        if "var" in action:
            self.commandsVar[action["var"]] = msg

    async def processCommands(self):
        for actions in self.command["actions"]:
            for action in actions:
                await self.callbacks[action](actions[action])
                if "print" in actions[action]:
                    print(await self.parseMessage(actions[action]["print"]))
        return self
