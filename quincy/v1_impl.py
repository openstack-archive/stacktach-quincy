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
import uuid


class Stream(object):
    def __init__(self, stream_id, trigger_name, state):
        self.last_updated = datetime.datetime.utcnow()
        self.stream_id = stream_id
        self.trigger_name = trigger_name
        self.state = state

    def to_dict(self):
        return {
            "distinguishing_traits": {
                "instance_id": str(uuid.uuid4()),
                "timestamp": {
                    "__type__": "timex.TimeRange",
                    "begin": "2015-01-26T00:00:00",
                    "end": "2015-01-27T00:00:00"
                }
            },
            "expire_timestamp": {
                "__type__": "datetime",
                "datetime": "2015-01-26T16:16:40.486940"
            },
            "fire_timestamp": None,
            "first_event": {
                "__type__": "datetime",
                "datetime": "2015-01-26T15:12:09.624219"
            },
            "id": self.stream_id,
            "last_event": {
                "__type__": "datetime",
                "datetime": str(self.last_updated)
            },
            "name": self.trigger_name,
            "state": self.state
        }


class Impl(object):
    def __init__(self, config, scratchpad):
        self.config = config
        self.scratchpad = scratchpad

    def get_streams(self, **kwargs):
        """kwargs may be:
            older_than
            younger_than
            state
            trigger_name
            distinquishing_traits
        """
        x = [Stream(1000, "EOD-Exists", "Collecting"),
             Stream(1001, "EOD-Exists", "Error"),
             Stream(1002, "Request-ID", "Ready")]

        return [stream.to_dict() for stream in x]

    def get_stream(self, stream_id, details):
        return Stream(str(uuid.uuid4()), "Request-ID", "Ready")

    def delete_stream(self, stream_id):
        pass

    def reset_stream(self, stream_id):
        pass
