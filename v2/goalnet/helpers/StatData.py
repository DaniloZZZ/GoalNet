from goalnet.helpers.log_init import log
import numpy as np

class Metrics:
    def __init__(self, data_type, providers=[], **kw):
        self.data_type = data_type
        self.providers_names = providers

    def get_providers_names(self):
        return self.providers_names

    def get(self, params, providers=[]):
        raise NotImplementedError

class Counter:
    def __init__(self, value=None):
        self.data = {}
        if value:
            self.data[value] = 1
    def __mul__(self, num):
        self.data = {k:v*num for k,v in self.data.items()}
        return self
    def __add__(self,value):
        if value==0:
            return self
        if isinstance(value, Counter):
            for k,v in value.data.items():
                val = self.data.get(k)
                if not val:
                    self.data[k] = 0
                self.data[k] += v
            return self
        val = self.data.get(value)
        if not val:
            self.data[value] = 0
        self.data[value] += 1
        return self
    def __radd__(self,value):
        return self.__add__(value)
    def dict(self):
        return self.data
    def __repr__(self):
        return "<Counter %s>"%self.data

class Number:
    def __init__(self, value=None):
        self.val = value
    def __mul__(self, num):
        return Number(self.val*num)
    def __add__(self, num):
        if isinstance(num,Number):
            return Number(self.val+num.val)
        return Number(self.val+num)
    def __radd__(self,value):
        return self.__add__(value)
    def dict(self):
        return {'val':self.val}
    def __repr__(self):
        return "<Number %s>"%self.val

def get_datum(val):
    if isinstance(val, int):
        return Number(val)
    else:
        return Counter(val)

class IntegralMetrics(Metrics):
    def get(self, params, providers):
        log.info("params of getting metrics %s"%params)
        start = params['start']
        end = params['end']

        duration  =  end-start
        step = params.get('step', duration)
        step_count = int(duration/step) if duration else 1
        domain_points = 43+13*step_count
        step_points = domain_points//step_count 
        dt = duration/(step_points) 
        log.debug("step count: %s, step_points: %s, step: %s"%(
            step_count,
            step_points,
            step)
        )

        domain = [ start + step*i for i in range(step_count) ] + [end]
        log.debug('domain for metrics: %s'%domain)
        prov = providers[0]
        values = []
        for step_start, step_end in zip(domain[:-1],domain[1:]):
            step_values = [ get_datum(prov[t])*dt for t in np.linspace(step_start, step_end, step_points, endpoint=False) ]
            val =  sum(step_values).dict()
            val.update({"time":step_start})
            values.append(val)

        log.info('returning values %s'%values)
        return {'data':values,'name':'integral','domain':domain}

class Records:
    def __init__(self, name, data=[]):
        self.name = name
        self.data = sorted(data, key=lambda x: x[1], reverse=True)

    def add(self, datum):
        self.data.append(datum)
        # sort the data if datum is from the past
        if len(self.data)>2:
            if datum[1] > self.data[-2][1]:
                self.data = sorted(self.data, key=lambda x: x[1], reverse=True)

    def get(self):
        return self.data

    def __getitem__(self,index):
        for value, ts in self.data:
            if index>=ts:
                return value
        # fallback to the oldest data
        return self.data[-1][0]

class StatData():
    def __init__(self, records_names=[], metrics_params=[]):
        self.records = {}
        self.metrics = {}
        self.datakey = 'value'
        self.timekey = 'time'
        for name in records_names:
            self.records[name]= Records(name=name)
        self.metrics['integral'] = IntegralMetrics(data_type='str')

    def record(self, data, action):
        record_name = data.get('name')
        if not record_name:
            return {"error":"no 'name' field for metric"}
        record = self.records.get(record_name)
        if action=='get':
            if not record:
                return {"error":'No such record'}
            return {'data':record.get()}
        if action=='put':
            if not record:
                # TODO: raise not found error
                log.error("No record with name '%s'"%record_name)
                return {"error":'No such record'}
            try:
                record.add((data[self.datakey],data[self.timekey]))
            except KeyError as e:
                return {"error":"key not found:%s"%e}
            return {'record_data_count':len(record.data)}
        if action=='add':
            self.records[record_name] = Records(name=record_name)
            return {'record_count':len(self.records)}
        if action=='delete':
            return self.records.pop(record_name, {'error':'no such records'})

    def metric(self, data, action):
        metrics_name = data.get('name')
        if not metrics_name:
            return {"error":"no 'name' field for metric"}
        metrics = self.metrics.get(metrics_name)
        if action=='get':
            if not metrics:
                # TODO: raise not found error
                log.error("No metrics with name '%s'"%metrics_name)
                return {"error":'No such metrics'}
            # get data providers
            if data.get('provider'):
                providers_names = [ data['provider'] ]
            else:
                providers_names = data['providers']
            # TODO: maybe should call self.record get here??
            try:
                providers = [ self.records[prov] for prov in providers_names ]
            except KeyError as e:
                return {"error":'no record found with name %s'%e}

            return metrics.get(params=data, providers=providers)

        if action=='add':
            self.metrics[metrics_name] = Metrics(**data)
            return {"status":"1"}

        if action=='delete':
            return self.metrics.pop(metrics_name,{'error':"no such metrics"})



