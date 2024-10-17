:::mermaid
graph RL
subgraph Minicam Motorizable
ATOMONE_0{{"ATOMONE_0 fa:fa-camera-retro"}}---|CY-CBL-6P-DCHIP-02|CI0_0
  subgraph ATOMONE_0_cameralens [No lens control required]
    ATOMONE_0
    Manual_ATOMONE_0
  end
ATOMONEMINI_0{{"ATOMONEMINI_0 fa:fa-camera-retro"}}---|CY-CBL-6P-DCHIP-02|CI0_0
  subgraph ATOMONEMINI_0_cameralens [No lens control required]
    ATOMONEMINI_0
    Manual_ATOMONEMINI_0
  end
end
subgraph "Control Room" 
CI0_0 --- |Ethernet|MinicamMotorizableSwitch
MinicamMotorizableSwitch --- |Ethernet|CY-RCP-DUO_0
end

:::
