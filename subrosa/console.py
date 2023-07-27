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

# Config format
configTemplate = {
    'darkMode': False,
    'acceptedTerms;%s' % version: False,
    'volume': 64,
    'fontOffset': 0,
}

class Console():
    def __init__(self, *, prefix:str = '/', sendUpdate = None):
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

        self.youtube = Source.Youtube(sendUpdate = sendUpdate)

        self.config = configTemplate.copy()
        if fd.isFile('config.txt'):
            try:
                self.config = json.loads(fd.readFile('config.txt'))
            except:
                pass
            for key in configTemplate.keys():
                if not key in self.config:
                    self.config[key] = configTemplate[key]
        self._updateConfig()

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

    def _updateConfig(self) -> None:
        fd.createFile('config.txt', json.dumps(self.config))

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

    def play(self, provider:str = None, id:str = None, log:bool = True):
        """
        Plays a track from an ID and a specified provider
        """
        if not provider and not id and self.track['media'] and not self.track['media'].is_playing():
            self.track['media'].resume()
            return self._log('Resumed %s' % self.track['id'], Color.GREEN)
        elif not provider and not id and self.track['media']:
            return self._log('This song is still playing!', Color.RED)
        elif not provider and not id:
            return self._log('You\'re not currently playing a song!', Color.RED)
        elif provider and not id:
            return self._log('Please enter both a provider and an ID', Color.RED)
        provider = self._getProvider(provider)
        if self.track['id'] != track['id']:
            self.stop()
        media = Source.PLAY_TRACK(provider, id)
        self.track['id'] = id
        self.track['provider'] = provider
        self.track['media'] = media
        media.play()
        if log:
            track_info = provider.TRACK_INFO(id)
            return self._log('Now playing %s from %s\nID: %s' % (track_info['title'], track_info['artist'], track_info['id']), Color.GREEN)
        return None

    def resume(self):
        return self.play(None, None)

    def list(self, provider:str):
        """
        Shows a list of tracks from a provider
        """
        provider = self._getProvider(provider)
        return self._log('\n'.join(provider.LIST_TRACKS()), Color.BLUE)

    def pause(self):
        """
        Pauses the currently playing track
        """
        if self.track == track:
            return self._log('Nothing is currently playing!', Color.RED)
        id = self.track['id']
        if self.track['media'].is_playing():
            self.track['media'].pause()
            return self._log('Successfully paused %s' % id, Color.GREEN)
        else:
            return self._log('Track is already paused!', Color.RED)

    def stop(self, log:bool = True):
        """
        Stops the currently playing track
        """
        if self.track == track:
            return self._log('Nothing is currently playing!', Color.RED) if log else None
        id = self.track['id']
        t = self.track['media']
        self.track = track.copy()
        t.stop()
        return self._log('Successfully stopped %s' % id, Color.RED) if log else None

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

    def playlist(self, provider:str, id:str):
        """
        Displays a playlist from an ID
        """
        provider = self._getProvider(provider)
        playlist = provider.GET_PLAYLIST(id)
        return self._log(playlist, Color.BLUE)
