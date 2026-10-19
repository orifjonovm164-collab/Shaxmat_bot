import os, json, random, requests

TG_TOKEN = os.environ["TG_TOKEN"]
GEMINI_KEY = os.environ["GEMINI_KEY"]
KANAL = os.environ["KANAL"]
MODEL = "gemini-3.8-flash"

PROMPT = """Shaxmat haqida bitta qiyin viktorina savoli tuz (o'zbek tilida).
Mavzu: ochilishlar, shaxmat tarixi, mashhur partiyalar yoki o'yinchilar.
Faqat JSON qaytar:
{"savol": "...", "variantlar": ["...","...","...","..."], "togri": 0, "izoh": "..."}
Cheklov: savol 300, har variant 100, izoh 200 belgigacha.
Faqat aniq, tekshirilgan faktlar. togri - to'g'ri variant raqami (0-3)."""

url = ("https://generativelanguage.googleapis.com/v1beta/models/"
       f"{MODEL}:generateContent?key={GEMINI_KEY}")
r = requests.post(url, json={
    "contents": [{"parts": [{"text": PROMPT}]}],
    "generationConfig": {"responseMimeType": "application/json"}
}, timeout=60).json()

if "candidates" not in r:
    print("GEMINI XATO:", r)
    raise SystemExit(1)

s = json.loads(r["candidates"][0]["content"]["parts"][0]["text"])
togri_matn = s["variantlar"][s["togri"]]
random.shuffle(s["variantlar"])
togri = s["variantlar"].index(togri_matn)

javob = requests.post(
    f"https://api.telegram.org/bot{TG_TOKEN}/sendPoll",
    data={"chat_id": KANAL, "question": s["savol"],
          "options": json.dumps(s["variantlar"], ensure_ascii=False),
          "type": "quiz", "correct_option_id": togri,
          "explanation": s["izoh"]}, timeout=15)
print(javob.json())
