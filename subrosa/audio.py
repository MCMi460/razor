from . import *

mix.Mix_Init(
    (mix.MIX_INIT_MP3)
)

result = mix.Mix_OpenAudio(48000, mix.MIX_DEFAULT_FORMAT, 0, 1024)
assert result == 0

if not 'MP3' in ( mix.Mix_GetChunkDecoder(n).decode('utf-8') for n in range(mix.Mix_GetNumChunkDecoders()) ):
    raise NotImplementedError('there is no mp3 decoder in mixer???')

class Audio:
    class State:
        Playing:int = 0
        Paused:int = 1
        Stopped:int = 2

    class Player():
        def __init__(self, file:str) -> None:
            file = os.path.abspath(file)
            if not os.path.isfile(file):
                raise FileNotFoundError('unknown file')
            self.music = mix.Mix_LoadMUS(file.encode('utf-8'))

        def play(self) -> None:
            mix.Mix_PlayMusic(self.music, 0)

        def pause(self) -> None:
            mix.Mix_PauseMusic()

        def resume(self) -> None:
            mix.Mix_ResumeMusic()

        def stop(self) -> None:
            mix.Mix_HaltMusic()
            mix.Mix_FreeMusic(self.music)
            self.music = None

        def set_time(self, time:int) -> None:
            mix.Mix_SetMusicPosition(time / 1000) # ms -> sec conversion

        def get_time(self) -> int:
            return int(mix.Mix_GetMusicPosition(self.music) * 1000) # ms conversion

        def get_length(self) -> int:
            return int(mix.Mix_MusicDuration(self.music) * 1000) # ms conversion

        def get_volume(self) -> int:
            return mix.Mix_GetMusicVolume()

        def set_volume(self, volume:int) -> None:
            mix.Mix_VolumeMusic(volume)

        def is_playing(self) -> bool:
            return Audio.State.Playing == self.get_state()

        def is_paused(self) -> bool:
            return bool(mix.Mix_PausedMusic())

        def get_state(self) -> 'Audio.State':
            return Audio.State.Paused if self.is_paused() else Audio.State.Playing if bool(mix.Mix_PlayingMusic()) else Audio.State.Stopped
