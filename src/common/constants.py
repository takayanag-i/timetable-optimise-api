from enum import Enum

BINARY_ZERO = 0
BINARY_ONE = 1


class ViolationCode(str, Enum):
    V1 = "v1"
    V3 = "v3"
