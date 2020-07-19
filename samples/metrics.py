from py2g_utils.mean import MeanMetrics
from py2g_utils.time import TimeMetrics
from py2g_utils.progress import ProgressMetrics
import random
from time import sleep

number_of_epochs = 5
number_of_steps = 10000
mean = MeanMetrics()
time = TimeMetrics()
progress = ProgressMetrics()
progress.start(number_of_steps)
progress.start(number_of_epochs, name='epochs')
for j in range(0, number_of_epochs):
    time.start('epoch')
    progress.restart()
    for i in range(0, number_of_steps):
        progress.step()
        time.start('step')
        result = random.normalvariate(2., 1.5)
        quality = random.normalvariate(5., 3.)
        mean.add('result', result)
        mean.add('quality', quality)
        time.end('step')
        progress.toConsole(every=500, other=[mean, time])
        sleep(1./number_of_steps)
    progress.step(name='epochs')
    time.end('epoch')

progress.toConsole(every=1, other=[mean, time])