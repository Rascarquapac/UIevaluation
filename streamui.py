import streamlit as st
import pandas    as pd
from pool     import Pool
from usecase  import Usecase
from property import Properties

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
        print("DEBUG:cyaneval->display_camera_table ...")
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
                    "Reference": None,
                    "Protocol":None,
                    "Message":None,
                    "Type":None
                },
                column_order=['Reference','Number','Cable','SupportURL','ManufacturerURL'],
                hide_index = True)
            return(pool.selected)
    def pool_edit_camera_per_type(self,pool,mode='network'):
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
                            'Lens': st.column_config.SelectboxColumn(
                                "Lens",
                                help="Lens type",
                                width="medium",
                                options= st.session_state.property.constraints[(key,'Lens')],
                                required=True),
                            'Network':  st.column_config.SelectboxColumn(
                                "Network",
                                help="Select the network type",
                                width="medium",
                                options=st.session_state.property.constraints[(key,'Network')],
                                required=True),
                            'Base':  st.column_config.SelectboxColumn(
                                "Basement",
                                help="Base type",
                                width="medium",
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
                        "Reference": None,
                        # "supportText": None,
                        "Message":None,
                    },
                    disabled=['Selected','Reference','Cable','SupportURL','ManufacturerURL'],
                    column_order=['Type','Number','Reference','Network','Lens','Base'],
                    hide_index = True,
                    use_container_width = True,
                    key = key+"_network",
        #            on_change = st.rerun,
                    )
                ## st.markdown(display)
                #print("\nDATAFRAME AFTER EDIT")
                #print(df)
                return(df)
        def edit_camera_lens(df,key):
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
                            'Lens': st.column_config.SelectboxColumn(
                                "Lens",
                                help="Lens type",
                                width="medium",
                                options= st.session_state.property.constraints[(key,'Lens')],
                                required=True),
                            'Network':  st.column_config.SelectboxColumn(
                                "Network",
                                help="Select the network type",
                                width="medium",
                                options=st.session_state.property.constraints[(key,'Network')],
                                required=True),
                            'Base':  st.column_config.SelectboxColumn(
                                "Basement",
                                help="Base type",
                                width="medium",
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
                        "Reference": None,
                        # "supportText": None,
                        "Message":None,
                    },
                    disabled=['Selected','Reference','Cable','SupportURL','ManufacturerURL'],
                    column_order=['Type','Number','Reference','Network','Lens','Base'],
                    hide_index = True,
                    use_container_width = True,
                    key = key+"_lens",
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
                if mode == 'network':
                    blocks[camera_type] = edit_camera_network(selected_rows,key=camera_type)
                elif mode == 'lens':
                    blocks[camera_type] = edit_camera_lens(selected_rows,key=camera_type)
                else:
                    raise("Mode of input should be 'network' or 'lens' ")
        pool.final = pd.concat(list(blocks.values()))
