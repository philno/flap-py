from appJar import gui
from random import uniform
from math import floor, sqrt

windowWidth = 800
windowHeight = 500
pipeWidth = 40
pipeColor = 'black'
gapHeight = 160
textSize = 32
def draw_pipe(x):
    """Draw a pipe"""
    gapMiddle = floor(uniform(0.25, 0.75) * windowHeight)
    step = gapHeight // 2
    gapTop = gapMiddle - step
    if (gapTop < 0):
        gapTop = 0
    gapBottom = gapMiddle + step
    if (gapBottom > windowHeight):
        gapBottom = windowHeight
    canvas.create_rectangle(x, 0, x + pipeWidth, gapTop, fill=pipeColor)
    canvas.create_rectangle(x, gapBottom, x + pipeWidth, windowHeight, fill=pipeColor)

app = gui('flap-py', str(windowWidth) + 'x' + str(windowHeight))

app.setFont(size=textSize)
canvas = app.addCanvas('game')
x = 100
while (x + 50 < windowWidth):
    draw_pipe(x)
    x = x + 4 * pipeWidth + 20
    
canvas.create_text(windowWidth/2, textSize + 2, text='0', fill='green')
centerY = windowHeight // 2
radius = 18
canvas.create_oval(radius, centerY - radius, radius*3, centerY + radius, fill='yellow')
app.go()