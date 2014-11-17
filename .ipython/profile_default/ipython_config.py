import os

c = get_config()

c.TerminalIPythonApp.display_banner = False
c.InteractiveShellApp.log_level = 20
c.InteractiveShellApp.extensions = []
c.InteractiveShellApp.exec_lines = [
            '%load_ext autoreload',
            '%autoreload 1',
            'import os',
            'import sys',
            'import json',
            'import pickle',
            'import datetime as dt',
            'import itertools as it',
            'import operator as op',
            'import numpy as np',
            'import pandas as pd',
            'import scipy as sp',
            'from pprint import pprint as pp'
                ]
c.InteractiveShellApp.exec_files = [
        os.path.expanduser('~/.ipython/profile_default/misc_ipython_functions.py')
        ]
c.InteractiveShell.autoindent = True
c.InteractiveShell.colors = 'LightBG'
c.InteractiveShell.confirm_exit = False
c.InteractiveShell.deep_reload = True
c.InteractiveShell.editor = 'vim'
c.InteractiveShell.xmode = 'Context'

c.PromptManager.in_template  = 'In [\#]: '
c.PromptManager.in2_template = '   .\D.: '
c.PromptManager.out_template = 'Out[\#]: '
c.PromptManager.justify = True

c.PrefilterManager.multi_line_specials = True

c.AliasManager.user_aliases = [
         ('la', 'ls -al')
         ]
