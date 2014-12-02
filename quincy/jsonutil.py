import json
import datetime
import timex


class ObjectEncoder(json.JSONEncoder):

    ENCODE_MAP = {datetime.datetime: "datetime",
                  timex.TimeRange: "timex.TimeRange",
                  timex.Timestamp: "timex.Timestamp"}

    def default(self, obj):
        if type(obj) in self.ENCODE_MAP:
            typename = self.ENCODE_MAP[type(obj)]
            encoder = getattr(self, '_encode_' + typename.replace('.', '_').lower())
            return encoder(obj, typename)
        return super(ObjectEncoder, self).default(obj)

    def _encode_datetime(self, obj, name):
        return {'__type__' : name,
                'datetime': obj.isoformat()}

    def _encode_timex_timestamp(self, obj, name):
        return {'__type__' : name,
                'timestamp': obj.timestamp.isoformat()}

    def _encode_timex_timerange(self, obj, name):
        return {'__type__' : name,
                'begin': obj.begin.isoformat(),
                'end': obj.end.isoformat()}


def dumps(obj, **kw):
    kw['cls'] = ObjectEncoder
    return json.dumps(obj, **kw)
