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
    # id
    # distinquishing_traits - find stream by dtrait values.
    #
    # Actions on a Stream:
    # details - get full details on stream (including distriquishing traits)
    # events - get the events collected for this stream.
    def on_get(self, req, resp):
        streams = self.impl.get_streams(resp)
        dicts = [stream.to_dict() for stream in streams]
        resp.body = json.dumps(dicts)


class StreamItem(common.FalconBase):
    pass


class Schema(object):
    def _v(self):
        return "/v%d" % self.version

    def __init__(self, version, api, impl):
        self.api = api
        self.impl = impl
        self.version = version

        self.stream_collection = StreamCollection(impl)
        self.stream_item = StreamItem(impl)

        self.api.add_route('%s/streams' % self._v(),
                           self.stream_collection)
        self.api.add_route('%s/streams/{stream_id}' % self._v(),
                           self.stream_item)
