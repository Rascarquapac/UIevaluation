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
EVA1_0{{"EVA1_0 fa:fa-camera-retro"}}---|Ethernet-RJ45|PassThru_1
Cineservo_EVA1_0([Cineservo])---|CY-CBL-6P-B4-02|PassThru_1
  subgraph EVA1_0_cameralens [Iris/Zoom/Focus control required]
    EVA1_0
    Cineservo_EVA1_0
  end
BURANO_0{{"BURANO_0 fa:fa-camera-retro"}}---|Ethernet-RJ45|PassThru_1
Cabrio_BURANO_0([Cabrio])---|CY-CBL-6P-B4-02|PassThru_1
  subgraph BURANO_0_cameralens [Iris/Zoom/Focus control required]
    BURANO_0
    Cabrio_BURANO_0
  end
FX9-XDCA_0{{"FX9-XDCA_0 fa:fa-camera-retro"}}---|XDCAback|PassThru_1
Cabrio_FX9-XDCA_0([Cabrio])---|CY-CBL-6P-B4-02|PassThru_1
  subgraph FX9-XDCA_0_cameralens [Iris/Zoom/Focus control required]
    FX9-XDCA_0
    Cabrio_FX9-XDCA_0
  end
VENICE1_0{{"VENICE1_0 fa:fa-camera-retro"}}---|Ethernet-RJ45|PassThru_1
Primelens_VENICE1_0([Primelens])---|CY-CBL-6P-TILTA-SERIAL|PassThru_1
  subgraph VENICE1_0_cameralens [Iris/Zoom/Focus control required]
    VENICE1_0
    Primelens_VENICE1_0
  end
end
subgraph Mirrorless
BGH1_0{{"BGH1_0 fa:fa-camera-retro"}}---|Ethernet-RJ45|PassThru_2
Primelens_BGH1_0([Primelens])---|CY-CBL-6P-TILTA-SERIAL|PassThru_2
  subgraph BGH1_0_cameralens [Iris control required]
    BGH1_0
    Primelens_BGH1_0
  end
ALPHA7CMARK2_0{{"ALPHA7CMARK2_0 fa:fa-camera-retro"}}---|USB-A-to-USB-C|PassThru_2
  subgraph ALPHA7CMARK2_0_cameralens [Iris control required]
    ALPHA7CMARK2_0
  end
end
subgraph Handheld Camcorder
JVCGY-HM850_0{{"JVCGY-HM850_0 fa:fa-camera-retro"}}---|JVCUSB-to-IP|PassThru_3
CameraIntegrated_JVCGY-HM850_0([Camera Integrated])---|Nocable|PassThru_3
  subgraph JVCGY-HM850_0_cameralens [Iris/Zoom/Focus control required]
    JVCGY-HM850_0
    CameraIntegrated_JVCGY-HM850_0
  end
end
subgraph PTZ
AW-HE130_0{{"AW-HE130_0 fa:fa-camera-retro"}}---|Ethernet-RJ45|PassThru_4
CameraIntegrated_AW-HE130_0([Camera Integrated])---|Nocable|PassThru_4
  subgraph AW-HE130_0_cameralens [Iris/Zoom/Focus control required]
    AW-HE130_0
    CameraIntegrated_AW-HE130_0
  end
BRC-X1000_0{{"BRC-X1000_0 fa:fa-camera-retro"}}---|Ethernet-RJ45|PassThru_4
CameraIntegrated_BRC-X1000_0([Camera Integrated])---|Nocable|PassThru_4
  subgraph BRC-X1000_0_cameralens [Iris/Zoom/Focus control required]
    BRC-X1000_0
    CameraIntegrated_BRC-X1000_0
  end
end
subgraph Shoulder Camcorder
VARICAM_0{{"VARICAM_0 fa:fa-camera-retro"}}---|Ethernet-RJ45|PassThru_5
B4-Mount_VARICAM_0([B4-Mount])---|Nocable|PassThru_5
  subgraph VARICAM_0_cameralens [No lens control required]
    VARICAM_0
    B4-Mount_VARICAM_0
  end
PXW-500_0{{"PXW-500_0 fa:fa-camera-retro"}}---|CY-CBL-SONY-8P-03|CI0_5
B4-Mount_PXW-500_0([B4-Mount])---|CY-CBL-6P-B4-02|CI0_5
  subgraph PXW-500_0_cameralens [Iris/Zoom/Focus control required]
    PXW-500_0
    B4-Mount_PXW-500_0
  end
end
subgraph BBlock
FCB-7520_0{{"FCB-7520_0 fa:fa-camera-retro"}}---|CY-CBL-6P-FAN100|CI0_6
B4-Mount_FCB-7520_0([B4-Mount])---|Nocable|CI0_6
  subgraph FCB-7520_0_cameralens [Iris control required]
    FCB-7520_0
    B4-Mount_FCB-7520_0
  end
end
subgraph "Control Room" 
CI0_0 --- |Ethernet|MiniCameraSwitch
PassThru_1 --- |Ethernet|CineStyleSwitch
PassThru_2 --- |Ethernet|MirrorlessSwitch
PassThru_3 --- |Ethernet|HandheldCamcorderSwitch
PassThru_4 --- |Ethernet|PTZSwitch
PassThru_5 --- |Ethernet|ShoulderCamcorderSwitch
CI0_5 --- |Ethernet|ShoulderCamcorderSwitch
CI0_6 --- |Ethernet|BBlockSwitch
MiniCameraSwitch --- |Ethernet|CY-RCP_0_0
CineStyleSwitch --- |Ethernet|CY-RCP_0_0
MirrorlessSwitch --- |Ethernet|CY-RCP_0_0
BBlockSwitch --- |Ethernet|CY-RCP_0_0
HandheldCamcorderSwitch --- |Ethernet|CY-RCP-DUO-J_0
PTZSwitch --- |Ethernet|CY-RCP-DUO-J_0
ShoulderCamcorderSwitch --- |Ethernet|CY-RCP-DUO-J_1
ShoulderCamcorderSwitch --- |Ethernet|CY-RCP-DUO-J_2
end

:::
