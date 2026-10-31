import customtkinter as ctk
import threading, keyboard, pyperclip, pyautogui, time, queue, os, sys
import pywinstyles
import Backend
import ctypes

# --- 1. SYSTEM MUTEX (PREVENTS DOUBLE-OPENING) ---
# This works even if the window hasn't loaded yet.
MUTEX_NAME = "Local_AI_Assistant_Unique_Mutex_ID"
kernel32 = ctypes.windll.kernel32
mutex = kernel32.CreateMutexW(None, False, MUTEX_NAME)
if kernel32.GetLastError() == 183:  # ERROR_ALREADY_EXISTS
    sys.exit(0)

# UI Global Settings
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


class DraggableBase(ctk.CTkToplevel):
    def __init__(self, parent, width, height, title="AI Assistant"):
        super().__init__(parent)
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.width, self.height = width, height
        self.configure(fg_color="white")

        try:
            pywinstyles.apply_style(self, "light")
            pywinstyles.set_opacity(self, value=0.98)
        except:
            pass

        self.title_bar = ctk.CTkFrame(self, height=35, fg_color="#F3F3F3", corner_radius=0)
        self.title_bar.pack(fill="x", side="top")

        self.title_lbl = ctk.CTkLabel(self.title_bar, text=title, font=("Segoe UI Variable Bold", 12),
                                      text_color="#333")
        self.title_lbl.pack(side="left", padx=15)

        self.close_btn = ctk.CTkButton(self.title_bar, text="✕", width=38, height=35, fg_color="transparent",
                                       hover_color="#e81123", text_color="black", corner_radius=0,
                                       command=self.withdraw)
        self.close_btn.pack(side="right")

        self.title_bar.bind("<ButtonPress-1>", self.start_drag)
        self.title_bar.bind("<B1-Motion>", self.do_drag)

    def start_drag(self, event):
        self.x, self.y = event.x, event.y

    def do_drag(self, event):
        dx, dy = event.x - self.x, event.y - self.y
        self.geometry(f"+{self.winfo_x() + dx}+{self.winfo_y() + dy}")

    def show(self):
        x, y = pyautogui.position()
        self.geometry(f"{self.width}x{self.height}+{x}+{y}")
        self.deiconify()
        self.focus_force()


class AIApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.withdraw()
        self.queue = queue.Queue()

        # Global Hotkey
        keyboard.add_hotkey('alt+c', lambda: self.queue.put("TOGGLE_LAUNCHER"), suppress=False)

        self.launcher = None
        self.tool_window = None
        self.process_queue()

    def process_queue(self):
        try:
            while not self.queue.empty():
                msg = self.queue.get_nowait()
                if msg == "TOGGLE_LAUNCHER": self.toggle_launcher()
        except:
            pass
        self.root.after(100, self.process_queue)

    def toggle_launcher(self):
        if self.launcher and self.launcher.winfo_exists():
            if self.launcher.state() == "normal" and self.launcher.winfo_viewable():
                self.launcher.withdraw()
            else:
                self.launcher.show()
            return
        self.show_launcher()

    def show_launcher(self):
        self.launcher = DraggableBase(self.root, 240, 520, title="🤖 AI Menu")

        menu_items = [
            ("📝 Summarise", "Sum"), ("🔄 Paraphrase", "Para"), ("✅ Fix Grammar", "Gram"),
            ("🌐 Translate", "Trans"), ("👶 Simplify (ELI5)", "Simp"), ("📋 Action Points", "Acts"),
            ("📈 Expand Text", "Expd"), ("💻 Code Snippet", "Code"), ("✍️ Creative Writer", "Write"),
            ("✉️ Reply Suggester", "Reply"), ("🧠 Tone Analyzer", "Tone")
        ]

        for text, mode in menu_items:
            ctk.CTkButton(self.launcher, text=text, anchor="w", height=40, fg_color="transparent",
                          text_color="black", hover_color="#f0f0f0", font=("Segoe UI Variable", 13),
                          command=lambda m=mode: self.open_tool(m)).pack(fill="x", padx=8, pady=1)

        ctk.CTkLabel(self.launcher, text="", height=2).pack()
        ctk.CTkButton(self.launcher, text="🛑 Quit App", anchor="w", height=40,
                      fg_color="#fee", text_color="#c00", hover_color="#fdd",
                      font=("Segoe UI Variable Bold", 13),
                      command=self.quit_app).pack(fill="x", padx=8, pady=5)
        self.launcher.show()

    def quit_app(self):
        keyboard.unhook_all()
        self.root.quit()
        sys.exit(0)

    def open_tool(self, mode):
        if self.tool_window and self.tool_window.winfo_exists(): self.tool_window.destroy()

        titles = {"Sum": "Summariser", "Para": "Paraphraser", "Gram": "Grammar Fixer", "Trans": "Translator",
                  "Simp": "Simplifier", "Acts": "Action Points", "Expd": "Expander", "Code": "Coder",
                  "Write": "Creative Writer", "Reply": "Reply Suggester", "Tone": "Tone Analyzer"}

        w, h = 440, (620 if mode in ["Para", "Trans"] else 550)
        self.tool_window = DraggableBase(self.root, w, h, title=f"AI - {titles[mode]}")

        container = ctk.CTkFrame(self.tool_window, fg_color="white")
        container.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        ctk.CTkLabel(container, text="INPUT / PROMPT", font=("Segoe UI Variable Bold", 10), text_color="#999").pack(
            anchor="w", pady=(10, 0))
        input_txt = ctk.CTkTextbox(container, height=120, fg_color="#fcfcfc", border_width=1, border_color="#ddd",
                                   text_color="black", wrap="word")
        input_txt.pack(fill="x", pady=(5, 5))
        ctk.CTkButton(container, text="Paste Clipboard", height=24, fg_color="#eee", text_color="black",
                      command=lambda: input_txt.insert("end", pyperclip.paste())).pack(pady=(0, 10))

        lang_var, tone_var, custom_tone = ctk.StringVar(value="Spanish"), ctk.StringVar(value="Professional"), None
        if mode == "Trans":
            f = ctk.CTkFrame(container, fg_color="#f9f9f9")
            f.pack(fill="x", pady=(0, 10))
            ctk.CTkOptionMenu(f, values=["Spanish", "French", "German", "Chinese", "Japanese", "Arabic"],
                              variable=lang_var).pack(padx=10, pady=10)
        elif mode == "Para":
            f = ctk.CTkFrame(container, fg_color="#f9f9f9")
            f.pack(fill="x", pady=(0, 10))
            ctk.CTkOptionMenu(f, values=["Professional", "Casual", "Sarcastic", "Academic"], variable=tone_var).pack(
                padx=10, pady=5)
            custom_tone = ctk.CTkEntry(f, placeholder_text="Or custom tone...", text_color="black", fg_color="white")
            custom_tone.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(container, text="🚀 RUN AI", height=42, fg_color="#0078d4",
                      command=lambda: self.run_logic(mode, input_txt, output_txt, status_lbl, lang_var, tone_var,
                                                     custom_tone)).pack(fill="x", pady=5)
        status_lbl = ctk.CTkLabel(container, text="Ready", font=("Segoe UI Variable", 11), text_color="#666");
        status_lbl.pack()

        footer = ctk.CTkFrame(container, fg_color="transparent")
        footer.pack(fill="x", side="bottom", pady=(5, 0))
        ctk.CTkButton(footer, text="📋 Copy", fg_color="#333",
                      command=lambda: pyperclip.copy(output_txt.get("1.0", "end-1c"))).pack(side="left", expand=True,
                                                                                            fill="x")
        ctk.CTkButton(footer, text="↩ Replace", fg_color="#0078d4",
                      command=lambda: self.replace_logic(output_txt.get("1.0", "end-1c"))).pack(side="left",
                                                                                                padx=(10, 0))

        output_txt = ctk.CTkTextbox(container, fg_color="#fcfcfc", border_width=1, border_color="#ddd",
                                    text_color="black", wrap="word")
        output_txt.pack(fill="both", expand=True, pady=(5, 5))
        self.tool_window.show()

    def run_logic(self, mode, in_w, out_w, stat_w, lang, tone, custom):
        text = in_w.get("1.0", "end-1c").strip()
        if not text: return
        m_path = Backend.get_resource_path(Backend.CONFIG["model_settings"]["model_path"])
        if not os.path.exists(m_path):
            stat_w.configure(text="❌ Model missing!", text_color="red");
            return

        out_w.delete("1.0", "end")
        stat_w.configure(text="⌛ AI is thinking...", text_color="#0078d4")
        final_tone = custom.get() if custom and custom.get().strip() else tone.get()

        def task():
            try:
                if mode == "Sum":
                    gen = Backend.summarize_text(text)
                elif mode == "Gram":
                    gen = Backend.grammar_check(text)
                elif mode == "Para":
                    gen = Backend.paraphrase_text(text, final_tone)
                elif mode == "Trans":
                    gen = Backend.translate_text(text, lang.get())
                elif mode == "Simp":
                    gen = Backend.simplify_text(text)
                elif mode == "Acts":
                    gen = Backend.extract_actions(text)
                elif mode == "Expd":
                    gen = Backend.expand_text(text)
                elif mode == "Code":
                    gen = Backend.write_code_snippet(text)
                elif mode == "Write":
                    gen = Backend.generate_creative_text(text)
                elif mode == "Reply":
                    gen = Backend.suggest_replies(text)
                elif mode == "Tone":
                    gen = Backend.analyze_sentiment(text)

                is_thinking = False
                for chunk in gen:
                    if "<think>" in chunk: is_thinking = True; continue
                    if "</think>" in chunk: is_thinking = False; continue
                    if not is_thinking:
                        self.root.after(0, lambda c=chunk: out_w.insert("end", c))
                        self.root.after(0, lambda: out_w.see("end"))
                self.root.after(0, lambda: stat_w.configure(text="✅ Done", text_color="green"))
            except Exception as e:
                err_str = str(e)
                self.root.after(0, lambda m=err_str: stat_w.configure(text=f"Error: {m}", text_color="red"))

        threading.Thread(target=task, daemon=True).start()

    def replace_logic(self, result):
        if not result.strip(): return
        self.tool_window.withdraw()
        pyperclip.copy(result);
        time.sleep(0.4);
        pyautogui.hotkey('ctrl', 'v')

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AIApp()
    app.run()