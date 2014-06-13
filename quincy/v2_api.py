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
import v1_api


class ArchiveCollection(common.FalconBase):
    def on_get(self, req, resp):
        archives = self.impl.get_archives(resp)
        dicts = [archive.to_dict() for archive in archives]
        resp.body = json.dumps(dicts)


class ArchiveItem(common.FalconBase):
    def on_get(self, req, resp):
        return "{}"


class Schema(v1_api.Schema):
    def __init__(self, version, api, impl):
        super(Schema, self).__init__(version, api, impl)
        self.archive_collection = ArchiveCollection(impl)
        self.archive_item = ArchiveItem(impl)

        self.api.add_route('%s/archives' % self._v(),  self.archive_collection)
        self.api.add_route('%s/archives/{archive_id}' % self._v(),
                           self.archive_item)
