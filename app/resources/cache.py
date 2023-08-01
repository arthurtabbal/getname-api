from flask_caching import Cache

config = {
    "CACHE_TYPE": "FileSystemCache",
    "CACHE_DEFAULT_TIMEOUT": 3600,
    "CACHE_DIR": "resources/.cache",
}


cache = Cache()