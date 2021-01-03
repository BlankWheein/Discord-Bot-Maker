import discord
from discord.ext import commands
from discord.utils import get
import json
import logging, sys, re, time, asyncio, os

from BotMakerExceptions import *


class cake:
    def __init__(self, ctx, command, this, guild=None, channel=None, message=None):
        """
        This section will explain the actions variables and how they are used.

        Members:
            :class:`self.channel` : This contexts channel object.
            
            :class:`self.message` : This contexts message object.
            
            :class:`self.guild` : This contexts guild object.

            :class:`self.running` : This controls if the command is running.

            :class:`self.command` : The command executed.

            :class:`self.this` : Discord object.

            :class:`self.client` : Discord Client object.

            :class:`self.commandsVar` : This contexts variables.

            :class:`self.commandsArgs` : Not used atm, trying to find out why...

            :class:`self.args` : Message arguments.

            :class:`self.events` : Events.

            :class:`self.callbacks` : Functions available.

            :class:`self.type_functions` : types.

            :class:`self.conditions` : Conditions for the if statements.

            :class:`self.exception` : The exceptions the command can raise.



        """
        self.dir = None
        self.running = True
        self.this = this
        self.message = None
        self.guild = None
        self.member_vars = []
        self.author = None
        self.channel = None
        if ctx is not None:
            self.guild = ctx.guild
            self.channel = ctx.channel
            self.message = ctx.message
            self.view = ctx.view
            self.author = ctx.message.author
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
                            "author": self.author,
                            "channel": self.channel, "time": time.time()}
        try:
            self.commandsVar["author.id"] = self.author.id
        except Exception:
            pass
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
            "pin_message": self.pin_message,
            # Pins a message from a variable or a message from id in the current channel
            "unpin_message": self.unpin_message,  # Same as Pin just unpin
            'get_message': self.get_message,  # Gets a message from the current channel and saves it in self.commandsVar
            "check_for_key_perms": self.check_for_key_perms,
            # Checks for specified perms if they have them go in true else go in false Supports or and and
            'raise_exception': self.raise_exception,  # Raises an exception (Useful with the try_catch action)
            'add_roles': self.add_roles,
            # Adds a role from the roles key for the target, which can be set to author. can set the reason which will show up in audit log
            'remove_roles': self.remove_roles,  # Same as add_roles just removes instead
            'set_category': self.set_category,  # Sets a category as the main category
            'exit_command': self.exit_command, # Exits the command
            'read_global_variables': self.read_global_variables, # Puts global variables in the local variables
            'write_global_variable': self.write_global_variable,
            'change_variable_value': self.change_variable_value,

            'read_member_file': self.read_member_file,
            'write_member_file': self.write_member_file,
            'add_member_var': self.add_member_var,
            'cooldown': self.cooldown
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
            'ValueError': ValueError,
            'ArgumentError': ArgumentError,
            'ChannelNotFound': ChannelNotFound
        }

    async def read_user_variables(self, action=None):
        pass
    async def exit_command(self, action=None):
        """
        This action stops the current command.

        Members:
            None

        """
        self.running = False


    async def create_guild_files(self, action=None):
        dirs = [f'vars/guilds/{self.guild.id}/members']
        cooldowns = f'vars/guilds/{self.guild.id}/cooldowns.txt'
        for dirName in dirs:
            try:
                os.makedirs(dirName)
                print("Directory ", dirName, " Created ")
            except FileExistsError:
                print("Directory ", dirName, " already exists")

        try:
            with open(cooldowns, "r") as file:
                pass
        except FileNotFoundError:
            with open(cooldowns, "w+") as file:
                json.dump({}, file, indent=2)
        finally:
            with open(cooldowns, "r") as file:
                data = json.load(file)
            if self.command["name"] not in data:
                data[self.command["name"]] = {}
            with open(cooldowns, "w+") as file:
                json.dump(data, file, indent=2)

    async def create_member_files(self, action=None):
        dirs = [f'vars/guilds/{self.guild.id}/members/{self.author.id}.txt']
        for dir in dirs:
            try:
                with open(dir, "r") as file:
                    pass
            except FileNotFoundError:
                print(f"Creating file: {dir}")
                with open(dir, "w+") as file:
                    json.dump({}, file, indent=2)

    async def read_member_file(self, action=None):

        if not self.author:
            return print("Author not defined")
        await self.create_member_files()
        with open(f'vars/guilds/{self.guild.id}/members/{self.author.id}.txt', "r") as file:
            data = json.load(file)
        for var in data:
            self.commandsVar[var] = data[var]
            self.member_vars.append(var)
        return data

    async def cooldown(self, action):
        """
        Cooldown

        Members:
            :mod:`cooldown` The cooldown in seconds

            :mod:`error` The value of the cooldown left

            :mod:`buckettype` The type of cooldown
        """
        if not self.guild: raise GuildNotFound
        if not self.author: raise MemberNotFound
        if not self.channel: raise ChannelNotFound

        cooldowns_path = f'vars/guilds/{self.guild.id}/cooldowns.txt'
        keys = {
            "channel": str(self.channel.id),
            "member": str(self.author.id),
            "guild": str(self.guild.id)
        }

        key = keys[action["buckettype"]]

        await self.create_guild_files()
        seconds = await self.get_variable(action, "cooldown")
        with open(cooldowns_path, "r") as file:
            data = json.load(file)

        if key in data[self.command["name"]]:
            if data[self.command["name"]][key] + seconds > time.time():
                timeleft = data[self.command['name']][key] + seconds - time.time()
                self.commandsVar[await self.get_variable(action, "error")] = f"Still on cooldown for {int(timeleft)}"
                raise Cooldown({int(timeleft)})
            else:
                data[self.command["name"]][key] = time.time()
        else:
            data[self.command["name"]][key] = time.time()

        with open(cooldowns_path, "w+") as file:
            json.dump(data, file, indent=2)






    async def write_member_file(self, action=None):
        if not self.author:
            return print("Author not found")

        data = {}
        for x in self.member_vars:
            data[x] = self.commandsVar[x]
        with open(f'vars/guilds/{self.guild.id}/members/{self.author.id}.txt', "w+") as file:
            json.dump(data, file, indent=2)
    async def add_member_var(self, action):
        """
        Adds a variable to a member

        Members:
            :mod:`key` The name of the variable

            :mod:`value` The default value of the variable

        ..note::
            This can also be used to reset a member

        """
        self.member_vars.append(await self.get_variable(action, "key"))
        self.commandsVar[await self.get_variable(action, "key")] = await self.get_variable(action, "value")






    async def write_global_variable(self, action):
        """
        Writes to the global variables

        Members:
            :mod:`key`

            :mod:`value`

        ..note::
            This requires :mod:`self.guild` to be set
        """
        if not self.guild: return
        await self.create_guild_files()
        data = await self.get_global_variables()
        data[str(await self.get_variable(action, "key"))] = await self.get_variable(action, "value")
        with open(f"vars/guilds/{self.guild.id}/global.txt", "w+") as file:
            json.dump(data, file, indent=2)
        print(data)

    async def change_variable_value(self, action):
        """
        Changes a value

        Members:

            :mod:`target` The target variable (should not be surrounded by {})

            :mod:`operator`:

                * :mod:`increment by 1`

                * :mod:`decrement by 1`

                * :mod:`add`

                * :mod:`subtract`

                * :mod:`times`

                * :mod:`divide`

                * :mod:`set`

            :mod:`value` The value to change with, this depends on the :mod:`operator`

        """

        try:
            self.commandsVar[await self.get_variable(action, "target")]
        except KeyError:
            self.commandsVar[await self.get_variable(action, "target")] = 0

        operator = await self.get_variable(action, "operator")
        if operator == "increment by 1":
            self.commandsVar[await self.get_variable(action, "target")] += 1
        elif operator == "decrement by 1":
            self.commandsVar[await self.get_variable(action, "target")] -= 1
        elif operator == "add":
            self.commandsVar[await self.get_variable(action, "target")] += await self.get_variable(action, "value")
        elif operator == "subtract":
            self.commandsVar[await self.get_variable(action, "target")] -= await self.get_variable(action, "value")
        elif operator == "times":
            self.commandsVar[await self.get_variable(action, "target")] *= await self.get_variable(action, "value")
        elif operator == "divide":
            self.commandsVar[await self.get_variable(action, "target")] /= await self.get_variable(action, "value")
        elif operator == "set":
            self.commandsVar[await self.get_variable(action, "target")] = await self.get_variable(action, "value")
        pass






    async def get_global_variables(self):
        if not self.guild: return
        await self.create_guild_files()
        self.global_var = f"vars/guilds/{self.guild.id}/global.txt"
        try:
            print("Trying")
            with open(self.global_var, "r") as file:
                pass
        except FileNotFoundError:
            with open(self.global_var, "w+") as file:
                json.dump({}, file, indent=2)
        finally:
            with open(self.global_var, "r") as file:
                data = json.load(file)
        return data

    async def read_global_variables(self, action=None):
        """
        Reads the variables in the json file and converts them to local variables.

        Members:
            None

        ..note::
            This required :mod:`self.guild` to be set.
        """
        await self.create_guild_files()
        data = await self.get_global_variables()


        for key in data:
            self.commandsVar[key] = data[key]

    async def set_category(self, action):
        """Sets the current category from id

        Members:
            :class:`id` : The id of the category

        **this will be removed after the command has been executed**"""
        for channel in self.guild.channels:
            if type(channel) is discord.CategoryChannel:
                if channel.id == await self.get_variable(action, "id"):
                    self.category = channel
                    self.commandsVar["category"] = channel
                    if "var" in action:
                        self.commandsVar[action["var"]] = channel

    async def add_roles(self, action):
        """
        Adds a role to the target

        Members:
            :class:`target` : (str / int / discord.member / author):  The target

            :class:`roles` : Role to add (Can only add 1 at a time)

            :class:`reason` : The reason why the role was added.

        .. note::
            :mod:`reason` can be left empty.

        """

        if type(action["target"]) is str:
            target = await self.get_variable(action, "target")
            print(target, "TARGET", self.guild.members, "GUILD")
            if type(target) is int:
                target = self.guild.get_member(target)
        else:
            target = self.guild.get_member(action["target"])
        if action["target"] == "author":
            target = self.author
        if type(action["roles"]) is str:
            roles = await self.get_variable(action, "roles")
            if type(roles) is int:
                roles = self.guild.get_role(roles)
        else:
            roles = self.guild.get_role(action["roles"])
        if action["reason"] == "":
            action["reason"] = "Reason Not Specified"
        await target.add_roles(roles, reason=action["reason"])

    async def remove_roles(self, action):
        """
        Removes a role to the target

        Members:
            :class:`target` : (str / int / discord.member / author):  The target

            :class:`roles` : Role to remove (Can only remove 1 at a time)

        """

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
        """Raises an exception

        Members:
            :class:`exception` : The exception to raise


        """
        raise self.exceptions[action["exception"]]

    async def check_for_key_perms(self, action):
        """ 
        Checks if they have perms for a certain action Supports :class:`and` and :class:`or`
        

        Members:
            :class:`type` : (str): Can be :class:`and` or :class:`or`

            :class:`perms` : The required permission

        
        
        """
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
        """ Processes the action list """

        if perms is True:
            await self.process_actions_list(action["true"])
        else:
            await self.process_actions_list(action["false"])

    async def get_message(self, action):
        """
        Gets a message from id

        Members:
            :class:`id` :  The id of the message.

            :class:`var` : The name of the variable to put the message into.
        
        .. note::
            This requires :mod:`self.channel` to be set.
        
        """
        id = await self.get_variable(action, "id")
        msg = await self.channel.fetch_message(id)
        if "var" in action:
            self.commandsVar[action["var"]] = msg
        else:
            self.commandsVar["msg"] = msg

    async def pin_message(self, action):
        """
        Pins the specified message

        Members:
            :mod:`message` : The message to pin.

        .. note::
            This requires :mod:`self.channel` to be set.

        """
        if type(action["message"]) == str:
            msg = await self.get_variable(action, "message")
            await msg.pin()
        else:
            msg = await self.channel.fetch_message(await self.get_variable(action, "message"))
            if msg is None:
                return MsgNotFoundError(action)
            await msg.pin()

    async def unpin_message(self, action):
        """
        Unpins the specified message

        Members:
            :mod:`message` : The message to unpin.

        .. note::
            This requires :mod:`self.channel` to be set.

        """
        if type(action["message"]) == str:
            msg = await self.get_variable(action, "message")
            await msg.unpin()
        else:
            msg = await self.channel.fetch_message(action["message"])
            await msg.unpin()

    async def wait(self, action):
        """
        Sleeps for x amount of time

        Members:
            :mod:`delay` : The amount of time to sleep in ms.

        """
        await asyncio.sleep( await self.get_variable(action, "delay"))

    async def try_catch(self, action):
        """
        Try catch.

        Members:
            :mod:`actions` : The list of actions to try.

            :mod:`exception` : The exception.

            :mod:`errorvar` : Saves the error message in this variable name.

            :mod:`error` : The list of actions if the exception is raised.

        .. note::
            If :mod:`errorvar` is none, the error message will be saved as `error`.
        
        """
        try:
            await self.process_actions_list(action["actions"])
        except self.exceptions[action["exception"]] as error:
            if action["errorvar"] is None or "":
                self.commandsVar["error"] = error, error.__class__
            else:
                self.commandsVar[action["errorvar"]] = error, error.__class__
            await self.process_actions_list(action["error"])

    async def withTyping(self, action):
        """
        Starts a context manager with :mod:`with Typing`.

        Members:
            :mod:`actions` : The list of actions the context manager wraps around

        .. note::
            This requires :mod:`self.channel` to be set.

        """

        if self.channel is None: raise ChannelNotSet(action)
        async with self.channel.typing():
            await self.process_actions_list(action["actions"])

    async def purge(self, action):
        """
        Purges messages from :mod:`self.channel`

        Members:
            :mod:`limit` : The max amount of messages to delete.
            
            :mod:`var` : The amount of messages deleted will be stored in this variable.

        .. note::
            This requires :mod:`self.channel` to be set.

            If :mod:`var` is not set it will not store the variable

        """
        if self.channel:
            limit = await self.get_variable(action, "limit")
            if type(limit) is not int:
                raise ValueError(limit)
            delete = await self.channel.purge(limit=limit)
            if action["var"] is not None and action["var"] != '':
                self.commandsVar[action["var"]] = len(delete)
        else:
            raise ChannelNotSet

    async def setPressence(self, action):
        """
        Sets the bots pressence

        Members:
            :mod:`game` : The message to display.
            
            :mod:`status` : The status to show.
             
             *  :mod:`dnd` : Shows the status **`Do not disturb`**
             *  :mod:`idle` : Shows the status **`Idle`**
             *  :mod:`offline` : Shows the status **`Invisible`**
             *  :mod:`online` : Shows the status **`Online`**

        .. note::
            If :mod:`status` is '' it will not update the status.

        """
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
            try:
                var = int(var)
            except Exception:
                pass
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
        self.commandsVar[await self.get_variable(action, "var")] = var
        pass

    async def if_statement(self, action):
        """
        If statement 
        
        Members:
            :mod:`var1` : Variable 1.
            
            :mod:`var2` : Variable 2.
            
            :mod:`operator` : The operator. This can be :mod:`self.conditions`.
            
            :mod:`true` : The list of actions if true.
            
            :mod:`false` : The list of actions if false.
        
        """
        var1 = await self.get_variable(action, "var1")
        var2 = await self.get_variable(action, "var2")
        operator = await self.get_variable(action, "operator")
        if self.conditions[operator](var1, var2):
            await self.process_actions_list(action["true"])
        else:
            await self.process_actions_list(action["false"])

    async def setGuild(self, action):
        """
        Sets the :mod:`self.guild` object

        Members:
            :mod:`id` : The id of the guild you are looking for.
            
            :mod:`print` : What to print to console when this action is complete

        .. note::
            :mod:`self.guild` will be automatically set if there is ctx
            
            ctx will be set if a command is used in a server.
        """
        guild = await self.get_variable(action, "id")
        print(guild)
        self.guild = self.client.get_guild(guild)
        print(self.guild)

        self.commandsVar["guild"] = self.guild
        for attribute in [attribute for attribute in dir(self.commandsVar["guild"]) if
                          not attribute.startswith('__')]:
            self.commandsVar[f"guild.{attribute}"] = getattr(self.commandsVar["guild"], attribute)

    async def setChannel(self, action):
        """
        Sets the :mod:`self.channel` object

        Members:
            :mod:`id` : The id of the channel you are looking for.
            
            :mod:`print` : What to print to console when this action is complete

        .. note::
            :mod:`self.channel` will be automatically set if there is ctx
            
            ctx will be set if a command is used in a server.
        
        """
        channel = await self.get_variable(action, "id")
        self.channel = self.client.get_channel(channel)
        self.commandsVar["channel"] = self.channel

    async def getRole(self, action):
        """
        Gets a :mod:`Role` object

        Members:
            :mod:`type` : How you are searching for the role, this can be name or id.

            :mod:`id` : The id of the role you are looking for.

            :mod:`name` : The name of the role you are looking for.
            
            :mod:`print` : What to print to console when this action is complete

        """

        if action["type"] == 'id':
            id = await self.get_variable(action, "id")
            role = get(self.guild.roles, id=id)
            if role is None: raise RoleIdNotFound(id)
            self.commandsVar[action["var"]] = role
        elif action["type"] == 'name':
            name = await self.get_variable(action, "name")
            role = get(self.guild.roles, name=name)
            if role is None: raise RoleNameNotFound(name)
            self.commandsVar[action["var"]] = role

    async def getMember(self, action):
        """
        Gets a :mod:`Member` object

        Members:
            :mod`type` : How you are searching for the member, this can be name or id.

            :mod:`id` : The id of the member you are looking for.

            :mod:`name` : The name of the member you are looking for.
            
            :mod:`print` : What to print to console when this action is complete

        """
        if action["type"] == 'id':
            id = await self.get_variable(action, "value")
            member = get(self.guild.members, id=id)
            if member is None: raise MemberIdNotFound(id)
            self.commandsVar[action["var"]] = member
        elif action["type"] == 'name':
            name = await self.get_variable(action, "value")
            member = get(self.guild.members, name=name)
            if member is None: raise MemberNameNotFound(name)
            self.commandsVar[action["var"]] = member

    async def getGuild(self, action):
        """
        Gets a :mod:`Guild` object

        Members:
            :mod`type` : How you are searching for the guild, this can be name or id.

            :mod:`id` : The id of the guild you are looking for.

            :mod:`name` : The name of the guild you are looking for.
            
            :mod:`print` : What to print to console when this action is complete

        """
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
        """
        Converts a variable to a discord object.

        Args:

            id : The id of the object
            target : the type to convert too. 

        Types:

            * discord.Member

            * discord.Role

            * discord.Channel
        
        """
        if target == "discord.Member":
            return get(self.client.get_all_members(), id=id)
        if target == "discord.Role":
            return self.guild.get_role(id)
        if target == "discord.Channel":
            return get(self.client.get_all_channels(), id=id)

    async def convert_var(self, action):
        """Requires action class with type and index"""
        if not self.args: return
        if 'discord' in action["type"]:
            strings_to_remove = ["@", "#", "<", ">", "&", "!"]
            print(action["index"])
            id = self.args[await self.get_variable(action, "index")]

            for x in strings_to_remove:
                id = re.sub(x, "", id)
            id = int(id)
            return await self.get_discord_object(id, action["type"])
        else:
            return self.type_functions[action["type"]](self.args[int(action["index"])])

    async def getArgument(self, action):
        """
        Converts an argument to a variable

        Members:
            :mod:`var` : The name to store the arugment as

            :mod:`type` : The type of variable

            :mod:`index` : The index of the argument

        """
        self.commandsVar[action["var"]] = await self.convert_var(action)

    async def getChannel(self, action):
        """
        Gets a :mod:`Channel` object

        Members:
            :mod`type` : How you are searching for the channel, this can be name or id.

            :mod:`id` : The id of the channel you are looking for.

            :mod:`name` : The name of the channel you are looking for.
            
            :mod:`print` : What to print to console when this action is complete

        """
        if action["type"] == 'id':
            id = await self.get_variable(action, "value")
            channel = get(self.guild.channels, id=id)
            if channel is None: raise ChannelNotFound(id)
            self.commandsVar[action["var"]] = channel
        elif action["type"] == 'name':
            name = await self.get_variable(action, "value")
            channel = get(self.guild.channels, name=name)
            if channel is None: raise ChannelNotFound(name)
            self.commandsVar[action["var"]] = channel

    async def get_variable(self, action, target):
        """Gets a variable from self.commandsVar using the key"""
        for key in self.commandsVar:
            if f"{{{key}}}" == action[target]:
                return self.commandsVar[key]
        try:
            var = int(action[target])
            return var
        except Exception:
            pass

        return action[target]

    async def print_function(self, action):
        """
        Prints the message to console

        Members:
            :mod:`message` The message to print
        
        .. note::
            Some characters can not be displayed in console. its recommended to use id's of objects if available
        
        """
        print(await self.parseMessage(action["message"]))

    async def forLoop(self, action):
        """
        For loop

        Members:
            :mod:`type` The type of for loop
                
                * :mod:`for x in`
                
                * :mod:`stop`

                * :mod:`start`
            
            :mod:`list` : the list to cycle through, used in for x in

            :mod:`stop` : the end number, used in start and stop

            :mod:`start` : the start number, used in start

            :mod:`actions` : the list of actions to do every iteration

            :mod:`var` : The current iteration of the for loop
        
        """
        if action["type"] == "for x in":
            variables = await self.get_variable(action, "list")
            for var in variables:
                self.commandsVar[action["var"]] = var
                await self.process_actions_list(action["actions"])
        elif action["type"] == "stop":
            for var in range(await self.get_variable(action, "stop")):
                self.commandsVar[action["var"]] = var
                await self.process_actions_list(action["actions"])
        elif action["type"] == "start":
            for var in range(await self.get_variable(action, "start"), await self.get_variable(action, "stop")):
                self.commandsVar[action["var"]] = var
                await self.process_actions_list(action["actions"])

    async def parseMessage(self, message: str):
        """
        Parses a string

        Args:
            message : the message to parse.
        
        
        """
        print("Parsing message '", message, "'")
        for variable in self.commandsVar:
            for attribute in [attribute for attribute in dir(self.commandsVar[variable]) if
                              not attribute.startswith('__')]:
                try:
                    stringtoreplace = f'{{{variable}.{attribute}}}'
                    message = re.sub(stringtoreplace, str(getattr(self.commandsVar[variable], attribute)), message)
                except Exception:
                    pass
        for variable in self.commandsVar:
            try:
                message = re.sub(f"{{{variable}}}", str(self.commandsVar[variable]), message)
            except Exception:
                pass
        return message

    async def create_list(self, action):

        """
        Creates an empty list

        Members:
            :mod:`var` The name to store the list as
        
        .. note::
            If :mod:`var` is not present nothing will happen

        """

        if "var" in action:
            self.commandsVar[action["var"]] = []

    async def append_to_list(self, action):
        """
        Appends to a list

        Members:
            :mod:`value` The value of the variable

            :mod:`target` the list to append to
        
        .. note::
            If :mod:`target` or :mod:`value` is not present nothing will happen

        """
        if "value" and "target" in action:
            self.commandsVar[action["target"]].append(await self.get_variable(action, "value"))

    async def pop_from_list(self, action):
        """
        Pops from list

        Members:
            :mod:`var` : the variable to save the value in

            :mod:`target` : the list to pop from

            :mod:`index` : The index to pop
        
        .. note::
            If either :mod:`target`, :mod:`var` or :mod:`index` is not present nothing will happen

        """
        if "target" and "var" and "index" in action:
            self.commandsVar[action["var"]] = self.commandsVar[await self.get_variable(action, "target")].pop(
                action["index"])

    async def sendMessage(self, action):
        """
        Sends a message in the channel

        Members:
            :mod:`message` : .

            :mod:`delete_after` : .

            :mod:`channel` : The channel to send the message.
                
                * :mod:`channel` : The channel the command was executed in

                * :mod:`author` : The author of the member who executed the channel

                * :mod:`variable` : Custom channel

            :mod:`var` : Saves the message object.
        
        """

        msg = None
        print(action["message"])
        message = await self.parseMessage(action["message"])
        delete_after = await self.get_variable(action, "delete_after")
        if delete_after == 0 or delete_after == '': delete_after = None
        channel = await self.get_variable(action, "channel")
        if self.guild and type(channel) == int:
            newchannel = self.client.get_channel(channel)
            if newchannel:
                channel = newchannel
            else:
                raise ChannelNotFound(channel)
        if self.channel and channel == "channel":
            msg = await self.channel.send(message, delete_after=delete_after)
        elif self.message and channel == "author":
            msg = await self.message.author.send(message, delete_after=delete_after)
        elif type(channel) == discord.TextChannel:
            msg = await channel.send(message, delete_after=delete_after)
        else:
            raise ChannelNotFound
        if "var" in action:
            self.commandsVar[action["var"]] = msg

    async def process_actions_list(self, action):
        """ Proccesses the actions list """
        for new_actions in action:
            for new_action in new_actions:
                if self.running:
                    await self.callbacks[new_action](new_actions[new_action])
                    print(action)
                    if "print" in new_actions[new_action]:
                        print(await self.parseMessage(new_actions[new_action]["print"]))

    async def processCommands(self):
        """ Proccesses the command actions """
        for actions in self.command["actions"]:
            for action in actions:
                try:
                    if self.running: await self.callbacks[action](actions[action])
                    print(action)
                except Exception as error:
                    print(action, error)
                    raise error
        return self
