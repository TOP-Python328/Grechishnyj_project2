"""
Controller (MVC).
"""
from sys import argv

import model

if 'cli' in argv:
    import view_cli as view
else:
    import view_gui as view