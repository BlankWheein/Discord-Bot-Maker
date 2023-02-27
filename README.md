### This repository is currently deprecated a new version is in the works [here](https://github.com/BlankWheein/Discord-Bot-Maker-2.0)





### Discord bot maker, to be used in conjunction with the discord bot maker website [repository](https://github.com/BlankWheein/Discord-Bot-Maker-Webpage)

## Possible commands using the discord bot maker:

* 'getRole': self.getRole,  # Gets a role from name or id in the current guild
* 'getGuild': self.getGuild,  # Gets a guild from id or name
* "getArgument": self.getArgument,  # Get an argument from the message
* 'getChannel': self.getChannel,  # Gets a channel from id or name
* 'sendMessage': self.sendMessage,  # Sends a message to a channel
* 'setVariable': self.set_var,  # Sets a variable in in self.commandsVar
* "ifStatement": self.if_statement,  # An if statement
* "getMember": self.getMember,  # Get a member from the current guild
* 'forLoop': self.forLoop,  # A for loop of stuff
* 'print': self.print_function,  # Prints something
* 'setGuild': self.setGuild,  # Sets the current guild
* 'setChannel': self.setChannel,  # Sets the current channel
* 'setPressence': self.setPressence,  # Sets the presence
* 'purge': self.purge,  # Deletes x amount of messages in a channel
* 'withTyping': self.withTyping, # Returns a context manager that allows you to type for an indefinite period of time.
* 'wait': self.wait,  # Waits x amount of seconds
* 'append_to_list': self.append_to_list,  # Appends a value to a list
* 'create_list': self.create_list,  # Creates a list and stores it in self.commandsVar
* 'pop_from_list': self.pop_from_list,  # Pops from a list and saves it as a variable
* 'try_catch': self.try_catch,  # List of actions inside a try/except
* 'wait_for': "",
* "pin_message": self.pin_message, # Pins a message from a variable or a message from id in the current channel
* "unpin_message": self.unpin_message,  # Same as Pin just unpin
* 'get_message': self.get_message,  # Gets a message from the current channel and saves it in self.commandsVar
* "check_for_key_perms": self.check_for_key_perms, # Checks for specified perms if they have them go in true else go in false Supports or and and
* 'raise_exception': self.raise_exception,  # Raises an exception (Useful with the try_catch action)
* 'add_roles': self.add_roles, # Adds a role from the roles key for the target, which can be set to author. can set the reason which will show up in audit log
* 'remove_roles': self.remove_roles,  # Same as add_roles just removes instead
* 'set_category': self.set_category,  # Sets a category as the main category
* 'exit_command': self.exit_command, # Exits the command
* 'read_global_variables': self.read_global_variables, # Puts global variables in the local variables
* 'write_global_variable': self.write_global_variable,
* 'change_variable_value': self.change_variable_value,
* 'read_member_file': self.read_member_file,
* 'write_member_file': self.write_member_file,
* 'add_member_var': self.add_member_var,
* 'cooldown': self.cooldown,
* 'random': self.rand,
* 'ifndef': self.ifndef

## The user is also able to store these simple data structures
* 'int': int,
* "str": str,
* 'dict': dict,
* 'list': list,
* 'tuple': tuple

### The user can also check these conditions on the data structures
* '==': lambda a, b: a == b,
* '<': lambda a, b: a < b,
* '!=': lambda a, b: a != b,
* '>': lambda a, b: a > b,
* '>=': lambda a, b: a >= b,
* '<=': lambda a, b: a <= b
