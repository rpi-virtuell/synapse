# -*- coding: utf-8 -*-
# Copyright 2014 matrix.org
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from twisted.internet import defer

from base import RestServlet, client_path_pattern

import json
import logging
import urllib


logger = logging.getLogger(__name__)


def register_servlets(hs, http_server):
    ClientDirectoryServer(hs).register(http_server)


class ClientDirectoryServer(RestServlet):
    PATTERN = client_path_pattern("/directory/room/(?P<room_alias>[^/]*)$")

    @defer.inlineCallbacks
    def on_GET(self, request, room_alias):
        room_alias = self.hs.parse_roomalias(urllib.unquote(room_alias))

        dir_handler = self.handlers.directory_handler
        res = yield dir_handler.get_association(room_alias)

        defer.returnValue((200, res))

    @defer.inlineCallbacks
    def on_PUT(self, request, room_alias):
        # TODO(erikj): Exceptions
        content = json.loads(request.content.read())

        logger.debug("Got content: %s", content)

        room_alias = self.hs.parse_roomalias(urllib.unquote(room_alias))

        logger.debug("Got room name: %s", room_alias.to_string())

        room_id = content["room_id"]
        servers = content["servers"]

        logger.debug("Got room_id: %s", room_id)
        logger.debug("Got servers: %s", servers)

        # TODO(erikj): Check types.
        # TODO(erikj): Check that room exists

        dir_handler = self.handlers.directory_handler

        try:
            yield dir_handler.create_association(
                room_alias, room_id, servers
            )
        except:
            logger.exception("Failed to create association")

        defer.returnValue((200, {}))
