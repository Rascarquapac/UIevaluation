import streamlit.components.v1 as components

class Draw():
    def __init__(self) -> None:
        self.code =     """
        graph LR
            A --> B --> C
        """
    def test(self):
        self.code = '''
        graph RL
            subgraph Venue
            cam_0{{"CV305-0 fa:fa-camera-retro"}}---|CY-CBL-6P-SONY-8P-03|CI0_0
            cam_1{{"CV305-0 fa:fa-camera-retro"}}---|CY-CBL-6P-SONY-8P-03|CI0_0
            cam_2{{"CV305-0 fa:fa-camera-retro"}}---|CY-CBL-6P-SONY-8P-03|CI0_1
            cam_2{{"CV305-0 fa:fa-camera-retro"}}---|CY-CBL-6P-SONY-8P-03|CI0_1
            end
            subgraph "Control Room" 
            CI0_0 --- |"Ethernet cable"|SWITCHER
            CI0_1 --- |"Ethernet cable"|SWITCHER
            SWITCHER --- |"Ethernet cable"|RCP_0
            end
        '''
        return self.code
        
    def mermaid(self) -> None:
        code = self.test()
        components.html(
            f"""
            <pre class="mermaid">
                {code}
            </pre>

            <script type="module">
                import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
                mermaid.initialize({{ startOnLoad: true }});
            </script>
            """
        )
