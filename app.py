import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="نظام الدعم السلوكي", page_icon="🛑")

st.title("🛑 نظام الدعم السلوكي المباشر (ERP)")
st.write("مرحباً بك. هذا التطبيق مخصص لمساعدتك في جلسات التعرض ومنع الاستجابة.")

with st.sidebar:
    st.header("الإعدادات")
    api_key = st.text_input("أدخل مفتاح Gemini API:", type="password")

if not api_key:
    st.warning("يرجى إدخال مفتاح Gemini API في القائمة الجانبية للبدء.")
else:
    try:
        genai.configure(api_key=api_key)
        
        # البحث عن أول موديل شغال تلقائياً تجنباً لأي خطأ
        available_models = [
            m.name for m in genai.list_models() 
            if 'generateContent' in m.supported_generation_methods
        ]
        
        if available_models:
            model_name = available_models[0]
            model = genai.GenerativeModel(model_name)

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
            st.error("لم يتم العثور على موديلات متوافقة مع مفتاح API.")
            
    except Exception as e:
        st.error(f"حدث خطأ في الاتصال: {e}")
