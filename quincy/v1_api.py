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

#set this to something reasonable.
DEFAULT_LIMIT = 200


def _convert_traits(dtraits):
    if dtraits is None:
        return None

    pairs = dtraits.split(';')
    lists = [pair.split(':') for pair in pairs]
    tuples = [(x[0].strip(), x[1].strip()) for x in lists]
    return dict(x for x in tuples)


def _find_streams(impl, req, resp, count=False):
    older_than = req.get_param('older_than')
    younger_than = req.get_param('younger_than')
    state = req.get_param('state')
    trigger = req.get_param('trigger_name')
    dtraits = req.get_param('distinguishing_traits')
    traits = _convert_traits(dtraits)
    mark = req.get_param('mark')
    limit = req.get_param('limit')

    if limit:
        try:
            limit = int(limit)
        except (ValueError, TypeError):
            limit = DEFAULT_LIMIT
    else:
        limit = DEFAULT_LIMIT

    if older_than:
        older_than = parser.parse(older_than)

    if younger_than:
        younger_than = parser.parse(younger_than)

    return impl.find_streams(count=count,
                            older_than=older_than,
                            younger_than=younger_than,
                            state=state,
                            trigger_name=trigger,
                            distinguishing_traits=traits,
                            mark=mark, limit=limit)


def _get_stream(impl, req, resp, stream_id):
    details = req.get_param('details')
    return impl.get_stream(stream_id, details)


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
        streams = _find_streams(self.impl, req, resp)
        resp.body = jsonutil.dumps(streams)


class StreamItem(common.FalconBase):
    def on_get(self, req, resp, stream_id):
        # could be /streams/123 or /streams/count
        stream_id = stream_id.lower()
        count = stream_id == 'count'
        if count:
            streams = _find_streams(self.impl, req, resp, count=count)
        else:
            streams = _get_stream(self.impl, req, resp, stream_id)
        resp.body = jsonutil.dumps(streams)

    def on_delete(self, req, resp, stream_id):
        self.impl.delete_stream(stream_id)

    def on_put(self, req, resp, stream_id):
        self.impl.reset_stream(stream_id)


def _find_events(impl, req, resp, count=False):
    from_datetime = req.get_param('from_datetime')
    to_datetime = req.get_param('to_datetime')
    event_name = req.get_param('event_name')
    traits = req.get_param('traits')
    traits = _convert_traits(traits)
    mark = req.get_param('mark')
    limit = req.get_param('limit')

    if limit:
        try:
            limit = int(limit)
        except (ValueError, TypeError):
            limit = DEFAULT_LIMIT
    else:
        limit = DEFAULT_LIMIT

    if from_datetime:
        from_datetime = parser.parse(from_datetime)

    if to_datetime:
        to_datetime = parser.parse(to_datetime)

    return impl.find_events(from_datetime=from_datetime,
                            to_datetime=to_datetime,
                            event_name=event_name,
                            traits=traits,
                            mark=mark, limit=limit, count=count)


def _get_event(impl, req, resp, message_id):
    return impl.get_event(message_id)


class EventCollection(common.FalconBase):
    # Retrieve events, independent of stream.
    # GET - list stream with qualifiers

    # Qualifiers:
    # datetime are ISO-8601 format, UTC
    # from_datetime - events with timestamp > from_datetime
    #                 default: now - 1hr
    # to_datetime - events with timestamp < to_datetime
    #                 default: now
    # event_name - events of event type
    # traits - find traits with specific traits
    # mark - marker for paged results
    # limit - max number of events to return (default: 200)
    def on_get(self, req, resp):
        events = _find_events(self.impl, req, resp)

        resp.body = jsonutil.dumps(events)


class EventItem(common.FalconBase):
    def on_get(self, req, resp, message_id):
        # could be /events/123 or /events/count
        message_id = message_id.lower()
        count = message_id == 'count'
        if count:
            events = _find_events(self.impl, req, resp, count=count)
        else:
            events = _get_event(self.impl, req, resp, message_id)

        resp.body = jsonutil.dumps(events)


class Schema(object):
    def _v(self):
        return "/v%d" % self.version

    def __init__(self, version, api, impl):
        self.api = api
        self.impl = impl
        self.version = version

        self.stream_collection = StreamCollection(impl)
        self.stream_item = StreamItem(impl)

        self.event_collection = EventCollection(impl)
        self.event_item = EventItem(impl)

        # Can't have a /streams/{item} route *and* a
        # /streams/foo route. Have to overload the StreamItem
        # handler.
        self.api.add_route('%s/streams/{stream_id}' % self._v(),
                           self.stream_item)
        self.api.add_route('%s/streams' % self._v(), self.stream_collection)

        self.api.add_route('%s/events/{message_id}' % self._v(), self.event_item)
        self.api.add_route('%s/events' % self._v(), self.event_collection)

