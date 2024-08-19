import streamlit as st
import pandas    as pd
from lens import Lens

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
    def pool_edit_camera_number(self,pool):
        # Validate inputs
        if (len(pool.step_match.index) != 0): 
            pool.step_select = st.data_editor(
                pool.step_match,
                height = 200,
                column_config={
                    'Number':st.column_config.NumberColumn(
                        "# of Cams",
                        help="How much camera of this type in your use-case (0-15)?",
                        min_value=0,
                        max_value=15,
                        step=1,
                        format="%d",
                    ),
                    "Reference": "Model",
                    "Brand": "Brand",
                    "Cable": "Cable",
                    "SupportURL": st.column_config.LinkColumn(
                        "Support URL",
                        help = "Reference in Cyanview Support Website",
                        validate = None,
    #                            display_text = "\[(.*?)\]",
                        display_text = "Support Link",
                        max_chars = 30 ),
                    "ManufacturerURL": st.column_config.LinkColumn(
                        "Brand URL",
                        help = "Reference on Brand website",
                        validate = None,
    #                            display_text = "\[(.*?)\]",
                        display_text = "Brand link",
                        max_chars = 30 ),
                    # "Reference": None,
                    # "supportText": None,
                    "Protocol":None,
                    "Message":None,
                    "Type":None
                },
                disabled=['Selected','Reference','Cable','SupportURL','ManufacturerURL'],
                column_order=['Number','Reference','Brand','Cable','SupportURL','ManufacturerURL'],
                hide_index = True,
                use_container_width = True,
                key = "camera_number",
    #            on_change = st.rerun,
                )
            return(pool.step_select)
    def pool_display_selected(self,pool):
        # Update the camera pool Dataframe with the number of camera selected on this step
        pool.df.update(pool.step_select)
        # Set the set of selected cameras
        pool.selected = pool.df[(pool.df['Number']>0)]
        # Trying to set properties of pool.selected for display
        pool.selected.style.set_properties(**{'background_color': 'lightgreen'})
        if (len(pool.selected.index) != 0):
            st.dataframe(
                pool.selected,
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
                    "SupportURL": st.column_config.LinkColumn(
                        "Support URL",
                        help = "Reference in Cyanview Support Website",
                        validate = None,
    #                            display_text = "\[(.*?)\]",
                        display_text = "Support Link",
                        max_chars = 30 ),
                    "ManufacturerURL": st.column_config.LinkColumn(
                        "Brand URL",
                        help = "Reference on Brand website",
                        validate = None,
    #                            display_text = "\[(.*?)\]",
                        display_text = "Brand link",
                        max_chars = 30 ),
                    "Protocol":None,
                    "Message":None,
                    "Type":None
                },
                column_order=['Number','Brand','Reference','Cable','SupportURL','ManufacturerURL'],
                hide_index = True)
            return(pool.selected)
    def pool_edit_camera_for_network(self,pool):
        def edit_camera_network(df,key):
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
                            format="%d",
                        ),
                        'Network': st.column_config.SelectboxColumn(
                            "IP Network",
                            help="Select the IP network type",
                            width="small",
                            default = st.session_state.property.constraints[(key,'Network')][0],
                            options = st.session_state.property.constraints[(key,'Network')],
                            required=True),
                        'Base':  st.column_config.SelectboxColumn(
                            "Basement",
                            help="Base type",
                            width="small",
                            options=st.session_state.property.constraints[(key,'Base')],
                            required=True),
                        "Brand": "Brand",
                        "Cable": "Cable",
                        "SupportURL": st.column_config.LinkColumn(
                            "Support URL",
                            help = "Reference in Cyanview Support Website",
                            validate = None,
        #                            display_text = "\[(.*?)\]",
                            display_text = "Support Link",
                            max_chars = 30 ),
                        "ManufacturerURL": st.column_config.LinkColumn(
                            "Brand URL",
                            help = "Reference on Brand website",
                            validate = None,
        #                            display_text = "\[(.*?)\]",
                            display_text = "Brand link",
                            max_chars = 30 ),
                        # "supportText": None,
                        "Message":None,
                        },
                    disabled=['Reference','Brand','Number','SupportURL'],
                    column_order=['Network','Reference','Brand','Number','SupportURL'],
                    hide_index = True,
                    use_container_width = True,
                    key = key+"_network",
        #            on_change = st.rerun,
                    )
                ## st.markdown(display)
                #print("\nDATAFRAME AFTER EDIT")
                #print(df)
                return(df)
        blocks = {}
        camera_types = pool.selected["Type"].unique()
        for camera_type in camera_types:
            #filter instance dataframe by type
            selected_rows = pool.selected.loc[pool.selected['Type'] == camera_type]
            if not selected_rows.empty :
                st.markdown(camera_type)
                blocks[camera_type] = edit_camera_network(selected_rows,key=camera_type)
        pool.final = pd.concat(list(blocks.values()))

    def pool_edit_camera_for_lens(self,pool):
        def edit_camera_lens(df,cameraLensCategory):
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
                        'lensControl':  st.column_config.SelectboxColumn(
                            "Lens Control",
                            help="Your needs for lens motorization",
                            # width="small",
                            options=st.session_state.property.constraints[(cameraLensCategory,'LensControls')],
                            #options=st.session_state.property.options['LensUserControls'],
                            required=True),
                        'lensType':  st.column_config.SelectboxColumn(
                            "Type of Lens",
                            help="Main characteristics of the lens",
                            # width="medium",
                            options=st.session_state.property.options['LensTypes'],
                            #options=st.session_state.property.constraints[(cameraLensCategory,'LensTypes')],
                            required=True),
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
                blocks[cameraLensCategory] = edit_camera_lens(selected_rows,cameraLensCategory)
        pool.final = pd.concat(list(blocks.values()))
