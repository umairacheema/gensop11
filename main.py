import os
import pyperclip
import streamlit as st
import datetime
from model import GenSOPModel
from openai import OpenAI

st.set_page_config(page_title="GenSOP Eleven", layout="wide")

st.markdown("""
    <style>
        .reportview-container {
            margin-top: 0em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)


sop_llm_model = None
#initialize OpenAI
client = OpenAI()

#Load model
def initialize_model():
    model = GenSOPModel()
    model.load_model()
    return model


if 'accumulated_text' not in st.session_state:
    st.session_state.accumulated_text = ""
st.image('./assets/logo.jpeg')
    #st.markdown(f"### SOP Generation")
st.markdown(f"\n{st.session_state.accumulated_text}")

#query model
def query_llm_model():
    #Initialize model
    
    st.session_state.accumulated_text = ""
    with st.spinner("Generating SOP content for Chemicals"):
        for chemical in selected_chemicals:
            with open('./chemicals/'+chemical, 'r') as file:
                file_contents = file.read()
                if(local_mode):
                    sop_llm_model = initialize_model()
                    text = sop_llm_model.generate_response('Extract all the useful information and create a standard operating procedure to handle this chemical safely in a lab from the html table'+file_contents)
                    st.session_state.accumulated_text += "\n#"+chemical+'\n' + text
                else:
                    create_sop_openai("create a standard operating procedure to handle this chemical safely in a lab using the following information:\n"+file_contents)

    
    with st.spinner("Generating SOP content for Instruments"):
        for instrument in selected_instruments:
            with open('./generic_instruments/'+instrument, 'r') as file:
                file_contents = file.read()
                if(local_mode):
                    sop_llm_model = initialize_model()
                    text = sop_llm_model.generate_response('Create a standard operating procedure to handle this instrument safely in a lab from the following text:'+file_contents)
                    st.session_state.accumulated_text += "\n#"+instrument+'\n' + text
                else:
                    create_sop_openai("create a standard operating procedure to handle this instrument safely in a lab using the following information:\n"+file_contents)
    current_datetime = datetime.datetime.now()
    # Format the date and time into a string
    filename = current_datetime.strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
    with open('./sops/'+filename, 'a') as file:
        file.write(st.session_state.accumulated_text)

def create_sop_openai(user_prompt):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
            "role": "user",
            "content": user_prompt
            }
        ]
        )
    st.session_state.accumulated_text +=  completion.choices[0].message.content
    current_datetime = datetime.datetime.now()
    # Format the date and time into a string
    filename = current_datetime.strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
    with open('./validated_sops/'+filename, 'a') as file:
        file.write(st.session_state.accumulated_text)

def validate_sop():
    with st.spinner("Validating and reformating the SOP"):
        if(len(selected_sections)>0):
            sections = str(selected_sections)
            user_prompt = "Write a detailed standard operating procedure document in microsoft word docx format with the sections "+sections+" using the following information: "+ st.session_state.accumulated_text
        else:
            user_prompt = "Write a detailed standard operating procedure document in microsoft word docx format by combining the following information: "+ st.session_state.accumulated_text
        completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
            "role": "user",
            "content": user_prompt
            }
        ]
        )
        st.session_state.accumulated_text = completion.choices[0].message.content
        st.balloons()
      



def reset():
    st.session_state.accumulated_text = ""
    

#Load list of chemicals and instruments
directory_path = './chemicals'
directory_path_generic_instruments = './generic_instruments'

# Get a list of all files and directories
chemical_entries = os.listdir(directory_path)
instrument_entries = os.listdir(directory_path_generic_instruments)

#User interface
st.logo('./assets/logo.jpeg',  size='large')

selected_chemicals = st.sidebar.multiselect(
    "Select Chemicals",
    chemical_entries
)

selected_instruments = st.sidebar.multiselect(
    "Select Instruments",
    instrument_entries
)

selected_sections = st.sidebar.multiselect(
    "Select Template Sections",
    ['Title and Identification', 'Purpose and Scope','Responsibilities','Definitions and Terminology','Safety Precautions','Procedure','Maintenance and Calibration','Troubleshooting']
)

local_mode = st.sidebar.toggle("Local model for SOP")

generate_button = st.sidebar.button(
    "Generate SOP",
    on_click=query_llm_model
)

validate_button = st.sidebar.button(
    "Validate SOP",
    on_click=validate_sop
)

if st.sidebar.button('Copy to Clipboard'):
    pyperclip.copy(st.session_state.accumulated_text)
    st.success('Text copied successfully!')

reset_button = st.sidebar.button(
    "  Reset SOP ",
    on_click=reset
)
