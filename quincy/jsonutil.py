# Copyright (c) 2014 Dark Secret Software Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import json
import timex


class ObjectEncoder(json.JSONEncoder):
    ENCODE_MAP = {datetime.datetime: "datetime",
                  timex.TimeRange: "timex.TimeRange",
                  timex.Timestamp: "timex.Timestamp"}

    def default(self, obj):
        if type(obj) in self.ENCODE_MAP:
            typename = self.ENCODE_MAP[type(obj)]
            encoder = getattr(self,
                              '_encode_' + typename.replace('.', '_').lower())
            return encoder(obj, typename)
        return super(ObjectEncoder, self).default(obj)

    def _encode_datetime(self, obj, name):
        return {'__type__': name,
                'datetime': obj.isoformat()}

    def _encode_timex_timestamp(self, obj, name):
        return {'__type__': name,
                'timestamp': obj.timestamp.isoformat()}

    def _encode_timex_timerange(self, obj, name):
        return {'__type__': name,
                'begin': obj.begin.isoformat(),
                'end': obj.end.isoformat()}


def dumps(obj, **kw):
    kw['cls'] = ObjectEncoder
    return json.dumps(obj, **kw)
