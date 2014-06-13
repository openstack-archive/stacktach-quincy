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

import v1_impl


class Archive(object):
    def __init__(self, aid, filename):
        self.aid = aid
        self.filename = filename

    def to_dict(self):
        return {"id": str(self.aid),
                "filename": self.filename}


class Impl(v1_impl.Impl):
    def get_archives(self, resp):
        filename_template = "events_%Y_%m_%d_%X_%f.dat"
        now = datetime.datetime.utcnow()
        ret = []
        for _ in range(4):
            ret.append(Archive(str(uuid.uuid4()),
                               now.strftime(filename_template)))
            now += datetime.timedelta(hours = 1)
        return ret
