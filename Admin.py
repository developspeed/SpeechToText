import streamlit as st
from deta import Deta

st.set_page_config(
    page_title="Admin | Whisper",
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
footer{
    visibility:hidden;
}
</style>
"""

st.markdown(hide_menu, unsafe_allow_html=True)

######################### Frontend UI of the Application #########################

# App Title Name
st.title("OpenAI Whisper Parameters")

################## Backend Logic of the Application #####################

#  !Database Key !Important
# a0vvxqkjjrd_UEZCetnYYiHbrAEFyCjeXjSKUbCbQp4W

deta = Deta('a0vvxqkjjrd_UEZCetnYYiHbrAEFyCjeXjSKUbCbQp4W')
db = deta.Base('whisper')

def getItem():
    return db.fetch().items

# Authentication
# with st.form("auth"):
st.sidebar.title("Login")
username = st.sidebar.text_input("Enter the Username")
password = st.sidebar.text_input("Enter the Password")

submit = st.sidebar.button("Login")
# if submit:
dataBase = getItem()
if username == dataBase[2]['username'] and password == dataBase[2]['password']:
    st.sidebar.success("Login Success")
    # st.balloons()
    with st.form("my_form"):
        
        st.write("Change the text")
        english = st.text_input("Enter the content in English",value=dataBase[3]["english"])
        dutch = st.text_input("Enter the content in Dutch",value=dataBase[3]["dutch"])
        french = st.text_input("Enter the content in French",value=dataBase[3]["french"])
        german = st.text_input("Enter the content in German",value=dataBase[3]["german"])
        spanish = st.text_input("Enter the content in Spanish",value=dataBase[3]["spanish"])

        model = st.selectbox("Model", (dataBase[1]['model'],"large", "medium", "small", "base", "tiny"))

        transcription = st.selectbox("Transcription", ("plain text", "srt", "vtt"),key=dataBase[1]['transcription'])
        
        temperature = st.text_input("Temperature", value=dataBase[1]['temperature'])
        st.markdown("`temperature to use for samplit`")

        patience = st.text_input("Patience",value=dataBase[1]['patience'])
        st.markdown("`optional patience value to use convetional beam search`")

        supToken = st.text_input("Suppress Tokens",value=dataBase[1]['suppress_tokens'])
        st.markdown("`comma seperated list of token punctuation`")

        initial_prompt = st.text_input("initial_prompt")
        st.markdown("`optional text to provide as a prompt for the first window.`")

        checkBoxVal = st.checkbox("Condition_on_Previous_Text",value=dataBase[1]['checkBoxVal'])
        st.markdown("`if True, provide the previous output of the model as a prompt for the next window; disabling may make the text inconsistent across windows, but the model becomes less prone to getting stuck in a failure loop`")

        temperature_increment_on_fallback = st.text_input("temperature_increment_on_fallback",value=dataBase[1]['temperature_increment_on_fallback'])
        st.markdown("`temperature to increase when falling back when the decoding fails to meet either of the thresholds below`")

        compression_ratio_threshold = st.text_input("compression_ratio_threshold",value=dataBase[1]['compression_ratio_threshold'])
        st.markdown("`if the gzip compression ratio is higher than this value, treat the decoding as failed`")

        logprob_threshold = st.text_input("logprob_threshold",value=dataBase[1]['logprob_threshold'])
        st.markdown("`if the average log probability is lower than this value, treat the decoding as failed default : -1`")

        no_speech_threshold = st.text_input("no_speech_threshold",value=dataBase[1]['no_speech_threshold'])
        st.markdown("`if the probability of the <|nospeech|> token is higher than this value AND the decoding has failed due to logprob_threshold, consider the segment as silence default : 0.6`")

        language = st.selectbox('Language',("","af","am","ar","as","az","ba","be","bg","bn","bo","br","bs","ca","cs","cy","da","de","el","en","es","et","eu","fa","fi","fo","fr","gl","gu","ha","haw","hi","hr","ht","hu","hy","id","is","it","iw","ja","jw","ka","kk","km","kn","ko","la","lb","ln","lo","lt","lv","mg","mi","mk","ml","mn","mr","ms","mt","my","ne","nl","nn","no","oc","pa","pl","ps","pt","ro","ru","sa","sd","si","sk","sl","sn","so","sq","sr","su","sv","sw","ta","te","tg","th","tk","tl","tr","tt","uk","ur","uz","vi","yi","yo","zh","Afrikaans","Albanian","Amharic","Arabic","Armenian","Assamese","Azerbaijani","Bashkir","Basque","Belarusian","Bengali","Bosnian","Breton","Bulgarian","Burmese","Castilian","Catalan","Chinese","Croatian","Czech","Danish","Dutch","English","Estonian","Faroese","Finnish","Flemish","French","Galician","Georgian","German","Greek","Gujarati","Haitian","Creole","Hausa","Hawaiian","Hebrew","Hindi","Hungarian","Icelandic","Indonesian","Italian","Japanese","Javanese","Kannada","Kazakh","Khmer","Korean","Lao","Latin","Latvian","Letzeburgesch","Lingala","Lithuanian","Luxembourgish","Macedonian","Malagasy","Malay","Malayalam","Maltese","Maori","Marathi","Moldavian","Moldovan","Mongolian","Myanmar","Nepali","Norwegian","Nynorsk","Occitan","Panjabi","Pashto","Persian","Polish","Portuguese","Punjabi","Pushto","Romanian","Russian","Sanskrit","Serbian","Shona","Sindhi","Sinhala","Sinhalese","Slovak","Slovenian","Somali","Spanish","Sundanese","Swahili","Swedish","Tagalog","Tajik","Tamil","Tatar","Telugu","Thai","Tibetan","Turkish","Turkmen","Ukrainian","Urdu","Uzbek","Valencian","Vietnamese","Welsh","Yiddish","Yoruba"))

        # API Key of replicate
        api_key = st.text_input("API Key for Replicate Model",value=dataBase[0]['api_key'])

        #chnage password and username
        st.write("Want to change the Username and Password ?")
        username = st.text_input("Enter the New Username",value=dataBase[2]['username'])
        password = st.text_input("Enter the New Password",value=dataBase[2]['password'])

        # security key change
        securityKey = st.text_input("Changing the Secret Key",value=dataBase[4]["secretKey"])

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        # submitted = st.button("Submit")
        if submitted:
            # Data Input for Model Values
            db.put({
                "key":"primeData",
                "model":model,
                "transcription": transcription,
                "temperature":temperature,
                "patience":patience,
                "suppress_tokens":supToken,
                "initial_prompt": initial_prompt,
                "checkBoxVal":checkBoxVal,
                "temperature_increment_on_fallback":temperature_increment_on_fallback,
                "compression_ratio_threshold":compression_ratio_threshold,
                "logprob_threshold":logprob_threshold,
                "no_speech_threshold":no_speech_threshold,
                # "language":language
            })

            # API key for replicate Insertion
            db.put({
                "key":"apiKeyReplicate",
                "api_key":api_key
            })

            # changing the password for admin
            db.put({
                'key':'qauth',
                'username':username,
                'password':password
            })

            #changing language content
            db.put({
                "key":"zlang",
                "english":english,
                "spanish":spanish,
                "german":german,
                "dutch":dutch,
                "french":french
            })

            # for changing the secret key
            db.put({
                "key":"zsecret",
                "secretKey":securityKey
            })
            st.success("Values are Set for User Model")
            

elif username == '' and password == '':
    st.sidebar.warning("Enter the Username and Password")

else:
    st.sidebar.error("Inncorrect Login Details")


