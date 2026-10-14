"""Workspace navigation and actionable home, using the existing business screens."""

import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk

from PIL import Image, ImageDraw, ImageTk

# Every section points to a real existing workflow, including recovery tools.
SECTIONS = [('Khu vực làm việc', 'session_view', 'Kho đang quản lý', 'Chọn kho, quản lý phiên và bảo mật tài khoản'), ('Dữ liệu', 'master_container', 'Sản phẩm & danh mục', 'Sản phẩm, ảnh, mô tả, đơn vị, kho và đối tác'), ('Nhập hàng', 'order_view', 'Đơn mua / đơn bán', 'Lập và theo dõi đơn hàng theo kho'), ('Nhập hàng', 'approval_view', 'Duyệt chứng từ', 'Rà soát chứng từ và quyết định theo thẩm quyền'), ('Nhập hàng', 'receipt_view', 'Nhận hàng', 'Ghi nhận hàng nhận và đối chiếu đơn mua'), ('Nhập hàng', 'opening_view', 'Tồn đầu kỳ', 'Khởi tạo tồn kho có kiểm đếm và phê duyệt'), ('Vận hành kho', 'issue_view', 'Giữ tồn & xuất hàng', 'Giữ chỗ, kiểm tra khả dụng và ghi nhận xuất hàng'), ('Kiểm soát', 'report_view', 'Tra cứu tồn & báo cáo', 'Tra cứu tồn, thẻ kho và xuất dữ liệu'), ('Tiện ích & quản trị', 'print_view', 'In phiếu & nhãn hàng', 'Xem trước, tạo phiếu và nhãn hàng hóa'), ('Tiện ích & quản trị', 'admin_view', 'Tài khoản & phân quyền', 'Quản lý người dùng, vai trò và phạm vi kho'), ('Tiện ích & quản trị', 'recovery_view', 'Bản nháp & khôi phục', 'Kiểm tra lệnh chưa rõ kết quả trước khi thao tác lại'), ('Tiện ích & quản trị', 'connection_view', 'Kiểm tra kết nối', 'Kiểm tra kết nối và trạng thái sẵn sàng của máy chủ')]


class _NavigationHighlight(tk.Canvas):
    """Rounded active-page surface; the native tree still owns navigation."""

    def __init__(self, tree, command):
        super().__init__(tree, highlightthickness=0, borderwidth=0, cursor="hand2", takefocus=False)
        self.tree, self.command = tree, command
        self.key = None
        self.photo = None
        self.photo_size = None
        self.job = None
        self.closed = False
        self.label_font = tkfont.Font(self, family="Arial", size=10, weight="bold")
        self.bind("<Button-1>", self.activate)
        for sequence in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
            self.bind(sequence, self.scroll)
        for sequence in ("<Configure>", "<Map>", "<<ThemeChanged>>", "<<TreeviewOpen>>",
                         "<<TreeviewClose>>", "<KeyRelease>", "<ButtonRelease-1>"):
            tree.bind(sequence, lambda event: self.redraw(), add="+")

    def activate(self, event=None):
        self.tree.focus_set()
        if self.key:
            self.tree.selection_set(self.key)
            self.tree.focus(self.key)
            self.command(self.key)
        return "break"

    def scroll(self, event):
        upward = getattr(event, "num", None) == 4 or getattr(event, "delta", 0) > 0
        self.tree.yview_scroll(-3 if upward else 3, "units")
        return "break"

    def redraw(self):
        if not self.closed and self.job is None:
            self.job = self.after_idle(self.paint)

    def paint(self):
        self.job = None
        bounds = self.tree.bbox(self.key) if self.key and self.tree.exists(self.key) else ()
        if not bounds:
            self.place_forget()
            return
        _, y, _, height = bounds
        width = max(1, self.tree.winfo_width() - 4)
        self.place(x=2, y=y, width=width, height=height)
        background = ttk.Style(self).lookup("Nav.Treeview", "background") or "#ffffff"
        self.configure(background=background)
        if self.photo_size != (width, height):
            # This is a UI selection background, not a hand-drawn icon.
            scale = 3
            image = Image.new("RGBA", (width * scale, height * scale))
            draw = ImageDraw.Draw(image)
            for x in range(image.width):
                ratio = x / max(1, image.width - 1)
                color = tuple(round(a + (b - a) * ratio) for a, b in zip((24, 116, 69), (55, 145, 87)))
                draw.line((x, 0, x, image.height), fill=(*color, 255))
            mask = Image.new("L", image.size)
            ImageDraw.Draw(mask).rounded_rectangle((0, 3, image.width - 1, image.height - 4),
                                                   radius=image.height // 2, fill=255)
            image.putalpha(mask)
            self.photo = ImageTk.PhotoImage(image.resize((width, height), Image.Resampling.LANCZOS), master=self)
            self.photo_size = (width, height)
        self.delete("all")
        self.create_image(0, 0, image=self.photo, anchor="nw")
        title = self.tree.item(self.key, "text")
        if self.label_font.measure(title) > width - 26:
            while title and self.label_font.measure(title + "…") > width - 26:
                title = title[:-1]
            title += "…"
        self.create_text(13, height / 2, text=title, anchor="w", fill="#ffffff", font=self.label_font)

    def destroy(self):
        self.closed = True
        if self.job is not None:
            self.after_cancel(self.job)
            self.job = None
        self.photo = self.label_font = self.command = None
        super().destroy()


class AdminNavigation(ttk.Frame):
    def __init__(self, parent, command):
        super().__init__(parent, padding=(8, 12, 6, 8), width=254)
        self.command = command
        ttk.Label(self, text="ĐIỀU HÀNH KHO", style="Muted.TLabel", font=("Segoe UI", 9, "bold")).pack(
            anchor="w", padx=8, pady=(0, 16)
        )
        self.tree = ttk.Treeview(self, show="tree", selectmode="browse", style="Nav.Treeview", takefocus=True)
        self.tree.column("#0", width=234, minwidth=214, stretch=True)
        scroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scroll.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(fill="both", expand=True)
        groups = {}
        for group, key, title, _ in SECTIONS:
            if group not in groups:
                groups[group] = "group_" + str(len(groups))
                self.tree.insert("", "end", iid=groups[group], text=group, open=True, tags=("group",))
            self.tree.insert(groups[group], "end", iid=key, text=title)
        self.tree.tag_configure("group", font=("Segoe UI", 9, "bold"))
        self.tree.bind("<ButtonRelease-1>", self.activate)
        self.tree.bind("<Return>", self.activate)
        self.tree.bind("<space>", self.activate)
        self.highlight = _NavigationHighlight(self.tree, command)

        def scrolled(first, last):
            scroll.set(first, last)
            self.highlight.redraw()

        self.tree.configure(yscrollcommand=scrolled)

    def activate(self, event=None):
        if event is not None and getattr(event, "num", None) == 1:
            clicked = self.tree.identify_row(event.y)
            # Clicking a group's disclosure arrow may leave the old leaf selected.
            # Let Treeview collapse it without reopening that leaf's screen.
            if not clicked or clicked.startswith("group_"):
                return
        selection = self.tree.selection()
        if selection and not selection[0].startswith("group_"):
            self.command(selection[0])

    def select(self, key):
        if self.tree.exists(key):
            self.highlight.key = key
            self.tree.selection_set(key)
            self.tree.see(key)
            self.highlight.redraw()
