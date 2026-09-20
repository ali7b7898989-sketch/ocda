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
        
        # السطر الوحيد الخاص بالموديل وهو الأحدث والمطلوب في رسالة الخطأ
        model = genai.GenerativeModel(
    "gemini-3.6-flash",
    system_instruction="أنت مساعد سلوكي متخصص في التعامل مع طقوس الوسواس القهري (OCD) وتقنية منع الاستجابة (ERP). أي عبارة يكتبها المستخدم (مثل: لازم أعيد، أكرر، خايف، مو نظيف) فسرها فوراً كدافع وسواسي. وجّه المستخدم مباشرة لمقاومة التكرار بأسلوب مشجع، واجعل إجابتك مركزة ومباشرة في 2 إلى 3 جمل فقط دون إطالة أو مواضيع عامة."
)


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
                
    except Exception as e:
        st.error(f"حدث خطأ في الاتصال: {e}")
