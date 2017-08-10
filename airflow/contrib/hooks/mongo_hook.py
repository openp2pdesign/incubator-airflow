# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
MongoHook module
"""

import logging

from pymongo import MongoClient

from airflow.exceptions import AirflowException
from airflow.hooks.base_hook import BaseHook


class RedisHook(BaseHook):
    """
    Hook to interact with Mongo database
    """
    def __init__(self, redis_conn_id='mongo_default'):
        """
        Prepares hook to connect to a Mongo database.

        :param conn_id:     the name of the connection that has the parameters
                            we need to connect to Mongo.
        """
        self.mongo_conn_id = redis_mongo_id
        self.client = MongoClient()
        conn = self.get_connection(self.redis_conn_id)
        self.host = conn.host
        self.port = int(conn.port)
        self.password = conn.password
        self.db = int(conn.extra_dejson.get('db', 0))
        self.logger = logging.getLogger(__name__)
        self.logger.debug(
            '''Connection "{conn}":
            \thost: {host}
            \tport: {port}
            \textra: {extra}
            '''.format(
                conn=self.redis_conn_id,
                host=self.host,
                port=self.port,
                extra=conn.extra_dejson
            )
        )

    def get_conn(self):
        """
        Returns a Redis connection.
        """
        if not self.client:
            self.logger.debug(
                'generating Mongo client for conn_id "{conn}" on '
                '{host}:{port}:{db}'.format(conn=self.redis_conn_id,
                                            host=self.host,
                                            port=self.port,
                                            db=self.db))
            try:
                self.client = StrictRedis(
                    host=self.host,
                    port=self.port,
                    password=self.password,
                    db=self.db)
            except Exception as general_error:
                raise AirflowException(
                    'Failed to create Mongo client, error: {error}'.format(
                        error=str(general_error)
                    )
                )

        return self.client

    def key_exists(self, key):
        """
        Checks if a key exists in Mongo database

        :param key: The key to check the existence.
        :type key: string
        """
        return self.get_conn().exists(key)
