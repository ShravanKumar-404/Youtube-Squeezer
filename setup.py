import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

options = {
    'build_exe': {
        'includes': ['atexit'],
        'include_files' : ['youtube.ui','icons','styles'],
    }
}

executables = [
    Executable('index.py', base=base)
]

setup(name='Youtube Squeezer',
      version='0.3',
      description='Youtube Squeezer Python Made',
      options=options,
      executables=executables
      )
