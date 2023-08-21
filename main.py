import streamlit as st

st.set_page_config(
    page_icon="📔",
    page_title="StoryGen",
    initial_sidebar_state="expanded"
)

hide_st_style ='''
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
'''
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("📔StoryGen")

import json
import google.generativeai as palm
from google.auth import credentials
from google.oauth2 import service_account
import google.cloud.aiplatform as aiplatform
import vertexai
from vertexai.language_models import TextGenerationModel
import requests
import time

##################### Vertext AI & PaLM API initialization #####################

config = st.secrets["GOOGLE_APPLICATION_CREDENTIALS"] #for deploying
# config ='''{
#   "type": "service_account",
#   "project_id": "optimal-route-suggestion",
#   "private_key_id": "19b0edee0b5acd92fd2068e84dec0c68d06eac6c",
#   "private_key": "-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCdBicLKZ6Bs/wj\\nAdo9UNmvPRE2dL3cZS3uIQeK4tx0Vvy3l0b56HdoLu0QMwTWgOWe+YWXfAUwGB7q\\n+0pm8w1+MOkqC0V2IBVJl5/c4CEx3u+24kVHi6bnC90IgReJwC0xwN1HaCJatESA\\n4fCJYnN1qRKXU1gx3KFGxl9UX3+sWG+TPoWATVfKlf5poLrzZJ9E9QglkMl+slpm\\nRjdb3M4f2pFmL1/190bilxfokLT3+LqC3GaIIPQY7lWlWACXt+ldvqsTiIMo/z+Z\\nGwoSJ4xwd+O3JtUHhh+KSRY6Oc43OIhJhKcqsXsuuRl4LWu//uImrt2oilcXguYU\\nJRSrvU8bAgMBAAECggEARCGrRzijwftqZ3YiT4CJM3P3x/0XdE2ihDRopWaR6Rjl\\nRnOpJD4tsVLLIcBBVSFQgI4b3QK+7YNJxwOJ4OmM7Tgjs054sSxykB/uCVRmktD8\\nignbrZN2s8F+Anag0/BCq9fXK2iPn3OgVZuzVqkVF/RoUKilF913TNI+Asn9B7YZ\\nkeoUqSNUUN5fjIgKNWMEvolKZu+TdYobxV9GOevX8FwTx87qmF9Ue8P1RxzyAD3X\\nMBjm5ohZufg6zctN0vxK2OXGvV9lc/qfsxtHhtRoyS3F0Da2NZIXSndl3Arh0Bcb\\nq8b9eo85yjcy+oGVwo00gytpJBk2k445EtwWW0p7oQKBgQDLU5Ux9N9hCT6p1f4N\\n0ngaihCxjxnGu4ZPR3tIiqG5JWN+0vr0obVr9A5m3LU7/AG9Bmm85MlQi6FmuoDw\\neqQY85nImx5z3i55CTx9HOOTpA2pbTIHNqZ8aPLxZI0he1Pnvu6qpiRH3d51Nby4\\nJ4Qbi+Wd+CmAy6jHib3yNL+eTQKBgQDFs9XGv/gfsparX1DMoAfU1v97WkXxUruI\\nxCmSlUpVb4kmDs4gk8x9GJcokvxEr5+iJUPkzwexW/LBaulAdJB3dR8phvGBqvag\\nMe04IkeKVuOXwTgM1QMZmbIvLL3fA546dgksXK5vZ5qal+N3GK/dLhIPQk7zo1nO\\nuy/Y5otnBwKBgQCjCBj4HpXCU8xYF8sGwD0nYo8yIEEV1aVDCljy+J3mO/GEbp1k\\n7AjxT5cAqXX0bAPk0jCUkopNODipi1/58wyDKUikzqRjWcK/sEU9OJ3N81w0/uZ/\\nXDWwSeKK5go3z5CeoLz0PhWXPnKyXu08aAsIn2r0+Fgm+qYRoQOaIuuGfQKBgCWy\\nNIDA+b6RfskOU4mwuc2LcQtEGzH4ZGmffY3FiXbg3XW0PPlZNRRlK+1AmXk/Q2DX\\nWiq2jvDyZ0cZ63+uuh0M5/QzFrlyr7O70U9yudFW3+5/mQBZXU30UFVOYqWzOuhK\\nuVUMFvaG+qOfcm+y9VVnA2qFaihqbSVN68Gfs9ThAoGAacSC7rPBXrYbWJaHpwcc\\nb0b/AODiz03HS/YPWpG778mJXueH7l05RYMCHmfQlLsCUia7j87MaVppok7lb7HY\\nH0fPt0y9fmPB/YT3rX/jsFrBDzuJynd2pYZqgjwWLjWfMRjlg1SdOpzdeK81yVCw\\nHCs87atWEc87lcaIVCzItbg=\\n-----END PRIVATE KEY-----\\n",
#   "client_email": "langchainapps@optimal-route-suggestion.iam.gserviceaccount.com",
#   "client_id": "103157086402886138790",
#   "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#   "token_uri": "https://oauth2.googleapis.com/token",
#   "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#   "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/langchainapps%40optimal-route-suggestion.iam.gserviceaccount.com",
#   "universe_domain": "googleapis.com"
# }
# ''' #for testing
service_account_info=json.loads(config)
service_account_info["private_key"]=service_account_info["private_key"].replace("\\n","\n")
# st.write(service_account_info)
my_credentials = service_account.Credentials.from_service_account_info(
    service_account_info
)
aiplatform.init(
    credentials=my_credentials,
)
project_id = service_account_info["project_id"]
vertexai.init(project=project_id, location="us-central1")

##################### Prompt Engineering #####################

def prompt_format(name,type,age,length,idea):
    txt=f'''
        Act as an experienced and famous Childhood Development Specialist named Francis with extensive creative writing and story writing experience.
        First I will describe what the plan is for you to do. Do NOT enact the plan until you've gone through the whole thing, step by step.
        1. The child's name: {name}
        2. The child's age: {age}
        3. Length of the story: {length} 
        4. Any specific elements that should be included or avoided in the story: {idea}
        5. A theme or genre for the story: {type}
        
        For the above given information, I'll generate a personalized bedtime story just for your little one! Let's get started.
        For the given child's information, synthesize an age-appropriate story to their specifications using the monomyth of Joseph Campbell as informed by Piaget, Lev Vygotsky, Erik Erikson, and Urie Bronfenbrenne. This WILL take a minimum of 2 pages of text to flesh out.
        The story should be both compelling and mesmerizing with memorable settings, and orginal situations. Above ALL it should not be "cliche". "Classic" is allright.
        Directly print the story. **DO NOT ADD ANY SENTENCE OTHER THAN THE STORY ITSELF**.
    '''
    
    return txt

parameters = {
    "max_output_tokens": 1024,
    "temperature": 0.5,
    "top_p": 0.8,
    "top_k": 40
}
model = TextGenerationModel.from_pretrained("text-bison@001")


def get_img(story):
    prompt=f'''
    Act as an experienced image prompt generator, think of a detailed description of a key moment or scene that would make for a great illustration for the below given story.
    Use this description to write a prompt for text-to-image AI to create an image of that moment. All the images must be in a cartoon art or disney style art or painting style.
    The prompt should be a paragraph containing the following details:
    Setting, description of surroundings, character name, character age, character gender, character outfit, character look, character action, style of art.
    Finally, **ONLY OUTPUT THE FINAL IMAGE PROMPT.** THE FINAL IMAGE PROMPT MUST NOT CONTAIN NEW LINE OR PARAGRAH, IT MUST BE A SINGLE PARAGRAPH.
    
    STORY: {story}
    '''
    img=model.predict(prompt,**parameters)
    
    URL="https://stablediffusionapi.com/api/v3/text2img"
    
    data='''{
        "key": "",
        "prompt": "",
        "negative_prompt": "((extra fingers)), mutated hands, ((poorly drawn hands)), ((poorly drawn face)), (((mutation))), (((deformed))), (((tiling))), ((naked)), ((tile)), ((fleshpile)), ((ugly)), (((abstract))), blurry, ((bad anatomy)), ((bad proportions)), ((extra limbs)), cloned face, (((skinny))), glitchy, ((extra breasts)), ((double torso)), ((extra arms)), ((extra hands)), ((mangled fingers)), ((missing breasts)), (missing lips), ((ugly face)), ((extra legs))",
        "width": "512",
        "height": "512",
        "samples": "1",
        "num_inference_steps": "20",
        "safety_checker": "no",
        "enhance_prompt": "yes",
        "seed": null,
        "guidance_scale": 7.5,
        "webhook": null,
        "track_id": null
    }'''
    
    data_json=json.loads(data)
    data_json["key"]=st.secrets["SD_KEY"] #for deploying
    data_json["prompt"]=img.text.strip()

    # st.write(data_json)
    # data_json=json.dumps(data_json,default=str)
    
    x = requests.post(URL, json = data_json)
    
    response=json.loads(x.text)

    if response["status"]=="success":
        return response["output"][0]
    elif response["status"]=="processing":
        new_req='''{
            "key":"",
            "request_id":""
        }'''
        new_data_json=json.loads(new_req)
        new_data_json["key"]=st.secrets["SD_KEY"] #for deploying
        new_data_json["request_id"]=response["id"]
        
        with st.spinner("Making the art more beautiful..."):
            time.sleep(response["eta"])            
            new_res=requests.post(response["fetch_result"],json=new_data_json)
            new_res_json=json.loads(new_res.text)
        
        return new_res_json["output"][0]
    

##################### User Interface ##################### 

with st.sidebar:
    
    name=st.text_input("Child's Name")
    story_type=st.selectbox("Story Type",["Bedtime Story","Moral Story","Fairytale","Adventure","Educational","Mystery",'Science Fiction'])
    age=st.selectbox("Child's Age",["2-4 years","5-7 years","8-10 years","10-12 years","12-14 years"])
    length=st.select_slider("Story Length",["Short (~600 words)","Medium (~800 words)","Long (~1000 words)"])
    idea=st.text_area("If you have any specific ideas, type in here...")
    
    start=st.button("Generate Story!")
    
if start:

    if name and story_type and age and length:
        if idea=="":
            idea="Nothing much specific. You may assume the details accordingly."
        
        prompt=prompt_format(name,story_type,age,length,idea)
        
        with st.spinner("Crafting the perfect story..."):
            story=model.predict(prompt,**parameters)
        
        with st.spinner("Painting some art for your story..."):
            img=get_img(story)

        st.image(img)
        st.divider()
        st.markdown(story.text)
        
    else:
        st.warning("Kindly fill all the details before generating the story",icon="⚠️")