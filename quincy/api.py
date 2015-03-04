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

import ConfigParser
import traceback


import falcon
import simport

import v1_api
import v2_api


class NotImplemented(Exception):
    pass


def _load_implementations(impl_map, versions, config, scratchpad):
    for version in versions:
        target = config.get('global', 'v%d_impl' % version)
        klass = simport.load(target)
        impl_map[version] = klass(config, scratchpad)


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
        print "Version %d using %s" % (version, impl)
        routes.append(klass(version, api, impl))

    # TODO(sandy): We need to create the top-level /v1, ... /vN
    # resources here too.
    return api


def _get_api(config_location=None):
    print "Using config_location=%s (None means default impl)" % config_location

    # The default implementation is internal and works with
    # a fake/static set of data.
    local_config = ConfigParser.ConfigParser()
    local_config.add_section('global')
    local_config.set('global', 'v1_impl', 'quincy.v1_impl:Impl')
    local_config.set('global', 'v2_impl', 'quincy.v2_impl:Impl')

    # There may have been prior versions
    # but they could be deprecated and dropped.
    # Only the versions specified here define
    # the currently supported StackTach.v3 API.
    enabled_versions = [1]  # [1, 2]

    if config_location:
        config = ConfigParser.ConfigParser()
        config.read(config_location)
        enabled_versions = [int(x) for x in
                                config.get('global', 'enabled_versions')
                                                            .split(',')]

    # Rather than every implementation duplicate resources, the
    # scratchpad is a shared storage area all the implementations
    # can use to share things (like pipeline drivers, etc).
    scratchpad = {}
    impl_map = {}
    _load_implementations(impl_map, enabled_versions, local_config,
        scratchpad)

    if config_location:
        # Overlay the impl_map with the implementations
        # specified in the config file.
        _load_implementations(impl_map, enabled_versions, config,
                              scratchpad)


    return _initialize(enabled_versions, impl_map)


def get_api(config_location=None):
    try:
        return _get_api(config_location)
    except Exception as e:
        print "Error getting API:", traceback.format_exc()
    return None
