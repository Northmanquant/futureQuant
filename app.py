import streamlit as st
from browser_agent import BrowserAgent
import threading

# ---------------- تنظیمات صفحه ----------------
st.set_page_config(
    page_title="futureQuant | ایجنت مرورگر",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 futureQuant — کنترل هوشمند مرورگر")
st.subheader("بگو چه کاری می‌خوای از اینترنت انجام بدم!")
st.divider()

# نگهداری نمونه ایجنت در جلسه
if "agent" not in st.session_state:
    st.session_state.agent = None
if "running" not in st.session_state:
    st.session_state.running = False

# دکمه‌های کنترل
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🚀 باز کردن مرورگر", disabled=st.session_state.running):
        st.session_state.agent = BrowserAgent()
        st.session_state.agent.start()
        st.session_state.running = True
        st.success("✅ مرورگر باز شد! الان می‌تونی دستور بدی.")

with col2:
    if st.button("❌ بستن مرورگر", disabled=not st.session_state.running):
        if st.session_state.agent:
            st.session_state.agent.close()
        st.session_state.agent = None
        st.session_state.running = False
        st.info("مرورگر بسته شد.")

with col3:
    st.info(f"وضعیت: {'فعال ✅' if st.session_state.running else 'غیرفعال ❌'}")

st.divider()

# دستورات آماده
st.header("📋 دستورات نمونه")
ex1 = "برو تلگرام رو باز کن"
ex2 = "برو گوگل رو باز کن"
ex3 = "به دوستم بگو امشب تماس می‌گیرم"
ex4 = "برو جی‌میل رو باز کن"

col_a, col_b, col_c, col_d = st.columns(4)
with col_a: st.code(ex1)
with col_b: st.code(ex2)
with col_c: st.code(ex3)
with col_d: st.code(ex4)

# دریافت دستور
st.divider()
command = st.text_input("✏️ دستورت رو بنویس:", placeholder="مثال: به علی بگو فردا قرارمون یادت نره")

if st.button("▶️ اجرا کن", disabled=not st.session_state.running):
    if command:
        with st.spinner("در حال انجام دادن... پنجره مرورگر رو ببین 👀"):
            result = st.session_state.agent.do_task(command)
            st.success(result)
    else:
        st.warning("اول دستورت رو بنویس!")

# هشدار امنیتی
st.divider()
st.warning("""
⚠️ نکته مهم:
- این برنامه فقط روی کامپیوتر خودت اجرا میشه
- برای اولین ورود به تلگرام، خودت وارد حساب شو — برنامه رمز رو نمی‌بیند و ذخیره نمی‌کند
- استفاده خودکار از حساب کاربری تلگرام ممکنه منجر به محدودیت حساب بشه
- این ابزار فقط برای استفاده شخصی و غیرحجومی طراحی شده
""")
