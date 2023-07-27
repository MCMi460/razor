# MCMi460 on Github
# Sets up dll files (for Windows)
import importlib.util, os.path, shutil

if os.path.exists('dll'):
    shutil.rmtree('dll')

path = os.path.join(
    importlib.util.find_spec('sdl2dll').submodule_search_locations[0],
    'dll',
)

print('[Copying SDL2 DLLs...]')
shutil.copytree(path, 'dll')
