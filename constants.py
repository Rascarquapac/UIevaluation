from enum import StrEnum,auto,unique
@unique
class CameraLensDevice (StrEnum):
    IP       = auto()  # Transparent connection
    CI0      = auto()  # Simple serial to IP conversion
    RIO_LIVE = auto()  # Serial to IP with multiple USB/IP connectors and LAN packets management
    RIO      = auto()  # Serial to IP  with multiple USB/connector, LAN and WAN packets management
    NIO      = auto()  # Multiple USB/connector, LAN packets management
    RSBM     = auto()  # IPtoBlackMagic SDI 
    UNDEFINED= auto()  # Undefined device
# Get a list of all values
if __name__ == "__main__":
    all_values = [member.value for member in CameraLensDevice]
    print(all_values)