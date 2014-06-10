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
import simport


import v1_api
import v2_api


class NotImplemented(Exception):
    pass


def _load_implementations(impl_map, versions, config):
    for version in versions:
        target = config.get('v%d_impl' % version)
        klass = simport.load(target)
        impl_map[version] = klass()


def _initialize(enabled_versions, implementation_map):
    # The de facto set of supported versions.
    versions = {1: v1_api.Schema,
                2: v2_api.Schema}

    api = falcon.API()

    routes = []
    for version in enabled_versions:
        klass = versions[version]
        impl = implementation_map.get(version)
        if not impl:
            raise NotImplemented("No implementation available for Quincy"
                                 " version %d" % version)
        routes.append(klass(version, api, impl))

    # TODO(sandy): We need to create the /v1
    #                                    ...
    #                                    /vN
    # resources here too.


if __name__ == '__main__':
    # There may have been prior versions
    # but they could be deprecated and dropped.
    # Only the versions specified here define
    # the currently supported StackTach.v3 API.
    enabled_versions = [1, 2]

    # The default implementation is internal and works with
    # a fake/static set of data.
    local_config = {'v1_impl': 'v1_impl:Impl',
                    'v2_impl': 'v2_impl:Impl'}

    impl_map = {}
    _load_implementations(impl_map, enabled_versions, local_config)

    # TODO(sandy): Overlay the impl_map with the implementations
    # specified in the config file.
    # config = ...
    # _load_implementations(impl_map, enabled_versions, config)

    _initialize(enabled_versions, impl_map)
