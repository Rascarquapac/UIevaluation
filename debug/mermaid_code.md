:::mermaid
graph RL
subgraph Mini Camera
ATOMONE_0{{"ATOMONE_0 fa:fa-camera-retro"}}---|CY-CBL-6P-DCHIP-02|CI0_0
  subgraph ATOMONE_0_cameralens [Iris control required]
    ATOMONE_0
  end
ATOMONEMINIZOOM_0{{"ATOMONEMINIZOOM_0 fa:fa-camera-retro"}}---|CY-CBL-6P-DCHIP-02|CI0_0
  subgraph ATOMONEMINIZOOM_0_cameralens [Iris/Zoom/Focus control required]
    ATOMONEMINIZOOM_0
  end
end
subgraph CineStyle
EVA1_0{{"EVA1_0 fa:fa-camera-retro"}}---|Ethernet-RJ45|RIO-LIVE_0
Cineservo_EVA1_0([Cineservo])---|CY-CBL-6P-B4-02|RIO-LIVE_0
  subgraph EVA1_0_cameralens [Iris/Zoom/Focus control required]
    EVA1_0
    Cineservo_EVA1_0
  end
BURANO_0{{"BURANO_0 fa:fa-camera-retro"}}---|Ethernet-RJ45|RIO-LIVE_1
Cabrio_BURANO_0([Cabrio])---|CY-CBL-6P-B4-02+
CY-CBL-6P-FUJI-02|RIO-LIVE_1
  subgraph BURANO_0_cameralens [Iris/Zoom/Focus control required]
    BURANO_0
    Cabrio_BURANO_0
  end
FX9-XDCA_0{{"FX9-XDCA_0 fa:fa-camera-retro"}}---|XDCAback|RIO-LIVE_2
Cabrio_FX9-XDCA_0([Cabrio])---|CY-CBL-6P-B4-02+
CY-CBL-6P-FUJI-02|RIO-LIVE_2
  subgraph FX9-XDCA_0_cameralens [Iris/Zoom/Focus control required]
    FX9-XDCA_0
    Cabrio_FX9-XDCA_0
  end
VENICE1_0{{"VENICE1_0 fa:fa-camera-retro"}}---|Ethernet-RJ45|RIO-LIVE_3
  subgraph VENICE1_0_cameralens [Iris/Zoom/Focus control required]
    VENICE1_0
    Primelens_VENICE1_0
  end
end
subgraph Mirrorless
BGH1_0{{"BGH1_0 fa:fa-camera-retro"}}---|Ethernet-RJ45|RIO-LIVE_4
  subgraph BGH1_0_cameralens [Iris control required]
    BGH1_0
    Primelens_BGH1_0
  end
ALPHA7CMARK2_0{{"ALPHA7CMARK2_0 fa:fa-camera-retro"}}---|USB-A-to-USB-C|IP_0
  subgraph ALPHA7CMARK2_0_cameralens [Iris control required]
    ALPHA7CMARK2_0
  end
end
subgraph Handheld Camcorder
JVCGY-HM850_0{{"JVCGY-HM850_0 fa:fa-camera-retro"}}---|JVCUSB-to-IP|IP_1
  subgraph JVCGY-HM850_0_cameralens [Iris/Zoom/Focus control required]
    JVCGY-HM850_0
    CameraIntegrated_JVCGY-HM850_0
  end
end
subgraph PTZ
AW-HE130_0{{"AW-HE130_0 fa:fa-camera-retro"}}---|Ethernet-RJ45|IP_2
  subgraph AW-HE130_0_cameralens [Iris/Zoom/Focus control required]
    AW-HE130_0
    CameraIntegrated_AW-HE130_0
  end
BRC-X1000_0{{"BRC-X1000_0 fa:fa-camera-retro"}}---|Ethernet-RJ45|IP_2
  subgraph BRC-X1000_0_cameralens [Iris/Zoom/Focus control required]
    BRC-X1000_0
    CameraIntegrated_BRC-X1000_0
  end
end
subgraph Shoulder Camcorder
VARICAM_0{{"VARICAM_0 fa:fa-camera-retro"}}---|Ethernet-RJ45|IP_3
  subgraph VARICAM_0_cameralens [No lens control required]
    VARICAM_0
    B4-Mount_VARICAM_0
  end
PXW-500_0{{"PXW-500_0 fa:fa-camera-retro"}}---|CY-CBL-SONY-8P-03|RIO-LIVE_5
B4-Mount_PXW-500_0([B4-Mount])---|CY-CBL-6P-B4-02|RIO-LIVE_5
  subgraph PXW-500_0_cameralens [Iris/Zoom/Focus control required]
    PXW-500_0
    B4-Mount_PXW-500_0
  end
end
subgraph BBlock
FCB-7520_0{{"FCB-7520_0 fa:fa-camera-retro"}}---|CY-CBL-6P-FAN100|CI0_1
  subgraph FCB-7520_0_cameralens [Iris control required]
    FCB-7520_0
    B4-Mount_FCB-7520_0
  end
end
subgraph "Control Room" 
CI0_0 --- |Ethernet|MiniCameraSwitch
RIO-LIVE_0 --- |Ethernet|CineStyleSwitch
RIO-LIVE_1 --- |Ethernet|CineStyleSwitch
RIO-LIVE_2 --- |Ethernet|CineStyleSwitch
RIO-LIVE_3 --- |Ethernet|CineStyleSwitch
RIO-LIVE_4 --- |Ethernet|MirrorlessSwitch
IP_0 --- |Ethernet|MirrorlessSwitch
IP_1 --- |Ethernet|HandheldCamcorderSwitch
IP_2 --- |Ethernet|PTZSwitch
IP_3 --- |Ethernet|ShoulderCamcorderSwitch
RIO-LIVE_5 --- |Ethernet|ShoulderCamcorderSwitch
CI0_1 --- |Ethernet|BBlockSwitch
MiniCameraSwitch --- |Ethernet|CY-RCP-DUO_0
CineStyleSwitch --- |Ethernet|CY-RCP-DUO-J_0
MirrorlessSwitch --- |Ethernet|CY-RCP-DUO-J_4
CineStyleSwitch --- |Ethernet|CY-RCP-DUO-J_1
CineStyleSwitch --- |Ethernet|CY-RCP-DUO-J_2
CineStyleSwitch --- |Ethernet|CY-RCP-DUO-J_3
MirrorlessSwitch --- |Ethernet|CY-RCP-DUO-J_5
HandheldCamcorderSwitch --- |Ethernet|CY-RCP-DUO-J_6
PTZSwitch --- |Ethernet|CY-RCP-DUO-J__0
ShoulderCamcorderSwitch --- |Ethernet|CY-RCP-DUO-J_7
BBlockSwitch --- |Ethernet|CY-RCP-DUO-J_9
ShoulderCamcorderSwitch --- |Ethernet|CY-RCP-DUO-J_8
end

:::
