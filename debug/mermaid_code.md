:::mermaid
graph RL
subgraph Minicam Motorizable
ATOMONE_0{{"ATOMONE_0 fa:fa-camera-retro"}}---|CY-CBL-6P-DCHIP-02|CI0_0
  subgraph ATOMONE_0_cameralens [No lens control required]
    ATOMONE_0
    Manual_ATOMONE_0
  end
end
subgraph Minicam IZT
ATOMONEMINIZOOM_0{{"ATOMONEMINIZOOM_0 fa:fa-camera-retro"}}---|CY-CBL-6P-DCHIP-02|CI0_1
  subgraph ATOMONEMINIZOOM_0_cameralens [Iris/Zoom/Focus control required]
    ATOMONEMINIZOOM_0
    CameraIntegrated_ATOMONEMINIZOOM_0
  end
end
subgraph "Control Room" 
CI0_0 --- |Ethernet|MinicamMotorizableSwitch
CI0_1 --- |Ethernet|MinicamIZTSwitch
MinicamMotorizableSwitch --- |Ethernet|CY-RCP-DUO_0
MinicamIZTSwitch --- |Ethernet|CY-RCP-DUO_1
end

:::
