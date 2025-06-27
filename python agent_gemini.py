import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

# 1. إعداد Gemini
def init_llm(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.0-flash-exp")

# 2. وظيفة للبحث في Google (باستخدام User-Agent)
def google_search(query, user_agent):
    headers = {"User-Agent": user_agent}
    url = f"https://www.google.com/search?q={query}"
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.select("div.BNeawe.s3v9rd.AP7Wnd")  # عنصر نصي بسيط

    output = []
    for r in results[:3]:  # نأخذ أول 3 نتائج فقط
        output.append(r.get_text())
    return "\n".join(output) if output else "لا توجد نتائج واضحة."

# 3. الواجهة الطرفية
def main():
    print("🤖 Gemini AI + Web Agent Terminal")

    api_key = input("🔑 أدخل مفتاح Gemini API: ").strip()
    user_agent = input("🧭 أدخل User-Agent (مثلاً مثل متصفحك): ").strip()
    if not user_agent:
        print("❌ User-Agent مطلوب. أعد التشغيل.")
        return

    model = init_llm(api_key)
    print("\n✅ جاهز. اكتب 'خروج' لإنهاء الجلسة.\n")

    while True:
        task = input("🗣️ أدخل سؤالك أو طلبك: ").strip()
        if task.lower() in ["خروج", "exit", "quit"]:
            break

        use_web = input("🌐 هل تريد البحث في Google أيضًا؟ (نعم/لا): ").strip().lower()
        google_data = ""

        if use_web in ["نعم", "y", "yes"]:
            print("🔎 يتم الآن البحث في Google...")
            try:
                google_data = google_search(task, user_agent)
                print("📄 بيانات من Google:\n", google_data)
            except Exception as e:
                print("❌ حدث خطأ أثناء البحث:", e)

        # إرسال إلى Gemini
        prompt = task + ("\n\nالمعلومات من Google:\n" + google_data if google_data else "")
        try:
            response = model.generate_content(prompt)
            print("\n🧠 رد Gemini:\n", response.text.strip(), "\n")
        except Exception as e:
            print("❌ خطأ من Gemini:", e)

if __name__ == "__main__":
    main()
