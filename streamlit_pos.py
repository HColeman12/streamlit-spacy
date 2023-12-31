import streamlit as st
import spacy
import time


@st.cache_resource
def load_model(model_name):
    nlp = spacy.load(model_name)
    return (nlp)
nlp = load_model("en_core_web_lg")

def extract_entities(ent_types, text):
    
    
    results = []
    doc = nlp(text)
    if ent_types == 'NOUN':
        for chunk in doc.noun_chunks:
            results.append((chunk.root.text, ent_types))
        return (results)
    else:
        for tok in doc:
            if tok.pos_ in ent_types:
                results.append((tok.text, tok.pos_))
        return (results)

st.title("Sentence Analyzer")

form1 = st.sidebar.form(key="Options")
form1.header("Parts of Speech")
ent_types = form1.selectbox("Select the entities you want", ["","Adjective","Adverb","Conjunction","Determiner","Interjection","Noun","Number","Preposition","Pronoun","Proper Noun","Subordinating Conjuncton","Verb"])



match ent_types:
    case "Adjective":
        ent_types = "ADJ"
    case "Adverb":
        ent_types = "ADV"
    case "Conjunction":
        ent_types = "CONJ"
    case "Determiner":
        ent_types = "DET"
    case "Interjection":
        ent_types = "INTJ"
    case "Noun":
        ent_types = "NOUN"
    case "Number":
        ent_types = "NUM"
    case "Pronoun":
        ent_types = "PRON"
    case "Proper Noun":
        ent_types = "PROPN"
    case "Preposition":
        ent_types = "ADP"
    case "Subordinating Conjunction":
        ent_types  = "SCONJ"
    case "Verb":
        ent_types = "VERB"
    case _:
        ent_types = ent_types

submitted = form1.form_submit_button("Find")

ph2 = st.empty()
text = ph2.text_area("Text", 
                    "",key=7)



hits = extract_entities(ent_types, text)

num_found = len(hits)
i = 0
j = 0


if submitted:
    j = 0
    changed_input = []
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for ele in text:
        if ele in punc:
            text = text.replace(ele, "")
    for w in text.split():
        if j < num_found:
            if w in hits[j][0]:
                w = ("<" + w + ">")
                changed_input.append(w)
                j = j + 1
            else:
                w = w
                changed_input.append(w)
        else:
            w = w
            changed_input.append(w)

    
    text = ph2.text_area('Text', value=str.join(' ',changed_input), key=33)


    if len(text) < 1:
        st.subheader('Please enter some text to be analyzed. :point_up_2:')
    elif num_found > 0:
        user_selected = hits[0][1]
        match ent_types:
            case "ADJ":
                user_output = "Adjective"
            case "ADV":
                user_output = "Adverb"
            case "CONJ":
                user_output = "Conjunction"
            case "DET":
                user_output = "Determiner"
            case "ADP":
                user_output = "Preposition"
            case "INTJ":
                user_output = "Interjection"
            case "NOUN":
                user_output = "Noun"
            case "NUM":
                user_output = "Number"
            case "PRON":
                user_output = "Pronoun"
            
            case "PROPN":
                user_output = "Proper Noun"
            case "SCONJ":
                user_output = "Subordinating Conjunction"
            case "VERB":
                user_output = "Verb"
            case _:
                user_output = ent_types
        st.write("Found the following ",num_found, user_output,"(s)")
        while i < num_found:
            #with st.spinner('Analyzing text...'):
             #   time.sleep(i + 1)
            st.success(hits[i][0])
            i = i + 1
    elif text != None and num_found < 1:
        st.write("None found.")
    
    





