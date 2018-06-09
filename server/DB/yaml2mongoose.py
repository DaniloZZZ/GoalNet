#!/usr/bin/python3
import yaml
import argparse
import ntpath   # for getting filename from file

def dict2json(d,indent=0,tab='  ',mapper=None):
    res = ""
    if  type(d)==dict:
        res+='\n'+indent*tab+'{\n'
        for key,val in d.items():
            v = dict2json(val,
                           indent=indent+1,
                           tab=tab,
                           mapper=mapper
                          )
            res+= indent*tab
            res+='"%s":%s,\n'%(key,v)
        res+=indent*tab+'}'
        return res
    elif mapper:
        try:
            v = mapper(d)
            if v:
                return v
        except:
            pass
    if type(d)==str:
        res+= '"%s"'%(d)
    elif type(d)==list:
        if len(d)>1:
            raise Exception("Only len(1) lists allowed!")
        v = dict2json(d[0],
                       indent=indent+1,
                       tab=tab,
                       mapper=mapper
                      )
        res+= '[ %s ]'%v
    else:
        res+= str(d)
    return res

def mongoose_mapper(val):
    table={
        'date': 'Date',
        'oid':  'Schema.Types.ObjectId',
        'str':  'String',
        'int':  'Number',
        'bool': 'Boolean'
    }
    return table.get(val)

def dict2mongoose(d,name="test"):
    res= """
// this code is automatically created by ProjectBoost

var mongoose = require('mongoose');
var Schema = mongoose.Schema;
module.exports = 
%(schema)s;
"""%{
    'name':name,
    'schema': dict2json(d,mapper=mongoose_mapper)
}
    return res

def main():
    parser = argparse.ArgumentParser(
        description='Create files')
    parser.add_argument('yaml_file',
                        help='path to yaml file')
    parser.add_argument('-n','--name',
                        help='name of the entity')
    args = parser.parse_args()
    #print ('reading config from ',args.yaml_file)

    with open(args.yaml_file,'r') as f:
        try:
            d = yaml.load(f)
        except yaml.YAMLError as exc:
            import sys,os
            print("Error parsing config file",
                  file=sys.stderr)
            print(exc)
            sys.exit(os.EX_CONFIG)
            return "ERR"

    #print(dict2yml(d))
    #print(dict2json(d))
    #print(dict2json(d,mapper=mongoose_mapper))
    ## yaml_file is like ./foo/bar/name.yaml
    def_name = ntpath.basename(args.yaml_file).split('.')[0]
    name = args.name or def_name
    print(dict2mongoose(d,name=name))

if __name__=="__main__":
    main()


def dict2yml(d,indent=0,tab='  '):
    res = ""
    for key,val in d.items():
        res+= indent*tab
        res+=key+':'
        if  type(val)==dict:
            res+='\n'
            res+=dict2yml(val,
                          indent=indent+1,
                          tab=tab)
        else:
            res+= str(val)
            res+= '\n'
    return res
