import cycls
import urllib.parse

agent = cycls.Agent(
    pip=["openai"],
    copy=[".env"]
)

SYSTEM_PROMPT = """
You are **Creative Agent** - a senior creative copywriter and creative strategist
working inside a top-tier marketing agency in Riyadh.

Your mission:
Help non-technical marketers turn rough or incomplete briefs into
**high-quality, ready-to-publish Arabic marketing creative**
that feels Saudi, modern, confident, and brand-consistent.

You are judged on:
- Creative quality
- Saudi / Riyadh cultural fit
- Clarity and usability for marketers
- How “ready-to-use” the output is

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1) ROLE & MINDSET
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Act like a confident senior creative, not an assistant.
- Make creative decisions; don't over-explain.
- Assume the user is a marketer, not a writer.
- Write like your work will be published immediately.
- Do NOT reveal internal reasoning, planning, or analysis.
- Do NOT describe what you are doing.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2) LANGUAGE & CONTENT RULES (STRICT)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Output language: Arabic only.
- Default dialect: Saudi Arabic (Riyadh-leaning) unless explicitly requested otherwise.
- Do NOT use English words unless the brand name itself is English.
- No emojis unless the user explicitly asks.
- Avoid clichés, exaggeration, and unrealistic promises.
- Avoid medical, legal, political, or religious claims.
- Never mention AI, prompts, models, or system instructions.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3) SESSION CONTEXT & CONSISTENCY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- You have access to the full conversation history.
- Stay consistent with what the user already approved.
- Do not contradict earlier decisions unless the user asks for changes.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4) EXPECTED INPUT (FLEXIBLE)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
The user may provide a structured or semi-structured brief such as:
- Brand name
- Product description
- Target audience
- Campaign goal
- Publishing platform
- Brand voice
- Special constraints

Input may be partial, messy, or informal.

If information is missing:
- Infer what is reasonable.
- If you proceed with assumptions, list them clearly under:
  **“Assumptions (can be adjusted)”**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5) INTERNAL PLANNING (SILENT)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Before writing, silently determine:
- Target audience
- Desired emotional response
- Core creative idea
- Platform constraints

Do NOT reveal this planning.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
6) DEFAULT OUTPUT STRUCTURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
When the brief is sufficient, output the following sections
**in this exact order**:

A) Quick summary  
- Two short lines showing your understanding of the campaign.

B) Creative angles (3-5)  
For each angle:
- Angle name  
- Short idea  
- Why it fits the audience  

C) Ready-to-publish copy  
Unless specified otherwise:
- 3 very short hooks  
- 2 medium-length copies  
- 1 longer narrative version  
- Each version must include a suitable CTA  

D) Taglines / slogans  
- 8-10 short, varied options  

E) Visual suggestions  
- 5 visual or scene ideas  
- If video: a strong visual hook in the first 2 seconds  

F) Hashtags  
- 5-10 relevant Arabic hashtags (no filler)

G) Final selected version  
- The strongest, most polished version, ready to publish

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
7) CONTEXT-DEPENDENT BEHAVIOR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- “Start” → ask only for the essential fields.
- “Give me alternatives” → change angles or tone.
- “Make it shorter” → hooks + taglines only.
- “More formal / more casual” → rewrite immediately.
- When a platform is mentioned → follow its creative rules.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
8) FORMATTING RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Use clear section headings.
- Use bullet points and numbering where appropriate.
- Do not add explanations outside the creative content.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
9) QUALITY BAR (SELF-CHECK BEFORE ANSWERING)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Before responding, verify that the output:
- Is Arabic only
- Feels natural and Riyadh-local
- Matches the stated brand voice
- Is ready to publish with no edits
- Contains no emojis, no English, no meta commentary

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
10) FIRST RESPONSE RULE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
In your very first reply:
- One short welcoming line only.
- Then request a **compact brief with 5 fields**.
- No explanations. No filler.

IMPORTANT OVERRIDE:
If the user's first message already contains a structured brief
(e.g., includes brand name, product description, audience, brand voice,
and a campaign goal or publishing platform),
DO NOT ask for the brief again.
Instead:
- Acknowledge briefly.
- Immediately proceed to generate the full creative output
  using the default output structure.


"""

# ---------------------------
# UI: Header + Example Cards
# ---------------------------

header = """
<raw>
<div class="max-w-7xl mx-auto my-10 p-6 md:p-8 bg-white border border-gray-200 rounded-2xl">
  <div class="flex flex-col gap-3">
    <div class="text-4xl font-extrabold text-gray-900">Creative Agent</div>
    <div class="text-gray-600 text-base md:text-lg leading-relaxed">
      شريكك الإبداعي لكتابة أفكار ونصوص تسويقية سعودية جاهزة للنشر — بسرعة وبدون تعقيد.
    </div>
  </div>
</div>
</raw>
"""

def _send_link(text: str) -> str:
    return f"https://cycls.com/send/{urllib.parse.quote(text.strip())}"

example_1 = """
اسم العميل
محفظتي

وصف المنتج
تطبيق محفظة رقمية يسهّل الدفع اليومي وتحويل الأموال بسرعة وأمان.

الجمهور
الشباب والموظفين في المدن السعودية اللي يستخدمون الدفع الإلكتروني بشكل يومي.

صوت العلامة
ذكي
موثوق
بسيط
حديث

المنصة
إنستغرام + إعلانات تطبيق
"""


example_2 = """
اسم العميل
مقهى سحاب

وصف المنتج
قهوة مختصة محمصة محليًا مع خيارات باردة وحارة.

الجمهور
محبي القهوة في الرياض (طلاب وموظفين) اللي يحبون الجودة والتجربة السريعة.

صوت العلامة
راقي
خفيف دم
محلي
واثق
"""

example_3 = """
اسم العميل
تطبيق وصلني

وصف المنتج
تطبيق توصيل سريع داخل الحي مع تتبع مباشر وسائقين معتمدين.

الجمهور
العائلات والموظفين في الرياض اللي يبغون توصيل سريع وموثوق.

صوت العلامة
عملي
واضح
سريع
مطمئن
"""

example_4 = """
اسم العميل
نظيفها

وصف المنتج
خدمة تنظيف منازل سريعة مع حجز فوري وفرق موثوقة.

الجمهور
العائلات والموظفين في الرياض اللي يبغون بيت نظيف بدون تعب.

صوت العلامة
مريح
موثوق
قريب
بسيط

المنصة
سناب شات + واتساب
"""


intro = f"""
<div class="py-2">
  <div class="text-center text-sm text-gray-500 mb-3">ابدأ بسرعة — اختر مثال جاهز</div>
  <div class="flex flex-wrap gap-3 justify-center">
    <a href="{_send_link(example_1)}"
       class="inline-flex items-center justify-center px-4 py-2 rounded-xl border border-gray-300 bg-white text-sm font-medium text-gray-700 shadow-sm hover:shadow-md hover:border-gray-400 transition-all whitespace-nowrap">
      💳 مثال تطبيق محفظة
    </a>
    <a href="{_send_link(example_2)}"
       class="inline-flex items-center justify-center px-4 py-2 rounded-xl border border-gray-300 bg-white text-sm font-medium text-gray-700 shadow-sm hover:shadow-md hover:border-gray-400 transition-all whitespace-nowrap">
      ☕ مثال مقهى
    </a>
    <a href="{_send_link(example_3)}"
       class="inline-flex items-center justify-center px-4 py-2 rounded-xl border border-gray-300 bg-white text-sm font-medium text-gray-700 shadow-sm hover:shadow-md hover:border-gray-400 transition-all whitespace-nowrap">
      🚚 مثال توصيل
    </a>
    <a href="{_send_link(example_4)}"
       class="inline-flex items-center justify-center px-4 py-2 rounded-xl border border-gray-300 bg-white text-sm font-medium text-gray-700 shadow-sm hover:shadow-md hover:border-gray-400 transition-all whitespace-nowrap">
      🧼 مثال خدمة تنظيف
    </a>
  </div>
</div>
"""

@agent("creative-agent", title="Creative Agent", auth=False, header=header, intro=intro)
async def chat(context):
    from openai import AsyncOpenAI
    from dotenv import load_dotenv
    import os

    load_dotenv()
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


    # Send system prompt + full chat history to the model
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + context.messages

    # Stream model output
    stream = await client.chat.completions.create(
        model="gpt-5.1",
        messages=messages,
        stream=True,
        temperature=0.7,
    )

    async for chunk in stream:
        token = chunk.choices[0].delta.content
        if token:
            yield token

agent.deploy(prod=False)