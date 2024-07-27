import pandas as pd

def lens_init(self):
    self.df = pd.DataFrame.from_dict({
            'Camera Brand Motorized Lens':  [None, None], 
            'ENG Canon Lens': [None, 'CY-CBL-B4-01'],
            'ENG Fuji Lens': [None, 'CY-CBL-B4 et CY-CBL-FUJI-2'],
            'Cine Lens': ['external', 'CY-CBL-B4 et CY-CBL-FUJI-2'], 
            'Photo Lens': ['external', None]}, 
        orient = 'index')
