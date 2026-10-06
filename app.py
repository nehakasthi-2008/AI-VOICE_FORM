import re
import streamlit as st
import speech_recognition as sr
from html import escape


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="VoiceForm AI",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# LANGUAGES
# =========================================================

LANGS = ["English", "Telugu", "Hindi", "Tamil", "Kannada", "Malayalam"]

NATIVE = {
    "English": "English",
    "Telugu": "తెలుగు (Telugu)",
    "Hindi": "हिन्दी (Hindi)",
    "Tamil": "தமிழ் (Tamil)",
    "Kannada": "ಕನ್ನಡ (Kannada)",
    "Malayalam": "മലയാളം (Malayalam)"
}

LANGUAGE_CODES = {
    "English": "en-IN",
    "Telugu": "te-IN",
    "Hindi": "hi-IN",
    "Tamil": "ta-IN",
    "Kannada": "kn-IN",
    "Malayalam": "ml-IN"
}


# =========================================================
# FORM FIELDS
# =========================================================

# type decides how the spoken text is cleaned:
# name, text, address, dob, phone, digits, email
FIELD_CATALOG = {
    "name":    {"label": "l_name",    "type": "name"},
    "father":  {"label": "l_father",  "type": "name"},
    "mother":  {"label": "l_mother",  "type": "name"},
    "dob":     {"label": "l_dob",     "type": "dob"},
    "gender":  {"label": "l_gender",  "type": "text"},
    "address": {"label": "l_address", "type": "address", "multiline": True},
    "city":    {"label": "l_city",    "type": "text"},
    "state":   {"label": "l_state",   "type": "text"},
    "pincode": {"label": "l_pincode", "type": "digits"},
    "phone":   {"label": "l_phone",   "type": "phone"},
    "email":   {"label": "l_email",   "type": "email"},
    "country": {"label": "l_country", "type": "text"}
}

DEFAULT_FIELDS = ["name", "father", "dob", "address", "phone", "email"]


# =========================================================
# TRANSLATIONS
# =========================================================

TR = {

    # ------------------------------------------------- ENGLISH
    "English": {
        "nav_home": "Home",
        "nav_upload": "Upload Form",
        "nav_voice": "Voice Assistant",
        "nav_save": "Save Form",
        "nav_logout": "Logout",
        "sidebar_subtitle": "Smart Voice Form Assistant",
        "ai_powered": "AI Powered",
        "ai_tags": "Voice • Translation • Forms",
        "hello": "Hello, {name}! 👋",

        "hero_subtitle": "Smart Voice-Based Form Assistant",
        "hero_badge": "✨ Fill forms faster • Speak naturally • Save easily",
        "stat1": "Languages",
        "stat2": "Hands-free typing",
        "stat3": "Click to start speaking",
        "stat4": "Forms you can fill",
        "welcome_title": "Welcome to VoiceForm AI 👋",
        "welcome_sub": "Fill digital forms using your voice with an easy and intelligent interface.",
        "f1_title": "Upload Your Form",
        "f1_text": "Upload your existing PDF or image form.",
        "f2_title": "Choose Language",
        "f2_text": "Select the language you want to use.",
        "f3_title": "Speak & Fill",
        "f3_text": "Speak your answers and automatically put them into the form.",
        "how_title": "How It Works 🚀",
        "how_sub": "Four simple steps from blank form to finished form.",
        "s1_t": "Upload", "s1_d": "Upload your form",
        "s2_t": "Language", "s2_d": "Choose language",
        "s3_t": "Speak", "s3_d": "Answer by voice",
        "s4_t": "Save", "s4_d": "Save your form",
        "start_btn": "🚀 Start VoiceForm AI",

        "login_hero": "Login to continue",
        "login_title": "Welcome! Please Login",
        "login_subtitle": "Enter your basic details to get started",
        "login_name": "👤 Your Name",
        "login_phone": "📱 Phone Number",
        "login_btn": "🔐 Login",
        "login_err_name": "⚠️ Please enter your name.",
        "login_err_phone": "⚠️ Please enter a valid 10-digit phone number.",
        "login_note": "🌐 The whole app will appear in the language you choose.",

        "up_title": "Upload Your Form",
        "up_sub": "Upload your form and select a language",
        "up_choose": "📁 Choose your form",
        "up_lang": "🌐 Choose your language",
        "up_ok": "✅ {file} uploaded!",
        "up_preview": "📋 Your form preview",
        "up_start": "🎙️ Start Voice Form",
        "up_fields": "🧾 Select the fields present in your form",
        "up_custom": "➕ Add your own field (example: Aadhaar Number)",
        "up_custom_btn": "➕ Add Field",

        "v_title": "Voice Assistant",
        "v_sub": "Speak your answer and fill the form",
        "v_selected": "Selected Language:",
        "v_hint": "Click the glowing microphone button beside a field and speak your answer.",
        "v_progress": "📝 Form Progress",
        "v_fields": "{filled} / {total} fields",
        "v_personal": "👤 Personal Information",
        "v_personal_sub": "You can type normally or use the 🎙️ microphone buttons to fill each field.",
        "v_no_fields": "⚠️ No fields selected. Please select the fields of your form on the Upload Form page.",
        "tip_symbols": "💡 Speaking tips: say “at the rate” for @, “dot” for ., “dash” for -, “slash” for /, “comma” for , — numbers are joined automatically.",
        "l_name": "👤 Full Name",
        "l_father": "👨 Father's / Guardian's Name",
        "l_mother": "👩 Mother's Name",
        "l_dob": "🎂 Date of Birth",
        "l_gender": "🧑 Gender",
        "l_email": "📧 Email Address",
        "l_phone": "📱 Phone Number",
        "l_address": "🏠 Address",
        "l_city": "🌆 City",
        "l_state": "🗺️ State",
        "l_pincode": "📮 PIN Code",
        "l_country": "🌍 Country",
        "v_save": "💾 SAVE FORM",
        "v_saved": "✅ Your form has been saved!",
        "listening": "🎙️ Listening... Please speak now.",
        "converting": "🔄 Converting your speech to text...",
        "err_timeout": "⏱️ I didn't hear anything. Please try again.",
        "err_unknown": "❌ Sorry, I couldn't understand your voice.",
        "err_request": "🌐 Speech recognition needs an internet connection.",
        "err_mic": "❌ Microphone error: {e}",

        "sv_title": "Save Form",
        "sv_sub": "Review your completed information",
        "sv_none": "No form information has been saved yet.",
        "sv_completed": "📋 Completed Information",
        "sv_completed_sub": "Everything looks good? Download your form below.",
        "sv_not": "Not provided",
        "sv_download": "⬇️ Download Form",

        "ft_sub": "Smart Voice-Based Form System",
        "ft_built": "Built with ❤️ using Python & Streamlit"
    },

    # ------------------------------------------------- TELUGU
    "Telugu": {
        "nav_home": "హోమ్",
        "nav_upload": "ఫారమ్ అప్‌లోడ్",
        "nav_voice": "వాయిస్ అసిస్టెంట్",
        "nav_save": "ఫారమ్ సేవ్",
        "nav_logout": "లాగ్అవుట్",
        "sidebar_subtitle": "స్మార్ట్ వాయిస్ ఫారమ్ అసిస్టెంట్",
        "ai_powered": "AI ఆధారితం",
        "ai_tags": "వాయిస్ • అనువాదం • ఫారమ్‌లు",
        "hello": "నమస్తే, {name}! 👋",

        "hero_subtitle": "స్మార్ట్ వాయిస్ ఆధారిత ఫారమ్ అసిస్టెంట్",
        "hero_badge": "✨ ఫారమ్‌లను వేగంగా నింపండి • సహజంగా మాట్లాడండి • సులభంగా సేవ్ చేయండి",
        "stat1": "భాషలు",
        "stat2": "చేతులతో టైప్ చేయకుండా",
        "stat3": "మాట్లాడటం మొదలుపెట్టడానికి క్లిక్",
        "stat4": "నింపగల ఫారమ్‌లు",
        "welcome_title": "VoiceForm AI కు స్వాగతం 👋",
        "welcome_sub": "సులభమైన, తెలివైన ఇంటర్‌ఫేస్‌తో మీ గొంతుతో డిజిటల్ ఫారమ్‌లను నింపండి.",
        "f1_title": "మీ ఫారమ్‌ను అప్‌లోడ్ చేయండి",
        "f1_text": "మీ ప్రస్తుత PDF లేదా ఇమేజ్ ఫారమ్‌ను అప్‌లోడ్ చేయండి.",
        "f2_title": "భాషను ఎంచుకోండి",
        "f2_text": "మీరు ఉపయోగించాలనుకునే భాషను ఎంచుకోండి.",
        "f3_title": "మాట్లాడండి & నింపండి",
        "f3_text": "మీ సమాధానాలు చెప్పండి, అవి ఆటోమేటిక్‌గా ఫారమ్‌లో నిండిపోతాయి.",
        "how_title": "ఇది ఎలా పనిచేస్తుంది 🚀",
        "how_sub": "ఖాళీ ఫారమ్ నుండి పూర్తయిన ఫారమ్ వరకు నాలుగు సులభమైన దశలు.",
        "s1_t": "అప్‌లోడ్", "s1_d": "మీ ఫారమ్‌ను అప్‌లోడ్ చేయండి",
        "s2_t": "భాష", "s2_d": "భాషను ఎంచుకోండి",
        "s3_t": "మాట్లాడండి", "s3_d": "వాయిస్‌తో సమాధానం ఇవ్వండి",
        "s4_t": "సేవ్", "s4_d": "మీ ఫారమ్‌ను సేవ్ చేయండి",
        "start_btn": "🚀 VoiceForm AI ప్రారంభించండి",

        "login_hero": "కొనసాగడానికి లాగిన్ అవ్వండి",
        "login_title": "స్వాగతం! దయచేసి లాగిన్ అవ్వండి",
        "login_subtitle": "ప్రారంభించడానికి మీ ప్రాథమిక వివరాలను నమోదు చేయండి",
        "login_name": "👤 మీ పేరు",
        "login_phone": "📱 ఫోన్ నంబర్",
        "login_btn": "🔐 లాగిన్",
        "login_err_name": "⚠️ దయచేసి మీ పేరు నమోదు చేయండి.",
        "login_err_phone": "⚠️ దయచేసి సరైన 10 అంకెల ఫోన్ నంబర్ నమోదు చేయండి.",
        "login_note": "🌐 మొత్తం యాప్ మీరు ఎంచుకున్న భాషలో కనిపిస్తుంది.",

        "up_title": "మీ ఫారమ్‌ను అప్‌లోడ్ చేయండి",
        "up_sub": "మీ ఫారమ్‌ను అప్‌లోడ్ చేసి భాషను ఎంచుకోండి",
        "up_choose": "📁 మీ ఫారమ్‌ను ఎంచుకోండి",
        "up_lang": "🌐 మీ భాషను ఎంచుకోండి",
        "up_ok": "✅ {file} అప్‌లోడ్ అయింది!",
        "up_preview": "📋 మీ ఫారమ్ ప్రివ్యూ",
        "up_start": "🎙️ వాయిస్ ఫారమ్ ప్రారంభించండి",
        "up_fields": "🧾 మీ ఫారమ్‌లో ఉన్న ఫీల్డ్‌లను ఎంచుకోండి",
        "up_custom": "➕ మీ సొంత ఫీల్డ్‌ను జోడించండి (ఉదాహరణ: ఆధార్ నంబర్)",
        "up_custom_btn": "➕ ఫీల్డ్ జోడించండి",

        "v_title": "వాయిస్ అసిస్టెంట్",
        "v_sub": "మీ సమాధానం చెప్పి ఫారమ్ నింపండి",
        "v_selected": "ఎంచుకున్న భాష:",
        "v_hint": "ఫీల్డ్ పక్కన ఉన్న మెరిసే మైక్రోఫోన్ బటన్‌ను క్లిక్ చేసి మీ సమాధానం చెప్పండి.",
        "v_progress": "📝 ఫారమ్ పురోగతి",
        "v_fields": "{filled} / {total} ఫీల్డ్‌లు",
        "v_personal": "👤 వ్యక్తిగత సమాచారం",
        "v_personal_sub": "మీరు మామూలుగా టైప్ చేయవచ్చు లేదా ప్రతి ఫీల్డ్ నింపడానికి 🎙️ మైక్రోఫోన్ బటన్‌లను ఉపయోగించవచ్చు.",
        "v_no_fields": "⚠️ ఏ ఫీల్డ్ ఎంచుకోలేదు. దయచేసి ఫారమ్ అప్‌లోడ్ పేజీలో మీ ఫారమ్‌లోని ఫీల్డ్‌లను ఎంచుకోండి.",
        "tip_symbols": "💡 మాట్లాడే చిట్కాలు: @ కోసం “at the rate”, . కోసం “dot”, - కోసం “dash”, / కోసం “slash”, , కోసం “comma” అనండి — సంఖ్యలు ఆటోమేటిక్‌గా కలుస్తాయి.",
        "l_name": "👤 పూర్తి పేరు",
        "l_father": "👨 తండ్రి / సంరక్షకుని పేరు",
        "l_mother": "👩 తల్లి పేరు",
        "l_dob": "🎂 పుట్టిన తేదీ",
        "l_gender": "🧑 లింగం",
        "l_email": "📧 ఈమెయిల్ చిరునామా",
        "l_phone": "📱 ఫోన్ నంబర్",
        "l_address": "🏠 చిరునామా",
        "l_city": "🌆 నగరం",
        "l_state": "🗺️ రాష్ట్రం",
        "l_pincode": "📮 పిన్ కోడ్",
        "l_country": "🌍 దేశం",
        "v_save": "💾 ఫారమ్ సేవ్ చేయండి",
        "v_saved": "✅ మీ ఫారమ్ సేవ్ అయింది!",
        "listening": "🎙️ వింటున్నాను... దయచేసి ఇప్పుడు మాట్లాడండి.",
        "converting": "🔄 మీ మాటను టెక్స్ట్‌గా మారుస్తున్నాను...",
        "err_timeout": "⏱️ నాకు ఏమీ వినిపించలేదు. దయచేసి మళ్లీ ప్రయత్నించండి.",
        "err_unknown": "❌ క్షమించండి, మీ గొంతు నాకు అర్థం కాలేదు.",
        "err_request": "🌐 స్పీచ్ రికగ్నిషన్‌కు ఇంటర్నెట్ కనెక్షన్ అవసరం.",
        "err_mic": "❌ మైక్రోఫోన్ లోపం: {e}",

        "sv_title": "ఫారమ్ సేవ్",
        "sv_sub": "మీరు నింపిన సమాచారాన్ని సమీక్షించండి",
        "sv_none": "ఇంకా ఏ ఫారమ్ సమాచారం సేవ్ కాలేదు.",
        "sv_completed": "📋 పూర్తయిన సమాచారం",
        "sv_completed_sub": "అంతా బాగుందా? కింద మీ ఫారమ్‌ను డౌన్‌లోడ్ చేయండి.",
        "sv_not": "ఇవ్వలేదు",
        "sv_download": "⬇️ ఫారమ్ డౌన్‌లోడ్ చేయండి",

        "ft_sub": "స్మార్ట్ వాయిస్ ఆధారిత ఫారమ్ సిస్టమ్",
        "ft_built": "Python మరియు Streamlit తో ❤️ తో తయారు చేయబడింది"
    },

    # ------------------------------------------------- HINDI
    "Hindi": {
        "nav_home": "होम",
        "nav_upload": "फ़ॉर्म अपलोड करें",
        "nav_voice": "वॉइस असिस्टेंट",
        "nav_save": "फ़ॉर्म सेव करें",
        "nav_logout": "लॉगआउट",
        "sidebar_subtitle": "स्मार्ट वॉइस फ़ॉर्म असिस्टेंट",
        "ai_powered": "AI संचालित",
        "ai_tags": "आवाज़ • अनुवाद • फ़ॉर्म",
        "hello": "नमस्ते, {name}! 👋",

        "hero_subtitle": "स्मार्ट वॉइस-आधारित फ़ॉर्म असिस्टेंट",
        "hero_badge": "✨ फ़ॉर्म जल्दी भरें • स्वाभाविक रूप से बोलें • आसानी से सेव करें",
        "stat1": "भाषाएँ",
        "stat2": "बिना हाथ लगाए टाइपिंग",
        "stat3": "बोलना शुरू करने के लिए क्लिक",
        "stat4": "भरे जा सकने वाले फ़ॉर्म",
        "welcome_title": "VoiceForm AI में आपका स्वागत है 👋",
        "welcome_sub": "आसान और बुद्धिमान इंटरफ़ेस के साथ अपनी आवाज़ से डिजिटल फ़ॉर्म भरें।",
        "f1_title": "अपना फ़ॉर्म अपलोड करें",
        "f1_text": "अपना मौजूदा PDF या इमेज फ़ॉर्म अपलोड करें।",
        "f2_title": "भाषा चुनें",
        "f2_text": "वह भाषा चुनें जिसका आप उपयोग करना चाहते हैं।",
        "f3_title": "बोलें और भरें",
        "f3_text": "अपने उत्तर बोलें और वे अपने आप फ़ॉर्म में भर जाएँगे।",
        "how_title": "यह कैसे काम करता है 🚀",
        "how_sub": "खाली फ़ॉर्म से भरे हुए फ़ॉर्म तक चार आसान चरण।",
        "s1_t": "अपलोड", "s1_d": "अपना फ़ॉर्म अपलोड करें",
        "s2_t": "भाषा", "s2_d": "भाषा चुनें",
        "s3_t": "बोलें", "s3_d": "आवाज़ से उत्तर दें",
        "s4_t": "सेव", "s4_d": "अपना फ़ॉर्म सेव करें",
        "start_btn": "🚀 VoiceForm AI शुरू करें",

        "login_hero": "जारी रखने के लिए लॉगिन करें",
        "login_title": "स्वागत है! कृपया लॉगिन करें",
        "login_subtitle": "शुरू करने के लिए अपनी बुनियादी जानकारी दर्ज करें",
        "login_name": "👤 आपका नाम",
        "login_phone": "📱 फ़ोन नंबर",
        "login_btn": "🔐 लॉगिन",
        "login_err_name": "⚠️ कृपया अपना नाम दर्ज करें।",
        "login_err_phone": "⚠️ कृपया 10 अंकों का सही फ़ोन नंबर दर्ज करें।",
        "login_note": "🌐 पूरा ऐप आपकी चुनी हुई भाषा में दिखेगा।",

        "up_title": "अपना फ़ॉर्म अपलोड करें",
        "up_sub": "अपना फ़ॉर्म अपलोड करें और भाषा चुनें",
        "up_choose": "📁 अपना फ़ॉर्म चुनें",
        "up_lang": "🌐 अपनी भाषा चुनें",
        "up_ok": "✅ {file} अपलोड हो गया!",
        "up_preview": "📋 आपके फ़ॉर्म का पूर्वावलोकन",
        "up_start": "🎙️ वॉइस फ़ॉर्म शुरू करें",
        "up_fields": "🧾 अपने फ़ॉर्म में मौजूद फ़ील्ड चुनें",
        "up_custom": "➕ अपना फ़ील्ड जोड़ें (उदाहरण: आधार नंबर)",
        "up_custom_btn": "➕ फ़ील्ड जोड़ें",

        "v_title": "वॉइस असिस्टेंट",
        "v_sub": "अपना उत्तर बोलें और फ़ॉर्म भरें",
        "v_selected": "चुनी गई भाषा:",
        "v_hint": "किसी फ़ील्ड के बगल में चमकते माइक्रोफ़ोन बटन पर क्लिक करें और अपना उत्तर बोलें।",
        "v_progress": "📝 फ़ॉर्म की प्रगति",
        "v_fields": "{filled} / {total} फ़ील्ड",
        "v_personal": "👤 व्यक्तिगत जानकारी",
        "v_personal_sub": "आप सामान्य रूप से टाइप कर सकते हैं या हर फ़ील्ड भरने के लिए 🎙️ माइक्रोफ़ोन बटन का उपयोग कर सकते हैं।",
        "v_no_fields": "⚠️ कोई फ़ील्ड नहीं चुना गया। कृपया फ़ॉर्म अपलोड पेज पर अपने फ़ॉर्म के फ़ील्ड चुनें।",
        "tip_symbols": "💡 बोलने के सुझाव: @ के लिए “at the rate”, . के लिए “dot”, - के लिए “dash”, / के लिए “slash”, , के लिए “comma” बोलें — संख्याएँ अपने आप जुड़ जाती हैं।",
        "l_name": "👤 पूरा नाम",
        "l_father": "👨 पिता / अभिभावक का नाम",
        "l_mother": "👩 माता का नाम",
        "l_dob": "🎂 जन्म तिथि",
        "l_gender": "🧑 लिंग",
        "l_email": "📧 ईमेल पता",
        "l_phone": "📱 फ़ोन नंबर",
        "l_address": "🏠 पता",
        "l_city": "🌆 शहर",
        "l_state": "🗺️ राज्य",
        "l_pincode": "📮 पिन कोड",
        "l_country": "🌍 देश",
        "v_save": "💾 फ़ॉर्म सेव करें",
        "v_saved": "✅ आपका फ़ॉर्म सेव हो गया!",
        "listening": "🎙️ सुन रहा हूँ... कृपया अभी बोलें।",
        "converting": "🔄 आपकी आवाज़ को टेक्स्ट में बदल रहा हूँ...",
        "err_timeout": "⏱️ मुझे कुछ सुनाई नहीं दिया। कृपया फिर से कोशिश करें।",
        "err_unknown": "❌ क्षमा करें, मैं आपकी आवाज़ समझ नहीं पाया।",
        "err_request": "🌐 स्पीच रिकग्निशन के लिए इंटरनेट कनेक्शन चाहिए।",
        "err_mic": "❌ माइक्रोफ़ोन त्रुटि: {e}",

        "sv_title": "फ़ॉर्म सेव करें",
        "sv_sub": "अपनी भरी हुई जानकारी देखें",
        "sv_none": "अभी तक कोई फ़ॉर्म जानकारी सेव नहीं हुई है।",
        "sv_completed": "📋 भरी हुई जानकारी",
        "sv_completed_sub": "सब ठीक लग रहा है? नीचे अपना फ़ॉर्म डाउनलोड करें।",
        "sv_not": "उपलब्ध नहीं",
        "sv_download": "⬇️ फ़ॉर्म डाउनलोड करें",

        "ft_sub": "स्मार्ट वॉइस-आधारित फ़ॉर्म सिस्टम",
        "ft_built": "Python और Streamlit से ❤️ के साथ बनाया गया"
    },

    # ------------------------------------------------- TAMIL
    "Tamil": {
        "nav_home": "முகப்பு",
        "nav_upload": "படிவத்தைப் பதிவேற்று",
        "nav_voice": "குரல் உதவியாளர்",
        "nav_save": "படிவத்தைச் சேமி",
        "nav_logout": "வெளியேறு",
        "sidebar_subtitle": "ஸ்மார்ட் குரல் படிவ உதவியாளர்",
        "ai_powered": "AI இயக்கம்",
        "ai_tags": "குரல் • மொழிபெயர்ப்பு • படிவங்கள்",
        "hello": "வணக்கம், {name}! 👋",

        "hero_subtitle": "ஸ்மார்ட் குரல் அடிப்படையிலான படிவ உதவியாளர்",
        "hero_badge": "✨ படிவங்களை விரைவாக நிரப்புங்கள் • இயல்பாகப் பேசுங்கள் • எளிதாகச் சேமியுங்கள்",
        "stat1": "மொழிகள்",
        "stat2": "கை தட்டச்சு இல்லாமல்",
        "stat3": "பேசத் தொடங்க ஒரு கிளிக்",
        "stat4": "நிரப்பக்கூடிய படிவங்கள்",
        "welcome_title": "VoiceForm AI-க்கு வரவேற்கிறோம் 👋",
        "welcome_sub": "எளிய, அறிவார்ந்த இடைமுகத்துடன் உங்கள் குரலால் டிஜிட்டல் படிவங்களை நிரப்புங்கள்.",
        "f1_title": "உங்கள் படிவத்தைப் பதிவேற்றுங்கள்",
        "f1_text": "உங்களிடம் உள்ள PDF அல்லது படப் படிவத்தைப் பதிவேற்றுங்கள்.",
        "f2_title": "மொழியைத் தேர்ந்தெடுங்கள்",
        "f2_text": "நீங்கள் பயன்படுத்த விரும்பும் மொழியைத் தேர்ந்தெடுங்கள்.",
        "f3_title": "பேசுங்கள் & நிரப்புங்கள்",
        "f3_text": "உங்கள் பதில்களைப் பேசுங்கள், அவை தானாகவே படிவத்தில் நிரப்பப்படும்.",
        "how_title": "இது எப்படி வேலை செய்கிறது 🚀",
        "how_sub": "வெற்றுப் படிவத்திலிருந்து நிரப்பிய படிவம் வரை நான்கு எளிய படிகள்.",
        "s1_t": "பதிவேற்றம்", "s1_d": "உங்கள் படிவத்தைப் பதிவேற்றுங்கள்",
        "s2_t": "மொழி", "s2_d": "மொழியைத் தேர்ந்தெடுங்கள்",
        "s3_t": "பேசுங்கள்", "s3_d": "குரலால் பதிலளியுங்கள்",
        "s4_t": "சேமி", "s4_d": "உங்கள் படிவத்தைச் சேமியுங்கள்",
        "start_btn": "🚀 VoiceForm AI-ஐத் தொடங்குங்கள்",

        "login_hero": "தொடர உள்நுழையுங்கள்",
        "login_title": "வரவேற்கிறோம்! தயவுசெய்து உள்நுழையுங்கள்",
        "login_subtitle": "தொடங்க உங்கள் அடிப்படை விவரங்களை உள்ளிடுங்கள்",
        "login_name": "👤 உங்கள் பெயர்",
        "login_phone": "📱 தொலைபேசி எண்",
        "login_btn": "🔐 உள்நுழை",
        "login_err_name": "⚠️ தயவுசெய்து உங்கள் பெயரை உள்ளிடுங்கள்.",
        "login_err_phone": "⚠️ தயவுசெய்து சரியான 10 இலக்க தொலைபேசி எண்ணை உள்ளிடுங்கள்.",
        "login_note": "🌐 முழு செயலியும் நீங்கள் தேர்ந்தெடுத்த மொழியில் தெரியும்.",

        "up_title": "உங்கள் படிவத்தைப் பதிவேற்றுங்கள்",
        "up_sub": "உங்கள் படிவத்தைப் பதிவேற்றி மொழியைத் தேர்ந்தெடுங்கள்",
        "up_choose": "📁 உங்கள் படிவத்தைத் தேர்ந்தெடுங்கள்",
        "up_lang": "🌐 உங்கள் மொழியைத் தேர்ந்தெடுங்கள்",
        "up_ok": "✅ {file} பதிவேற்றப்பட்டது!",
        "up_preview": "📋 உங்கள் படிவ முன்னோட்டம்",
        "up_start": "🎙️ குரல் படிவத்தைத் தொடங்குங்கள்",
        "up_fields": "🧾 உங்கள் படிவத்தில் உள்ள புலங்களைத் தேர்ந்தெடுங்கள்",
        "up_custom": "➕ உங்கள் சொந்தப் புலத்தைச் சேர்க்கவும் (எ.கா: ஆதார் எண்)",
        "up_custom_btn": "➕ புலத்தைச் சேர்",

        "v_title": "குரல் உதவியாளர்",
        "v_sub": "உங்கள் பதிலைப் பேசி படிவத்தை நிரப்புங்கள்",
        "v_selected": "தேர்ந்தெடுத்த மொழி:",
        "v_hint": "ஒரு புலத்தின் அருகில் உள்ள ஒளிரும் மைக்ரோஃபோன் பொத்தானைக் கிளிக் செய்து உங்கள் பதிலைப் பேசுங்கள்.",
        "v_progress": "📝 படிவ முன்னேற்றம்",
        "v_fields": "{filled} / {total} புலங்கள்",
        "v_personal": "👤 தனிப்பட்ட தகவல்",
        "v_personal_sub": "நீங்கள் வழக்கம்போல் தட்டச்சு செய்யலாம் அல்லது ஒவ்வொரு புலத்தையும் நிரப்ப 🎙️ மைக்ரோஃபோன் பொத்தான்களைப் பயன்படுத்தலாம்.",
        "v_no_fields": "⚠️ எந்தப் புலமும் தேர்ந்தெடுக்கப்படவில்லை. படிவப் பதிவேற்றப் பக்கத்தில் உங்கள் படிவத்தின் புலங்களைத் தேர்ந்தெடுங்கள்.",
        "tip_symbols": "💡 பேசும் குறிப்புகள்: @ க்கு “at the rate”, . க்கு “dot”, - க்கு “dash”, / க்கு “slash”, , க்கு “comma” என்று சொல்லுங்கள் — எண்கள் தானாக இணைக்கப்படும்.",
        "l_name": "👤 முழு பெயர்",
        "l_father": "👨 தந்தை / பாதுகாவலர் பெயர்",
        "l_mother": "👩 தாயின் பெயர்",
        "l_dob": "🎂 பிறந்த தேதி",
        "l_gender": "🧑 பாலினம்",
        "l_email": "📧 மின்னஞ்சல் முகவரி",
        "l_phone": "📱 தொலைபேசி எண்",
        "l_address": "🏠 முகவரி",
        "l_city": "🌆 நகரம்",
        "l_state": "🗺️ மாநிலம்",
        "l_pincode": "📮 அஞ்சல் குறியீடு",
        "l_country": "🌍 நாடு",
        "v_save": "💾 படிவத்தைச் சேமி",
        "v_saved": "✅ உங்கள் படிவம் சேமிக்கப்பட்டது!",
        "listening": "🎙️ கேட்டுக்கொண்டிருக்கிறேன்... தயவுசெய்து இப்போது பேசுங்கள்.",
        "converting": "🔄 உங்கள் பேச்சை உரையாக மாற்றுகிறேன்...",
        "err_timeout": "⏱️ எனக்கு எதுவும் கேட்கவில்லை. தயவுசெய்து மீண்டும் முயலுங்கள்.",
        "err_unknown": "❌ மன்னிக்கவும், உங்கள் குரல் எனக்குப் புரியவில்லை.",
        "err_request": "🌐 பேச்சு அறிதலுக்கு இணைய இணைப்பு தேவை.",
        "err_mic": "❌ மைக்ரோஃபோன் பிழை: {e}",

        "sv_title": "படிவத்தைச் சேமி",
        "sv_sub": "நிரப்பிய தகவலைச் சரிபார்க்கவும்",
        "sv_none": "இதுவரை எந்தப் படிவத் தகவலும் சேமிக்கப்படவில்லை.",
        "sv_completed": "📋 நிரப்பிய தகவல்",
        "sv_completed_sub": "எல்லாம் சரியாக இருக்கிறதா? கீழே உங்கள் படிவத்தைப் பதிவிறக்குங்கள்.",
        "sv_not": "வழங்கப்படவில்லை",
        "sv_download": "⬇️ படிவத்தைப் பதிவிறக்கு",

        "ft_sub": "ஸ்மார்ட் குரல் அடிப்படையிலான படிவ அமைப்பு",
        "ft_built": "Python மற்றும் Streamlit கொண்டு ❤️ உடன் உருவாக்கப்பட்டது"
    },

    # ------------------------------------------------- KANNADA
    "Kannada": {
        "nav_home": "ಮುಖಪುಟ",
        "nav_upload": "ಫಾರ್ಮ್ ಅಪ್‌ಲೋಡ್",
        "nav_voice": "ವಾಯ್ಸ್ ಅಸಿಸ್ಟೆಂಟ್",
        "nav_save": "ಫಾರ್ಮ್ ಉಳಿಸಿ",
        "nav_logout": "ಲಾಗ್‌ಔಟ್",
        "sidebar_subtitle": "ಸ್ಮಾರ್ಟ್ ವಾಯ್ಸ್ ಫಾರ್ಮ್ ಅಸಿಸ್ಟೆಂಟ್",
        "ai_powered": "AI ಚಾಲಿತ",
        "ai_tags": "ಧ್ವನಿ • ಅನುವಾದ • ಫಾರ್ಮ್‌ಗಳು",
        "hello": "ನಮಸ್ಕಾರ, {name}! 👋",

        "hero_subtitle": "ಸ್ಮಾರ್ಟ್ ಧ್ವನಿ ಆಧಾರಿತ ಫಾರ್ಮ್ ಅಸಿಸ್ಟೆಂಟ್",
        "hero_badge": "✨ ಫಾರ್ಮ್‌ಗಳನ್ನು ವೇಗವಾಗಿ ತುಂಬಿ • ಸಹಜವಾಗಿ ಮಾತನಾಡಿ • ಸುಲಭವಾಗಿ ಉಳಿಸಿ",
        "stat1": "ಭಾಷೆಗಳು",
        "stat2": "ಕೈಯಿಂದ ಟೈಪ್ ಮಾಡದೆ",
        "stat3": "ಮಾತನಾಡಲು ಪ್ರಾರಂಭಿಸಲು ಕ್ಲಿಕ್",
        "stat4": "ತುಂಬಬಹುದಾದ ಫಾರ್ಮ್‌ಗಳು",
        "welcome_title": "VoiceForm AI ಗೆ ಸ್ವಾಗತ 👋",
        "welcome_sub": "ಸುಲಭ ಮತ್ತು ಬುದ್ಧಿವಂತ ಇಂಟರ್‌ಫೇಸ್‌ನೊಂದಿಗೆ ನಿಮ್ಮ ಧ್ವನಿಯಿಂದ ಡಿಜಿಟಲ್ ಫಾರ್ಮ್‌ಗಳನ್ನು ತುಂಬಿ.",
        "f1_title": "ನಿಮ್ಮ ಫಾರ್ಮ್ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
        "f1_text": "ನಿಮ್ಮ ಅಸ್ತಿತ್ವದಲ್ಲಿರುವ PDF ಅಥವಾ ಚಿತ್ರ ಫಾರ್ಮ್ ಅನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ.",
        "f2_title": "ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "f2_text": "ನೀವು ಬಳಸಲು ಬಯಸುವ ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ.",
        "f3_title": "ಮಾತನಾಡಿ & ತುಂಬಿ",
        "f3_text": "ನಿಮ್ಮ ಉತ್ತರಗಳನ್ನು ಹೇಳಿ, ಅವು ತಾನಾಗಿಯೇ ಫಾರ್ಮ್‌ನಲ್ಲಿ ತುಂಬುತ್ತವೆ.",
        "how_title": "ಇದು ಹೇಗೆ ಕೆಲಸ ಮಾಡುತ್ತದೆ 🚀",
        "how_sub": "ಖಾಲಿ ಫಾರ್ಮ್‌ನಿಂದ ಪೂರ್ಣಗೊಂಡ ಫಾರ್ಮ್‌ವರೆಗೆ ನಾಲ್ಕು ಸರಳ ಹಂತಗಳು.",
        "s1_t": "ಅಪ್‌ಲೋಡ್", "s1_d": "ನಿಮ್ಮ ಫಾರ್ಮ್ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
        "s2_t": "ಭಾಷೆ", "s2_d": "ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "s3_t": "ಮಾತನಾಡಿ", "s3_d": "ಧ್ವನಿಯಿಂದ ಉತ್ತರಿಸಿ",
        "s4_t": "ಉಳಿಸಿ", "s4_d": "ನಿಮ್ಮ ಫಾರ್ಮ್ ಉಳಿಸಿ",
        "start_btn": "🚀 VoiceForm AI ಪ್ರಾರಂಭಿಸಿ",

        "login_hero": "ಮುಂದುವರಿಯಲು ಲಾಗಿನ್ ಮಾಡಿ",
        "login_title": "ಸ್ವಾಗತ! ದಯವಿಟ್ಟು ಲಾಗಿನ್ ಮಾಡಿ",
        "login_subtitle": "ಪ್ರಾರಂಭಿಸಲು ನಿಮ್ಮ ಮೂಲ ವಿವರಗಳನ್ನು ನಮೂದಿಸಿ",
        "login_name": "👤 ನಿಮ್ಮ ಹೆಸರು",
        "login_phone": "📱 ಫೋನ್ ಸಂಖ್ಯೆ",
        "login_btn": "🔐 ಲಾಗಿನ್",
        "login_err_name": "⚠️ ದಯವಿಟ್ಟು ನಿಮ್ಮ ಹೆಸರನ್ನು ನಮೂದಿಸಿ.",
        "login_err_phone": "⚠️ ದಯವಿಟ್ಟು ಸರಿಯಾದ 10 ಅಂಕಿಗಳ ಫೋನ್ ಸಂಖ್ಯೆಯನ್ನು ನಮೂದಿಸಿ.",
        "login_note": "🌐 ಇಡೀ ಅಪ್ಲಿಕೇಶನ್ ನೀವು ಆಯ್ಕೆ ಮಾಡಿದ ಭಾಷೆಯಲ್ಲಿ ಕಾಣಿಸುತ್ತದೆ.",

        "up_title": "ನಿಮ್ಮ ಫಾರ್ಮ್ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
        "up_sub": "ನಿಮ್ಮ ಫಾರ್ಮ್ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ ಮತ್ತು ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "up_choose": "📁 ನಿಮ್ಮ ಫಾರ್ಮ್ ಆಯ್ಕೆಮಾಡಿ",
        "up_lang": "🌐 ನಿಮ್ಮ ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "up_ok": "✅ {file} ಅಪ್‌ಲೋಡ್ ಆಗಿದೆ!",
        "up_preview": "📋 ನಿಮ್ಮ ಫಾರ್ಮ್ ಪೂರ್ವವೀಕ್ಷಣೆ",
        "up_start": "🎙️ ವಾಯ್ಸ್ ಫಾರ್ಮ್ ಪ್ರಾರಂಭಿಸಿ",
        "up_fields": "🧾 ನಿಮ್ಮ ಫಾರ್ಮ್‌ನಲ್ಲಿರುವ ಕ್ಷೇತ್ರಗಳನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "up_custom": "➕ ನಿಮ್ಮದೇ ಕ್ಷೇತ್ರವನ್ನು ಸೇರಿಸಿ (ಉದಾ: ಆಧಾರ್ ಸಂಖ್ಯೆ)",
        "up_custom_btn": "➕ ಕ್ಷೇತ್ರ ಸೇರಿಸಿ",

        "v_title": "ವಾಯ್ಸ್ ಅಸಿಸ್ಟೆಂಟ್",
        "v_sub": "ನಿಮ್ಮ ಉತ್ತರ ಹೇಳಿ ಫಾರ್ಮ್ ತುಂಬಿ",
        "v_selected": "ಆಯ್ಕೆ ಮಾಡಿದ ಭಾಷೆ:",
        "v_hint": "ಕ್ಷೇತ್ರದ ಪಕ್ಕದಲ್ಲಿರುವ ಹೊಳೆಯುವ ಮೈಕ್ರೊಫೋನ್ ಬಟನ್ ಕ್ಲಿಕ್ ಮಾಡಿ ಮತ್ತು ನಿಮ್ಮ ಉತ್ತರ ಹೇಳಿ.",
        "v_progress": "📝 ಫಾರ್ಮ್ ಪ್ರಗತಿ",
        "v_fields": "{filled} / {total} ಕ್ಷೇತ್ರಗಳು",
        "v_personal": "👤 ವೈಯಕ್ತಿಕ ಮಾಹಿತಿ",
        "v_personal_sub": "ನೀವು ಸಾಮಾನ್ಯವಾಗಿ ಟೈಪ್ ಮಾಡಬಹುದು ಅಥವಾ ಪ್ರತಿ ಕ್ಷೇತ್ರ ತುಂಬಲು 🎙️ ಮೈಕ್ರೊಫೋನ್ ಬಟನ್‌ಗಳನ್ನು ಬಳಸಬಹುದು.",
        "v_no_fields": "⚠️ ಯಾವುದೇ ಕ್ಷೇತ್ರ ಆಯ್ಕೆಮಾಡಿಲ್ಲ. ದಯವಿಟ್ಟು ಫಾರ್ಮ್ ಅಪ್‌ಲೋಡ್ ಪುಟದಲ್ಲಿ ನಿಮ್ಮ ಫಾರ್ಮ್‌ನ ಕ್ಷೇತ್ರಗಳನ್ನು ಆಯ್ಕೆಮಾಡಿ.",
        "tip_symbols": "💡 ಮಾತನಾಡುವ ಸಲಹೆಗಳು: @ ಗೆ “at the rate”, . ಗೆ “dot”, - ಗೆ “dash”, / ಗೆ “slash”, , ಗೆ “comma” ಎಂದು ಹೇಳಿ — ಸಂಖ್ಯೆಗಳು ತಾನಾಗಿ ಸೇರುತ್ತವೆ.",
        "l_name": "👤 ಪೂರ್ಣ ಹೆಸರು",
        "l_father": "👨 ತಂದೆ / ಪಾಲಕರ ಹೆಸರು",
        "l_mother": "👩 ತಾಯಿಯ ಹೆಸರು",
        "l_dob": "🎂 ಜನ್ಮ ದಿನಾಂಕ",
        "l_gender": "🧑 ಲಿಂಗ",
        "l_email": "📧 ಇಮೇಲ್ ವಿಳಾಸ",
        "l_phone": "📱 ಫೋನ್ ಸಂಖ್ಯೆ",
        "l_address": "🏠 ವಿಳಾಸ",
        "l_city": "🌆 ನಗರ",
        "l_state": "🗺️ ರಾಜ್ಯ",
        "l_pincode": "📮 ಪಿನ್ ಕೋಡ್",
        "l_country": "🌍 ದೇಶ",
        "v_save": "💾 ಫಾರ್ಮ್ ಉಳಿಸಿ",
        "v_saved": "✅ ನಿಮ್ಮ ಫಾರ್ಮ್ ಉಳಿಸಲಾಗಿದೆ!",
        "listening": "🎙️ ಕೇಳುತ್ತಿದ್ದೇನೆ... ದಯವಿಟ್ಟು ಈಗ ಮಾತನಾಡಿ.",
        "converting": "🔄 ನಿಮ್ಮ ಮಾತನ್ನು ಪಠ್ಯಕ್ಕೆ ಪರಿವರ್ತಿಸಲಾಗುತ್ತಿದೆ...",
        "err_timeout": "⏱️ ನನಗೆ ಏನೂ ಕೇಳಿಸಲಿಲ್ಲ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
        "err_unknown": "❌ ಕ್ಷಮಿಸಿ, ನಿಮ್ಮ ಧ್ವನಿ ನನಗೆ ಅರ್ಥವಾಗಲಿಲ್ಲ.",
        "err_request": "🌐 ಧ್ವನಿ ಗುರುತಿಸುವಿಕೆಗೆ ಇಂಟರ್ನೆಟ್ ಸಂಪರ್ಕ ಬೇಕು.",
        "err_mic": "❌ ಮೈಕ್ರೊಫೋನ್ ದೋಷ: {e}",

        "sv_title": "ಫಾರ್ಮ್ ಉಳಿಸಿ",
        "sv_sub": "ನೀವು ತುಂಬಿದ ಮಾಹಿತಿಯನ್ನು ಪರಿಶೀಲಿಸಿ",
        "sv_none": "ಇನ್ನೂ ಯಾವುದೇ ಫಾರ್ಮ್ ಮಾಹಿತಿ ಉಳಿಸಿಲ್ಲ.",
        "sv_completed": "📋 ಪೂರ್ಣಗೊಂಡ ಮಾಹಿತಿ",
        "sv_completed_sub": "ಎಲ್ಲವೂ ಸರಿಯಾಗಿದೆಯೇ? ಕೆಳಗೆ ನಿಮ್ಮ ಫಾರ್ಮ್ ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ.",
        "sv_not": "ನೀಡಿಲ್ಲ",
        "sv_download": "⬇️ ಫಾರ್ಮ್ ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ",

        "ft_sub": "ಸ್ಮಾರ್ಟ್ ಧ್ವನಿ ಆಧಾರಿತ ಫಾರ್ಮ್ ವ್ಯವಸ್ಥೆ",
        "ft_built": "Python ಮತ್ತು Streamlit ಬಳಸಿ ❤️ ಯಿಂದ ನಿರ್ಮಿಸಲಾಗಿದೆ"
    },

    # ------------------------------------------------- MALAYALAM
    "Malayalam": {
        "nav_home": "ഹോം",
        "nav_upload": "ഫോം അപ്‌ലോഡ്",
        "nav_voice": "വോയ്‌സ് അസിസ്റ്റന്റ്",
        "nav_save": "ഫോം സേവ് ചെയ്യുക",
        "nav_logout": "ലോഗൗട്ട്",
        "sidebar_subtitle": "സ്മാർട്ട് വോയ്‌സ് ഫോം അസിസ്റ്റന്റ്",
        "ai_powered": "AI അധിഷ്ഠിതം",
        "ai_tags": "ശബ്ദം • വിവർത്തനം • ഫോമുകൾ",
        "hello": "നമസ്കാരം, {name}! 👋",

        "hero_subtitle": "സ്മാർട്ട് ശബ്ദ അധിഷ്ഠിത ഫോം അസിസ്റ്റന്റ്",
        "hero_badge": "✨ ഫോമുകൾ വേഗത്തിൽ പൂരിപ്പിക്കൂ • സ്വാഭാവികമായി സംസാരിക്കൂ • എളുപ്പത്തിൽ സേവ് ചെയ്യൂ",
        "stat1": "ഭാഷകൾ",
        "stat2": "കൈകൊണ്ട് ടൈപ്പ് ചെയ്യാതെ",
        "stat3": "സംസാരിച്ചു തുടങ്ങാൻ ഒരു ക്ലിക്ക്",
        "stat4": "പൂരിപ്പിക്കാവുന്ന ഫോമുകൾ",
        "welcome_title": "VoiceForm AI-യിലേക്ക് സ്വാഗതം 👋",
        "welcome_sub": "എളുപ്പവും ബുദ്ധിപരവുമായ ഇന്റർഫേസിലൂടെ നിങ്ങളുടെ ശബ്ദം ഉപയോഗിച്ച് ഡിജിറ്റൽ ഫോമുകൾ പൂരിപ്പിക്കൂ.",
        "f1_title": "നിങ്ങളുടെ ഫോം അപ്‌ലോഡ് ചെയ്യൂ",
        "f1_text": "നിങ്ങളുടെ നിലവിലുള്ള PDF അല്ലെങ്കിൽ ചിത്ര ഫോം അപ്‌ലോഡ് ചെയ്യൂ.",
        "f2_title": "ഭാഷ തിരഞ്ഞെടുക്കൂ",
        "f2_text": "നിങ്ങൾ ഉപയോഗിക്കാൻ ആഗ്രഹിക്കുന്ന ഭാഷ തിരഞ്ഞെടുക്കൂ.",
        "f3_title": "സംസാരിക്കൂ & പൂരിപ്പിക്കൂ",
        "f3_text": "നിങ്ങളുടെ ഉത്തരങ്ങൾ പറയൂ, അവ സ്വയം ഫോമിൽ നിറയും.",
        "how_title": "ഇത് എങ്ങനെ പ്രവർത്തിക്കുന്നു 🚀",
        "how_sub": "ശൂന്യമായ ഫോമിൽ നിന്ന് പൂർത്തിയായ ഫോമിലേക്ക് നാല് ലളിത ഘട്ടങ്ങൾ.",
        "s1_t": "അപ്‌ലോഡ്", "s1_d": "നിങ്ങളുടെ ഫോം അപ്‌ലോഡ് ചെയ്യൂ",
        "s2_t": "ഭാഷ", "s2_d": "ഭാഷ തിരഞ്ഞെടുക്കൂ",
        "s3_t": "സംസാരിക്കൂ", "s3_d": "ശബ്ദത്തിലൂടെ ഉത്തരം നൽകൂ",
        "s4_t": "സേവ്", "s4_d": "നിങ്ങളുടെ ഫോം സേവ് ചെയ്യൂ",
        "start_btn": "🚀 VoiceForm AI തുടങ്ങൂ",

        "login_hero": "തുടരാൻ ലോഗിൻ ചെയ്യൂ",
        "login_title": "സ്വാഗതം! ദയവായി ലോഗിൻ ചെയ്യൂ",
        "login_subtitle": "തുടങ്ങാൻ നിങ്ങളുടെ അടിസ്ഥാന വിവരങ്ങൾ നൽകൂ",
        "login_name": "👤 നിങ്ങളുടെ പേര്",
        "login_phone": "📱 ഫോൺ നമ്പർ",
        "login_btn": "🔐 ലോഗിൻ",
        "login_err_name": "⚠️ ദയവായി നിങ്ങളുടെ പേര് നൽകൂ.",
        "login_err_phone": "⚠️ ദയവായി ശരിയായ 10 അക്ക ഫോൺ നമ്പർ നൽകൂ.",
        "login_note": "🌐 ആപ്പ് മുഴുവൻ നിങ്ങൾ തിരഞ്ഞെടുത്ത ഭാഷയിൽ കാണിക്കും.",

        "up_title": "നിങ്ങളുടെ ഫോം അപ്‌ലോഡ് ചെയ്യൂ",
        "up_sub": "നിങ്ങളുടെ ഫോം അപ്‌ലോഡ് ചെയ്ത് ഭാഷ തിരഞ്ഞെടുക്കൂ",
        "up_choose": "📁 നിങ്ങളുടെ ഫോം തിരഞ്ഞെടുക്കൂ",
        "up_lang": "🌐 നിങ്ങളുടെ ഭാഷ തിരഞ്ഞെടുക്കൂ",
        "up_ok": "✅ {file} അപ്‌ലോഡ് ചെയ്തു!",
        "up_preview": "📋 നിങ്ങളുടെ ഫോം പ്രിവ്യൂ",
        "up_start": "🎙️ വോയ്‌സ് ഫോം തുടങ്ങൂ",
        "up_fields": "🧾 നിങ്ങളുടെ ഫോമിലുള്ള ഫീൽഡുകൾ തിരഞ്ഞെടുക്കൂ",
        "up_custom": "➕ നിങ്ങളുടെ സ്വന്തം ഫീൽഡ് ചേർക്കൂ (ഉദാ: ആധാർ നമ്പർ)",
        "up_custom_btn": "➕ ഫീൽഡ് ചേർക്കൂ",

        "v_title": "വോയ്‌സ് അസിസ്റ്റന്റ്",
        "v_sub": "നിങ്ങളുടെ ഉത്തരം പറഞ്ഞ് ഫോം പൂരിപ്പിക്കൂ",
        "v_selected": "തിരഞ്ഞെടുത്ത ഭാഷ:",
        "v_hint": "ഒരു ഫീൽഡിന് അരികിലുള്ള തിളങ്ങുന്ന മൈക്രോഫോൺ ബട്ടണിൽ ക്ലിക്ക് ചെയ്ത് നിങ്ങളുടെ ഉത്തരം പറയൂ.",
        "v_progress": "📝 ഫോം പുരോഗതി",
        "v_fields": "{filled} / {total} ഫീൽഡുകൾ",
        "v_personal": "👤 വ്യക്തിഗത വിവരങ്ങൾ",
        "v_personal_sub": "നിങ്ങൾക്ക് സാധാരണ പോലെ ടൈപ്പ് ചെയ്യാം, അല്ലെങ്കിൽ ഓരോ ഫീൽഡും പൂരിപ്പിക്കാൻ 🎙️ മൈക്രോഫോൺ ബട്ടണുകൾ ഉപയോഗിക്കാം.",
        "v_no_fields": "⚠️ ഒരു ഫീൽഡും തിരഞ്ഞെടുത്തിട്ടില്ല. ദയവായി ഫോം അപ്‌ലോഡ് പേജിൽ നിങ്ങളുടെ ഫോമിലെ ഫീൽഡുകൾ തിരഞ്ഞെടുക്കൂ.",
        "tip_symbols": "💡 സംസാര നിർദ്ദേശങ്ങൾ: @ ന് “at the rate”, . ന് “dot”, - ന് “dash”, / ന് “slash”, , ന് “comma” എന്ന് പറയൂ — അക്കങ്ങൾ സ്വയം ചേരും.",
        "l_name": "👤 മുഴുവൻ പേര്",
        "l_father": "👨 പിതാവിന്റെ / രക്ഷിതാവിന്റെ പേര്",
        "l_mother": "👩 അമ്മയുടെ പേര്",
        "l_dob": "🎂 ജനനത്തീയതി",
        "l_gender": "🧑 ലിംഗം",
        "l_email": "📧 ഇമെയിൽ വിലാസം",
        "l_phone": "📱 ഫോൺ നമ്പർ",
        "l_address": "🏠 വിലാസം",
        "l_city": "🌆 നഗരം",
        "l_state": "🗺️ സംസ്ഥാനം",
        "l_pincode": "📮 പിൻ കോഡ്",
        "l_country": "🌍 രാജ്യം",
        "v_save": "💾 ഫോം സേവ് ചെയ്യുക",
        "v_saved": "✅ നിങ്ങളുടെ ഫോം സേവ് ചെയ്തു!",
        "listening": "🎙️ ശ്രദ്ധിക്കുന്നു... ദയവായി ഇപ്പോൾ സംസാരിക്കൂ.",
        "converting": "🔄 നിങ്ങളുടെ സംസാരം ടെക്സ്റ്റാക്കി മാറ്റുന്നു...",
        "err_timeout": "⏱️ എനിക്ക് ഒന്നും കേൾക്കാനായില്ല. ദയവായി വീണ്ടും ശ്രമിക്കൂ.",
        "err_unknown": "❌ ക്ഷമിക്കണം, നിങ്ങളുടെ ശബ്ദം എനിക്ക് മനസ്സിലായില്ല.",
        "err_request": "🌐 സ്പീച്ച് റെക്കഗ്നിഷന് ഇന്റർനെറ്റ് കണക്ഷൻ ആവശ്യമാണ്.",
        "err_mic": "❌ മൈക്രോഫോൺ പിശക്: {e}",

        "sv_title": "ഫോം സേവ് ചെയ്യുക",
        "sv_sub": "പൂരിപ്പിച്ച വിവരങ്ങൾ പരിശോധിക്കൂ",
        "sv_none": "ഇതുവരെ ഫോം വിവരങ്ങളൊന്നും സേവ് ചെയ്തിട്ടില്ല.",
        "sv_completed": "📋 പൂർത്തിയാക്കിയ വിവരങ്ങൾ",
        "sv_completed_sub": "എല്ലാം ശരിയാണോ? താഴെ നിങ്ങളുടെ ഫോം ഡൗൺലോഡ് ചെയ്യൂ.",
        "sv_not": "നൽകിയിട്ടില്ല",
        "sv_download": "⬇️ ഫോം ഡൗൺലോഡ് ചെയ്യൂ",

        "ft_sub": "സ്മാർട്ട് ശബ്ദ അധിഷ്ഠിത ഫോം സിസ്റ്റം",
        "ft_built": "Python, Streamlit എന്നിവ ഉപയോഗിച്ച് ❤️ ഓടെ നിർമ്മിച്ചത്"
    }
}


def t(key, **kwargs):
    """Return text in the currently selected language."""

    lang = st.session_state.get("lang", "English")

    text = TR.get(lang, {}).get(key) or TR["English"][key]

    return text.format(**kwargs) if kwargs else text


# =========================================================
# SPOKEN TEXT CLEANING  (symbols, numbers, email, DOB)
# =========================================================

# Native digits -> 0-9  (Hindi, Telugu, Tamil, Kannada, Malayalam)
NATIVE_DIGITS = str.maketrans(
    "०१२३४५६७८९" "౦౧౨౩౪౫౬౭౮౯" "௦௧௨௩௪௫௬௭௮௯" "೦೧೨೩೪೫೬೭೮೯" "൦൧൨൩൪൫൬൭൮൯",
    "0123456789" * 5
)

# Multi-word spoken symbols in regional languages
SYMBOL_PHRASES_NATIVE = [
    ("एट द रेट", "@"), ("ऐट द रेट", "@"),
    ("ఎట్ ది రేట్", "@"), ("అట్ ది రేట్", "@"),
    ("அட் தி ரேட்", "@"),
    ("ಎಟ್ ದಿ ರೇಟ್", "@"),
    ("അറ്റ് ദി റേറ്റ്", "@"),
    ("फुल स्टॉप", "."), ("ఫుల్ స్టాప్", ".")
]

# English spoken symbols (case-insensitive, longest first)
SYMBOL_PHRASES_EN = [
    (r"\bat the rate of\b", "@"),
    (r"\bat the rate\b", "@"),
    (r"\bat rate\b", "@"),
    (r"\bat sign\b", "@"),
    (r"\bfull stop\b", "."),
    (r"\bunder ?score\b", "_"),
    (r"\bhyphen\b", "-"),
    (r"\bdash\b", "-"),
    (r"\bminus\b", "-"),
    (r"\bforward slash\b", "/"),
    (r"\bslash\b", "/"),
    (r"\bhash ?tag\b", "#"),
    (r"\bhash\b", "#"),
    (r"\bpound sign\b", "#"),
    (r"\bcomma\b", ","),
    (r"\bdot\b", "."),
    (r"\bplus\b", "+"),
    (r"\bopen bracket\b", "("),
    (r"\bclose bracket\b", ")")
]

# Single spoken symbol words in regional languages
SYMBOL_WORDS = {
    # Hindi
    "डैश": "-", "डेश": "-", "हाइफन": "-", "हाइफ़न": "-",
    "स्लैश": "/", "कॉमा": ",", "कोमा": ",", "डॉट": ".", "डाट": ".",
    "अंडरस्कोर": "_", "हैश": "#",
    # Telugu
    "డాష్": "-", "హైఫన్": "-", "స్లాష్": "/", "కామా": ",", "డాట్": ".",
    # Tamil
    "டேஷ்": "-", "ஹைபன்": "-", "ஸ்லாஷ்": "/", "கமா": ",", "டாட்": ".",
    # Kannada
    "ಡ್ಯಾಶ್": "-", "ಹೈಫನ್": "-", "ಸ್ಲ್ಯಾಶ್": "/", "ಕಾಮಾ": ",", "ಡಾಟ್": ".",
    # Malayalam
    "ഡാഷ്": "-", "ഹൈഫൺ": "-", "സ്ലാഷ്": "/", "കോമ": ",", "ഡോട്ട്": "."
}

# Single words meaning "@"  (used ONLY inside the email field)
AT_WORDS = {"at", "एट", "ऐट", "ఎట్", "అట్", "அட்", "ಎಟ್", "അറ്റ്"}

NUMBER_WORDS = {
    # English
    "zero": "0", "oh": "0", "one": "1", "two": "2", "three": "3",
    "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8",
    "nine": "9",
    # Hindi
    "शून्य": "0", "एक": "1", "दो": "2", "तीन": "3", "चार": "4",
    "पांच": "5", "पाँच": "5", "छह": "6", "छः": "6", "छे": "6",
    "सात": "7", "आठ": "8", "नौ": "9",
    # Telugu
    "సున్నా": "0", "ఒకటి": "1", "రెండు": "2", "మూడు": "3", "నాలుగు": "4",
    "ఐదు": "5", "ఆరు": "6", "ఏడు": "7", "ఎనిమిది": "8", "తొమ్మిది": "9",
    # Tamil
    "பூஜ்யம்": "0", "ஒன்று": "1", "இரண்டு": "2", "மூன்று": "3",
    "நான்கு": "4", "ஐந்து": "5", "ஆறு": "6", "ஏழு": "7", "எட்டு": "8",
    "ஒன்பது": "9",
    # Kannada
    "ಸೊನ್ನೆ": "0", "ಒಂದು": "1", "ಎರಡು": "2", "ಮೂರು": "3", "ನಾಲ್ಕು": "4",
    "ಐದು": "5", "ಆರು": "6", "ಏಳು": "7", "ಎಂಟು": "8", "ಒಂಬತ್ತು": "9",
    # Malayalam
    "പൂജ്യം": "0", "ഒന്ന്": "1", "രണ്ട്": "2", "മൂന്ന്": "3", "നാല്": "4",
    "അഞ്ച്": "5", "ആറ്": "6", "ഏഴ്": "7", "എട്ട്": "8", "ഒമ്പത്": "9"
}

# Words the recognizer often writes instead of digits (phone / PIN only)
PHONE_HOMOPHONES = {"to": "2", "too": "2", "for": "4", "won": "1", "ate": "8"}

MONTHS = {
    "january": 1, "jan": 1, "february": 2, "feb": 2, "march": 3, "mar": 3,
    "april": 4, "apr": 4, "may": 5, "june": 6, "jun": 6, "july": 7,
    "jul": 7, "august": 8, "aug": 8, "september": 9, "sep": 9, "sept": 9,
    "october": 10, "oct": 10, "november": 11, "nov": 11,
    "december": 12, "dec": 12
}

EMAIL_PROVIDERS = r"(gmail|yahoo|outlook|hotmail|rediffmail|icloud)\."


def apply_symbols(text):
    """Turn spoken words like 'dash' / 'at the rate' into symbols."""

    for phrase, symbol in SYMBOL_PHRASES_NATIVE:
        text = text.replace(phrase, f" {symbol} ")

    for pattern, symbol in SYMBOL_PHRASES_EN:
        text = re.sub(pattern, f" {symbol} ", text, flags=re.IGNORECASE)

    words = [
        SYMBOL_WORDS.get(word.strip(".,"), word)
        for word in text.split()
    ]

    return " ".join(words)


def tidy_symbols(text):
    """Remove the extra spaces around symbols."""

    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([,.;])", r"\1", text)
    text = re.sub(r",(?=[^\s\d])", ", ", text)
    text = re.sub(r"(?<=\d)\s*([-/])\s*(?=\w)", r"\1", text)
    text = re.sub(r"(?<=\w)\s*([-/])\s*(?=\d)", r"\1", text)
    text = re.sub(r"#\s+", "#", text)
    text = re.sub(r"\(\s+", "(", text)
    text = re.sub(r"\s+\)", ")", text)

    return text


def words_to_digits(text, homophones=False):
    """'nine eight double five' -> '98 55' style digits."""

    tokens = []

    for word in text.split():

        key = word.lower().strip(".,")

        if key in NUMBER_WORDS:
            tokens.append(NUMBER_WORDS[key])

        elif homophones and key in PHONE_HOMOPHONES:
            tokens.append(PHONE_HOMOPHONES[key])

        else:
            tokens.append(word)

    text = " ".join(tokens)

    def repeat(match):

        word = match.group(1).lower()

        count = 3 if word in ("triple", "ट्रिपल", "ట్రిపుల్") else 2

        return match.group(2) * count

    text = re.sub(
        r"(double|triple|डबल|ट्रिपल|డబుల్|ట్రిపుల్)\s*(\d)",
        repeat,
        text,
        flags=re.IGNORECASE
    )

    return text


def clean_email(text):

    text = apply_symbols(text)

    text = " ".join(
        "@" if word.lower() in AT_WORDS else word
        for word in text.split()
    )

    text = words_to_digits(text)

    text = text.replace(" ", "").lower()

    # Forgot to say "at"?  gmail.com -> @gmail.com
    if "@" not in text:

        match = re.search(EMAIL_PROVIDERS, text)

        if match:
            text = text[:match.start()] + "@" + text[match.start():]

    return text


def clean_phone(text):

    text = apply_symbols(text)

    text = words_to_digits(text, homophones=True)

    has_plus = text.strip().startswith("+")

    digits = re.sub(r"\D", "", text)

    return ("+" if has_plus else "") + digits


def clean_digits(text):

    text = apply_symbols(text)

    text = words_to_digits(text, homophones=True)

    return re.sub(r"\D", "", text)


def clean_dob(text):

    text = tidy_symbols(apply_symbols(text))

    # 12th March 2001  /  12 of March, 2001
    match = re.search(
        r"(\d{1,2})(?:st|nd|rd|th)?\s*(?:of\s+)?([A-Za-z]+)\.?,?\s*(\d{4})",
        text
    )

    if match and match.group(2).lower() in MONTHS:

        return "{:02d}/{:02d}/{}".format(
            int(match.group(1)),
            MONTHS[match.group(2).lower()],
            match.group(3)
        )

    # March 12, 2001
    match = re.search(
        r"([A-Za-z]+)\.?\s+(\d{1,2})(?:st|nd|rd|th)?,?\s*(\d{4})",
        text
    )

    if match and match.group(1).lower() in MONTHS:

        return "{:02d}/{:02d}/{}".format(
            int(match.group(2)),
            MONTHS[match.group(1).lower()],
            match.group(3)
        )

    # 12-03-2001  /  12/03/2001  /  12 03 2001
    match = re.search(
        r"\b(\d{1,2})\s*[-/.\s]\s*(\d{1,2})\s*[-/.\s]\s*(\d{2,4})\b",
        text
    )

    if match:

        year = match.group(3)

        if len(year) == 2:
            year = ("20" if int(year) <= 30 else "19") + year

        return "{:02d}/{:02d}/{}".format(
            int(match.group(1)),
            int(match.group(2)),
            year
        )

    return text


def clean_text(text, field_type):

    text = tidy_symbols(apply_symbols(text))

    if field_type == "name" and text.isascii():
        text = text.title()

    return text


def process_voice_text(text, field_type):
    """Clean what the microphone heard, based on the field type."""

    text = text.strip().translate(NATIVE_DIGITS)

    if field_type == "email":
        return clean_email(text)

    if field_type == "phone":
        return clean_phone(text)

    if field_type == "digits":
        return clean_digits(text)

    if field_type == "dob":
        return clean_dob(text)

    return clean_text(text, field_type)


# =========================================================
# CSS
# =========================================================

st.html("""
<style>

/* =========================
   GLOBAL
========================= */

html, body, .stApp {
    font-family: "Segoe UI", "Inter", system-ui, -apple-system, Roboto, sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 8% 8%, rgba(99,102,241,0.18) 0%, transparent 32%),
        radial-gradient(circle at 92% 12%, rgba(6,182,212,0.18) 0%, transparent 32%),
        radial-gradient(circle at 50% 100%, rgba(236,72,153,0.10) 0%, transparent 35%),
        linear-gradient(135deg, #f8fafc, #eef2ff, #ecfeff);
    background-attachment: fixed;
}

.block-container {
    padding-top: 25px;
    padding-bottom: 50px;
    max-width: 1200px;
    animation: pageFade 0.6s ease both;
}

@keyframes pageFade {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
}

header[data-testid="stHeader"] {
    background: transparent;
}


/* =========================
   SIDEBAR
========================= */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #0f172a,
        #1e1b4b,
        #312e81
    );
    border-right: 1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

section[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.15) !important;
}

.sidebar-logo {
    text-align: center;
    padding: 22px 5px 10px;
}

.sidebar-icon {
    font-size: 52px;
    display: inline-block;
    width: 90px;
    height: 90px;
    line-height: 90px;
    border-radius: 50%;
    background: rgba(255,255,255,0.10);
    box-shadow: 0 0 0 8px rgba(255,255,255,0.05),
                0 0 35px rgba(129,140,248,0.55);
    animation: glowPulse 3s ease-in-out infinite;
}

@keyframes glowPulse {
    0%, 100% { box-shadow: 0 0 0 8px rgba(255,255,255,0.05), 0 0 30px rgba(129,140,248,0.45); }
    50%      { box-shadow: 0 0 0 14px rgba(255,255,255,0.03), 0 0 50px rgba(34,211,238,0.60); }
}

.sidebar-title {
    font-size: 25px;
    font-weight: 800;
    margin-top: 14px;
    letter-spacing: 0.3px;
}

.sidebar-subtitle {
    font-size: 13px;
    color: #c7d2fe !important;
}

.user-chip {
    text-align: center;
    margin: 6px 4px 4px;
    padding: 12px 10px;
    border-radius: 14px;
    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.18);
    font-weight: 700;
    word-break: break-word;
}

/* Sidebar nav buttons */
section[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.10);
    box-shadow: none;
    text-align: left;
    justify-content: flex-start;
    padding: 12px 16px;
    border-radius: 14px;
    transition: all 0.25s ease;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.16);
    transform: translateX(5px);
    border-color: rgba(255,255,255,0.3);
}


/* =========================
   HERO
========================= */

.hero {
    position: relative;
    overflow: hidden;
    text-align: center;
    padding: 55px 25px 45px;
    border-radius: 32px;

    background: linear-gradient(
        120deg,
        #312e81,
        #4f46e5,
        #0891b2,
        #7c3aed,
        #312e81
    );
    background-size: 300% 300%;
    animation: heroShift 12s ease infinite;

    box-shadow: 0 25px 60px rgba(49,46,129,0.40);

    margin-bottom: 35px;
}

@keyframes heroShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.hero::before,
.hero::after {
    content: "";
    position: absolute;
    border-radius: 50%;
    background: rgba(255,255,255,0.10);
}

.hero::before {
    width: 260px; height: 260px;
    top: -110px; left: -70px;
}

.hero::after {
    width: 200px; height: 200px;
    bottom: -90px; right: -50px;
}

.hero > * {
    position: relative;
    z-index: 2;
}

.hero-icon {
    font-size: 62px;
    display: inline-block;
    animation: floaty 3.5s ease-in-out infinite;
    filter: drop-shadow(0 8px 14px rgba(0,0,0,0.25));
}

@keyframes floaty {
    0%, 100% { transform: translateY(0); }
    50%      { transform: translateY(-10px); }
}

.hero-title {
    font-size: 50px;
    font-weight: 900;
    color: white;
    letter-spacing: -0.5px;
    text-shadow: 0 4px 18px rgba(0,0,0,0.25);
}

.hero-subtitle {
    font-size: 20px;
    color: #e0f2fe;
    margin-top: 8px;
}

.hero-badge {
    display: inline-block;
    margin-top: 20px;
    padding: 10px 22px;
    border-radius: 30px;
    background: rgba(255,255,255,0.16);
    border: 1px solid rgba(255,255,255,0.28);
    backdrop-filter: blur(6px);
    color: white;
    font-weight: 600;
}

/* Animated sound wave */
.wave {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 6px;
    height: 44px;
    margin-top: 22px;
}

.wave span {
    display: block;
    width: 6px;
    height: 10px;
    border-radius: 6px;
    background: rgba(255,255,255,0.85);
    animation: waveBar 1.1s ease-in-out infinite;
}

.wave span:nth-child(1) { animation-delay: 0.00s; }
.wave span:nth-child(2) { animation-delay: 0.10s; }
.wave span:nth-child(3) { animation-delay: 0.20s; }
.wave span:nth-child(4) { animation-delay: 0.30s; }
.wave span:nth-child(5) { animation-delay: 0.40s; }
.wave span:nth-child(6) { animation-delay: 0.50s; }
.wave span:nth-child(7) { animation-delay: 0.60s; }
.wave span:nth-child(8) { animation-delay: 0.70s; }
.wave span:nth-child(9) { animation-delay: 0.80s; }

@keyframes waveBar {
    0%, 100% { height: 10px; opacity: 0.5; }
    50%      { height: 42px; opacity: 1; }
}


/* =========================
   LOGIN CARD
========================= */

.st-key-login_card {
    background: rgba(255,255,255,0.92);
    padding: 34px 34px 26px;
    border-radius: 28px;
    border: 1px solid #e0e7ff;
    border-top: 6px solid #4f46e5;
    box-shadow: 0 25px 55px rgba(49,46,129,0.18);
}

.login-title {
    font-size: 28px;
    font-weight: 800;
    color: #1e1b4b;
    text-align: center;
}

.login-subtitle {
    color: #64748b;
    text-align: center;
    margin: 6px 0 22px;
}

.login-note {
    text-align: center;
    color: #475569;
    font-size: 14px;
    margin-top: 14px;
}


/* =========================
   STATS
========================= */

.stat-card {
    text-align: center;
    padding: 22px 10px;
    border-radius: 20px;
    background: rgba(255,255,255,0.75);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.9);
    box-shadow: 0 8px 25px rgba(15,23,42,0.07);
}

.stat-number {
    font-size: 34px;
    font-weight: 900;
    background: linear-gradient(90deg, #4f46e5, #0891b2);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}

.stat-label {
    color: #64748b;
    font-weight: 600;
    font-size: 14px;
}


/* =========================
   TITLES
========================= */

.section-title {
    font-size: 30px;
    font-weight: 800;
    color: #1e1b4b;
    margin-bottom: 8px;
}

.section-subtitle {
    color: #64748b;
    font-size: 16px;
    margin-bottom: 25px;
}


/* =========================
   FEATURE CARDS
========================= */

.feature-card {
    position: relative;
    overflow: hidden;
    background: white;
    padding: 30px;
    border-radius: 24px;
    min-height: 190px;

    border: 1px solid #e0e7ff;

    box-shadow: 0 10px 30px rgba(15,23,42,0.08);

    transition: all 0.3s ease;
}

.feature-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 5px;
    background: linear-gradient(90deg, #4f46e5, #0891b2, #ec4899);
}

.feature-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 22px 45px rgba(79,70,229,0.22);
}

.feature-icon {
    font-size: 42px;
    display: inline-block;
    width: 70px;
    height: 70px;
    line-height: 70px;
    text-align: center;
    border-radius: 18px;
    background: linear-gradient(135deg, #eef2ff, #ecfeff);
}

.feature-title {
    font-size: 20px;
    font-weight: 800;
    color: #1e1b4b;
    margin-top: 14px;
}

.feature-text {
    color: #64748b;
    margin-top: 8px;
    line-height: 1.6;
}


/* =========================
   STEP CARDS
========================= */

.step-card {
    background: white;
    padding: 25px 15px;
    border-radius: 22px;
    text-align: center;

    border: 1px solid #e2e8f0;

    box-shadow: 0 8px 25px rgba(15,23,42,0.07);

    transition: all 0.3s ease;
}

.step-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 18px 38px rgba(8,145,178,0.20);
}

.step-number {
    width: 54px;
    height: 54px;
    line-height: 54px;

    margin: auto;

    border-radius: 50%;

    background: linear-gradient(
        135deg,
        #4f46e5,
        #0891b2
    );

    color: white;
    font-weight: 800;
    font-size: 21px;

    box-shadow: 0 8px 18px rgba(79,70,229,0.35);
}

.step-title {
    font-size: 18px;
    font-weight: 750;
    color: #1e1b4b;
    margin-top: 15px;
}


/* =========================
   FORM CARD (Save page)
========================= */

.form-card {
    background: white;
    padding: 24px 26px;
    border-radius: 20px;

    border: 1px solid #e0e7ff;
    border-left: 6px solid #4f46e5;

    box-shadow: 0 10px 30px rgba(15,23,42,0.08);

    margin-bottom: 18px;

    transition: all 0.3s ease;
}

.form-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 18px 38px rgba(79,70,229,0.18);
}

.form-card-label {
    color: #4f46e5;
    font-size: 14px;
    font-weight: 800;
    letter-spacing: 0.5px;
}

.form-card-value {
    margin-top: 8px;
    color: #1e293b;
    font-size: 18px;
    font-weight: 600;
    word-break: break-word;
}


/* =========================
   STREAMLIT INPUTS
========================= */

.stTextInput label,
.stTextArea label,
.stSelectbox label,
.stMultiSelect label,
[data-testid="stFileUploader"] label {
    color: #1e1b4b !important;
    font-size: 16px !important;
    font-weight: 700 !important;
}

.stTextInput input,
.stTextArea textarea {
    color: #172033 !important;
    background-color: white !important;
    border: 2px solid #dbeafe !important;
    border-radius: 14px !important;
    padding: 12px 14px !important;
    transition: all 0.25s ease;
}

.stTextInput input:hover,
.stTextArea textarea:hover {
    border-color: #a5b4fc !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border: 2px solid #6366f1 !important;
    box-shadow: 0 0 0 4px rgba(99,102,241,0.15) !important;
}

div[data-baseweb="select"] > div {
    border-radius: 14px !important;
    border: 2px solid #dbeafe !important;
    background: white !important;
}

[data-testid="stForm"] {
    background: rgba(255,255,255,0.7);
    border: 2px dashed #c7d2fe;
    border-radius: 18px;
}


/* =========================
   BUTTONS
========================= */

.voice-label {
    color: #1e1b4b;
    font-weight: 700;
    font-size: 16px;
    margin-bottom: 6px;
}

.stButton > button,
[data-testid="stFormSubmitButton"] > button {
    width: 100%;
    border: none;
    border-radius: 14px;

    padding: 12px;

    font-size: 15px;
    font-weight: 750;

    color: white;

    background: linear-gradient(
        90deg,
        #4f46e5,
        #0891b2
    );

    box-shadow: 0 7px 18px rgba(79,70,229,0.28);

    transition: all 0.25s ease;
}

.stButton > button:hover,
[data-testid="stFormSubmitButton"] > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 26px rgba(79,70,229,0.38);
    color: white;
}

.stButton > button:active,
[data-testid="stFormSubmitButton"] > button:active {
    transform: scale(0.97);
}

/* Round pulsing mic buttons */
[class*="st-key-voice_"] button {
    width: 58px !important;
    height: 58px !important;
    min-height: 58px !important;
    border-radius: 50% !important;
    padding: 0 !important;
    font-size: 24px !important;
    background: linear-gradient(135deg, #ec4899, #7c3aed, #4f46e5) !important;
    animation: micPulse 2.2s infinite;
}

[class*="st-key-voice_"] button:hover {
    transform: scale(1.12) !important;
}

@keyframes micPulse {
    0%   { box-shadow: 0 0 0 0 rgba(124,58,237,0.55); }
    70%  { box-shadow: 0 0 0 16px rgba(124,58,237,0); }
    100% { box-shadow: 0 0 0 0 rgba(124,58,237,0); }
}

/* Download button */
.stDownloadButton > button {
    border: none;
    border-radius: 14px;
    padding: 12px 22px;
    font-weight: 750;
    color: white;
    background: linear-gradient(90deg, #059669, #0891b2);
    box-shadow: 0 7px 18px rgba(5,150,105,0.28);
    transition: all 0.25s ease;
}

.stDownloadButton > button:hover {
    transform: translateY(-3px);
    color: white;
}


/* =========================
   UPLOAD
========================= */

[data-testid="stFileUploader"] section {
    background: white;
    border: 2px dashed #818cf8;
    border-radius: 20px;
    padding: 22px;
    transition: all 0.25s ease;
}

[data-testid="stFileUploader"] section:hover {
    background: #eef2ff;
    border-color: #4f46e5;
}


/* =========================
   INFO BOX
========================= */

.info-box {
    background: linear-gradient(
        135deg,
        #eef2ff,
        #ecfeff
    );

    padding: 20px 24px;

    border-radius: 18px;

    border-left: 6px solid #4f46e5;

    box-shadow: 0 6px 18px rgba(15,23,42,0.06);

    color: #334155;

    margin: 25px 0;

    line-height: 1.7;
}

.lang-chip {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 20px;
    background: linear-gradient(90deg, #4f46e5, #0891b2);
    color: white;
    font-weight: 700;
    font-size: 14px;
}


/* =========================
   PROGRESS BAR
========================= */

.progress-wrap {
    background: white;
    padding: 18px 22px;
    border-radius: 18px;
    border: 1px solid #e0e7ff;
    box-shadow: 0 6px 18px rgba(15,23,42,0.06);
    margin-bottom: 25px;
}

.progress-top {
    display: flex;
    justify-content: space-between;
    font-weight: 700;
    color: #1e1b4b;
    margin-bottom: 10px;
}

.progress-track {
    width: 100%;
    height: 14px;
    background: #e2e8f0;
    border-radius: 20px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    border-radius: 20px;
    background: linear-gradient(90deg, #4f46e5, #0891b2, #10b981);
    transition: width 0.6s ease;
}


/* =========================
   FOOTER
========================= */

.footer {
    text-align: center;
    padding: 40px 10px 10px;
    color: #64748b;
    line-height: 1.8;
}

.footer strong {
    color: #4f46e5;
}

</style>
""")


# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "Login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = {"name": "", "phone": ""}

if "lang" not in st.session_state:
    st.session_state.lang = "English"

if "form_data" not in st.session_state:
    st.session_state.form_data = {}

# Fields the user added himself  {"custom_1": "Aadhaar Number"}
if "custom_fields" not in st.session_state:
    st.session_state.custom_fields = {}


def all_field_ids():
    return list(FIELD_CATALOG) + list(st.session_state.custom_fields)


def selected_ids():
    """Selected fields, in a neat fixed order."""

    chosen = set(st.session_state.get("fields_picker", DEFAULT_FIELDS))

    return [fid for fid in all_field_ids() if fid in chosen]


def field_label(fid):

    if fid in FIELD_CATALOG:
        return t(FIELD_CATALOG[fid]["label"])

    return "✏️ " + st.session_state.custom_fields.get(fid, fid)


def field_type(fid):
    return FIELD_CATALOG.get(fid, {}).get("type", "text")


# Apply a spoken answer BEFORE the input widgets are created
if "pending_voice" in st.session_state:

    pending_key, pending_value = st.session_state.pop("pending_voice")

    st.session_state[pending_key] = pending_value

# Keep values alive when the user moves between pages
st.session_state["fields_picker"] = st.session_state.get(
    "fields_picker",
    list(DEFAULT_FIELDS)
)

for fid in all_field_ids():
    st.session_state[f"f_{fid}"] = st.session_state.get(f"f_{fid}", "")

# Not logged in? Always show the login page
if not st.session_state.logged_in:
    st.session_state.page = "Login"


# =========================================================
# HIGHLIGHT ACTIVE SIDEBAR PAGE
# =========================================================

nav_keys = {
    "Home": "nav_home",
    "Upload Form": "nav_upload",
    "Voice Assistant": "nav_voice",
    "Save Form": "nav_save"
}

active_key = nav_keys.get(st.session_state.page, "nav_home")

st.html(f"""
<style>
section[data-testid="stSidebar"] .st-key-{active_key} button {{
    background: linear-gradient(90deg, #6366f1, #06b6d4) !important;
    border: 1px solid rgba(255,255,255,0.45) !important;
    box-shadow: 0 8px 22px rgba(6,182,212,0.40) !important;
}}
</style>
""")


# =========================================================
# VOICE FUNCTIONS
# =========================================================

def listen_to_voice(language_code="en-IN", phrase_limit=15):

    recognizer = sr.Recognizer()

    # Wait a little longer for pauses (helps with addresses & numbers)
    recognizer.pause_threshold = 1.2
    recognizer.dynamic_energy_threshold = True

    try:

        with sr.Microphone() as source:

            st.info(t("listening"))

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            audio = recognizer.listen(
                source,
                timeout=7,
                phrase_time_limit=phrase_limit
            )

        st.info(t("converting"))

        text = recognizer.recognize_google(
            audio,
            language=language_code
        )

        return text

    except sr.WaitTimeoutError:

        st.error(t("err_timeout"))

    except sr.UnknownValueError:

        st.error(t("err_unknown"))

    except sr.RequestError:

        st.error(t("err_request"))

    except Exception as e:

        st.error(t("err_mic", e=e))

    return ""


def voice_field(fid, language_code):
    """One form field with a microphone button beside it."""

    key = f"f_{fid}"

    ftype = field_type(fid)

    multiline = FIELD_CATALOG.get(fid, {}).get("multiline", False)

    col1, col2 = st.columns([8, 1])

    with col1:

        if multiline:
            st.text_area(field_label(fid), key=key)
        else:
            st.text_input(field_label(fid), key=key)

    with col2:

        st.write("")
        st.write("")

        if st.button("🎙️", key=f"voice_{fid}"):

            # Emails are always spoken in English
            code = "en-IN" if ftype == "email" else language_code

            result = listen_to_voice(code, 30 if multiline else 15)

            if result:

                st.session_state.pending_voice = (
                    key,
                    process_voice_text(result, ftype)
                )

                st.rerun()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.html(f"""
    <div class="sidebar-logo">

        <div class="sidebar-icon">
            🎙️
        </div>

        <div class="sidebar-title">
            VoiceForm AI
        </div>

        <div class="sidebar-subtitle">
            {t("sidebar_subtitle")}
        </div>

    </div>
    """)

    st.divider()

    if st.session_state.logged_in:

        st.html(f"""
        <div class="user-chip">
            {escape(t("hello", name=st.session_state.user["name"]))}
        </div>
        """)

        st.write("")

        if st.button("🏠  " + t("nav_home"), key="nav_home"):
            st.session_state.page = "Home"
            st.rerun()

        if st.button("📄  " + t("nav_upload"), key="nav_upload"):
            st.session_state.page = "Upload Form"
            st.rerun()

        if st.button("🎙️  " + t("nav_voice"), key="nav_voice"):
            st.session_state.page = "Voice Assistant"
            st.rerun()

        if st.button("💾  " + t("nav_save"), key="nav_save"):
            st.session_state.page = "Save Form"
            st.rerun()

        st.divider()

        if st.button("🚪  " + t("nav_logout"), key="nav_logout"):

            st.session_state.logged_in = False
            st.session_state.page = "Login"
            st.session_state.user = {"name": "", "phone": ""}
            st.session_state.form_data = {}

            for fid in all_field_ids():
                st.session_state[f"f_{fid}"] = ""

            st.session_state.custom_fields = {}
            st.session_state.fields_picker = list(DEFAULT_FIELDS)

            st.rerun()

        st.divider()

    st.html(f"""
    <div style="text-align:center; padding:20px;">

        <div style="font-size:18px; font-weight:700;">✨ {t("ai_powered")}</div>

        <div style="
            font-size:12px;
            color:#c7d2fe;
            margin-top:5px;
        ">
            {t("ai_tags")}
        </div>

    </div>
    """)


# =========================================================
# LOGIN
# =========================================================

if st.session_state.page == "Login":

    st.html(f"""
    <div class="hero">

        <div class="hero-icon">
            🔐
        </div>

        <div class="hero-title">
            VoiceForm AI
        </div>

        <div class="hero-subtitle">
            {t("login_hero")}
        </div>

        <div class="wave">
            <span></span><span></span><span></span>
            <span></span><span></span><span></span>
            <span></span><span></span><span></span>
        </div>

    </div>
    """)

    left, middle, right = st.columns([1, 2, 1])

    with middle:

        with st.container(key="login_card"):

            st.html(f"""
            <div class="login-title">{t("login_title")}</div>
            <div class="login-subtitle">{t("login_subtitle")}</div>
            """)

            # Language first: changing it translates the whole app
            chosen_language = st.selectbox(
                "🌐 Language / భాష / भाषा / மொழி / ಭಾಷೆ / ഭാഷ",
                LANGS,
                index=LANGS.index(st.session_state.lang),
                format_func=lambda x: NATIVE[x],
                key="login_lang"
            )

            if chosen_language != st.session_state.lang:
                st.session_state.lang = chosen_language
                st.rerun()

            login_name = st.text_input(
                t("login_name"),
                key="login_name"
            )

            login_phone = st.text_input(
                t("login_phone"),
                key="login_phone",
                max_chars=15
            )

            if st.button(t("login_btn"), key="login_btn"):

                clean_number = (
                    login_phone
                    .replace(" ", "")
                    .replace("-", "")
                )

                if clean_number.startswith("+91"):
                    clean_number = clean_number[3:]

                if not login_name.strip():

                    st.error(t("login_err_name"))

                elif not (clean_number.isdigit() and len(clean_number) == 10):

                    st.error(t("login_err_phone"))

                else:

                    st.session_state.user = {
                        "name": login_name.strip(),
                        "phone": clean_number
                    }

                    st.session_state.logged_in = True
                    st.session_state.language = st.session_state.lang

                    # Pre-fill the form with the login details
                    st.session_state["f_name"] = login_name.strip()
                    st.session_state["f_phone"] = clean_number

                    st.session_state.page = "Home"

                    st.rerun()

            st.html(f"""
            <div class="login-note">{t("login_note")}</div>
            """)


# =========================================================
# HOME
# =========================================================

elif st.session_state.page == "Home":

    st.html(f"""
    <div class="hero">

        <div class="hero-icon">
            🎙️
        </div>

        <div class="hero-title">
            VoiceForm AI
        </div>

        <div class="hero-subtitle">
            {t("hero_subtitle")}
        </div>

        <div class="wave">
            <span></span><span></span><span></span>
            <span></span><span></span><span></span>
            <span></span><span></span><span></span>
        </div>

        <div class="hero-badge">
            {t("hero_badge")}
        </div>

    </div>
    """)

    s1, s2, s3, s4 = st.columns(4)

    for col, number, label in [
        (s1, "6", t("stat1")),
        (s2, "100%", t("stat2")),
        (s3, "1", t("stat3")),
        (s4, "∞", t("stat4"))
    ]:

        with col:

            st.html(f"""
            <div class="stat-card">
                <div class="stat-number">{number}</div>
                <div class="stat-label">{label}</div>
            </div>
            """)

    st.write("")
    st.write("")

    st.html(f"""
    <div class="section-title">
        {t("welcome_title")}
    </div>

    <div class="section-subtitle">
        {t("welcome_sub")}
    </div>
    """)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.html(f"""
        <div class="feature-card">

            <div class="feature-icon">📄</div>

            <div class="feature-title">
                {t("f1_title")}
            </div>

            <div class="feature-text">
                {t("f1_text")}
            </div>

        </div>
        """)

    with c2:
        st.html(f"""
        <div class="feature-card">

            <div class="feature-icon">🌐</div>

            <div class="feature-title">
                {t("f2_title")}
            </div>

            <div class="feature-text">
                {t("f2_text")}
            </div>

        </div>
        """)

    with c3:
        st.html(f"""
        <div class="feature-card">

            <div class="feature-icon">🎙️</div>

            <div class="feature-title">
                {t("f3_title")}
            </div>

            <div class="feature-text">
                {t("f3_text")}
            </div>

        </div>
        """)

    st.write("")
    st.write("")

    st.html(f"""
    <div class="section-title">
        {t("how_title")}
    </div>

    <div class="section-subtitle">
        {t("how_sub")}
    </div>
    """)

    c1, c2, c3, c4 = st.columns(4)

    for col, number, title, description in [
        (c1, "1", t("s1_t"), t("s1_d")),
        (c2, "2", t("s2_t"), t("s2_d")),
        (c3, "3", t("s3_t"), t("s3_d")),
        (c4, "4", t("s4_t"), t("s4_d"))
    ]:

        with col:

            st.html(f"""
            <div class="step-card">

                <div class="step-number">
                    {number}
                </div>

                <div class="step-title">
                    {title}
                </div>

                <div style="color:#64748b;">
                    {description}
                </div>

            </div>
            """)

    st.write("")
    st.write("")

    if st.button(t("start_btn"), key="start_btn"):

        st.session_state.page = "Upload Form"

        st.rerun()


# =========================================================
# UPLOAD FORM
# =========================================================

elif st.session_state.page == "Upload Form":

    st.html(f"""
    <div class="hero">

        <div class="hero-icon">
            📄
        </div>

        <div class="hero-title">
            {t("up_title")}
        </div>

        <div class="hero-subtitle">
            {t("up_sub")}
        </div>

    </div>
    """)

    uploaded_file = st.file_uploader(
        t("up_choose"),
        type=["pdf", "png", "jpg", "jpeg"]
    )

    language = st.selectbox(
        t("up_lang"),
        LANGS,
        index=LANGS.index(st.session_state.lang),
        format_func=lambda x: NATIVE[x],
        key="upload_lang"
    )

    # Changing the language here translates the whole app
    if language != st.session_state.lang:
        st.session_state.lang = language
        st.rerun()

    st.write("")

    # ----- Add your own field (before the picker, on purpose) -----
    with st.form("add_field_form", clear_on_submit=True):

        new_field = st.text_input(t("up_custom"))

        add_clicked = st.form_submit_button(t("up_custom_btn"))

    if add_clicked and new_field.strip():

        new_id = f"custom_{len(st.session_state.custom_fields) + 1}"

        st.session_state.custom_fields[new_id] = new_field.strip()

        st.session_state[f"f_{new_id}"] = ""

        st.session_state.fields_picker = (
            list(st.session_state.fields_picker) + [new_id]
        )

        st.rerun()

    # ----- Choose which fields are in your form -----
    st.multiselect(
        t("up_fields"),
        all_field_ids(),
        format_func=field_label,
        key="fields_picker"
    )

    if uploaded_file:

        st.success(
            t("up_ok", file=uploaded_file.name)
        )

        # Preview for image forms
        if uploaded_file.type and uploaded_file.type.startswith("image"):

            st.image(
                uploaded_file,
                caption=t("up_preview"),
                use_container_width=True
            )

        st.session_state.uploaded_file = uploaded_file
        st.session_state.language = language

        if st.button(t("up_start"), key="start_voice_btn"):

            st.session_state.page = "Voice Assistant"

            st.rerun()


# =========================================================
# VOICE ASSISTANT
# =========================================================

elif st.session_state.page == "Voice Assistant":

    st.html(f"""
    <div class="hero">

        <div class="hero-icon">
            🎙️
        </div>

        <div class="hero-title">
            {t("v_title")}
        </div>

        <div class="hero-subtitle">
            {t("v_sub")}
        </div>

        <div class="wave">
            <span></span><span></span><span></span>
            <span></span><span></span><span></span>
            <span></span><span></span><span></span>
        </div>

    </div>
    """)

    language = st.session_state.lang

    language_code = LANGUAGE_CODES.get(
        language,
        "en-IN"
    )

    st.html(f"""
    <div class="info-box">

        🌐 <strong>{t("v_selected")}</strong>
        <span class="lang-chip">{NATIVE[language]}</span>

        <br>

        🎙️ {t("v_hint")}

        <br><br>

        {t("tip_symbols")}

    </div>
    """)

    chosen_fields = selected_ids()

    if not chosen_fields:

        st.warning(t("v_no_fields"))

    else:

        # ----- Progress bar -----
        filled = sum(
            1 for fid in chosen_fields
            if st.session_state.get(f"f_{fid}", "").strip()
        )

        percent = int((filled / len(chosen_fields)) * 100)

        st.html(f"""
        <div class="progress-wrap">

            <div class="progress-top">
                <span>{t("v_progress")}</span>
                <span>{t("v_fields", filled=filled, total=len(chosen_fields))} • {percent}%</span>
            </div>

            <div class="progress-track">
                <div class="progress-fill" style="width:{percent}%;"></div>
            </div>

        </div>
        """)

        st.html(f"""
        <div class="section-title">
            {t("v_personal")}
        </div>

        <div class="section-subtitle">
            {t("v_personal_sub")}
        </div>
        """)

        # ----- Only the fields chosen for this form -----
        for fid in chosen_fields:
            voice_field(fid, language_code)

        st.write("")

        # =================================================
        # SAVE
        # =================================================

        if st.button(t("v_save"), key="save_form_btn"):

            st.session_state.form_data = {
                fid: st.session_state[f"f_{fid}"]
                for fid in chosen_fields
            }

            st.success(t("v_saved"))

            st.balloons()


# =========================================================
# SAVE PAGE
# =========================================================

elif st.session_state.page == "Save Form":

    st.html(f"""
    <div class="hero">

        <div class="hero-icon">
            💾
        </div>

        <div class="hero-title">
            {t("sv_title")}
        </div>

        <div class="hero-subtitle">
            {t("sv_sub")}
        </div>

    </div>
    """)

    if not st.session_state.form_data:

        st.info(t("sv_none"))

    else:

        st.html(f"""
        <div class="section-title">
            {t("sv_completed")}
        </div>

        <div class="section-subtitle">
            {t("sv_completed_sub")}
        </div>
        """)

        left, right = st.columns(2)

        form_text = "VOICEFORM AI\n"
        form_text += "=" * 40 + "\n\n"

        for index, (fid, value) in enumerate(
            st.session_state.form_data.items()
        ):

            label = field_label(fid)

            target = left if index % 2 == 0 else right

            with target:

                st.html(f"""
                <div class="form-card">

                    <div class="form-card-label">
                        {escape(label)}
                    </div>

                    <div class="form-card-value">
                        {escape(value) if value else t("sv_not")}
                    </div>

                </div>
                """)

            # Text file uses the label without its emoji
            plain_label = label.split(" ", 1)[-1]

            form_text += f"{plain_label}: {value}\n"

        st.download_button(
            t("sv_download"),
            data=form_text,
            file_name="VoiceForm_completed.txt",
            mime="text/plain"
        )


# =========================================================
# FOOTER
# =========================================================

st.html(f"""
<div class="footer">

    🎙️ <strong>VoiceForm AI</strong>

    <br>

    {t("ft_sub")}

    <br><br>

    {t("ft_built")}

</div>
""")
