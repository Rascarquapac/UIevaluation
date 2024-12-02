:::mermaid
graph RL
subgraph PTZ
AW-UE150_0{{"AW-UE150_0 fa:fa-camera-retro"}}---|Ethernet-RJ45|IP_0
  subgraph AW-UE150_0_cameralens [Iris/Zoom/Focus control required]
    AW-UE150_0
    CameraIntegrated_AW-UE150_0
  end
end
subgraph Shoulder Camcorder
PXW-350_0{{"PXW-350_0 fa:fa-camera-retro"}}---|CY-CBL-SONY-8P-03|CI0_0
  subgraph PXW-350_0_cameralens [No lens control required]
    PXW-350_0
    B4-Mount_PXW-350_0
  end
end
subgraph "Control Room" 
IP_0 --- |Ethernet|PTZSwitch
CI0_0 --- |Ethernet|ShoulderCamcorderSwitch
PTZSwitch --- |Ethernet|CY-RCP-DUO-J__0
ShoulderCamcorderSwitch --- |Ethernet|CY-RCP-DUO-J_0
end

:::
