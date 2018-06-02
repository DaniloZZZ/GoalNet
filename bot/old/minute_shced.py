import config
import log
import tgflow as tgf
import schedule, time
import threading

lg=log.bot.info

tgf.configure(token=config.token,state='start')
def sch(i):
	def send():
            print('sending')
            tgf.send_state('notif',i.chat.id)
	#t = threading.Timer(sec, send)
	#t.start()
	#s.enter(sec,1,send)
	#s.run(blocking=False)
	lg('exit sch')
	return send

def set_sc(i):
    lg('sceduling every %i min'%int(i.text))
    j = schedule.every(int(i.text)).minutes.do(sch(i))
    return 'cancel', {'time':int(i.text), 'job':j}

def cancel(d):
    lg("cancelling. data",d)
    schedule.cancel_job(d.get('job'))
    lg("gobs running",schedule.jobs)
    return 'start'

UI ={
    'start':{
        't':'hello there!',
        'b':[
            {'create sch':lambda i: 'get_time'}
        ]
    },
    'get_time':{
        't':'send me minutes interval',
        'react':tgf.action(set_sc,react_to='text')
    },
    'cancel':{
        't':tgf.paste('cancel sched %i','time'),
        'b':[
            {'cancel':tgf.action(cancel)}
        ]

    }
}

def runs():
    while True:
        schedule.run_pending()
        time.sleep(1)
t = threading.Timer(1,runs)
t.start()

tgf.start(UI)


