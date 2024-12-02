:::mermaid
graph RL
subgraph PTZ
CameraIntegrated_AW-UE150_0([CameraIntegrated])<-->AW-UE150_0
AW-UE150_0[AWUE1500]<-->|Ethernet-RJ45|IP_13
end
subgraph Shoulder Camcorder
PXW-350_0{{"PXW-350_0 fa:fa-camera-retro"}}---|CY-CBL-SONY-8P-03|CI0_19
  subgraph PXW-350_0_cameralens [No lens control required]
    PXW-350_0
    B4-Mount_PXW-350_0
  end
end
subgraph "Control Room" 
IP_13 --- |Ethernet|PTZSwitch
CI0_19 --- |Ethernet|ShoulderCamcorderSwitch
PTZSwitch --- |Ethernet|CY-RCP-DUO-J__0
ShoulderCamcorderSwitch --- |Ethernet|CY-RCP-DUO-J_0
end

:::
