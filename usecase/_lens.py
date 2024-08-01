import pandas as pd

def lens_init(self):
    def check(parameters):
        (lensUserControlNeeds,cameraLensControl,reference,cameraType,userLensSpecificity,lensMotorization)=parameters
        return
    def select(parameters):
        (lensUserControlNeeds,cameraLensControl,reference,cameraType,userLensSpecificity,lensMotorization)=parameters
        if cameraType == 'Mini Camera' :
            if "AtomOne" in reference : cameraLensSpecificity = "B4 case"
        elif cameraType == 'Slow Motion' and "SSM500-B4" in reference : cameraLensSpecificity = "B4 case"
        elif cameraType == 'Shoulder Camcorder': cameraLensSpecificity = "B4 case"
        elif cameraType == 'Block': cameraLensSpecificity = "B4 case"
        elif cameraType == 'Large Sensor' and userLensSpecificity == "Canon" : cameraLensSpecificity = "B4 case"
        else : cameraLensSpecificity = "Pending"
        #TODO Cas Sony Venice Non Traité
        #TODO manage "lensMotorization" (e) variable
        match (lensUserControlNeeds,cameraLensControl,cameraLensSpecificity,userLensSpecificity,lensMotorization):
            case ("None",b,c,d,e)         : return ("","","No","No control of lens is required by user")
            case (a,"Fixed Lens",b,c,d,e) : return ("","","No","The lens is not interchangeable, or the lens is not controllable or it is controlable through the camera. No extra cable is required")
            case ("Iris only","Iris only",c,d,e) : return ("","","No","The user needs only te control of iris and it can be done through the camera")
            case ("Iris/Focus","Iris/Zoom/Focus",c,d,e) : return ("","","No","The user needs the control of Iris/Zoom/Focus and it can be done through the camera")
            case ("Iris/Zoom/Focus","Iris/Zoom/Focus",c,d,e) : return ("","","No","The user needs the control of Iris/Zoom/Focus and it can be done through the camera")
            case ("Iris/Zoom/Focus","Iris only","B4 case",d,e) : return ("CY-CBL-6P-B4-01",0,"No","The user needs the control of Iris/Zoom/Focus and it can be done through the camera")
            case ("Iris/Zoom/Focus",b,"Cabrio",d,e) : return ("CY-CBL-6P-B4-01","CY-CBL-6P-FUJI-02","No","The user needs the control of Iris/Zoom/Focus and it can be done through the camera")
            case ("Iris only",b,"Tilta",d,e) : return ("CY-CBL-6P-TILTA-SERIAL","","Tilta","The user needs the control of Iris only, it cannot be done through the camera and the user want to use a Tilta motor")
            case ("Iris/Focus",b,"Tilta",d,e) : return ("CY-CBL-6P-TILTA-SERIAL","","Tilta","The user needs the control of Iris/Focus, it cannot be done through the camera and the user want to use Tilta motors")
            case ("Iris/Zoom/Focus",b,"Tilta",d,e) : return ("CY-CBL-6P-TILTA-SERIAL","","Tilta","The user needs the control of Iris/Zoom/Focus, it cannot be done through the camera and the user want to use Tilta motors")
            case ("Iris only",b,"Arri",d,e) : return ("CY-CBL-6P-TILTA-SERIAL","","Arri","The user needs the control of Iris only, it cannot be done through the camera and the user want to use ARRI motor")
            case ("Iris/Focus",b,"Arri",d,e) : return ("ARRI CFroce cable","","Arri","The user needs the control of Iris/Focus, it cannot be done through the camera and the user want to use ARRI motors")
            case ("Iris/Zoom/Focus",b,"Arri",d,e) : return ("ARRI CFroce cable","","Arri","The user needs the control of Iris/Zoom/Focus, it cannot be done through the camera and the user want to use ARRI motors")
            case _: return(0,0,"No","No control","This case is probably not supported")

    (self.df['LensCable0'],self.df['LensCable1'],self.df['LensMotor'] ) = self.df.apply(lambda row: select(
        (
            row['LensUserControlNeeds'],
            row['CameraLensControl'],
            row['Reference'],
            row['CameraTypes'],
            row['LensUserSpecificity'],
            row['LensUserMotorization']
        )
        ), 
        axis=1)    
