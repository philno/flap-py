import pygal
import json
from pygal.style import CleanStyle

generations = []
counter = 1
try:
    while(True):
        filePath = 'stats/birds_gen' + str(counter) + '.json'
        with open(filePath, mode='r') as f:
            currentGen = json.load(f)
        generations.append(currentGen)
        counter += 1
except:
    # ignore
    pass

GEN_LEN = len(generations)
GEN_LABELS = range(1, GEN_LEN + 1)

# map all birds to their score value
scores = []
bestScores = []
topScores = []
avgScores = []
showBest = 16
for gen in generations:
    current = [b['score'] for b in gen]
    current.sort()
    scores.append(current)
    current = current[-showBest:]
    bestScores.append(current)
    avgScores.append(sum(current) / showBest)
    topScores.append(current[-1])
        
score_chart = pygal.Line(x_title='Rank (lower is better)', y_title='Score (higher is better)', logarithmic=True)
score_chart.title = 'Score for best ' + str(showBest) + ' of each generation (logarithmic)'
score_chart.x_labels = range(showBest, 0, -1)
for i, b in enumerate(bestScores):
    score_chart.add('Generation ' + str(i + 1), b)
score_chart.render_in_browser()

top_chart = pygal.Line(x_title='Generation', y_title='Score (higher is better)', fill=True)
top_chart.title = 'Top Score and Average Score of best ' + str(showBest) + ' of each generation'
top_chart.x_labels = GEN_LABELS
top_chart.add('Top Score', topScores)
top_chart.add('Average Score of best ' + str(showBest), avgScores)
top_chart.render_in_browser()

box_plot = pygal.Box(box_mode="tukey", x_title='Generation', y_title='Score (higher is better)', logarithmic=True)
box_plot.title = 'Score for each generation (logarithmic tukey box plot)'
box_plot.text = 'abc'
box_plot.x_labels = GEN_LABELS
for i, b in enumerate(scores):
    box_plot.add('Generation ' + str(i + 1), b)
box_plot.render_in_browser()