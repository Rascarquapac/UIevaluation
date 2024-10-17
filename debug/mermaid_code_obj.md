:::mermaid
graph RL
subgraph Minicam Motorizable
ATOMONE_0{{"ATOMONE_0 fa:fa-camera-retro"}}---|CY-CBL-6P-DCHIP-02|CI0_4
  subgraph ATOMONE_0_cameralens [No lens control required]
    ATOMONE_0
    Manual_ATOMONE_0
  end
end
subgraph Minicam IZT
CameraIntegrated_ATOMONEMINIZOOM_0([CameraIntegrated])<-->ATOMONEMINIZOOM_0
ATOMONEMINIZOOM_0[AtomOne mini Zoom0]<-->|CY-CBL-6P-DCHIP-02|CI0_5
end
subgraph "Control Room" 
CI0_4 --- |Ethernet|MinicamMotorizableSwitch
CI0_5 --- |Ethernet|MinicamIZTSwitch
MinicamMotorizableSwitch --- |Ethernet|CY-RCP-DUO_0
MinicamIZTSwitch --- |Ethernet|CY-RCP-DUO_1
end

:::
