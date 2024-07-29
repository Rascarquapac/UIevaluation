import pandas as pd

def lens_init(self):
    pass
    def select(parameters):
        match parameters:
            case (a,b,c,d,e): return (a,b,c) 
            case _: return(c,d,e)
        return
    (self.df['LensCable0'],self.df['LensCable1'],self.df['LensMotor'] ) = self.df.apply(lambda row: select(
        (
            row['CameraLensSpecificity'],
            row['Reference'],
            row['LensControlNeeds'],
            row['UserLensSpecificity'],
            row['LensMotorization']
        )
        ), 
        axis=1)    
