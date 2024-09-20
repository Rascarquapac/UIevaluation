import streamlit as st
import pandas    as pd
from cyancameralens import Lens

class StreamUI():
    def __init__(self) -> None:
        pass
    ############## CAMERA TABLE FROM USECASE !! UNUSED !!!#########
    def usecase_display_camera_table(self,usecase):
        print("DEBUG:cyaneval->display_camera_table ...")
        if (len(usecase.df.index) != 0):
            st.dataframe(
                usecase.df,
                column_config={
                    "Reference": "Model",
                    'Number':st.column_config.NumberColumn(
                        "# of Cams",
                        help="How much camera of this type in your use-case (0-15)?",
                        min_value=0,
                        max_value=15,
                        step=1,
                        format="%d",
                    ),
                    "Brand": "Brand",
                    "Cable": "Cable",
                    'Lens': "Lens Type",
                    'Network': None,
                    'Base': None,
                    "SupportURL": None,
                    "ManufacturerURL": None,
                    "Reference": None,
                    #"supportText": None,
                    "Protocol":None,
                    "Message":None,
                    "Type":None
                },
                column_order=['Reference','Instance','Network','Lens','Base'],
                hide_index = True)
    def usecase_edit_camera_table(self,usecase,key='1'):
        # Validate inputs
        if (len(usecase.df.index) != 0): 
            # display = usecase.text_message()
            usecase.df = st.data_editor(
                usecase.df,
                key = key,
                column_config={
                    'Instance': "Instance",
                    'Number':st.column_config.NumberColumn(
                        "# Cams",
                        help="How much camera of this type in your use-case (0-15)?",
                        min_value=0,
                        max_value=15,
                        step=1,
                        default=0,
                        format="%d",
                    ),
                    "Reference": "Model",
                    'Lens': st.column_config.SelectboxColumn(
                        "Lens",
                        help="Lens type",
                        width="medium",
                        options= usecase.property.constraints[(key,'Lens')],
                        required=True),
                    'Network':  st.column_config.SelectboxColumn(
                        "Network",
                        help="Select the network type",
                        width="medium",
                        options=usecase.property.constraints[(key,'Network')],
                        required=True),
                    'Base':  st.column_config.SelectboxColumn(
                        "Basement",
                        help="Base type",
                        width="medium",
                        options=usecase.property.constraints[(key,'Base')],
                        required=True),
                    "Brand": None,
                    "Cable": None,
                    "SupportURL": None,
                    "ManufacturerURL": None,
                    "Reference": None,
                    #"supportText": None,
                    "Protocol":None,
                    "Message":None,
                    "Type":None
                },
                disabled=['Instance','Reference','Number','Cable'],
                column_order=['Reference','Instance','Network','Lens','Base'],
                hide_index = True)
            ## st.markdown(display)
            print("\nDATAFRAME AFTER EDIT")
            print(usecase.df)
            # usecase.print_selected()
            return (usecase.df)    

    ################## CAMERA TABLE FROM POOL #######################       
    def pool_edit_camera_for_lens(self,pool):
        def edit_camera_lens(df,cameraLensCategory,constraints):
            print(df)
            if (len(df.index) != 0): 
                df = st.data_editor(
                    df,
                    column_config={
                        "Type": "Type",
                        "Reference": "Model",
                        'Number':st.column_config.NumberColumn(
                            "# Cams",
                            help="How much camera of this type in your use-case (0-15)?",
                            min_value=0,
                            max_value=15,
                            step=1,
                            default=0,
                            format="%d"),
                        'lensControl': st.column_config.SelectboxColumn(
                            "Lens Control",
                            help= "Your needs for lens motorization",
                            # width="small",
                            options = st.session_state.property.constraints[(cameraLensCategory,'LensControls')],
                            #options=st.session_state.property.options['LensUserControls'],
                            required = True),
                        'lensType':  st.column_config.SelectboxColumn(
                            "Type of Lens",
                            help="Main characteristics of the lens",
                            # width="medium",
                            #options = st.session_state.property.options['LensTypes'],
                            options=st.session_state.property.constraints[(cameraLensCategory,'LensTypes')],
                            required = True),
                        'lensMotor':  st.column_config.SelectboxColumn(
                            "Motorization",
                            help="Type of motorization",
                            # width="small",
                            options = st.session_state.property.constraints[(cameraLensCategory,'LensMotors')],
                            required=True),
                        "Brand": "Brand",
                        },
                    disabled=['Reference','Brand','Number'],
                    column_order=['Reference','lensControl','lensType','lensMotor','Brand','Number'],
                    hide_index = True,
                    use_container_width = True,
                    #key = key+"_lens",
        #            on_change = st.rerun,
                    )
                ## st.markdown(display)
                #print("\nDATAFRAME AFTER EDIT")
                #print(df)
                return(df)
        lens = Lens()
        blocks = {}
        #cameraLensCategory est l'élément de sélection
        if 'LensTypes' not in pool.df.columns:
            pool.df['LensTypes']=""
        print("DF Columns:",pool.df.columns)
        print("SELECTED Columns:",pool.selected.columns)
        cameraLensCategories = pool.selected["CameraLensCategory"].unique()
        for cameraLensCategory in cameraLensCategories:
            #filter instance dataframe by type
            selected_rows = pool.selected.loc[pool.selected['CameraLensCategory'] == cameraLensCategory]
            if not selected_rows.empty :
                st.markdown(cameraLensCategory)
                constraints = Lens.filter_constraints(cameraLensCategory)
                blocks[cameraLensCategory] = edit_camera_lens(selected_rows,cameraLensCategory,constraints)
        pool.final = pd.concat(list(blocks.values()))
        print("StreamUI->pool_edit_camera_for_lens-> POOL.FINAL columns:\n",pool.final.columns)
