
import data as d
from multiprocessing import Process


d.init()
def foo():
    d.add_num(132)
p  =Process(target=foo)
print("starting process")
p.start()

d.out()
print('joining')
p.join()
d.out()
print('done')

