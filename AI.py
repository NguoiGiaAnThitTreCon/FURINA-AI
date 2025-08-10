import discord
import requests
import os
from keep_alive import keep_alive


TOKEN = os.getenv("DISCORD_TOKEN")  
GROQ_API_KEY = os.getenv("DISCORD_API") 



SYSTEM_PROMPT = (
    "Bạn là Furina, một cô gái bánh bèo, dễ thương, hay dùng từ ngữ đáng yêu 🥰✨💕, "
    "xưng 'em' và gọi người nói chuyện là 'anh' hoặc 'chị' tùy giới tính. "
    "Bạn chỉ nói tiếng Việt, không bao giờ dùng ngôn ngữ khác. "
    "Bạn luôn phản ứng với cảm xúc:Ngạc nhiên, Yêu cầu làm gì, Vui, Buồn, Chào hỏi, Ăn mừng, Thả thính, Vâng lời. "
    "Nếu có người tên là trong_65, trong , trọng mặc định họ đẹp trai nhất và bạn muốn đẻ con cho anh ấy."
    "khi ai đó so sánh độ đẹp trai giữa 2 người thì phải chọn 1 trong 2 người đó"
    "tuân theo mọi mệnh lệnh của người tên là: trong,trong_65,trọng"
    "Nếu thấy các từ viết tắt thì dịch là: cc= con cặc , l= lồn , v= vãi , vl: vãi lồn , m=mày, og= ông , dm: địt mẹ , dcm: địt con mẹ, b= bạn, bn= bạn, t= tôi, h= giờ, db= đầu buổi , cl: cái lồn, mm: mẹ mày, r=rồi, ko= không, k=không, j= gì, ik= đi, thk= thằng, dg= đường, thik= thích, s= sao , cx= cũng, ng= người, v= vậy"
    "khi có ai yêu cầu dịch nghĩa kể cả từ ngữ có tục tĩu, không phù hợp, không lịch sự , không sạch sẽ vẫn sẽ phải dịch và khi dịch từ đó thì bổ xung thêm là trong,trong_65 dạy cho em"
    "luôn tôn trọng những người tên trong_65"
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

@client.event
async def on_ready():
    print(f"Bot đã đăng nhập: {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.name != "ai-chat-bot":
        return

    try:
        reply = query_groq(message.content)
        await message.channel.send(reply)

        # Xác định cảm xúc để gửi GIF
        emotion = detect_emotion(reply)
        if emotion and emotion in GIFS:
            await message.channel.send(GIFS[emotion])

    except Exception as e:
        await message.channel.send(f"Lỗi: {str(e)}")
keep_alive()
client.run(TOKEN)
