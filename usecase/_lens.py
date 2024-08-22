from lens import Lens
def lens_cable(self):
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

    def select(parameters):
        (cameraType,cameraMount,cameraBrand,cameraModel,lensControl,lensType,lensMotor) = parameters
        check(parameters)
        # define constant values
        (no_cable,cable_B4,cable_tilta,cable_fuji,cable_arri) = ("No cable","CY-CBL-6P-B4-02","CY-CBL-6P-TILTA-SERIAL","CY-CBL-6P-FUJI-02","ARRI CFroce cable")
        (no_motor,motor_arri,motor_tilta,motor_dreamchip) = ("No motor","ARRI motors","TILTA motors","DREAMCHIP motors set")
        # Set cameraLensCategory
        cameraLensCategory = Lens.get_cameraLensCategory(cameraType,cameraMount)
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
            # Canon cameras and (CineServo or B4-Mount)
            case ("Cine Interchangeable","Canon",c,d,"CineServo",f) : 
                result =(no_cable,no_cable,no_motor,"No Cyanview cable is required, the iris is controlled through the Canon camera")     
            case ("Cine Interchangeable","Canon",c,d,"B4-Mount",f) : 
                result =(no_cable,no_cable,no_motor,"No Cyanview cable is required, the iris is controlled through the Canon camera")     
            # URSA cameras and (CineServo or B4-Mount)
            case ("Cine Interchangeable",b,"URSA",d,"CineServo",f) :
                result =(no_cable,no_cable,no_motor,"No Cyanview cable is required, the iris is controlled through the URSA camera")
            case ("Cine Interchangeable",b,"URSA",d,"B4-Mount",f) :
                result =(no_cable,no_cable,no_motor,"No Cyanview cable is required, the iris is controlled through the URSA camera") 
            # (Neither URSA nor Canon cameras) and (CineServo or B4-Mount)
            case ("Cine Interchangeable",b,c,"Iris","CineServo",f) :
                result =(no_cable,no_cable,no_motor,"No Cyanview cable is required, the iris is controlled through the camera")
            case ("Cine Interchangeable",b,c,"IZF","CineServo",f) :
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
                result = (cable_B4,cable_fuji,no_motor,"The user needs the control of Iris/Zoom/Focus and it can be done through the camera")
            # Primelens (or… RTI) Motors
            case ("Cine Interchangeable",b,c,d,"Primelens","Tilta") : 
                result = (cable_tilta,no_cable,motor_tilta,"The user needs the control of Iris/Zoom/Focus, it cannot be done through the camera and the user want to use Tilta motors")
            case ("Cine Interchangeable",b,c,d,"Primelens","Arri") : 
                result = (cable_arri,no_cable,motor_arri,"The user needs the control of Iris/Focus, it cannot be done through the camera and the user want to use ARRI motors")
            case ("Cine Interchangeable","Dreamchip",c,d,e,"Dreamchip") : 
                result = (no_cable,no_cable,motor_dreamchip,"The user needs the control of Iris/Zoom and it can be done through the camera")
            case _: 
                result =(no_cable,no_cable,no_motor,"This case is probably not supported")
        print("_lens->lens_cable_selext->RESULT: ",result)
        return result
    def select_cable0(parameters):
        return select(parameters)[0]
    def select_cable1(parameters):
        return select(parameters)[1]
    def select_motor(parameters):
        return select(parameters)[2]
    
    self.df['LensCable0'] = self.df.apply(lambda row: select_cable0((row['Type'],row['LensMount'],row['Brand'], row['Reference'],row['lensControl'],row['lensType'],row['lensMotor'])), axis=1)
    self.df['LensCable1'] = self.df.apply(lambda row: select_cable1((row['Type'],row['LensMount'],row['Brand'], row['Reference'],row['lensControl'],row['lensType'],row['lensMotor'])), axis=1)
    self.df['LensMotor']  = self.df.apply(lambda row: select_motor((row['Type'],row['LensMount'],row['Brand'], row['Reference'],row['lensControl'],row['lensType'],row['lensMotor'])), axis=1)
    