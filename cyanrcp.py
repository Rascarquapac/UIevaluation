
class RCP():
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
class RCP_TBD(RCP):
    def __init__(self):
        super().__init__(0,False)
class RCP_DUO(RCP):
    def __init__(self):
        super().__init__(2,False)
class RCP_QUATTRO(RCP):
    def __init__(self):
        super().__init__(4,False)
class RCP_OCTO(RCP):
    def __init__(self):
        super().__init__(8,False)
class RCP_FULL(RCP):
    def __init__(self):
        super().__init__(200,False)
class RCP_DUO_J(RCP):
    def __init__(self):
        super().__init__(2,True)
class RCP_QUATTRO_J(RCP):
    def __init__(self):
        super().__init__(4,True)
class RCP_OCTO_J(RCP):
    def __init__(self):
        super().__init__(8,True)
class RCP_J(RCP):
    def __init__(self):
        super().__init__(200,True)
