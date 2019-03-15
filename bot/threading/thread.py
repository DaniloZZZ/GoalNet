import data as d
import threading

d.init()
d.out()
def foo():
    print("calling add_num from thread")
    d.add_num(132)

t  =threading.Thread(target=foo)
print("starting thread")
t.start()
print('joining to thread')
t.join()
d.out()
print('done')

