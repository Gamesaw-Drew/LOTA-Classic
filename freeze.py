import sys
from cx_Freeze import setup, Executable

options = {
    'build_exe': {
        'path': sys.path,
        'include_msvcr': 1,
        'include_files': ['Resources.mf'],
        'packages': ['Game']
    }
}

executables = [
    Executable('main.py')
]

setup(name='Legend of the AMD Alpha',
      version='0.1',
      description='The Overlord XD',
      options=options,
      executables=executables
      )
