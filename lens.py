import pandas as pd

class Lens():
    def __init__(self) -> None:
            pass
    def cameraLensCategories(self):
          return(["Broadcast","Cine Interchangeable","IZF Integrated","Fixed Lens","Unknown"])
    @classmethod
    def get_cameraLensCategory(self,cameraType,cameraMount):
        # Set cameraLensCategory
        # print("###############################################")
        # print(f"cameraType= {cameraType}  cameraMount= {cameraMount}")
        match (cameraType,cameraMount):
            case ("Unknown",b) : cameraLensCategory = "Unknown"
            case (a,"Unknown") : cameraLensCategory = "Unknown"
            case ("Slow Motion",b) | ("System",b)|("BBlock",b)|("Shoulder Camcorder",b) : cameraLensCategory = "Broadcast"
            case ("CineStyle",b)|("Mirrorless",b)       : cameraLensCategory = "Cine Interchangeable"
            case ("PTZ",b) | ("Handheld Camcorder",b)   : cameraLensCategory = "IZF Integrated"
            case ("Mini Camera","No-Xchange-Manual")    : cameraLensCategory = "Fixed Lens"
            case ("Mini Camera","No-Xchange-Motorized") : cameraLensCategory = "IZF Integrated"
            case ("Mini Camera",b)                      : cameraLensCategory = "Cine Interchangeable"
            case _: raise KeyError(f"cameraType= {cameraType}, cameraMount= {cameraMount}")
        return cameraLensCategory

    def cameraLensConstraints(self,cameraLensCategory):
        # Set user possible alternatives for his lens needs: lensControl, lensType, lensMotor
        match cameraLensCategory:
            case "Broadcast": return (['No Need','Iris','IZF'],['B4-Mount'],['No extra motors'])
            case "Cine Interchangeable": return (['No Need','Iris','IZF'],['B4-Mount','E-mount','Cabrio','Cineservo','Primelens','Motorized Others','TBD'],['No extra motors','Tilta','Arri','Dreamchip','TBD'])
            case "IZF Integrated": return (['IZF'],['Camera Integrated'],['No extra motors'])
            case "Fixed Lens": return (["No Need"],['Fixed and Manual'],['No extra motors'])
            case "Unknown": return (["No Need"],['Fixed and Manual'],['No extra motors'])
            case _: raise KeyError(f"cameraLensCategory= {cameraLensCategory} is not supported")
    @classmethod
    def filter_constraints(cls,cameraLensCategory):
        pass
    def cameraLensInit(self,cameraLensCategory):
        # Set user possible alternatives for his lens needs: lensControl, lensType, lensMotor
        match cameraLensCategory:
                case "Broadcast": return ('No Need','B4-Mount','No extra motors')
                case "Cine Interchangeable": return ('No Need','TBD','TBD')
                case "IZF Integrated": return ('IZF','Camera Integrated','No extra motors')
                case "Fixed Lens": return ("No Need",'Fixed and Manual','No extra motors')
                case "Unknown": return ("No Need",'Fixed and Manual','No extra motors')
                case _: raise KeyError(f"cameraLensCategory= {cameraLensCategory} is not supported")
                