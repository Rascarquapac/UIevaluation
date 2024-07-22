# Evaluate Cyanview ressources base on use-case description
A sample Streamlit application do determine Cyanview resources required by a givien use-case.

# TODO
## CYANVIEW DATA DESCRIPTION
-  Improve camera database:
  - add a field for "Control Level" (for Broadcast ? Cinematic ?, General ?)
  - add field on maxDelaySystainable for decinding about network
  - fill missing protocol
- Improve generic explanation on choices and special attention
  - create a FAQs pages on Odoo (bifirectionality, HF,)
- Develop Network selection
- Develop Lens selection
- Develop Extra-Devices (Tally, GPIO, NIO,…) selection
- Develop Non-Camera-Device-Control (switchers,…)
- Develop storing in database and emailing for quote request
- Manage target application (Specialty, Broadcast, Cinematic,Remote Production)
- Details:
  - SSM500 should require a RCP-Full ( 1 x camera ?)
  - Downloading SVG file
  - Analyze and display schematic on any change
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
    USER --> TEXT
    USER --> GSHEET
    TEXT[messages.md] -->|Genpy.py| TEXDIC(picklize.text_to_dic)
    GSHEET[Cyanview Description.gs] --> GET_GSHEET(get_gsheet)
    subgraph pickelize
    TEXDIC --> DIC
    DIC --> TEXTPKL
    GET_GSHEET[picklize.get_gsheets] -->CONSTRAINTS
    GET_GSHEET -->OPTIONS
    GET_GSHEET -->CAMERAS
    GET_GSHEET -->PROTOCOLS
    CONSTRAINTS[Constraints sheet] -->|Genpy.py| CSVPKL(picklize.csv_to_pkl)
    OPTIONS[Options sheet] -->|Genpy.py| CSVPKL
    CAMERAS[Cameras sheet] -->|Genpy.py| CSVPKL
    PROTOCOLS[CameraProtocols sheet] -->|Genpy.py| CSVPKL
    end
    TEXTPKL --> PKLMESS(messages.pkl) 
    CSVPKL  --> PKLOPTI(options.pkl)
    CSVPKL ---> PKLCONS(constraints.pkl)
    CSVPKL ---> PKLCAMS(cameras.pkl)
    subgraph salesagent
    PKLCAMS --> STREAMLIT1
    PKLMESS --> STREAMLIT1
    PKLCONS --> STREAMLIT1
    PKLOPTI --> STREAMLIT1
    STREAMLIT1 --> ANALYZE
    ANALYZE --> GRAPHICS(Display graphics)
    ANALYZE --> COMMENTANALYZE(Provide analysis feedback)
    GRAPHICS --> MERMAID(Mermaid Graph)
    GRAPHICS --> GRAPHVIZ[Graphviz Graph fa:fa-car Car]
    end
```