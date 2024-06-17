import streamlit as st
import streamlit.components.v1 as components
import graphviz

class Draw():
    def __init__(self,name) -> None:
        self.graph = graphviz.Graph(name=name)
        self.graph.attr(rankdir='RL', size='6,3',style='filled',color='lightyellow',label=name)
        self.graph.node_attr.update(style='filled',shape= 'box',color='lightcyan1')
        self.graph.edge_attr.update(fontsize='8pt')
        self.subgraphs = {} # subgraphs XOR nodes  
        self.nodes={}
    def add_node(self,name):
        # add a node to the current graph
        self.nodes[name] = self.graph.node(name=name,label=name)
    #@st.cache_data    
    def mermaid(self) -> None:
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
        st.components.v1.html(
            f"""
            <pre class="mermaid">
                {self.code}
            </pre>

            <script type="module">
                import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
                mermaid.initialize({{ startOnLoad: true }});
            </script>
            """,
            height=500,
            scrolling=True
        )
    def graphviztest(self):
        #Main Graph
        graph = graphviz.Graph(name= 'Test',comment='Cyanview Test')
        graph.attr(rankdir='RL', size='6,3')
        with graph.subgraph(name='cluster_venue') as venue:
            venue.attr(name= 'Venue',comment='Cyanview Venue',rankdir='RL', size='10,3',style='filled',color='lightyellow',label='Venue')
            venue.node_attr.update(style='filled',shape= 'box',color='lightcyan1')
            venue.edge_attr.update(fontsize='10pt')
            venue.node(name='cam_0', label="CV305-0")
            venue.node(name='cam_1', label="CV305-1")
            venue.node(name='cam_2', label="CV305-2")
            venue.node(name='cam_3', label="CV305-3")
            venue.node('ci0_0','CI0_0')
            venue.node('ci0_1','CI0_1')
            venue.edge('cam_0','ci0_0','CY-CBL-6P-SONY-8P-03')
            venue.edge('cam_1','ci0_0','CY-CBL-6P-SONY-8P-03')
            venue.edge('cam_2','ci0_1','CY-CBL-6P-SONY-8P-03')
            venue.edge('cam_3','ci0_1','CY-CBL-6P-SONY-8P-03')
        with graph.subgraph(name='cluster_room') as croom:
            croom.subgraph(name= 'Control Room',comment='Cyanview Control Room')
            croom.attr(name= 'Control Room',rankdir='RL', size='6,3',style='filled',color='lightyellow',label='Control Room')
            croom.node_attr.update(style='filled',shape= 'box',color='lightcyan1')
            croom.node('poe_switcher','PoE Switcher')
            croom.node('rcp_0','RCP_0')
            croom.edge('poe_switcher','rcp_0','Ethernet cable')
        graph.edge('ci0_0','poe_switcher','Ethernet cable')
        graph.edge('ci0_1','poe_switcher','Ethernet cable')
        return(graph)
    def to_graphviz(self,instance):
        pass


