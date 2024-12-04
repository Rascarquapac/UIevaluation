:::mermaid
graph RL
subgraph CineStyle
FX6_0{{"FX6_0 fa:fa-camera-retro"}}---|IP-to-USB-C|IP_0
  subgraph FX6_0_cameralens [No lens control required]
    FX6_0
  end
end
subgraph "Control Room" 
IP_0 --- |Ethernet|CineStyleSwitch
CineStyleSwitch --- |Ethernet|CY-RCP-DUO-J_0
end

:::
