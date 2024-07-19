from usecase import Usecase
from usecase_analyze import *
from usecase_streamlit import *
from usecase_draw import *
from usecase_debug import *

if __name__ == "__main__":
    instance = Usecase()
    instance.debug_camerapool_to_usecase()    
    instance.analyze()
    instance.draw_all()
    instance.top.render(filename='./images/top_draw_all', format='svg')
    mermaid_code = instance.get_mermaid_code()
    print(mermaid_code)
    graph = instance.graph_mermaid(mermaid_code)
    instance.streamlit_mermaid(graph)
