import datetime
import json


class CustomEncoder(json.JSONEncoder):

    def default(self, obj):
        """
        This method will only be called if an object is passed to the parent JSON encoder in the case
        it doesn't know how to deal with.

        In case the object passed to the encode method of JSON that is by default json serializable [eg.: list]
         this method will not be called
        """
        if isinstance(obj, datetime.datetime):
            # Return a JSON object where each parameter of the datetime object is a key in a dictionary.
            return {
                '_type': 'datetime',
                'year': obj.year,
                'month': obj.month,
                'day': obj.day,
                'hour': obj.hour,
                'minute': obj.minute,
                'second': obj.second
            }
        elif isinstance(obj, datetime.timedelta):
            return {
                '_type': 'timedelta',
                'days': obj.days,
                'seconds': obj.seconds,
                'microseconds': obj.microseconds
            }

        # In case the object passed is not serializable by default and,
        # is not implemented above; the default method will fall through here. In which case:

        # Pass the object back to the default JSON handler and:
        return super().default(obj)  # Let the default JSON handler output the error: not serializable.


class CustomDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    @staticmethod
    def object_hook(obj):
        if '_type' in obj:
            decodes = {'datetime': datetime.datetime, 'timedelta': datetime.timedelta}
            data_type = obj.pop('_type')

        # This line will return either:
        # a decoded object of a type specified in the "decodes" dictionary
        # or obj without any modification to it's type in case the type is not implemented yet.

        return decodes.get(data_type, lambda **kwargs: kwargs)(**obj)


# Testing:

now = datetime.datetime.now()

encoded_datetime_data = json.dumps(now, cls=CustomEncoder, indent=2)
decoded_datetime_data = json.loads(encoded_datetime_data, cls=CustomDecoder)

encoded_timedelta_data = json.dumps(datetime.timedelta(0), cls=CustomEncoder, indent=2)
decoded_timedelta_data = json.loads(encoded_timedelta_data, cls=CustomDecoder)

encoded_array = json.dumps([1, 2, 3, 4], cls=CustomEncoder, indent=2)
decoded_array = json.loads(encoded_array, cls=CustomDecoder)

print(encoded_datetime_data)
print(decoded_datetime_data)
print(type(decoded_datetime_data))

print(encoded_timedelta_data)
print(decoded_timedelta_data)
print(type(decoded_timedelta_data))

print(encoded_array)
print(decoded_array)
print(type(decoded_array))


class Nothing:
    pass


# This will fail: (TypeError: Object of type Nothing is not JSON serializable)
encoded_nothing_data = json.dumps(Nothing(), cls=CustomEncoder)
decoded_nothing_data = json.loads(encoded_nothing_data, cls=CustomDecoder)

