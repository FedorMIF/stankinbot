# -*- coding: utf-8 -*-
import re

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from os import listdir
from os.path import isfile, join

onlyfiles = [f for f in listdir('src/') if isfile(join('src/', f))]

for f in onlyfiles:
    drawing = svg2rlg(f'src/{f}')
    f = re.sub('\.svg', '.png', f)
    renderPM.drawToFile(drawing, f'src/png/{f}', fmt='PNG')