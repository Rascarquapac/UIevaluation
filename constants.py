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

class CyanGlue():
    def __init__(self,serial_port_max,usba_port_max,ethernet_port_max,poe_powered):
        self.instance_id = 0
        self.serial_port_used = 0
        self.usba_port_used = 0
        self.ethernet_port_used = 0
        self.instanciated = False
        self.serial_port_max  = serial_port_max
        self.usba_port_max = usba_port_max
        self.ethernet_port_max = ethernet_port_max
        self.poe_powered = poe_powered
class CI0(CyanGlue):
    def __init__(self):
        CyanGlue.__init__(2,0,0,True)
class CI03P(CyanGlue):
    def __init__(self):
        CyanGlue.__init__(3,0,0,True)
class RSBM(CyanGlue):
    def __init__(self):
        CyanGlue.__init__(0,0,0,True)
        self.sdi_in_port = 1
        self.sdi_out_port = 1
class RIO(CyanGlue):
    def __init__(self):
        CyanGlue.__init__(2,2,1,False)
class NIO(CyanGlue):
    def __init__(self):
        CyanGlue.__init__(0,2,1,False)
        self.gpio_used = 0
        self.gpio_max  = 16
class CyanRCP():
    def __init__(self,licence,joystick):
        self.instance_id = 0
        self.jack_port_used = 0
        self.usba_port_used = 0
        self.ethernet_port_used = 0
        self.instanciated = False
        self.jack_port_max  = 1
        self.usba_port_max = 2
        self.ethernet_port_max = 1
        self.poe_powered = True
        self.joystick = joystick
        self.licence  = licence
class RCP_DUO(CyanRCP):
    def __init__(self):
        CyanRCP(2,False)
class RCP_QUATTRO(CyanRCP):
    def __init__(self):
        CyanRCP(4,False)
class RCP_OCTO(CyanRCP):
    def __init__(self):
        CyanRCP(8,False)
class RCP(CyanRCP):
    def __init__(self):
        CyanRCP(200,False)
class RCP_DUO_J(CyanRCP):
    def __init__(self):
        CyanRCP(2,True)
class RCP_QUATTRO_J(CyanRCP):
    def __init__(self):
        CyanRCP(4,True)
class RCP_OCTO_J(CyanRCP):
    def __init__(self):
        CyanRCP(8,True)
class RCP_J(CyanRCP):
    def __init__(self):
        CyanRCP(200,True)
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
class Lens():
    def __init__(self):
        pass

# Get a list of all values
if __name__ == "__main__":
    all_values = [member.value for member in CameraLensDevice]
    print(all_values)