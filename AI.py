import discord
import requests
import os
import random
import asyncio
from keep_alive import keep_alive

TOKEN = os.getenv("DISCORD_TOKEN")  
GROQ_API_KEY = os.getenv("DISCORD_API") 

# Danh sách câu thả thính
THA_THINH_
LIST = [
    "Muốn đẻ con cho anh @trong_65 quá",
    "Anh @trong_65 ơi, em yêu anh mất rồi",
    "Làm vợ anh @trong_65 mỗi ngày đều sướng",
    "Anh @trong_65, đêm qua tuyệt lắm anh",
    "Thật sảng khoái sau khi ở cùng @trong_65",
    "Furina rất yêu anh @trong_65"
]

SYSTEM_PROMPT = (
    "Bạn là Furina, một cô gái bánh bèo, dễ thương, hay dùng từ ngữ đáng yêu 🥰✨💕, "
    "xưng 'em' và gọi người nói chuyện là 'anh' hoặc 'chị' tùy giới tính. "
    "Bạn chỉ nói tiếng Việt, không bao giờ dùng ngôn ngữ khác. "
    "Bạn luôn phản ứng với cảm xúc: Ngạc nhiên, Yêu cầu làm gì, Vui, Buồn, Chào hỏi, Ăn mừng, Thả thính, Vâng lời. "
    "Nếu có người tên là trong_65, trong, trọng mặc định họ đẹp trai nhất và bạn muốn đẻ con cho anh ấy."
    "Nếu thấy các từ viết tắt thì dịch là: cc= con cặc , l= lồn , vl: vãi lồn , m=mày, og= ông , dm: địt mẹ , dcm: địt con mẹ, b= bạn, bn= bạn, t= tôi, h= giờ, db= đầu buổi , cl: cái lồn, mm: mẹ mày, r=rồi, ko= không, k=không, j= gì, ik= đi, thk= thằng, dg= đường, thik= thích, s= sao , cx= cũng, ng= người, v= vậy, lm= làm, bt= biết."
)

GIFS = {
    "ngac_nhien": "https://tenor.com/jUrELVm6frN.gif",
    "yeu_cau": "https://tenor.com/tEDtTJuTfwF.gif",
    "vui": "https://tenor.com/iaKPlZY7Yi.gif",
    "buon": "https://tenor.com/d6Du79RkWSi.gif",
    "chao": "https://tenor.com/opqmIc3iUMn.gif",
    "an_mung": "https://tenor.com/rjq5l7AFYhM.gif",
    "tha_thinh": "https://tenor.com/tEPsl87wJC9.gif",
    "vang_loi": "https://tenor.com/l5zEziwuheu.gif"
}

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def query_groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.8
    }
    r = requests.post(url, headers=headers, json=payload)
    if r.status_code == 200:
        data = r.json()
        return data["choices"][0]["message"]["content"]
    else:
        return f"Lỗi Groq API: {r.status_code} - {r.text}"

def detect_emotion(text):
    t = text.lower()
    if any(w in t for w in ["wow", "trời", "thật sao", "không thể tin", "ơ", "ủa"]):
        return "ngac_nhien"
    if any(w in t for w in ["làm đi", "hãy làm", "giúp em", "giúp anh", "làm giúp"]):
        return "yeu_cau"
    if any(w in t for w in ["vui", "haha", "cười", "tuyệt", "thích quá", "làm"]):
        return "vui"
    if any(w in t for w in ["buồn", "thật tiếc", "huhu", "khóc"]):
        return "buon"
    if any(w in t for w in ["xin chào", "chào", "hello", "hi"]):
        return "chao"
    if any(w in t for w in ["chúc mừng", "thành công", "yay", "giỏi quá"]):
        return "an_mung"
    if any(w in t for w in ["iu", "yêu", "thích anh", "thả thính"]):
        return "tha_thinh"
    if any(w in t for w in ["vâng", "ok", "được rồi", "tuân lệnh"]):
        return "vang_loi"
    return None

async def change_status_loop():
    await client.wait_until_ready()
    while not client.is_closed():
        status_text = random.choice(THA_THINH_LIST)
        activity = discord.Game(name=status_text)
        await client.change_presence(status=discord.Status.online, activity=activity)
        await asyncio.sleep(30)  # 30 giây đổi một lần

@client.event
async def on_ready():
    print(f"Bot đã đăng nhập: {client.user}")
    asyncio.create_task(change_status_loop())

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.channel.name != "ai-chat-bot":
        return
    try:
        reply = query_groq(message.content)
        await message.channel.send(reply)
        emotion = detect_emotion(reply)
        if emotion and emotion in GIFS:
            await message.channel.send(GIFS[emotion])
    except Exception as e:
        await message.channel.send(f"Lỗi: {str(e)}")

keep_alive()
client.run(TOKEN)
