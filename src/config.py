#Spanish Wikipedia
BASE_URL = "https://es.wikipedia.org/wiki"
TARGET = "/Filosofía"


BASE_HEADERS = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "accept": "application/json",
    "accept-language": "es",
    "accept-encoding": "gzip, deflate, br, zstd",
}

FAILSAFE = 100