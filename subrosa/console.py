# MCMi460 on Github
from . import *

# Blatantly ripped from 3DS-RPC
os.system('')
class Color:
    DEFAULT = '\033[0m'
    RED = '\033[91m'
    PURPLE = '\033[0;35m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'

class Console():
    def __init__(self, *, prefix:str = '/'):
        self.prefix = prefix
        self.commands = {}
        for func in dir(self):
            if callable(getattr(self, func)) and not func.startswith('_'):
                function = getattr(self, func)
                self.commands[func] = {
                    'function': function,
                    'docstring': str(function.__doc__).strip(),
                }

        self.tip = ('Type \'help\' to view the configuration menu', Color.YELLOW)

    def _main(self):
        self._log(*self.tip)
        while True:
            userInput = input(Color.DEFAULT + '> ' + Color.PURPLE).strip().lower()
            args = userInput.split(' ')

            try:
                self.commands[args[0]]['function'](*args[1:])
            except KeyError:
                self._missingCommand(userInput)
            except AssertionError:
                self._missingSubcommand(args)
            except:
                self._log(traceback.format_exc().strip(), Color.RED)

    def _log(self, text:str, color:str = Color.DEFAULT):
        text = color + str(text)
        print(text)
        return text

    def _missingCommand(self, command:str):
        return self._log('\'%s\' is not a real command!' % command, Color.RED), self._log(*self.tip)

    def _missingSubcommand(self, args:list):
        return self._log('\'%s\' is not a supported subcommand of \'%s\'!' % (args[1], args[0]), Color.RED)

    def exit(self):
        """
        Quits application
        """
        self._log('Exiting...', Color.RED)
        return os._exit(0)

    def help(self, command:str = None):
        """
        Shows a formatted list of all available commands
        self, command:str
        """
        if not command:
            return self._log('\n'.join(( '%s: %s' % (key, self.commands[key]['docstring']) for key in self.commands.keys())), Color.YELLOW)
        assert command in self.commands.keys()
        return self._log(( '%s: %s' % (command, self.commands[command]['docstring'])), Color.YELLOW)

    def clear(self):
        """
        Clears the console
        """
        return print('\033[H\033[J', end = '')

    def status(self):
        """
        Shows your currently playing song
        """
        return self._log('lorem ipsum', Color.BLUE)

    def download(self, provider:str, id:str):
        """
        Downloads a track from a specified provider
        """
        return

    def play(self, provider:str, id:str):
        """
        Plays a track from an ID
        """
        return
