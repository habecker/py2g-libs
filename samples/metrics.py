from py2g_libs.mean import MeanMetrics
from py2g_libs.time import TimeMetrics
from py2g_libs.progress import ProgressMetrics
import random
from time import sleep

number_of_epochs = 20
number_of_steps = 100
mean = MeanMetrics()
time = TimeMetrics()
progress = ProgressMetrics()
progress.start(number_of_steps, name='step')
progress.start(number_of_epochs, name='epoch')
for j in range(0, number_of_epochs):
    time.start('epoch')
    progress.restart(name='step')
    for i in range(0, number_of_steps):
        progress.step(name='step')
        time.start('step')
        result = random.normalvariate(2., 1.5)
        quality = random.normalvariate(5., 3.)
        mean.add('result', result)
        mean.add('quality', quality)
        time.end('step')
        progress.toConsole(main='step', every=20, other=[mean, time])
        sleep(1./number_of_steps)
    progress.step(name='epoch')
    time.end('epoch')

progress.toConsole(every=1, other=[mean, time])