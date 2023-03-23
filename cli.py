# MCMi460 on Github
from subrosa import *

if __name__ == '__main__':
    # Begin main thread for user
    con = console.Console()

    try:
        con._main() # Begin main loop for console program
    except KeyboardInterrupt:
        mix.Mix_Quit()
