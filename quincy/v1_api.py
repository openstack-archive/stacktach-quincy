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

from quincy import jsonutil

from dateutil import parser

import common


class StreamCollection(common.FalconBase):
    # HTTP Operations on a stream
    # GET - list stream with qualifiers
    # DELETE - mark stream for deletion
    # POST - move stream to READY or reset error count

    # GET Qualifiers:
    # older_than
    # younger_than
    # state
    # trigger_name
    # distinguishing_traits - find stream by dtrait values.
    #
    # Actions on a Stream:
    # details - get full details on stream (including events &
    #                                       distriquishing traits)

    def on_get(self, req, resp):
        older_than = req.get_param('older_than')
        younger_than = req.get_param('younger_than')
        state = req.get_param('state')
        trigger = req.get_param('trigger_name')
        traits = req.get_param('distinguishing_traits')

        if older_than:
            older_than = parser.parse(older_than)

        if younger_than:
            younger_than = parser.parse(younger_than)

        streams = self.impl.get_streams(older_than=older_than,
                                        younger_than=younger_than,
                                        state=state,
                                        trigger_name=trigger,
                                        distinguishing_traits=traits)
        resp.body = jsonutil.dumps(streams)


class StreamItem(common.FalconBase):
    def on_get(self, req, resp, stream_id, action=None):
        details = req.get_param('details')
        streams = self.impl.get_stream(stream_id, details)
        resp.body = jsonutil.dumps(streams)

    def on_delete(self, req, resp, stream_id):
        self.impl.delete_stream(stream_id)

    def on_put(self, req, resp, stream_id, action=None):
        reset = action == 'reset'
        self.impl.reset_stream(stream_id)


class StreamCount(common.FalconBase):
    def on_get(self, req, resp):
        older_than = req.get_param('older_than')
        younger_than = req.get_param('younger_than')
        state = req.get_param('state')
        trigger = req.get_param('trigger_name')
        traits = req.get_param('distinguishing_traits')

        if older_than:
            older_than = parser.parse(older_than)

        if younger_than:
            younger_than = parser.parse(younger_than)

        streams = self.impl.get_streams(count=True,
                                        older_than=older_than,
                                        younger_than=younger_than,
                                        state=state,
                                        trigger_name=trigger,
                                        distinguishing_traits=traits)
        resp.body = jsonutil.dumps(streams)


class Schema(object):
    def _v(self):
        return "/v%d" % self.version

    def __init__(self, version, api, impl):
        self.api = api
        self.impl = impl
        self.version = version

        self.stream_collection = StreamCollection(impl)
        self.stream_item = StreamItem(impl)
        self.stream_count = StreamCount(impl)

        self.api.add_route('%s/streams' % self._v(),
                           self.stream_collection)
        self.api.add_route('%s/streams/{stream_id}' % self._v(),
                           self.stream_item)
        self.api.add_route('%s/streams/count' % self._v(),
                           self.stream_count)
