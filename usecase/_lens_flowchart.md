:::mermaid
flowchart TD
    TYPE_SHOU(Shoulder) -->CAM_BROAD[Broadcast]
    TYPE_SYST(System) -->CAM_BROAD[Broadcast]
    TYPE_BBLB(BBlock) -->CAM_BROAD[Broadcast]
    TYPE_SLOW(Slow Motion\nB4-mount) -->CAM_BROAD
    TYPE_MINI_XCH-->CAM_CINE_OR_XCH
    TYPE_CINE(CineStyle) -->CAM_CINE_OR_XCH
    TYPE_MIRR(Mirrorless) -->CAM_CINE_OR_XCH[Cinestyle\nMirrorless]
    TYPE_MINI_FIXNOXCH -->|No Lens X|CAM_NOXCH[Fixed Lens]
    TYPE_MINI_WITHIZF-->|IZF integrated|CAM_IZFNOX[IZF integrated]
    TYPE_HAND(Handheld) -->CAM_IZFNOX[IZF integrated]
    TYPE_PTZ(PTZ) -->CAM_IZFNOX
    subgraph Camera Type
        TYPE_SHOU
        TYPE_SYST
        TYPE_BBLB
        TYPE_SLOW
        TYPE_MIRR
        TYPE_CINE
        TYPE_MINI_XCH(Minicam\nLens Xchange)
        TYPE_MINI_WITHIZF(Minicam\nwith IZF)
        TYPE_HAND
        TYPE_PTZ
        TYPE_MINI_FIXNOXCH(Minicam\nFixed lens)
    end
    subgraph Camera Property
        CAM_BROAD[Broadcast]
        CAM_NOXCH
        CAM_IZFNOX
        CAM_CINE_OR_XCH[CineStyle\nMirrorless\nXchangeable]
    end
    CAM_BROAD-->LENS_B4_1
    CAM_CINE_OR_XCH-->|URSA \nor \nCanon|LENS_B4_2
    CAM_CINE_OR_XCH-->|URSA \nor \nCanon|LENS_CINESER_2
    CAM_CINE_OR_XCH-->|/URSA \nand \n/Canon|LENS_B4_3
    CAM_CINE_OR_XCH-->|/URSA \nand \n/Canon|LENS_CINESER_3
    CAM_CINE_OR_XCH-->LENS_EMOUNT
    CAM_CINE_OR_XCH-->LENS_CABRIO
    CAM_CINE_OR_XCH-->LENS_NONMOT_ARRI
    CAM_CINE_OR_XCH-->LENS_NONMOT_TILT
    CAM_NOXCH-->LENS_NO
    CAM_IZFNOX-->LENS_INTER
    subgraph USER Lens Choice
        direction TB
        LENS_B4_1[B4-Lens 1]
        LENS_B4_2[B4-Lens 2]
        LENS_B4_3[B4-Lens 3]
        LENS_CABRIO[Cabrio]
        LENS_CINESER_2[CineServo 2]
        LENS_CINESER_3[CineServo 3]
        LENS_EMOUNT[E-Mount]
        LENS_NONMOT_ARRI[Non Motorized\nand ARRI motors]
        LENS_NONMOT_TILT[Non Motorized\nand TILTA motors]
        LENS_NO["|"]
        LENS_INTER["|"]
    end
    LENS_B4_1-->|Iris|THROU_CAM_1
    LENS_B4_1-->|IZF|CABLE_B4_1
    LENS_NONMOT_TILT-->CABLE_TILTA
    LENS_NONMOT_ARRI-->CABLE_ARRI[Arri\nCForce cable]
    LENS_NO-->NO_CONTROL
    LENS_CABRIO-->CABLE_B4_FUJI
    LENS_CINESER_2-->THROU_CAM_2
    LENS_CINESER_3-->|Iris|THROU_CAM_3
    LENS_CINESER_3-->|IZF|CABLE_B4_3
    LENS_EMOUNT-->|Iris|THROU_CAM_4
    LENS_EMOUNT-->|IZF|CABLE_TILTA_4
    LENS_B4_2-->THROU_CAM_2
    LENS_B4_3-->|Iris|THROU_CAM_3
    LENS_B4_3-->|IZF|CABLE_B4_3
    LENS_INTER-->THROU_CAM_INTER[Through\ncamera]
    subgraph Control
       CABLE_B4_1[Cyanview\nB4 cable]
       CABLE_B4_3[Cyanview\nB4 cable]
       CABLE_B4_FUJI[Cyanview\nB4+FUJI\ncables]
       CABLE_TILTA[Cyanview\nTilta cable]
       CABLE_TILTA_4[Cyanview\nTilta cable]
       CABLE_ARRI
       THROU_CAM_1[Through\ncamera]
       THROU_CAM_2[Through\ncamera]
       THROU_CAM_3[Through\ncamera]
       THROU_CAM_4[Through\ncamera]
       THROU_CAM_INTER[Through\ncamera]
       NO_CONTROL[No lens\ncontrol]
    end
:::
