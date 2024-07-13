import sqlite3
import redis
import os


class Database():
    def __init__(self, file, *args):
        if file:
            self.conn = sqlite3.connect(file)
        else:
            self.conn = None
        self.cursor = self.conn.cursor()
        self.cache = redis.Redis(host=os.environ.get("REDIS_HOST", "localhost"), port=os.environ.get("REDIS_PORT", 6379), db=args['db'])

    def execute(self, query, *args):
        result = self.cursor.execute(query, args)
        self.conn.commit()
        fetched_result = result.fetchall()
        return fetched_result

    def set_cache(self, key, value):
        self.cache.set(key, value)

    def get_cache(self, key):
        return self.cache.get(key)