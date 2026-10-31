# import re, os, sys, json
# from llama_cpp import Llama
#
# def get_resource_path(relative_path):
#     if getattr(sys, 'frozen', False):
#         base_path = os.path.dirname(sys.executable)
#     else:
#         base_path = os.path.dirname(os.path.abspath(__file__))
#     return os.path.join(base_path, relative_path)
#
# # --- CONFIGURATION SYSTEM ---
# DEFAULT_CONFIG = {
#     "model_settings": {
#         "model_path": "model.gguf",
#         "n_ctx": 2048,
#         "n_gpu_layers": -1,
#         "flash_attn": True,
#         "n_threads": 0,
#         "type_k": 8, "type_v": 8
#     },
#     "inference_params": {
#         "temperature": 0.3,
#         "min_p": 0.05,
#         "repeat_penalty": 1.1,
#         "max_tokens_buffer": 800
#     }
# }
#
# def load_config():
#     path = get_resource_path("config.json")
#     if not os.path.exists(path):
#         with open(path, "w") as f: json.dump(DEFAULT_CONFIG, f, indent=4)
#         return DEFAULT_CONFIG
#     try:
#         with open(path, "r") as f: return json.load(f)
#     except: return DEFAULT_CONFIG
#
# CONFIG = load_config()
# llm = None
#
# def get_llm():
#     global llm
#     if llm is None:
#         ms = CONFIG["model_settings"]
#         p = get_resource_path(ms["model_path"])
#         if not os.path.exists(p): raise FileNotFoundError(f"Missing model file: {p}")
#         llm = Llama(model_path=p, n_ctx=ms["n_ctx"], n_gpu_layers=ms["n_gpu_layers"],
#                     flash_attn=ms["flash_attn"], n_threads=ms["n_threads"] or os.cpu_count(), verbose=False)
#     return llm
#
# def get_params(dynamic_max=500):
#     p = CONFIG["inference_params"]
#     return {"temperature": p["temperature"], "min_p": p["min_p"], "repeat_penalty": p["repeat_penalty"],
#             "max_tokens": dynamic_max + p["max_tokens_buffer"], "stream": True}
#
# # --- GENERATORS ---
#
# def summarize_text(text):
#     model = get_llm(); model.reset()
#     stream = model.create_chat_completion(messages=[{"role": "system", "content": "Summarize concisely."}, {"role": "user", "content": text}], **get_params(250))
#     for chunk in stream:
#         if 'content' in chunk['choices'][0]['delta']: yield chunk['choices'][0]['delta']['content']
#
# def paraphrase_text(text, tone):
#     model = get_llm(); model.reset()
#     stream = model.create_chat_completion(messages=[{"role": "system", "content": f"Rewrite as {tone}."}, {"role": "user", "content": text}], **get_params(len(text)+100))
#     for chunk in stream:
#         if 'content' in chunk['choices'][0]['delta']: yield chunk['choices'][0]['delta']['content']
#
# def grammar_check(text):
#     model = get_llm(); model.reset()
#     stream = model.create_chat_completion(messages=[{"role": "system", "content": "Fix grammar. Output only text."}, {"role": "user", "content": text}], **get_params(len(text)+50))
#     for chunk in stream:
#         if 'content' in chunk['choices'][0]['delta']: yield chunk['choices'][0]['delta']['content']
#
# def translate_text(text, target_lang):
#     model = get_llm(); model.reset()
#     stream = model.create_chat_completion(messages=[{"role": "system", "content": f"Translate to {target_lang}."}, {"role": "user", "content": text}], **get_params(len(text)*2))
#     for chunk in stream:
#         if 'content' in chunk['choices'][0]['delta']: yield chunk['choices'][0]['delta']['content']
#
# def simplify_text(text):
#     model = get_llm(); model.reset()
#     stream = model.create_chat_completion(messages=[{"role": "system", "content": "Simplify for a child."}, {"role": "user", "content": text}], **get_params(len(text)))
#     for chunk in stream:
#         if 'content' in chunk['choices'][0]['delta']: yield chunk['choices'][0]['delta']['content']
#
# def extract_actions(text):
#     model = get_llm(); model.reset()
#     stream = model.create_chat_completion(messages=[{"role": "system", "content": "List action items as bullets."}, {"role": "user", "content": text}], **get_params(400))
#     for chunk in stream:
#         if 'content' in chunk['choices'][0]['delta']: yield chunk['choices'][0]['delta']['content']
#
# def expand_text(text):
#     model = get_llm(); model.reset()
#     stream = model.create_chat_completion(messages=[{"role": "system", "content": "Elaborate professionally."}, {"role": "user", "content": text}], **get_params(len(text)+400))
#     for chunk in stream:
#         if 'content' in chunk['choices'][0]['delta']: yield chunk['choices'][0]['delta']['content']
#
# def write_code_snippet(text):
#     model = get_llm(); model.reset()
#     stream = model.create_chat_completion(messages=[{"role": "system", "content": "Write clean code snippet."}, {"role": "user", "content": text}], **get_params(800))
#     for chunk in stream:
#         if 'content' in chunk['choices'][0]['delta']: yield chunk['choices'][0]['delta']['content']
#
# def generate_creative_text(text):
#     model = get_llm(); model.reset()
#     stream = model.create_chat_completion(messages=[{"role": "system", "content": "Be a creative writer."}, {"role": "user", "content": text}], **get_params(800))
#     for chunk in stream:
#         if 'content' in chunk['choices'][0]['delta']: yield chunk['choices'][0]['delta']['content']
#
# def suggest_replies(text):
#     model = get_llm(); model.reset()
#     prompt = f"Based on this message, suggest 3 distinct replies (Professional, Friendly, and Brief):\n{text}"
#     stream = model.create_chat_completion(messages=[{"role": "system", "content": "You suggest email/message replies."}, {"role": "user", "content": prompt}], **get_params(500))
#     for chunk in stream:
#         if 'content' in chunk['choices'][0]['delta']: yield chunk['choices'][0]['delta']['content']
#
# def analyze_sentiment(text):
#     model = get_llm(); model.reset()
#     prompt = f"Analyze the tone and sentiment of this text. Is it polite, aggressive, or professional? Give a quick summary:\n{text}"
#     stream = model.create_chat_completion(messages=[{"role": "system", "content": "You are a tone and sentiment analyzer."}, {"role": "user", "content": prompt}], **get_params(300))
#     for chunk in stream:
#         if 'content' in chunk['choices'][0]['delta']: yield chunk['choices'][0]['delta']['content']

import re, os, sys, json
from llama_cpp import Llama

def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

# --- CONFIGURATION SYSTEM ---
DEFAULT_CONFIG = {
    "model_settings": {
        "model_path": "model.gguf",
        "n_ctx": 2048,
        "n_gpu_layers": -1,
        "flash_attn": True,
        "n_threads": 0,
        "type_k": 8, "type_v": 8
    },
    "inference_params": {
        "temperature": 0.1, # Lowered for higher factual accuracy
        "min_p": 0.05,
        "repeat_penalty": 1.15, # Increased slightly to prevent loops
        "max_tokens_buffer": 800
    }
}

def load_config():
    path = get_resource_path("config.json")
    if not os.path.exists(path):
        with open(path, "w") as f: json.dump(DEFAULT_CONFIG, f, indent=4)
        return DEFAULT_CONFIG
    try:
        with open(path, "r") as f: return json.load(f)
    except: return DEFAULT_CONFIG

CONFIG = load_config()
llm = None

def get_llm():
    global llm
    if llm is None:
        ms = CONFIG["model_settings"]
        p = get_resource_path(ms["model_path"])
        if not os.path.exists(p): raise FileNotFoundError(f"Missing model file: {p}")
        llm = Llama(model_path=p, n_ctx=ms["n_ctx"], n_gpu_layers=ms["n_gpu_layers"],
                    flash_attn=ms["flash_attn"], n_threads=ms["n_threads"] or os.cpu_count(), verbose=False)
    return llm

def get_params(dynamic_max=500):
    p = CONFIG["inference_params"]
    return {"temperature": p["temperature"], "min_p": p["min_p"], "repeat_penalty": p["repeat_penalty"],
            "max_tokens": dynamic_max + p["max_tokens_buffer"], "stream": True}

# --- PRECISION GENERATORS ---

def summarize_text(text):
    model = get_llm(); model.reset()
    sys_msg = "You are a high-precision summarization engine. Condense the provided text into one single, factually accurate paragraph. Do not add outside information. Do not use phrases like 'The text says'."
    prompt = f"SOURCE TEXT:\n{text}\n\nTASK: Summarize the source above into a factual, concise paragraph."
    stream = model.create_chat_completion(messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": prompt}], **get_params(300))
    for chunk in stream:
        if 'content' in chunk['choices'][0]['delta']: yield chunk['choices'][0]['delta']['content']

def paraphrase_text(text, tone):
    model = get_llm(); model.reset()
    sys_msg = f"You are a rewriting expert. Rewrite the text to be {tone} in style. Maintain the exact original meaning and all factual details. Do not invent new facts."
    prompt = f"ORIGINAL TEXT:\n{text}\n\nTASK: Rewrite this in a {tone} tone."
    stream = model.create_chat_completion(messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": prompt}], **get_params(len(text)+150))
    for chunk in stream:
        if 'content' in chunk['choices'][0]['delta']: yield chunk['choices'][0]['delta']['content']

def grammar_check(text):
    model = get_llm(); model.reset()
    sys_msg = "You are a professional English editor. Fix all grammar, spelling, and punctuation errors. Maintain the user's original intent. Output ONLY the corrected text without any introduction or commentary."
    prompt = f"TEXT TO FIX:\n{text}\n\nFIXED TEXT:"
    stream = model.create_chat_completion(messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": prompt}], **get_params(len(text)+50))
    for chunk in stream:
        if 'content' in chunk['choices'][0]['delta']: yield chunk['choices'][0]['delta']['content']

def translate_text(text, target_lang):
    model = get_llm(); model.reset()
    sys_msg = f"You are a world-class translator. Translate the text into natural, fluent {target_lang}. Preserve the original tone and formatting exactly."
    prompt = f"ENGLISH TEXT:\n{text}\n\n{target_lang.upper()} TRANSLATION:"
    stream = model.create_chat_completion(messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": prompt}], **get_params(len(text)*2))
    for chunk in stream:
        if 'content' in chunk['choices'][0]['delta']: yield chunk['choices'][0]['delta']['content']

def simplify_text(text):
    model = get_llm(); model.reset()
    sys_msg = "You are a clear-communication expert. Rewrite complex information using simple words so that a 10-year-old could understand it perfectly. Keep the facts accurate."
    prompt = f"COMPLEX TEXT:\n{text}\n\nSIMPLE VERSION:"
    stream = model.create_chat_completion(messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": prompt}], **get_params(len(text)))
    for chunk in stream:
        if 'content' in chunk['choices'][0]['delta']: yield chunk['choices'][0]['delta']['content']

def extract_actions(text):
    model = get_llm(); model.reset()
    sys_msg = "You are a highly organized project assistant. Identify every specific task or action item mentioned in the text and list them clearly as bullet points. Ignore general conversation."
    prompt = f"SOURCE TEXT:\n{text}\n\nACTION ITEMS:"
    stream = model.create_chat_completion(messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": prompt}], **get_params(400))
    for chunk in stream:
        if 'content' in chunk['choices'][0]['delta']: yield chunk['choices'][0]['delta']['content']

def expand_text(text):
    model = get_llm(); model.reset()
    sys_msg = "You are a detailed professional writer. Expand the provided short text into a comprehensive, professional explanation. Add context and depth while staying strictly relevant to the original topic."
    prompt = f"SHORT TEXT:\n{text}\n\nDETAILED EXPANSION:"
    stream = model.create_chat_completion(messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": prompt}], **get_params(len(text)+400))
    for chunk in stream:
        if 'content' in chunk['choices'][0]['delta']: yield chunk['choices'][0]['delta']['content']

def write_code_snippet(text):
    model = get_llm(); model.reset()
    sys_msg = "You are a Senior Software Engineer. Provide only the code snippet requested with minimal, helpful comments. No conversational filler or explanations before or after the code."
    prompt = f"CODING REQUEST:\n{text}\n\nCODE:"
    stream = model.create_chat_completion(messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": prompt}], **get_params(800))
    for chunk in stream:
        if 'content' in chunk['choices'][0]['delta']: yield chunk['choices'][0]['delta']['content']

def generate_creative_text(text):
    model = get_llm(); model.reset()
    sys_msg = "You are a creative author. Generate high-quality literature, poetry, or storytelling based on the prompt. Use vivid imagery and professional style."
    prompt = f"PROMPT:\n{text}\n\nCREATIVE RESPONSE:"
    stream = model.create_chat_completion(messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": prompt}], **get_params(800))
    for chunk in stream:
        if 'content' in chunk['choices'][0]['delta']: yield chunk['choices'][0]['delta']['content']

def suggest_replies(text):
    model = get_llm(); model.reset()
    sys_msg = "You are a communication coach. Based on the incoming message, provide three distinct reply options: 1) Professional/Formal, 2) Friendly/Casual, and 3) Short/Direct."
    prompt = f"INCOMING MESSAGE:\n{text}\n\nREPLY OPTIONS:"
    stream = model.create_chat_completion(messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": prompt}], **get_params(500))
    for chunk in stream:
        if 'content' in chunk['choices'][0]['delta']: yield chunk['choices'][0]['delta']['content']

def analyze_sentiment(text):
    model = get_llm(); model.reset()
    sys_msg = "You are a sentiment analysis expert. Evaluate the tone, emotional state, and professional standing of the provided text. State if it is positive, negative, or neutral and explain why briefly."
    prompt = f"TEXT TO ANALYZE:\n{text}\n\nSENTIMENT ANALYSIS:"
    stream = model.create_chat_completion(messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": prompt}], **get_params(300))
    for chunk in stream:
        if 'content' in chunk['choices'][0]['delta']: yield chunk['choices'][0]['delta']['content']