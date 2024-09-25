:::mermaid
graph RL
subgraph Minicam Motorizable
ATOMONE_0{{"ATOMONE_0 fa:fa-camera-retro"}}---|CY-CBL-6P-DCHIP-02|CI0_4
  subgraph ATOMONE_0_cameralens [self.Iris/Zoom/Focus control required]
    ATOMONE_0
    CameraIntegrated_ATOMONE_0
  end
ATOMONE_1{{"ATOMONE_1 fa:fa-camera-retro"}}---|CY-CBL-6P-DCHIP-02|CI0_4
  subgraph ATOMONE_1_cameralens [self.Iris/Zoom/Focus control required]
    ATOMONE_1
    CameraIntegrated_ATOMONE_1
  end
ATOMONEMINIZOOM_0{{"ATOMONEMINIZOOM_0 fa:fa-camera-retro"}}---|CY-CBL-6P-DCHIP-02|CI0_5
  subgraph ATOMONEMINIZOOM_0_cameralens [self.Iris/Zoom/Focus control required]
    ATOMONEMINIZOOM_0
    CameraIntegrated_ATOMONEMINIZOOM_0
  end
ATOMONEMINIZOOM_1{{"ATOMONEMINIZOOM_1 fa:fa-camera-retro"}}---|CY-CBL-6P-DCHIP-02|CI0_5
  subgraph ATOMONEMINIZOOM_1_cameralens [self.Iris/Zoom/Focus control required]
    ATOMONEMINIZOOM_1
    CameraIntegrated_ATOMONEMINIZOOM_1
  end
end
subgraph Handheld Camcorder
JVCGY-HM850_0{{"JVCGY-HM850_0 fa:fa-camera-retro"}}---|JVCUSB-to-IP|IP_5
  subgraph JVCGY-HM850_0_cameralens [self.Iris/Zoom/Focus control required]
    JVCGY-HM850_0
    CameraIntegrated_JVCGY-HM850_0
  end
end
subgraph PTZ
AW-HE130_0{{"AW-HE130_0 fa:fa-camera-retro"}}---|Ethernet-RJ45|IP_6
  subgraph AW-HE130_0_cameralens [self.Iris/Zoom/Focus control required]
    AW-HE130_0
    CameraIntegrated_AW-HE130_0
  end
AW-HE130_1{{"AW-HE130_1 fa:fa-camera-retro"}}---|Ethernet-RJ45|IP_6
  subgraph AW-HE130_1_cameralens [self.Iris/Zoom/Focus control required]
    AW-HE130_1
    CameraIntegrated_AW-HE130_1
  end
AW-HE130_2{{"AW-HE130_2 fa:fa-camera-retro"}}---|Ethernet-RJ45|IP_6
  subgraph AW-HE130_2_cameralens [self.Iris/Zoom/Focus control required]
    AW-HE130_2
    CameraIntegrated_AW-HE130_2
  end
BRC-X400_0{{"BRC-X400_0 fa:fa-camera-retro"}}---|Ethernet-RJ45|IP_6
  subgraph BRC-X400_0_cameralens [self.Iris/Zoom/Focus control required]
    BRC-X400_0
    CameraIntegrated_BRC-X400_0
  end
end
subgraph CineStyle
AU-EVA1_0{{"AU-EVA1_0 fa:fa-camera-retro"}}---|Ethernet-RJ45|IP_7
  subgraph AU-EVA1_0_cameralens [self.No lens control required]
    AU-EVA1_0
  end
AU-EVA1_1{{"AU-EVA1_1 fa:fa-camera-retro"}}---|Ethernet-RJ45|IP_7
  subgraph AU-EVA1_1_cameralens [self.No lens control required]
    AU-EVA1_1
  end
BURANO_0{{"BURANO_0 fa:fa-camera-retro"}}---|Ethernet-RJ45|IP_7
  subgraph BURANO_0_cameralens [self.No lens control required]
    BURANO_0
  end
FX9-XDCA_0{{"FX9-XDCA_0 fa:fa-camera-retro"}}---|XDCAback|IP_7
  subgraph FX9-XDCA_0_cameralens [self.No lens control required]
    FX9-XDCA_0
  end
FX9-XDCA_1{{"FX9-XDCA_1 fa:fa-camera-retro"}}---|XDCAback|IP_7
  subgraph FX9-XDCA_1_cameralens [self.No lens control required]
    FX9-XDCA_1
  end
end
subgraph Mirrorless
BGH1_0{{"BGH1_0 fa:fa-camera-retro"}}---|Ethernet-RJ45|IP_8
  subgraph BGH1_0_cameralens [self.No lens control required]
    BGH1_0
  end
ALPHA_0{{"ALPHA_0 fa:fa-camera-retro"}}---|USB-A-to-USB-C|IP_8
  subgraph ALPHA_0_cameralens [self.No lens control required]
    ALPHA_0
  end
end
subgraph Shoulder Camcorder
VARICAM_0{{"VARICAM_0 fa:fa-camera-retro"}}---|Ethernet-RJ45|IP_9
  subgraph VARICAM_0_cameralens [self.No lens control required]
    VARICAM_0
    B4-Mount_VARICAM_0
  end
PXW-500_0{{"PXW-500_0 fa:fa-camera-retro"}}---|CY-CBL-SONY-8P-03|CI0_6
  subgraph PXW-500_0_cameralens [self.No lens control required]
    PXW-500_0
    B4-Mount_PXW-500_0
  end
end
subgraph BBlock
FCB-8230_0{{"FCB-8230_0 fa:fa-camera-retro"}}---|CY-CBL-6P-FAN100|CI0_7
  subgraph FCB-8230_0_cameralens [self.No lens control required]
    FCB-8230_0
    B4-Mount_FCB-8230_0
  end
FCB-8230_1{{"FCB-8230_1 fa:fa-camera-retro"}}---|CY-CBL-6P-FAN100|CI0_7
  subgraph FCB-8230_1_cameralens [self.No lens control required]
    FCB-8230_1
    B4-Mount_FCB-8230_1
  end
end
subgraph "Control Room" 
CI0_4 --- |Ethernet|MinicamMotorizableSwitch
CI0_5 --- |Ethernet|MinicamMotorizableSwitch
IP_5 --- |Ethernet|HandheldCamcorderSwitch
IP_6 --- |Ethernet|PTZSwitch
IP_7 --- |Ethernet|CineStyleSwitch
IP_8 --- |Ethernet|MirrorlessSwitch
IP_9 --- |Ethernet|ShoulderCamcorderSwitch
CI0_6 --- |Ethernet|ShoulderCamcorderSwitch
CI0_7 --- |Ethernet|BBlockSwitch
MinicamMotorizableSwitch --- |Ethernet|CY-RCP-QUATTRO_0
HandheldCamcorderSwitch --- |Ethernet|CY-RCP-DUO-J_0
PTZSwitch --- |Ethernet|CY-RCP-QUATTRO-J_0
CineStyleSwitch --- |Ethernet|CY-RCP-DUO-J_1
CineStyleSwitch --- |Ethernet|CY-RCP-DUO-J_2
MirrorlessSwitch --- |Ethernet|CY-RCP-DUO-J_6
CineStyleSwitch --- |Ethernet|CY-RCP-DUO-J_3
CineStyleSwitch --- |Ethernet|CY-RCP-DUO-J_4
CineStyleSwitch --- |Ethernet|CY-RCP-DUO-J_5
MirrorlessSwitch --- |Ethernet|CY-RCP-DUO-J_7
ShoulderCamcorderSwitch --- |Ethernet|CY-RCP-DUO-J_8
BBlockSwitch --- |Ethernet|CY-RCP-DUO-J_10
BBlockSwitch --- |Ethernet|CY-RCP-DUO-J_11
ShoulderCamcorderSwitch --- |Ethernet|CY-RCP-DUO-J_9
end

:::
