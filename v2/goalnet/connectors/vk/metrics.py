
from tinycalltrace import TinyCallTrace
class Datum:
    def __init__(value, time, dur=None):
        self.value = value
        self.time = time
        self.duration = dur

class Metrics():
    def __init__(self,data=None):
        self.data = data
        self.data.sort(key=lambda x: x[1],reverse=True)
        self.max_dur = 600

    def fix_to_down(self,data):
        tip = data[0][1]
        new_records = []
        for value,ts in data:
            if value and tip - ts > self.max_dur:
                new_records.append((0,ts+self.max_dur))
            tip = ts
        data +=new_records
        data.sort(key=lambda x: x[1],reverse=True)
        return data

    def sum_from_to(self, start, end):
        counter = 0
        tip = end
        data  =self.fix_to_down(self.data)
        for value,ts in data:
            dur = tip - ts
            if dur<0:
                continue
            if start > ts:
                counter += value*abs(start-tip)
                return counter
            counter += value*dur
            tip = ts
        return counter

    def __getitem__(self,key):
        if isinstance(key,slice):
            counter = 0
            if not key.step:
                return self.sum_from_to(key.start, key.stop)
            else:
                r = []
                ts = key.start
                while ts<key.stop:
                    s = self.sum_from_to(ts,ts+key.step)
                    r.append(s)
                    ts = ts + key.step
                return r

        for value,ts in self.data:
            if key>=ts:
                return value

def test_metrics():
    m = Metrics(list(zip(range(0,20,2),range(0,10))))
    m = Metrics([(1,0),(0,1),(1,2),(1,44)])
    print(m[3])
    print(m[0.5:5])
    print(m[0.5:40:2])

if __name__=="__main__":
    test_metrics()
