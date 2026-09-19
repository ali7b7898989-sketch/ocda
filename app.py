import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="نظام الدعم السلوكي", page_icon="🛑", layout="centered")

st.title("🛑 نظام الدعم السلوكي المباشر (ERP)")
st.write("مرحباً بك. هذا التطبيق مخصص لمساعدتك في جلسات التعرض ومنع الاستجابة.")

with st.sidebar:
    st.header("الإعدادات")
    api_key = st.text_input("أدخل مفتاح Gemini API:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("اكتب ما تشعر به الآن...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
        
        response = model.generate_content(user_input)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        with st.chat_message("assistant"):
            st.write(response.text)
else:
    st.warning("يرجى إدخال مفتاح الـ API في القائمة الجانبية للبدء.")
