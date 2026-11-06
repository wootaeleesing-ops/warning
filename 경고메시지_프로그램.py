import tkinter as tk
from tkinter import ttk, messagebox

class WarningPopupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("경고 메시지 만들기")
        self.root.geometry("560x500")
        self.root.minsize(500, 440)
        self.root.configure(bg="#f3f5f9")

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TButton", font=("맑은 고딕", 10), padding=8)
        style.configure("TLabel", background="#f3f5f9", font=("맑은 고딕", 10))
        style.configure("Header.TLabel", font=("맑은 고딕", 19, "bold"), foreground="#172033")
        style.configure("Hint.TLabel", foreground="#64748b", font=("맑은 고딕", 9))

        outer = ttk.Frame(root, padding=24)
        outer.pack(fill="both", expand=True)
        ttk.Label(outer, text="경고 메시지 만들기", style="Header.TLabel").pack(anchor="w")
        ttk.Label(outer, text="표시할 제목과 내용을 입력한 다음 미리보기 또는 띄우기를 누르세요.", style="Hint.TLabel").pack(anchor="w", pady=(5, 18))
        ttk.Label(outer, text="창 제목").pack(anchor="w")
        self.title_entry = ttk.Entry(outer, font=("맑은 고딕", 10))
        self.title_entry.insert(0, "알림")
        self.title_entry.pack(fill="x", pady=(5, 14))
        ttk.Label(outer, text="메시지 내용").pack(anchor="w")
        self.message_text = tk.Text(outer, height=7, wrap="word", font=("맑은 고딕", 11), padx=10, pady=10, relief="solid", bd=1)
        self.message_text.insert("1.0", "확인이 필요한 사항이 있습니다.")
        self.message_text.pack(fill="both", expand=True, pady=(5, 14))
        options = ttk.Frame(outer)
        options.pack(fill="x", pady=(0, 16))
        ttk.Label(options, text="아이콘").pack(side="left")
        self.icon_var = tk.StringVar(value="경고")
        self.icon_box = ttk.Combobox(options, textvariable=self.icon_var, values=["경고", "오류", "정보", "질문"], state="readonly", width=10)
        self.icon_box.pack(side="left", padx=(10, 20))
        self.topmost_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options, text="항상 위에 표시", variable=self.topmost_var).pack(side="left")
        buttons = ttk.Frame(outer)
        buttons.pack(fill="x")
        ttk.Button(buttons, text="미리보기", command=self.preview).pack(side="left")
        ttk.Button(buttons, text="경고창 띄우기", command=self.show_popup).pack(side="right")
        ttk.Label(outer, text="※ 이 프로그램은 사용자가 직접 실행하는 일반 알림창을 표시합니다.", style="Hint.TLabel").pack(anchor="w", pady=(16, 0))

    def get_values(self):
        title = self.title_entry.get().strip() or "알림"
        message = self.message_text.get("1.0", "end").strip()
        if not message:
            messagebox.showwarning("내용 필요", "표시할 메시지를 입력해 주세요.", parent=self.root)
            return None
        return title, message

    def show_popup(self):
        values = self.get_values()
        if not values:
            return
        title, message = values
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.configure(bg="#ffffff")
        popup.resizable(False, False)
        popup.transient(self.root)
        popup.attributes("-topmost", self.topmost_var.get())
        frame = tk.Frame(popup, bg="#ffffff", padx=24, pady=22)
        frame.pack(fill="both", expand=True)
        icon_text = {"경고": "⚠", "오류": "✖", "정보": "ℹ", "질문": "?"}.get(self.icon_var.get(), "⚠")
        icon_color = {"경고": "#d97706", "오류": "#dc2626", "정보": "#2563eb", "질문": "#0f766e"}.get(self.icon_var.get(), "#d97706")
        tk.Label(frame, text=icon_text, font=("맑은 고딕", 30, "bold"), fg=icon_color, bg="#ffffff").pack(side="left", anchor="n", padx=(0, 18))
        text_frame = tk.Frame(frame, bg="#ffffff")
        text_frame.pack(side="left", fill="both", expand=True)
        tk.Label(text_frame, text=title, font=("맑은 고딕", 13, "bold"), fg="#172033", bg="#ffffff", anchor="w").pack(fill="x")
        tk.Label(text_frame, text=message, font=("맑은 고딕", 10), fg="#334155", bg="#ffffff", justify="left", wraplength=340, anchor="w").pack(fill="x", pady=(8, 18))
        ttk.Button(text_frame, text="확인", command=popup.destroy).pack(anchor="e")
        popup.update_idletasks()
        x = self.root.winfo_rootx() + (self.root.winfo_width() - popup.winfo_width()) // 2
        y = self.root.winfo_rooty() + (self.root.winfo_height() - popup.winfo_height()) // 2
        popup.geometry(f"+{max(0, x)}+{max(0, y)}")
        popup.grab_set()
        popup.focus_force()

    def preview(self):
        values = self.get_values()
        if not values:
            return
        title, message = values
        fn = {"경고": messagebox.showwarning, "오류": messagebox.showerror, "정보": messagebox.showinfo, "질문": messagebox.askyesno}.get(self.icon_var.get(), messagebox.showwarning)
        fn(title, message, parent=self.root)

if __name__ == "__main__":
    root = tk.Tk()
    app = WarningPopupApp(root)
    root.mainloop()
