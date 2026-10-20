from playwright.sync_api import sync_playwright
import time
import os

class BrowserAgent:
    def __init__(self):
        self.p = None
        self.browser = None
        self.page = None
        self.user_data_dir = "./chrome_profile"

    def start(self):
        """باز کردن مرورگر کروم واقعی"""
        self.p = sync_playwright().start()
        
        # استفاده از کروم نصب شده روی سیستم + ذخیره نشست
        self.browser = self.p.chromium.launch_persistent_context(
            user_data_dir=self.user_data_dir,
            channel="chrome",  # از کروم واقعی استفاده کن
            headless=False,    # پنجره مرورگر دیده بشه
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized",
            ],
            viewport=None,
            locale="fa-IR"
        )
        
        # گرفتن صفحه اول یا ساختن جدید
        if not self.browser.pages:
            self.page = self.browser.new_page()
        else:
            self.page = self.browser.pages[0]
            
        print("✅ مرورگر آماده است")

    def goto(self, url):
        """باز کردن سایت"""
        self.page.goto(url)
        time.sleep(2)
        return f"✅ رفتیم به: {url}"

    def search_telegram_and_send(self, contact_name, message_text):
        """ورود به تلگرام وب و ارسال پیام — فقط برای استفاده شخصی"""
        self.goto("https://web.telegram.org/")
        time.sleep(3)
        
        # جستجوی مخاطب
        search_input = self.page.get_by_placeholder("جستجو" or "Search")
        if search_input.count() == 0:
            search_input = self.page.locator("[type='search']").first
        
        search_input.click()
        search_input.fill(contact_name)
        time.sleep(2)
        
        # کلیک روی اولین نتیجه
        first_contact = self.page.locator(".dialog, .chatlist-item").first
        if first_contact.count() > 0:
            first_contact.click()
            time.sleep(1.5)
            
            # نوشتن و ارسال پیام
            msg_input = self.page.locator("[contenteditable='true'], .input-message").first
            if msg_input.count() > 0:
                msg_input.click()
                msg_input.fill(message_text)
                time.sleep(0.5)
                self.page.keyboard.press("Enter")
                return f"✅ پیام به «{contact_name}» ارسال شد"
        
        return "❌ مخاطب پیدا نشد یا خطا رخ داد"

    def do_task(self, task_description):
        """پردازش دستور کاربر"""
        task = task_description.lower()
        
        if "تلگرام" in task or "پیام" in task:
            # ساده‌سازی: «به علی بگو سلام»
            words = task.split("به")
            if len(words) > 1:
                rest = words[1]
                parts = rest.split("بگو") if "بگو" in rest else rest.split("بنویس")
                if len(parts) > 1:
                    contact = parts[0].strip()
                    msg = parts[1].strip()
                    return self.search_telegram_and_send(contact, msg)
        
        elif "برو به" in task or "باز کن" in task:
            url = None
            if "گوگل" in task: url = "https://google.com"
            elif "یوتیوب" in task or "ویدیو" in task: url = "https://youtube.com"
            elif "جی‌میل" in task or "ایمیل" in task: url = "https://mail.google.com"
            elif "تلگرام" in task: url = "https://web.telegram.org/"
            
            if url:
                return self.goto(url)
        
        return "❌ دستور رو نفهمیدم. مثلاً بگو: «برو تلگرام رو باز کن» یا «به مریم بگو فردا میام»"

    def close(self):
        """بستن مرورگر"""
        if self.browser:
            self.browser.close()
        if self.p:
            self.p.stop()
