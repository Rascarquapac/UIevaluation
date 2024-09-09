import pandas as pd

class CameraLens():
    def __init__(self,df_index,reference,protocol,cable) -> None:
        self.df_index  = df_index
        self.reference = reference
        self.protocol  = protocol
        self.camera_cable = cable
        self.camera_types = ['Shoulder Camcorder','System','BBlock','Slow Motion','CineStyle','Mirrorless','Minicam','Minicam Motorizable','Mini IZT','Handheld Camcorder','PTZ','Undefined']
        self.camera_categories = ['Broadcast','Cine Interchangeable','IZF Integrated','Fixed Lens','Minicam Motorizable Lens','Undefined']
        # case "Broadcast": return (['No Need','Iris','IZF'],['B4-Mount'],['No extra motors'])
        #     case "Cine Interchangeable": return (['No Need','Iris','IZF'],['B4-Mount','E-mount','Cabrio','Cineservo','Primelens','Motorized Others','TBD'],
        # ['No extra motors','Tilta','Arri','Dreamchip','TBD'])
        #     case "IZF Integrated": return (['IZF'],['Camera Integrated'],['No extra motors'])
        #     case "Fixed Lens": return (["No Need"],['Fixed and Manual'],['No extra motors'])
        #     case "Unknown": return (["No Need"],['Fixed and Manual'],['No extra motors'])
        # User options of IZF control per camera type
        self.options_needs_IZF={
             'Broadcast':['No Need','Iris','IZF'],
             'Cine Interchangeable':['No Need','Iris','IZF'],
             'IZF Integrated':['IZF'],
             'Fixed Lens':['No Need'],
             'Minicam Motorizable Lens':['No Need','IZF'],
             'Undefined':["No Need"]
        }
        # User options of lens type per camera category
        self.options_needs_lens_type={
             'Broadcast':['B4-Mount'],
             'Cine Interchangeable':['B4-Mount','E-mount','Cabrio','Cineservo','Primelens','Motorized Others','TBD'],
             'IZF Integrated':['Camera Integrated'],
             'Fixed Lens':['Manual'], # "Manual" only ?
             'Minicam Motorizable Lens':['Manual'],
             'Undefined':["No Need"]
        }
        # User options of lens type per camera category
        self.options_needs_motor_type={
             'Broadcast':['No extra motors'],
             'Cine Interchangeable':['No extra motors','Tilta','Arri','TBD'],
             'IZF Integrated':['Camera Integrated'],
             'Fixed Lens':['Manual'], # "Manual" only ?
             'Minicam Motorizable Lens':['No extra motors','Dreamchip'],
             'Undefined':['No extra motors']
        }
        # Inti values for user options per camera category
        self.options_needs_init = {
            "Broadcast" : ('No Need','B4-Mount','No extra motors'),
            "Cine Interchangeable" : ('No Need','TBD','TBD'),
            "IZF Integrated" : ('IZF','Camera Integrated','No extra motors'),
            "Fixed Lens" : ("No Need",'Manual','No extra motors'),
            'Minicam Motorizable Lens' : ("No Need",'Manual','No extra motors'),
            "Unknown" : ("No Need",'Manual','No extra motors')
        }
                # case "Broadcast": return ('No Need','B4-Mount','No extra motors')
                # case "Cine Interchangeable": return ('No Need','TBD','TBD')
                # case "IZF Integrated": return ('IZF','Camera Integrated','No extra motors')
                # case "Fixed Lens": return ("No Need",'Fixed and Manual','No extra motors')
                # case "Unknown": return ("No Need",'Fixed and Manual','No extra motors')
    def cameraLens_category(self,cameraType,cameraMount):
        # cameraMount can be suppressed except for exception
        match (cameraType,cameraMount):
            case ("Undefined",b) : cameraLensCategory = "Unknown"
            case (a,"Undefined") : cameraLensCategory = "Unknown"
            case ("Slow Motion",b) | ("System",b)|("BBlock",b)|("Shoulder Camcorder",b) : cameraLensCategory = "Broadcast"
            case ("CineStyle",b)|("Mirrorless",b)       : cameraLensCategory = "Cine Interchangeable"
            case ("PTZ",b) | ("Handheld Camcorder",b)|("Mini IZT",b)   : cameraLensCategory = "IZF Integrated"
            case ("Minicam",b)    : cameraLensCategory = "Fixed Lens"
            case ("Minicam Motorizable",b) : cameraLensCategory = "Minicam Motorizable Lens"
            case _: raise KeyError(f"cameraType= {cameraType}, cameraMount= {cameraMount}")
        return cameraLensCategory
    # Select camera cable + lens cable + lens motor from user needs in Cyanview control
    def select(parameters):
        def check(parameters):
            print("Lens->lens_cable->check->PARAMETERS:\n",parameters)
            (cameraType,cameraMount,cameraBrand,cameraModel,lensControl,lensType,lensMotor) = parameters
            if cameraType not in ["Shoulder Camcorder","System","BBlock","Slow Motion","Mirrorless","CineStyle","Mini Camera","PTZ","Handheld Camcorder","Unknown"]:
                raise KeyError(f"cameraType= {cameraType}")
            if cameraMount not in ['B4-Mount','C-Mount','E-Mount','S-Mount','EF-Mount','MFT-Mount','RF-Mount','LPL-Mount','PL-Mount','LNE-Mount','L-Mount','No-Xchange-Manual','No-Xchange-Motorized','Unknown']:
                raise KeyError(f"cameraMount= {cameraMount}")
            if lensControl not in ['No Need','Iris','IZF']:
                raise KeyError(f"lesnControl= {lensControl}")
            if lensType not in ['B4-Mount','E-mount','Cabrio','Cineservo','Primelens','Motorized Others','Camera Integrated','Fixed and Manual','TBD']:
                raise KeyError(f"lensType= {lensType}")
            if lensMotor not in ['No extra motors','Tilta','Arri','Dreamchip','TBD']:
                raise KeyError(f"lensMotor= {lensMotor}")
            return
        (cameraType,cameraMount,cameraBrand,cameraModel,lensControl,lensType,lensMotor) = parameters
        check(parameters)
        # define constant values
        (no_cable,cable_B4,cable_tilta,cable_fuji,cable_arri) = ("No cable","CY-CBL-6P-B4-02","CY-CBL-6P-TILTA-SERIAL","CY-CBL-6P-FUJI-02","ARRI CFroce cable")
        (no_motor,motor_arri,motor_tilta,motor_dreamchip) = ("No motor","ARRI motors","TILTA motors","DREAMCHIP motors set")
        # Set cameraLensCategory
        cameraLensCategory = CameraLens.get_cameraLensCategory(cameraType,cameraMount)
        # Set cables and motors
        print("\n_lens->lens_cable_selext->PARAMETERS: ",parameters)
        print("\n_lens->lens_cable_selext->MATCH INPUT: ",(cameraLensCategory,cameraBrand,cameraModel,lensControl,lensType,lensMotor) )
        match (cameraLensCategory,cameraBrand,cameraModel,lensControl,lensType,lensMotor):
            # No Cyanview lens control is needed
            case(a,b,c,"No Need",e,f) : 
                result = (no_cable,no_cable,no_motor,"No lens control by Cyanview is requested by the user")
            # Broadcast camera have a B4-mount
            case ("Broadcast",b,c,"Iris",e,f) : 
                result = (no_cable,no_cable,no_motor,"The lens iris is controllable trhough the camera protocol. No extra cable is required")
            case ("Broadcast",b,c,"IZF",e,f)  : 
                result = (cable_B4,no_cable,no_motor,"The lens iris is controllable trhough the camera protocol but an extra B4 cable is required to control Zoom and Focus")
            #  Camera with no lens interchange cannot be controlled
            case ("IZF Integrated",b,c,d,e,f)    : 
                result = (no_cable,no_cable,no_motor,"The lens could not be interchanged and lens could be controlled through the camera prorocol")
            #  Camera with no lens interchange cannot be controlled
            case ("Fixed Lens",b,c,d,e,f)    : 
                result = (no_cable,no_cable,no_motor,"The lens could not be interchanged and there is probably no motor solution for this case")
            # CineStyle, Mirrorless, Mini camera with lens interchange
            # Canon cameras and (Cineservo or B4-Mount)
            case ("Cine Interchangeable","Canon",c,d,"Cineservo",f) : 
                result =(no_cable,no_cable,no_motor,"No Cyanview cable is required, the iris is controlled through the Canon camera")     
            case ("Cine Interchangeable","Canon",c,d,"B4-Mount",f) : 
                result =(no_cable,no_cable,no_motor,"No Cyanview cable is required, the iris is controlled through the Canon camera")     
            # URSA cameras and (Cineservo or B4-Mount)
            case ("Cine Interchangeable",b,"URSA",d,"Cineservo",f) :
                result =(no_cable,no_cable,no_motor,"No Cyanview cable is required, the iris is controlled through the URSA camera")
            case ("Cine Interchangeable",b,"URSA",d,"B4-Mount",f) :
                result =(no_cable,no_cable,no_motor,"No Cyanview cable is required, the iris is controlled through the URSA camera") 
            # (Neither URSA nor Canon cameras) and (Cineservo or B4-Mount)
            case ("Cine Interchangeable",b,c,"Iris","Cineservo",f) :
                result =(no_cable,no_cable,no_motor,"No Cyanview cable is required, the iris is controlled through the camera")
            case ("Cine Interchangeable",b,c,"IZF","Cineservo",f) :
                result =(cable_B4,no_cable,no_motor,"Cyanview B4 adapter is require for Zoom/Focus control")
            case ("Cine Interchangeable",b,c,"Iris","B4-Mount",f) :
                result =(no_cable,no_cable,no_motor,"No Cyanview cable is required, the iris is controlled through the camera")
            case ("Cine Interchangeable",b,c,"IZF","B4-Mount",f) :
                result =(cable_B4,no_cable,no_motor,"Cyanview B4 adapter is require for Zoom/Focus control")
            # E-Mount lens (only Sony cameras ??? XDE)
            case ("Cine Interchangeable",b,c,"Iris","E-mount",f) :
                result =(no_cable,no_cable,no_motor,"No Cyanview cable is required, the iris is controlled through the camera")
            case ("Cine Interchangeable",b,c,"IZF","E-mount",f) :
                result =(cable_tilta,no_cable,motor_tilta,"Adding Tilta motors and Cyanview Tilta adapter is required for Zoom/Focus control")
            # Cabrio lens
            case ("Cine Interchangeable",b,c,d,"Cabrio",f) : 
                result = (f'{cable_B4} +\n{cable_fuji}',no_motor,no_cable,"The user needs the control of Iris/Zoom/Focus and it can be done through the camera")
            # Primelens (or… RTI) Motors
            case ("Cine Interchangeable",b,c,d,"Primelens","Tilta") : 
                result = (no_cable,cable_tilta,motor_tilta,"The user needs the control of Iris/Zoom/Focus, it cannot be done through the camera and the user want to use Tilta motors")
            case ("Cine Interchangeable",b,c,d,"Primelens","Arri") : 
                result = (no_cable,cable_arri,motor_arri,"The user needs the control of Iris/Focus, it cannot be done through the camera and the user want to use ARRI motors")
            case ("Cine Interchangeable","Dreamchip",c,d,e,"Dreamchip") : 
                result = (no_cable,no_cable,motor_dreamchip,"The user needs the control of Iris/Zoom and it can be done through the camera")
            case _: 
                result =(no_cable,no_cable,no_motor,"This case is probably not supported")
        print(f"_lens->lens_cable_selext->RESULT: {result}")
        return result

    ########## FLAT ANALYZIS
        self.camera_type='Undefined'
        self.camera_category='Undefined'
    # to be replaced by attribute
    def cameraLensCategories(self):
          return(["Broadcast","Cine Interchangeable","IZF Integrated","Fixed Lens","Unknown"])
class Lens():
    def __init__(self) -> None:
        pass    
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
    def cameraLensCategories(self):
          return(["Broadcast","Cine Interchangeable","IZF Integrated","Fixed Lens","Unknown"])
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
