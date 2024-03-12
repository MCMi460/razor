# MCMi460 on Github
from . import *

# Update this to have custom ffmpeg path later
try:
    import ffmpeg
except:
    pass

def describe(preFile:str, outFile:str, coverFile:str, metadata:dict):
    try:
        stream = ffmpeg.output(
            ffmpeg.input(preFile),
            ffmpeg.input(coverFile),
            outFile,
            **{
                'metadata:g:0': 'title=' + metadata['title'],
                'metadata:g:1': 'artist=' + metadata['artist'],
                'metadata:g:2': 'album=Razor Exported Media',
                'metadata:g:3': 'album_artist=Various People',
                'metadata:s:v': 'comment=Cover (front)',
                'c': 'copy',
            },
        )
        print('[DEBUG]: ' + ' '.join(ffmpeg.compile(stream)))
        ffmpeg.run(
            stream,
            overwrite_output = True,
            capture_stdout = True,
            capture_stderr = True
        )
    except ffmpeg.Error as e:
        print('stdout:', e.stdout.decode('utf8'))
        print('stderr:', e.stderr.decode('utf8'))
        raise e
