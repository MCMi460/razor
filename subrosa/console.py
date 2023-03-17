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

# Track format
track = {
    'id': '',
    'provider': None,
    'media': None,
}

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

        # Currently playing track:
        self.track = track.copy()

        self.youtube = Source.Youtube()

    def _main(self):
        self._log(*self.tip)
        while True:
            userInput = input(Color.DEFAULT + '> ' + Color.PURPLE).strip()
            if list( userInput.lower().startswith(i) for i in ('download', 'play') ).count(True) == 0:
                userInput = userInput.lower()
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

    def _getProvider(self, provider:str) -> object:
        if provider.strip().lower() in ('youtube', 'yt'):
            provider = self.youtube
        #elif ...
        else:
            raise Exception('provider unknown')
        return provider

    def exit(self):
        """
        Quits application
        """
        self._log('Exiting...', Color.RED)
        self.stop(False)
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
        if self.track == track or not self.track['media'].is_playing():
            self.track = track.copy()
            return self._log('There\'s no track playing right now!', Color.RED)
        track_info = self.track['provider'].TRACK_INFO(self.track['id'])

        return self._log('%s from %s\nID: %s' % (track_info['title'], track_info['artist'], track_info['id']), Color.YELLOW)

    def download(self, provider:str, id:str):
        """
        Downloads a track from a specified provider
        """
        provider = self._getProvider(provider)
        if provider.DOWNLOAD_TRACK(id):
            return self._log('Successfully downloaded %s' % id, Color.GREEN)
        else:
            return self._log('Failed to download %s' % id, Color.RED)

    def play(self, provider:str, id:str):
        """
        Plays a track from an ID and a specified provider
        """
        if self.track != track:
            self.stop()
        provider = self._getProvider(provider)
        media = Source.PLAY_TRACK(provider, id)
        self.track['id'] = id
        self.track['provider'] = provider
        self.track['media'] = media
        media.play()
        track_info = provider.TRACK_INFO(id)
        return self._log('Now playing %s from %s\nID: %s' % (track_info['title'], track_info['artist'], track_info['id']), Color.GREEN)

    def list(self, provider:str):
        """
        Shows a list of tracks from a provider
        """
        provider = self._getProvider(provider)
        return self._log('\n'.join(provider.LIST_TRACKS()), Color.BLUE)

    def stop(self, log = True):
        """
        Stops the currently playing track
        """
        if self.track == track:
            return self._log('Nothing is currently playing!', Color.RED) if log else None
        id = self.track['id']
        if self.track['media'].is_playing():
            self.track['media'].stop()
            self.track = track.copy()
            return self._log('Successfully stopped %s' % id, Color.RED) if log else None
        else:
            self.track = track.copy()
            return None

    def search(self, provider:str, *terms):
        """
        Searches for IDs that match a search term
        """
        provider = self._getProvider(provider)
        results = provider.SEARCH(' '.join(terms))
        response = []
        for result in results:
            if not 'Music' in result['categories']:
                continue
            response.append(
            ('Title: %s\n'
            + 'Uploader: %s\n'
            + 'ID: %s') % (result['title'], result['uploader'], result['id'])
            )
        return self._log('\n---\n'.join(response[0:5]), Color.BLUE)
