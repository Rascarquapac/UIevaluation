from enum import StrEnum,auto,unique
@unique
class CameraLensDevice (StrEnum):
    IP        = auto()  # Transparent connection
    CI0       = auto()  # Simple serial to IP conversion
    RIO_LIVE  = auto()  # Serial to IP with multiple USB/IP connectors and LAN packets management
    RIO       = auto()  # Serial to IP  with multiple USB/connector, LAN and WAN packets management
    NIO       = auto()  # Multiple USB/connector, LAN packets management
    RSBM      = auto()  # IPtoBlackMagic SDI 
    UNDEFINED = auto()  # Undefined device
class CameraProtocol():
    def __init__(self,brand,type,cable,supportURL,max_delay,control_coverage,bidirectionnal):
        self.brand = brand
        self.type = type
        self.cable = cable
        self.supportURL = supportURL
        self.max_delay = max_delay
        self.control_coverage = control_coverage
        self.bidirectional = bidirectionnal
class Camera(CameraProtocol):
    def __init__(self,protocol,model,reference,mount,b4_connector):
        for key,value in protocol.__dict__.items():
            self.__dict__[key] = value
        self.model     = model
        self.reference = reference
        self.mount     = mount
        self.b4_connector = b4_connector

# Get a list of all values
if __name__ == "__main__":
    all_values = [member.value for member in CameraLensDevice]
    print(all_values)