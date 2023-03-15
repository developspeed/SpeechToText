import os
import replicate
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from io import BytesIO
from deta import Deta   

st.set_page_config(
    page_title="Speech Recognizer",
    # page_icon=im,
    layout="wide",
)

hide_menu = """
<style>
#MainMenu{
    visibility:hidden;
}
.css-14xtw13 e8zbici0{
    visibility:hidden;
}
.css-j7qwjs e1fqkh3o7{
    visibility:hidden;
}
footer{
    visibility:hidden;
}
</style>
"""
 
st.markdown(hide_menu , unsafe_allow_html=True)


# Initializing the Database
deta = Deta('a0vvxqkjjrd_UEZCetnYYiHbrAEFyCjeXjSKUbCbQp4W')
db = deta.Base('whisper')

def getItem():
    return db.fetch().items
######################### Frontend UI of the Application #########################

# App Title Name
col1 , col2 , col3 = st.columns(3)
with col1:
    st.title("Speech Recognizer")
with col3:
    st.write("")
    st.write("")
    link = '[Return to Magicaibox](https://www.magicaibox.site/controlpanel/udashboard)'
    html = """
        <style>
        a{
            border-radius:2px;
            border:1px solid;
            text-decoration:none;
            padding:6px;
            color: black;
        }
        a:hover{
            text-decoration:none;
            color:red;
            border:1px solid red;
        }
        .css-1fv8s86 e16nr0p34{
            float: right;
            margin-top: -50px;
        }
    """
    st.markdown(link, unsafe_allow_html=True)
    st.markdown(html, unsafe_allow_html=True)


key = st.sidebar.text_input("Enter the Security Key")
auth = getItem()
if key == auth[4]["secretKey"]:
    st.sidebar.success("Welcome")
    # Initializing the database
    

    language = getItem()
    lang = st.sidebar.selectbox("Specify the Page Language",("Dutch","English","French","Spanish","German"))

    if lang == "Dutch":
        st.markdown(language[3]["dutch"])
    elif lang == "English":
        st.markdown(language[3]["english"])
    elif lang == "French":
        st.markdown(language[3]["french"])
    elif lang == "Spanish":
        st.markdown(language[3]["spanish"])
    else:
        st.markdown(language[3]["german"])

    st.sidebar.write("__________________________")
    st.write("______________________________________________________________________________________________________________________")



    # Taking audio file from mic
    audio_file = audio_recorder(
        text="Click the mic to record your audio -  ",
        recording_color="#ab562c",
        neutral_color="#6aa36f",
        icon_name="microphone",
        icon_size="2x",
        pause_threshold=4.0
    )

    st.write("__________________________________________________________________")

    # uploading files
    audio_upload = st.file_uploader("Upload Audio", type=["wav", "mp3", "m4a"])


    # Playing audio file
    if audio_file:
        st.audio(audio_file, format="audio/wav")
    
    if audio_upload:
        st.audio(audio_upload, format="audio/wav")

    # converting bytes to ioBytes object
    newAudio = BytesIO(audio_file)


    # Setting the Environment of the application using the API token of Replicate from the database
    apiKey = getItem()
    # os.environ['REPLICATE_API_TOKEN'] = "12229e73fd19da262b8a02e3cc386b842cad82ba"
    os.environ['REPLICATE_API_TOKEN'] = apiKey[0]["api_key"]

    # Setting the models of replicate open ai whisper
    model = replicate.models.get("openai/whisper")
    version = model.versions.get("e39e354773466b955265e969568deb7da217804d8e771ea8c9cd0cef6591f8bc")


    # To define the language of the audio file leave blank for automatic detection
    st.sidebar.write('Language spoken in the audio, specify None to perform language detection')
    option = st.sidebar.selectbox('Choose Language',("","af","am","ar","as","az","ba","be","bg","bn","bo","br","bs","ca","cs","cy","da","de","el","en","es","et","eu","fa","fi","fo","fr","gl","gu","ha","haw","hi","hr","ht","hu","hy","id","is","it","iw","ja","jw","ka","kk","km","kn","ko","la","lb","ln","lo","lt","lv","mg","mi","mk","ml","mn","mr","ms","mt","my","ne","nl","nn","no","oc","pa","pl","ps","pt","ro","ru","sa","sd","si","sk","sl","sn","so","sq","sr","su","sv","sw","ta","te","tg","th","tk","tl","tr","tt","uk","ur","uz","vi","yi","yo","zh","Afrikaans","Albanian","Amharic","Arabic","Armenian","Assamese","Azerbaijani","Bashkir","Basque","Belarusian","Bengali","Bosnian","Breton","Bulgarian","Burmese","Castilian","Catalan","Chinese","Croatian","Czech","Danish","Dutch","English","Estonian","Faroese","Finnish","Flemish","French","Galician","Georgian","German","Greek","Gujarati","Haitian","Creole","Hausa","Hawaiian","Hebrew","Hindi","Hungarian","Icelandic","Indonesian","Italian","Japanese","Javanese","Kannada","Kazakh","Khmer","Korean","Lao","Latin","Latvian","Letzeburgesch","Lingala","Lithuanian","Luxembourgish","Macedonian","Malagasy","Malay","Malayalam","Maltese","Maori","Marathi","Moldavian","Moldovan","Mongolian","Myanmar","Nepali","Norwegian","Nynorsk","Occitan","Panjabi","Pashto","Persian","Polish","Portuguese","Punjabi","Pushto","Romanian","Russian","Sanskrit","Serbian","Shona","Sindhi","Sinhala","Sinhalese","Slovak","Slovenian","Somali","Spanish","Sundanese","Swahili","Swedish","Tagalog","Tajik","Tamil","Tatar","Telugu","Thai","Tibetan","Turkish","Turkmen","Ukrainian","Urdu","Uzbek","Valencian","Vietnamese","Welsh","Yiddish","Yoruba"))

    st.write("__________________________________________________________________")
    col4 , col5 = st.columns(2)
    with col5:
        st.checkbox("Translate",value=True)
    with col4:
        if st.button("Transcribe Audio"):
            if audio_file is not None:

                databaseValue = getItem()
                inputs = {
                    # Audio file
                    'audio': newAudio,
                    'model': "large-v2",
                    'transcription': databaseValue[1]["transcription"],
                    'translate': True,
                    'temperature': databaseValue[1]["temperature"],
                    'suppress_tokens': databaseValue[1]["suppress_tokens"],
                    'condition_on_previous_text': databaseValue[1]["checkBoxVal"],
                    'temperature_increment_on_fallback': databaseValue[1]["temperature_increment_on_fallback"],
                    'compression_ratio_threshold': databaseValue[1]["compression_ratio_threshold"],
                    'logprob_threshold': databaseValue[1]["logprob_threshold"],
                    'no_speech_threshold': databaseValue[1]["no_speech_threshold"],
                }

                try:
                    st.warning("Transcribing Audio...")
                    output = version.predict(**inputs)

                    # Audio Language Detection
                    st.write("Detected Language : ", output['detected_language'])
                    st.subheader("Output")
                    st.text_area(" ",value=output["transcription"])

                    # Translated Item
                    st.text_area("English Translated",value=output["translation"])
                    st.success("Transcription Completed!")
                
                except Exception:
                    st.error("Looks like some parameters are incorrect in settings or API expired.")
            
            if audio_upload is not None:
            
                databaseValue = getItem()
                inputs = {
                    # Audio file
                    'audio': audio_upload,
                    'model': "large-v2",
                    'transcription': databaseValue[1]["transcription"],
                    'translate': True,
                    'temperature': 0,
                    'suppress_tokens': -1,
                    'condition_on_previous_text': True,
                    'temperature_increment_on_fallback': 0.2,
                    'compression_ratio_threshold': 2.4,
                    'logprob_threshold': -1,
                    'no_speech_threshold': 0.6,
                }
                try:
                    st.warning("Transcribing Audio...")
                    output = version.predict(**inputs)

                    # Audio Language Detection
                    st.write("Detected Language : ", output['detected_language'])
                    st.subheader("Output")
                    st.text_area(" ",value=output["transcription"])

                    # Translated Item
                    st.text_area("English Translated",value=output["translation"])
                    st.success("Transcription Completed!")
                
                except Exception:
                    st.error("Looks like some parameters are incorrect in settings or API expired.")
        

elif key == "":
    st.sidebar.warning("Enter Secret Key")
else:
    st.sidebar.error("Incorrect Secret Key")



st.write("______________________________________________________________________________")

