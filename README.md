# Evaluate Cyanview ressources base on use-case description
A sample Streamlit application do determine Cyanview resources required by a givien use-case.

# TODO
## CYANVIEW DATA DESCRIPTION
-  Improve camera data:
  - add a field for "Control Level" (for Broadcast ? Cinematic ?, General ?)
## FAQ
- Delay in camera process control
- RIO vs CI0
- RIO, RIO-Live and CI0 Pro & Cons
  - according to network
  - flexibility
  - power supply
- Delay with 
## MERMAID
- Display result with Mermaid
  - Check [this solution](https://discuss.streamlit.io/t/st-markdown-does-not-render-mermaid-graphs/25576/4)
## CODE
## SSL Certificates:
/Applications/Python\ 3.12/Install\ Certificates.command
## FLOWCHART
```
flowchart TD
    TEXT[messages.md] -->|Genpy.py| DATA(data.py)
    XLS[Cyanview Description.xls] -->CONSTRAINTS
    XLS[Cyanview Description.xls] -->OPTIONS
    XLS[Cyanview Description.xls] -->CAMERAS
    XLS[Cyanview Description.xls] -->PROTOCOLS
    CONSTRAINTS[Constraints sheet] -->|Genpy.py| DATA(data.py)
    OPTIONS[Options sheet] -->|Genpy.py| DATA(data.py)
    CAMERAS[Cameras sheet] -->|Genpy.py| DATA(data.py)
    PROTOCOLS[CameraProtocols sheet] -->|Genpy.py| DATA(data.py)
    DATA --> CAMERA[camera:df]
    DATA --> MESSAGE[message:dict]
    CAMERA --> STREAMLIT1
    MESSAGE --> STREAMLIT1
    STREAMLIT1[Streamlit:Select Cameras] --> INSTANCES[instance:df]
    STREAMLIT1 --> COMMENT[Display Comments]
    INSTANCES --> STREAMLIT2[STREAMLIT2]
    ANALYZE --> GRAPHICS(Display graphics)
    STREAMLIT2[Streamlit: Set Environment] --> ANALYZE(Analyze user's data)
    ANALYZE --> COMMENTANALYZE(Provide analysis feedback)
    GRAPHICS --> MERMAID(Mermaid Graph)
    GRAPHICS --> GRAPHVIZ[Graphviz Graph fa:fa-car Car]
```