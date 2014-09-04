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
        self.distinquishing_traits = []

    def to_dict(self):
        return {"last_updated": str(self.last_updated),
                "stream_id": self.stream_id,
                "trigger_name": self.trigger_name,
                "state": self.state,
                "distinquishing_traits": self.distinquishing_traits}


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
        x = [Stream(str(uuid.uuid4()), "EOD-Exists", "Collecting"),
             Stream(str(uuid.uuid4()), "EOD-Exists", "Error"),
             Stream(str(uuid.uuid4()), "Request-ID", "Ready")]

        return [stream.to_dict() for stream in x]

    def get_stream(self, stream_id, details):
        return Stream(str(uuid.uuid4()), "Request-ID", "Ready")

    def delete_stream(self, stream_id):
        pass

    def reset_stream(self, stream_id):
        pass
