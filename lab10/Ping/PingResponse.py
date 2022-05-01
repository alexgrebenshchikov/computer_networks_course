from enum import Enum


class PingResponse(Enum):
    SUCCESS = 0
    TIMEOUT = 1
    UNKNOWN_HOST = 2
    NETWORK_INACCESSIBLE = 3
    HOST_INACCESSIBLE = 4
    UNKNOWN_ERROR = 5

    @staticmethod
    def from_error_code(code):
        if code == 0:
            return PingResponse.NETWORK_INACCESSIBLE
        if code == 1:
            return PingResponse.HOST_INACCESSIBLE
        return PingResponse.UNKNOWN_ERROR
