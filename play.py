import sys
from src import main

w = 0
help = 0
for opt in sys.argv:
    if opt == '-window' or opt == '-w':
        w = 1
    if opt == '-help' or opt == '-h':
        print('-window   -w   Open in window mode')
        help = 1

if not help:
    game = main.Main(w, resolution = (1200, 768))
    game.run()
