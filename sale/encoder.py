# this file will encode django objects to json
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from json import loads, dumps

def serialize_object(obj):
    temp_output = serializers.serialize("python", [obj])[0]
    output = {}
    #adding all fields to the array
    for key in temp_output["fields"].keys():
        output[key] = temp_output["fields"][key]
    #adding info dictionary
    output['info'] = {'class': temp_output['model']}
    output['id'] = temp_output['pk']
    output = dumps(output, cls=DjangoJSONEncoder)
    return loads(output)
    
def serialize_iterable(objs):
    temp_output = serializers.serialize("python", objs)
    output = []
    for obj in temp_output:
        obj_dict = {}
        for key in obj["fields"].keys():
            obj_dict[key] = obj["fields"][key]
            obj_dict['info'] = {'class': obj['model']}
            obj_dict['id'] = obj['pk']
            
        output.append(loads(dumps(obj_dict, cls=DjangoJSONEncoder)))
        
    return output