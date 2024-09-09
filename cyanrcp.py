
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
