# 🤖 Local AI Assistant

**An offline, always-on-top AI writing toolkit for Windows — one hotkey away.**

Press <kbd>Alt</kbd>+<kbd>C</kbd>, pick a tool, and get AI help on whatever you're doing. No browser, no API keys, no internet, no data leaving your machine. Everything runs on a local [LiquidAI LFM2-700M](https://huggingface.co/LiquidAI/LFM2-700M) GGUF model via [llama.cpp](https://github.com/ggml-org/llama.cpp).

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11-0078D4?logo=windows&logoColor=white)
![UI](https://img.shields.io/badge/UI-CustomTkinter-1f6feb)
![Inference](https://img.shields.io/badge/inference-llama.cpp-000000)
![Offline](https://img.shields.io/badge/100%25-offline-success)

---

## ✨ Features

- **Fully offline** — inference runs locally through `llama_cpp_python`. Nothing is sent anywhere.
- **Global hotkey launcher** — <kbd>Alt</kbd>+<kbd>C</kbd> summons a floating menu at your cursor, from any app.
- **11 built-in writing tools** — summarise, paraphrase, fix grammar, translate, and more.
- **Streaming output** — tokens appear as they're generated, with `<think>` reasoning blocks automatically filtered out.
- **Works inside other apps** — paste straight from your clipboard and push the result back with **Replace** (auto-pastes into the window you were using).
- **Frameless, draggable, always-on-top windows** — stays where you put it, never steals focus from your work.
- **Single-instance guard** — a Windows mutex prevents duplicate copies of the app from running.
- **JSON-configurable** — swap models, tune temperature, threads and GPU offload without touching code.

---

## 🧰 Tools

| Tool | What it does |
| --- | --- |
| 📝 **Summarise** | Condenses long text into one factual paragraph |
| 🔄 **Paraphrase** | Rewrites text in a chosen tone — Professional, Casual, Sarcastic, Academic, or your own |
| ✅ **Fix Grammar** | Corrects grammar, spelling and punctuation, returns the text only |
| 🌐 **Translate** | Translates into Spanish, French, German, Chinese, Japanese or Arabic |
| 👶 **Simplify (ELI5)** | Explains complex text so a 10-year-old could follow |
| 📋 **Action Points** | Extracts tasks and action items as bullet points |
| 📈 **Expand Text** | Turns a short note into a detailed, professional explanation |
| 💻 **Code Snippet** | Generates clean code with minimal comments, no filler |
| ✍️ **Creative Writer** | Stories, poetry and copy with vivid imagery |
| ✉️ **Reply Suggester** | Three reply options: formal, friendly, short |
| 🧠 **Tone Analyzer** | Detects sentiment and professional tone with a short justification |

---

## ⚙️ How it works

```
Alt+C ──▶ Hotkey thread ──▶ queue.Queue ──▶ Tk main thread
                                              │
                                              ▼
                                     Launcher window
                                              │  pick a tool
                                              ▼
                    ┌────────────── Tool window (CTkToplevel) ──────────────┐
                    │  input textbox ──▶ Backend.<tool_function>()          │
                    │                              │                        │
                    │                     llama.cpp streaming               │
                    │                              │                        │
                    │  output textbox ◀── root.after(0, insert chunk)       │
                    └───────────────────────────────────────────────────────┘
```

Two design details worth knowing:

- **Hotkeys never touch Tk directly.** `keyboard` runs its own thread, so it only pushes a message onto a `queue.Queue`. The Tk loop drains that queue every 100 ms — no cross-thread widget access, no crashes.
- **The model is loaded lazily and kept in memory.** The first run of a tool pays a one-time load cost; later calls reuse the same `Llama` instance and call `reset()` to clear the KV cache.

---

## 📋 Requirements

| | |
| --- | --- |
| OS | Windows 10 / 11 (uses `ctypes` mutex, `pywinstyles`, Win32 title-bar styling) |
| Python | 3.11 (tested on 3.11.9) |
| RAM | ~1.5 GB free (model is ~470 MB on disk) |
| GPU | Optional — Metal/CUDA/Vulkan offload enabled by default via `n_gpu_layers: -1` |
| Model | **LFM2-700M Q4_K_M** GGUF (~470 MB), *not* included in this repo |

Python dependencies:

```txt
customtkinter==5.2.2
llama_cpp_python==0.3.16
keyboard==0.13.5
pyperclip==1.11.0
pyautogui==0.9.54
pywinstyles==1.8
pillow==12.0.0
```

---

## 🚀 Getting started

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/local-ai-assistant.git
cd local-ai-assistant
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

<details>
<summary><strong>No requirements.txt yet? Paste this.</strong></summary>

```powershell
pip install customtkinter==5.2.2 llama_cpp_python==0.3.16 keyboard==0.13.5 pyperclip==1.11.0 pyautogui==0.9.54 pywinstyles==1.8 pillow==12.0.0
```

</details>

> GPU users: install the CUDA wheel for `llama_cpp_python` instead, e.g.
> `pip install llama_cpp_python==0.3.16 --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu124`

### 4. Download the model

Grab a quantised GGUF and save it in the project root as **`model.gguf`**:

```
Tool/
├── AI_Assistant.py
├── Backend.py
├── config.json
└── model.gguf        <-- ~470 MB, download separately
```

Recommended: `LFM2-700M-Q4_K_M.gguf` from [unsloth/LFM2-700M-GGUF](https://huggingface.co/unsloth/LFM2-700M-GGUF).

Any GGUF that supports the ChatML-style template will work — point `model_settings.model_path` at it in `config.json`.

### 5. Run it

```powershell
python AI_Assistant.py
```

The app starts hidden. Press <kbd>Alt</kbd>+<kbd>C</kbd> to open the menu.

> No console window desired? Launch with `pythonw AI_Assistant.py`.

---

## 🖱️ Usage

1. Press <kbd>Alt</kbd>+<kbd>C</kbd> — the AI menu opens at your cursor.
2. Pick a tool (e.g. ✅ Fix Grammar).
3. Click **Paste Clipboard** to pull in text you copied from anywhere, or type directly.
4. Hit **🚀 RUN AI** and watch the answer stream in.
5. **📋 Copy** copies the result, or **↩ Replace** hides the window, copies the result and pastes it into the app you were last using.

Drag any window by its title bar. Click ✕ to hide it (the app keeps running). Use **🛑 Quit App** in the menu to exit fully.

---

## 🔧 Configuration

Settings live in `config.json` (created from defaults on first run if missing):

```json
{
  "model_settings": {
    "model_path": "model.gguf",
    "n_ctx": 2048,
    "n_gpu_layers": -1,
    "flash_attn": true,
    "n_threads": 8,
    "type_k": 8,
    "type_v": 8
  },
  "inference_params": {
    "temperature": 0.2,
    "min_p": 0.05,
    "repeat_penalty": 1.1,
    "max_tokens_buffer": 500
  }
}
```

| Key | Meaning |
| --- | --- |
| `model_path` | Path to the GGUF, relative to the script or `.exe` |
| `n_ctx` | Context window in tokens (input + output share this) |
| `n_gpu_layers` | Layers offloaded to GPU — `-1` = all, `0` = pure CPU |
| `flash_attn` | Flash attention (needs a compatible backend) |
| `n_threads` | CPU threads; `0` = use all cores |
| `temperature` | Lower = more factual and repeatable |
| `min_p` | Min-p sampling threshold |
| `repeat_penalty` | Penalty for repeated tokens; raise if output loops |
| `max_tokens_buffer` | Headroom added to each task's estimated token budget |

> `type_k` / `type_v` are reserved for KV-cache quantisation and are currently **not** forwarded to llama.cpp.

Changed `config.json` while the app is open? Restart it — the model is loaded once and cached.

---

## 📁 Project structure

```
Tool/
├── AI_Assistant.py   # Entry point: mutex guard, hotkey, launcher + tool windows, streaming UI
├── Backend.py        # Model loader, config handling, one streaming generator per tool
├── backup.py         # Earlier single-file prototype (reference only, not used at runtime)
├── config.json       # Model + inference settings
├── model.gguf        # Local quantised model (git-ignored, download separately)
└── requirements.txt  # Python dependencies
```

`AI_Assistant.py` → `Backend.py` is the only real dependency edge: the UI layer never imports `llama_cpp` itself.

---

## 🩺 Troubleshooting

| Problem | Fix |
| --- | --- |
| **"❌ Model missing!"** | `model.gguf` isn't next to the script (or where `model_path` points). Check the spelling and the working directory. |
| **Hotkey does nothing** | Another app owns <kbd>Alt</kbd>+<kbd>C</kbd>. Change it in `AI_Assistant.py` (`keyboard.add_hotkey('alt+c', ...)`). |
| **Hotkeys work only as admin** | Windows blocks low-level hooks for non-elevated apps when the target app is elevated. Run the assistant as administrator too. |
| **App exits immediately on launch** | That's the single-instance mutex — an instance is already running. Check Task Manager. |
| **Slow responses / high CPU** | Lower `n_threads`, shorten the input, or reduce `max_tokens_buffer`. A 700M model is fast on CPU but not instant on long text. |
| **GPU not used / crash on load** | Set `n_gpu_layers` to `0` and re-run. Some builds need `flash_attn: false`. |
| **Output loops or repeats** | Increase `repeat_penalty` (e.g. `1.2`) and/or lower `temperature`. |
| **Input silently truncated** | `n_ctx` is 2048 tokens. Very long text gets clipped — split it up. |
| **Replace pastes into the wrong window** | Focus the target window before clicking **↩ Replace**; the 0.4 s delay is there to let focus settle. |

---

## 🔒 Privacy

No telemetry, no network calls, no cloud provider. The only outbound traffic is the one-time model download you do yourself. Your text and the model's output stay in RAM and, if you choose, on your clipboard.

---

## ⚠️ Known limitations

- **700M parameters** — great for rewriting and formatting, not for deep reasoning or factual research. Bad output is a model limit, not a bug.
- **One tool window at a time** — opening a new tool closes the previous one.
- **No history** — output is never saved; copy it before closing.
- **Windows only** — relies on Win32 APIs for the mutex and window styling.
- **English-centric prompts** — the translate tool works, but prompts and tones are English-first.
- **`backup.py` is dead code** — an earlier prototype kept for reference.

---

## 🗺️ Roadmap

- [ ] Streaming stop / cancel button
- [ ] Custom prompt tool with a saved-prompt library
- [ ] Configurable hotkey and system-tray icon
- [ ] Response history with pinning
- [ ] PyInstaller build script for a single `.exe`
- [ ] macOS / Linux support behind a platform layer

---

## 🤝 Contributing

Issues and PRs are welcome. If you're adding a tool:

1. Add a generator to `Backend.py` that `yield`s text chunks (`get_params(...)` + `get_llm().reset()`).
2. Add an entry to `menu_items` and `titles` in `AI_Assistant.py`.
3. Add the `elif mode == ...` branch in `run_logic`.

Keep prompts strict about output format — this model follows short, imperative system prompts best.

---

## 🙏 Acknowledgements

- [LiquidAI / LFM2](https://huggingface.co/LiquidAI) — the model this was built around
- [Unsloth](https://huggingface.co/unsloth) — quantised GGUF release
- [llama.cpp](https://github.com/ggml-org/llama.cpp) and [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- [keyboard](https://github.com/boppreh/keyboard), [PyAutoGUI](https://github.com/asweigart/pyautogui), [pyperclip](https://github.com/asweigart/pyperclip), [pywinstyles](https://github.com/Akascape/py-window-styles)

---

## 📄 License

No license has been added yet — add a `LICENSE` file (MIT is a good default) before publishing. Note that the model weights carry their own license (see the LFM2 model card).
