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
st.title("Speech Recognizer")


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

    # Uploading audio file

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


    ################## Backend Logic of the Application #####################


    # Setting the Environment of the application using the API token of Replicate from the database
    apiKey = getItem()
    # os.environ['REPLICATE_API_TOKEN'] = "12229e73fd19da262b8a02e3cc386b842cad82ba"
    os.environ['REPLICATE_API_TOKEN'] = apiKey[0]["api_key"]


    # Grabbing the models models
    model = replicate.models.get("openai/whisper")
    version = model.versions.get("30414ee7c4fffc37e260fcab7842b5be470b9b840f2b608f5baa9bbef9a259ed")

    # To define the language of the audio file leave blank for automatic detection
    st.sidebar.write('Language spoken in the audio, specify None to perform language detection')
    option = st.sidebar.selectbox('Choose Language',("","af","am","ar","as","az","ba","be","bg","bn","bo","br","bs","ca","cs","cy","da","de","el","en","es","et","eu","fa","fi","fo","fr","gl","gu","ha","haw","hi","hr","ht","hu","hy","id","is","it","iw","ja","jw","ka","kk","km","kn","ko","la","lb","ln","lo","lt","lv","mg","mi","mk","ml","mn","mr","ms","mt","my","ne","nl","nn","no","oc","pa","pl","ps","pt","ro","ru","sa","sd","si","sk","sl","sn","so","sq","sr","su","sv","sw","ta","te","tg","th","tk","tl","tr","tt","uk","ur","uz","vi","yi","yo","zh","Afrikaans","Albanian","Amharic","Arabic","Armenian","Assamese","Azerbaijani","Bashkir","Basque","Belarusian","Bengali","Bosnian","Breton","Bulgarian","Burmese","Castilian","Catalan","Chinese","Croatian","Czech","Danish","Dutch","English","Estonian","Faroese","Finnish","Flemish","French","Galician","Georgian","German","Greek","Gujarati","Haitian","Creole","Hausa","Hawaiian","Hebrew","Hindi","Hungarian","Icelandic","Indonesian","Italian","Japanese","Javanese","Kannada","Kazakh","Khmer","Korean","Lao","Latin","Latvian","Letzeburgesch","Lingala","Lithuanian","Luxembourgish","Macedonian","Malagasy","Malay","Malayalam","Maltese","Maori","Marathi","Moldavian","Moldovan","Mongolian","Myanmar","Nepali","Norwegian","Nynorsk","Occitan","Panjabi","Pashto","Persian","Polish","Portuguese","Punjabi","Pushto","Romanian","Russian","Sanskrit","Serbian","Shona","Sindhi","Sinhala","Sinhalese","Slovak","Slovenian","Somali","Spanish","Sundanese","Swahili","Swedish","Tagalog","Tajik","Tamil","Tatar","Telugu","Thai","Tibetan","Turkish","Turkmen","Ukrainian","Urdu","Uzbek","Valencian","Vietnamese","Welsh","Yiddish","Yoruba"))

    st.write("__________________________________________________________________")
    if st.button("Transcribe Audio"):
        if audio_file is not None:
            databaseValue = getItem()
            inputs = {
                # Audio file
                'audio': newAudio,

                # Choose a Whisper model.
                'model': databaseValue[1]["model"],

                # Choose the format for the transcription
                'transcription': databaseValue[1]["transcription"],

                # Translate the text to English when set to True
                'translate': True,

                # language spoken in the audio, specify None to perform language
                # detection
                # 'language': ...,

                # temperature to use for sampling
                'temperature': databaseValue[1]["temperature"],

                # optional patience value to use in beam decoding, as in
                # https://arxiv.org/abs/2204.05424, the default (1.0) is equivalent to
                # conventional beam search
                'patience': databaseValue[1]["patience"],

                # comma-separated list of token ids to suppress during sampling; '-1'
                # will suppress most special characters except common punctuations
                'suppress_tokens': databaseValue[1]["suppress_tokens"],

                # optional text to provide as a prompt for the first window.
                'initial_prompt': databaseValue[1]["initial_prompt"],

                # if True, provide the previous output of the model as a prompt for
                # the next window; disabling may make the text inconsistent across
                # windows, but the model becomes less prone to getting stuck in a
                # failure loop
                'condition_on_previous_text': databaseValue[1]["checkBoxVal"],

                # temperature to increase when falling back when the decoding fails to
                # meet either of the thresholds below
                'temperature_increment_on_fallback': databaseValue[1]["temperature_increment_on_fallback"],

                # if the gzip compression ratio is higher than this value, treat the
                # decoding as failed
                'compression_ratio_threshold': databaseValue[1]["compression_ratio_threshold"],

                # if the average log probability is lower than this value, treat the
                # decoding as failed
                'logprob_threshold': databaseValue[1]["logprob_threshold"],

                # if the probability of the <|nospeech|> token is higher than this
                # value AND the decoding has failed due to `logprob_threshold`,
                # consider the segment as silence
                'no_speech_threshold': databaseValue[1]["no_speech_threshold"],
            }

            # https://replicate.com/openai/whisper/versions/30414ee7c4fffc37e260fcab7842b5be470b9b840f2b608f5baa9bbef9a259ed#output-schema
            try:
                st.warning("Transcribing Audio...")
                output = version.predict(**inputs)
                # print(output)
                # Performing the Analysis
                output = version.predict(**inputs)

                # Audio Language Detection
                st.write("Detected Language : ", output['detected_language'])
                
                st.subheader("Output")
                st.text_area(" ",value=output["transcription"])

                # Translated Item
                st.checkbox("Translate",value=True)
                st.text_area("English Translated",value=output["translation"])
                st.success("Transcription Completed!")
            
            except Exception:
                st.error("Looks like some parameters are incorrect in settings or API expired.")
        
        if audio_upload is not None:
            databaseValue = getItem()
            inputs = {
                # Audio file
                'audio': audio_upload,

                # Choose a Whisper model.
                'model': databaseValue[1]["model"],

                # Choose the format for the transcription
                'transcription': databaseValue[1]["transcription"],

                # Translate the text to English when set to True
                'translate': True,

                # language spoken in the audio, specify None to perform language
                # detection
                # 'language': ...,

                # temperature to use for sampling
                'temperature': databaseValue[1]["temperature"],

                # optional patience value to use in beam decoding, as in
                # https://arxiv.org/abs/2204.05424, the default (1.0) is equivalent to
                # conventional beam search
                'patience': databaseValue[1]["patience"],

                # comma-separated list of token ids to suppress during sampling; '-1'
                # will suppress most special characters except common punctuations
                'suppress_tokens': databaseValue[1]["suppress_tokens"],

                # optional text to provide as a prompt for the first window.
                'initial_prompt': databaseValue[1]["initial_prompt"],

                # if True, provide the previous output of the model as a prompt for
                # the next window; disabling may make the text inconsistent across
                # windows, but the model becomes less prone to getting stuck in a
                # failure loop
                'condition_on_previous_text': databaseValue[1]["checkBoxVal"],

                # temperature to increase when falling back when the decoding fails to
                # meet either of the thresholds below
                'temperature_increment_on_fallback': databaseValue[1]["temperature_increment_on_fallback"],

                # if the gzip compression ratio is higher than this value, treat the
                # decoding as failed
                'compression_ratio_threshold': databaseValue[1]["compression_ratio_threshold"],

                # if the average log probability is lower than this value, treat the
                # decoding as failed
                'logprob_threshold': databaseValue[1]["logprob_threshold"],

                # if the probability of the <|nospeech|> token is higher than this
                # value AND the decoding has failed due to `logprob_threshold`,
                # consider the segment as silence
                'no_speech_threshold': databaseValue[1]["no_speech_threshold"],
            }

            # https://replicate.com/openai/whisper/versions/30414ee7c4fffc37e260fcab7842b5be470b9b840f2b608f5baa9bbef9a259ed#output-schema
            try:
                st.warning("Transcribing Audio...")
                output = version.predict(**inputs)
                # print(output)
                # Performing the Analysis
                output = version.predict(**inputs)

                # Audio Language Detection
                st.write("Detected Language : ", output['detected_language'])
                
                st.subheader("Output")
                st.text_area(" ",value=output["transcription"])

                # Translated Item
                st.checkbox("Translate",value=True)
                st.text_area("English Translated",value=output["translation"])
                st.success("Transcription Completed!")
            
            except Exception:
                st.error("Looks like some parameters are incorrect in settings or API expired.")
    
        else:
            st.sidebar.error("Please Upload an Audio")
elif key == "":
    st.sidebar.warning("Enter Secret Key")
else:
    st.sidebar.error("Incorrect Secret Key")
