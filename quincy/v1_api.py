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

import json

import common


class EventCollection(common.FalconBase):
    def on_get(self, req, resp):
        events = self.impl.get_events(resp)
        resp.body = json.dumps(event)


class EventItem(common.FalconBase):
    pass


class Schema(object):
    def _v(self):
        return "/v%d" % self.version

    def __init__(self, version, api, impl):
        self.api = api
        self.impl = impl
        self.event_collection = EventCollection(impl)
        self.event_item = EventItem(impl)
        self.version = version

        self.api.add_route('%s/events' % self._v(),  self.event_collection)
        self.api.add_route('%s/events/{event_id}' % self._v(), self.event_item)
