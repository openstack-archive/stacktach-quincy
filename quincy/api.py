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

import falcon

import v1_api


class V1TestImplementation(object):
    def get_events(self, resp):
        return []


versions = {1: v1_api.Schema,
            2: v2_api.Schema}


enabled_versions = [1, 2]
api = falcon.API()

routes = []
for version in enabled_version:
    klass = versions[version]
    routes.append(version, klass(api))
