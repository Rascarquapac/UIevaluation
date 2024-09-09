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
