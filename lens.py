import pandas as pd

class Lens():
    def __init__(self) -> None:
            pass
    def cameraLensCategories(self):
          return(["Broadcast","Cine Interchangeable","IZF Integrated","Fixed Lens","Unknown"])
    def get_cameraLensCategory(self,cameraType,cameraMount):
        # Set cameraLensCategory
        print("###############################################")
        print(f"cameraType= {cameraType}  cameraMount= {cameraMount}")
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
            case "Broadcast": return (['No Need','Iris','IZT'],['B4-Mount'],['No extra motors'])
            case "Cine Interchangeable": return (['No Need','Iris','IZT'],['B4-Mount','E-mount','Cabrio','Cineservo','Primelens','Motorized Others','TBD'],['No extra motors','Tilta','Arri','Dreamchip','TBD'])
            case "IZF Integrated": return (['IZT'],['No-Xchange-Motorized'],['No extra motors'])
            case "Fixed Lens": return (["No Need"],['No-Xchange-Manual'],['No extra motors'])
            case "Unknown": return (["No Need"],['No-Xchange-Manual'],['No extra motors'])
            case _: raise KeyError(f"cameraLensCategory= {cameraLensCategory} is not supported")

    def cameraLensInit(self,cameraLensCategory):
        # Set user possible alternatives for his lens needs: lensControl, lensType, lensMotor
        match cameraLensCategory:
                case "Broadcast": return ('No Need','B4-Mount','No extra motors')
                case "Cine Interchangeable": return ('No Need','TBD','TBD')
                case "IZF Integrated": return ('IZT','No-Xchange-Motorized','No extra motors')
                case "Fixed Lens": return ("No Need",'No-Xchange-Manual','No extra motors')
                case "Unknown": return ("No Need",'No-Xchange-Manual','No extra motors')
                case _: raise KeyError(f"cameraLensCategory= {cameraLensCategory} is not supported")
                
    def lens_cable(self):
        def check(parameters):
            (cameraType,cameraMount,cameraBrand,cameraModel,lensControl,lensType,lensMotor) = parameters
            if cameraType not in ["Shoulder Camcorder","System","BBlock","Slow Motion","Mirrorless","CineStyle","Mini Camera","PTZ","Handheld Camcorder","Unknown"]:
                raise KeyError(f"cameraType= {cameraType}")
            if cameraMount not in ['B4-Mount','C-Mount','E-Mount','S-Mount','EF-Mount','MFT-Mount','RF-Mount','LPL-Mount','PL-Mount','LNE-Mount','L-Mount','No-Xchange-Manual','No-Xchange-Motorized','Unknown']:
                raise KeyError(f"cameraMount= {cameraMount}")
            if lensControl not in ['No Need','Iris','IZT']:
                raise KeyError(f"lesnControl= {lensControl}")
            if lensType not in ['B4-Mount','E-mount','Cabrio','Cineservo','Primelens','Motorized Others','TBD']:
                raise KeyError(f"lensType= {lensType}")
            if lensMotor not in ['No extra motors','Tilta','Arri','Dreamchip','TBD']:
                raise KeyError(f"lensMotor= {lensMotor}")
            return

        def select(parameters):
            (cameraType,cameraMount,cameraBrand,cameraModel,lensControl,lensType,lensMotor) = parameters
            check(parameters)
            # Set cameraLensCategory
            cameraLensCategory=self.get_cameraLensCategory(cameraType,cameraMount)
            # Set cables and motors
            match (cameraLensCategory,cameraBrand,cameraModel,lensControl,lensType,lensMotor):
                # No Cyanview lens control is needed
                case(a,b,c,"No Need",e,f) : 
                    return ("No cable","No cable","No motor","No lens control by Cyanview is requested by the user")
                # Broadcast camera have a B4-mount
                case ("Broadcast",b,c,"Iris",e,f) : 
                    return ("No Cable","No Cable","No motor","The lens iris is controllable trhough the camera protocol. No extra cable is required")
                case ("Broadcast",b,c,"IZF",e,f)  : 
                    return ("B4-cable","No Cable","No motor","The lens iris is controllable trhough the camera protocol but an extra B4 cable is required to control Zoom and Focus")
                #  Camera with no lens interchange cannot be controlled
                case ("IZF Integrated",b,c,d,f)    : 
                    return ("No Cable","No Cable","No motor","The lens could not be interchanged and lens could be controlled through the camera prorocol")
                #  Camera with no lens interchange cannot be controlled
                case ("No-Xchange-Manual",b,c,d,f)    : 
                    return ("No cable","No cable","No motor","The lens could not be interchanged and there is probably no motor solution for this case")
                # CineStyle, Mirrorless, Mini camera with lens interchange
                # Canon cameras and (CineServo or B4-Mount)
                case ("Cine Interchangeable","Canon",c,d,"CineServo",f) : 
                    return("No Cable","No Cable","No Motor","No Cyanview cable is required, the iris is controlled through the Canon camera")     
                case ("Cine Interchangeable","Canon",c,d,"B4-Mount",f) : 
                    return("No Cable","No Cable","No Motor","No Cyanview cable is required, the iris is controlled through the Canon camera")     
                # URSA cameras and (CineServo or B4-Mount)
                case ("Cine Interchangeable",b,"URSA",d,"CineServo",f) :
                    return("No Cable","No Cable","No Motor","No Cyanview cable is required, the iris is controlled through the URSA camera")
                case ("Cine Interchangeable",b,"URSA",d,"B4-Mount",f) :
                    return("No Cable","No Cable","No Motor","No Cyanview cable is required, the iris is controlled through the URSA camera") 
                # (Neither URSA nor Canon cameras) and (CineServo or B4-Mount)
                case ("Cine Interchangeable",b,c,"Iris","CineServo",f) :
                    return("No cable","No Cable","No Motor","No Cyanview cable is required, the iris is controlled through the camera")
                case ("Cine Interchangeable",b,c,"IZF","CineServo",f) :
                    return("B4-cable","No Cable","No Motor","Cyanview B4 adapter is require for Zoom/Focus control")
                case ("Cine Interchangeable",b,c,"Iris","B4-Mount",f) :
                    return("No cable","No Cable","No Motor","No Cyanview cable is required, the iris is controlled through the camera")
                case ("Cine Interchangeable",b,c,"IZF","B4-Mount",f) :
                    return("B4-cable","No Cable","No Motor","Cyanview B4 adapter is require for Zoom/Focus control")
                # E-Mount lens (only Sony cameras ??? XDE)
                case ("Cine Interchangeable",b,c,"Iris","E-mount",f) :
                    return("No cable","No Cable","No Motor","No Cyanview cable is required, the iris is controlled through the camera")
                case ("Cine Interchangeable",b,c,"IZF","E-mount",f) :
                    return("Tilta-cable","No Cable","Tilta motors","Adding Tilta motors and Cyanview Tilta adapter is required for Zoom/Focus control")
                # Cabrio lens
                case ("Cine Interchangeable",b,c,d,"Cabrio",f) : 
                    return ("CY-CBL-6P-B4-01","CY-CBL-6P-FUJI-02","No","The user needs the control of Iris/Zoom/Focus and it can be done through the camera")
                # Primelens (or… RTI) Motors
                case ("Cine Interchangeable",b,c,d,"Primelens","Tilta") : 
                    return ("CY-CBL-6P-TILTA-SERIAL","","Tilta","The user needs the control of Iris/Zoom/Focus, it cannot be done through the camera and the user want to use Tilta motors")
                case ("Cine Interchangeable",b,c,d,"Primelens","Arri") : 
                    return ("ARRI CFroce cable","","Arri","The user needs the control of Iris/Focus, it cannot be done through the camera and the user want to use ARRI motors")
                case ("Cine Interchangeable","Dreamchip",c,d,e,"Dreamchip") : 
                    return ("No cable","No cable","Dreamchip","The user needs the control of Iris/Zoom and it can be done through the camera")
                case _: 
                    return(0,0,"No","No control","This case is probably not supported")
                
        (self.df['LensCable0'],self.df['LensCable1'],self.df['LensMotor'] ) = self.df.apply(lambda row: select(
            (
                row['CameraTypes'],
                row['CameraMounts'],
                row['CameraBrands'],
                row['Model'],
                row['LensUserControlNeeds'],
                row['LensUserMotorization']
            )
            ), 
            axis=1)
    def lens_init(self):
        pass  
