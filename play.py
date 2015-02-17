import sys
from src import main

w = 0
resolution = 1200, 768
for opt in sys.argv:
    if opt == '-w':
        w = 1
    if ',' in opt:
        s = opt.replace('(', '')
        s = s.replace(')', '')
        width, height = s.split(',')
        width = int(width)
        height = int(height)
        resolution = width, height
game = main.Main(w, resolution)
game.run()
