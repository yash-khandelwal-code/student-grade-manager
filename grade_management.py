# Grade Management System

import tkinter as tk
from tkinter import messagebox, font
import turtle
import random

# ---- some global stuff ----
students = {}  # storing students here, name -> list of marks

BG = "#1a1a2e"
CARD = "#16213e"
ACCENT = "#e94560"
GREEN = "#0f9b58"
TEXT = "#eaeaea"
MUTED = "#888"

# ---------- turtle chart function ----------
def show_turtle_chart(name, marks):
    """draws a bar chart using turtle for the selected student"""
    subjects = ["Math", "Science", "English", "Hindi", "CS"]

    win = turtle.Screen()
    win.title(f"Marks Chart - {name}")
    win.bgcolor("#1a1a2e")
    win.setup(width=650, height=450)

    t = turtle.Turtle()
    t.speed(6)
    t.hideturtle()

    colors = ["#e94560", "#0f9b58", "#f5a623", "#4a90e2", "#bd10e0"]

    # draw axes
    t.pencolor("#888888")
    t.pensize(2)
    t.penup()
    t.goto(-270, -150)
    t.pendown()
    t.goto(-270, 200)   # y axis
    t.penup()
    t.goto(-270, -150)
    t.pendown()
    t.goto(300, -150)   # x axis

    # draw bars
    bar_width = 70
    gap = 20
    x_start = -230

    for i, (subj, mark) in enumerate(zip(subjects, marks)):
        bar_height = int(mark * 3)  # scale marks
        x = x_start + i * (bar_width + gap)

        # draw bar
        t.penup()
        t.goto(x, -150)
        t.pendown()
        t.fillcolor(colors[i])
        t.begin_fill()
        t.goto(x, -150 + bar_height)
        t.goto(x + bar_width, -150 + bar_height)
        t.goto(x + bar_width, -150)
        t.goto(x, -150)
        t.end_fill()

        # subject label
        t.penup()
        t.goto(x + bar_width // 2, -175)
        t.pencolor("#eaeaea")
        t.write(subj, align="center", font=("Arial", 9, "normal"))

        # mark on top of bar
        t.goto(x + bar_width // 2, -150 + bar_height + 5)
        t.write(str(mark), align="center", font=("Arial", 9, "bold"))

    # title
    t.penup()
    t.goto(0, 215)
    t.pencolor("#e94560")
    t.write(f"Marks Chart: {name}", align="center", font=("Arial", 14, "bold"))

    win.mainloop()


# ---------- main app ----------
class GradeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Grade Manager")
        self.root.geometry("860x580")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.build_ui()

    def build_ui(self):
        # ---- header ----
        header = tk.Frame(self.root, bg=ACCENT, height=55)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="  📊 Student Grade Manager",
                 bg=ACCENT, fg="white",
                 font=("Courier New", 16, "bold")).pack(side="left", padx=10, pady=10)

        tk.Label(header, text="Unit 5 Project  ",
                 bg=ACCENT, fg="white",
                 font=("Courier New", 9)).pack(side="right", padx=10)

        # ---- main layout ----
        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=15, pady=10)

        # LEFT PANEL - input form
        left = tk.Frame(body, bg=CARD, width=340, relief="flat", bd=0)
        left.pack(side="left", fill="y", padx=(0, 10))
        left.pack_propagate(False)

        tk.Label(left, text="Add Student", bg=CARD, fg=ACCENT,
                 font=("Courier New", 13, "bold")).pack(pady=(15, 5))

        tk.Frame(left, bg=ACCENT, height=2).pack(fill="x", padx=20)

        # name field
        tk.Label(left, text="Student Name:", bg=CARD, fg=TEXT,
                 font=("Courier New", 10)).pack(anchor="w", padx=20, pady=(12, 2))
        self.name_var = tk.StringVar()
        name_entry = tk.Entry(left, textvariable=self.name_var,
                              bg="#0d1b2a", fg=TEXT, insertbackground=TEXT,
                              font=("Courier New", 11), relief="flat", bd=5)
        name_entry.pack(fill="x", padx=20)

        # marks fields
        subjects = ["Math", "Science", "English", "Hindi", "CS"]
        self.mark_vars = []
        for subj in subjects:
            tk.Label(left, text=f"{subj} Marks (0-100):", bg=CARD, fg=TEXT,
                     font=("Courier New", 10)).pack(anchor="w", padx=20, pady=(8, 2))
            var = tk.StringVar()
            e = tk.Entry(left, textvariable=var,
                         bg="#0d1b2a", fg=TEXT, insertbackground=TEXT,
                         font=("Courier New", 11), relief="flat", bd=5)
            e.pack(fill="x", padx=20)
            self.mark_vars.append(var)

        # buttons
        btn_frame = tk.Frame(left, bg=CARD)
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="➕ Add Student", command=self.add_student,
                  bg=ACCENT, fg="white", font=("Courier New", 10, "bold"),
                  relief="flat", padx=12, pady=6, cursor="hand2").pack(side="left", padx=5)

        tk.Button(btn_frame, text="🗑 Clear", command=self.clear_form,
                  bg="#333", fg=TEXT, font=("Courier New", 10),
                  relief="flat", padx=12, pady=6, cursor="hand2").pack(side="left", padx=5)

        # RIGHT PANEL - student list + results
        right = tk.Frame(body, bg=BG)
        right.pack(side="left", fill="both", expand=True)

        tk.Label(right, text="Student Records", bg=BG, fg=ACCENT,
                 font=("Courier New", 13, "bold")).pack(anchor="w")

        tk.Frame(right, bg=ACCENT, height=2).pack(fill="x", pady=(2, 8))

        # listbox with scrollbar
        list_frame = tk.Frame(right, bg=BG)
        list_frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self.listbox = tk.Listbox(list_frame, bg=CARD, fg=TEXT,
                                  font=("Courier New", 11),
                                  selectbackground=ACCENT, selectforeground="white",
                                  relief="flat", bd=0,
                                  yscrollcommand=scrollbar.set,
                                  activestyle="none")
        self.listbox.pack(fill="both", expand=True)
        scrollbar.config(command=self.listbox.yview)
        self.listbox.bind("<<ListboxSelect>>", self.show_details)

        # details box
        self.detail_frame = tk.Frame(right, bg=CARD, relief="flat")
        self.detail_frame.pack(fill="x", pady=(8, 0))

        self.detail_label = tk.Label(self.detail_frame,
                                     text="← Select a student to see details",
                                     bg=CARD, fg=MUTED,
                                     font=("Courier New", 10),
                                     justify="left", padx=10, pady=8)
        self.detail_label.pack(anchor="w")

        # bottom buttons
        bot = tk.Frame(right, bg=BG)
        bot.pack(fill="x", pady=(8, 0))

        tk.Button(bot, text="📈 Show Chart (Turtle)", command=self.open_chart,
                  bg=GREEN, fg="white", font=("Courier New", 10, "bold"),
                  relief="flat", padx=10, pady=6, cursor="hand2").pack(side="left", padx=(0, 8))

        tk.Button(bot, text="❌ Remove Student", command=self.remove_student,
                  bg="#555", fg=TEXT, font=("Courier New", 10),
                  relief="flat", padx=10, pady=6, cursor="hand2").pack(side="left")

        tk.Button(bot, text="🏆 Show Topper", command=self.show_topper,
                  bg="#f5a623", fg="white", font=("Courier New", 10, "bold"),
                  relief="flat", padx=10, pady=6, cursor="hand2").pack(side="right")

    # ---- helper: calculate grade ----
    def get_grade(self, avg):
        if avg >= 90: return "A+", GREEN
        elif avg >= 75: return "A", "#4a90e2"
        elif avg >= 60: return "B", "#f5a623"
        elif avg >= 45: return "C", "#888"
        else: return "F", ACCENT

    # ---- add student ----
    def add_student(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("Oops", "Please enter student name!")
            return

        marks = []
        for i, var in enumerate(self.mark_vars):
            val = var.get().strip()
            if not val:
                messagebox.showerror("Oops", f"Please enter marks for subject {i+1}")
                return
            try:
                m = int(val)
                if not (0 <= m <= 100):
                    raise ValueError
                marks.append(m)
            except ValueError:
                messagebox.showerror("Oops", f"Marks should be a number between 0 and 100!")
                return

        if name in students:
            if not messagebox.askyesno("Exists", f"{name} already exists. Overwrite?"):
                return

        students[name] = marks
        self.refresh_list()
        self.clear_form()
        messagebox.showinfo("Done!", f"{name} added successfully ✓")

    # ---- refresh listbox ----
    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for name, marks in students.items():
            avg = sum(marks) / len(marks)
            grade, _ = self.get_grade(avg)
            self.listbox.insert(tk.END, f"  {name:<20}  Avg: {avg:.1f}   [{grade}]")

    # ---- show details on select ----
    def show_details(self, event):
        sel = self.listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        name = list(students.keys())[idx]
        marks = students[name]
        avg = sum(marks) / len(marks)
        grade, color = self.get_grade(avg)
        subjects = ["Math", "Science", "English", "Hindi", "CS"]

        detail = f"  Student: {name}   |   "
        detail += "   ".join([f"{s}: {m}" for s, m in zip(subjects, marks)])
        detail += f"   |   Avg: {avg:.1f}   Grade: {grade}"

        self.detail_label.config(text=detail, fg=color)

    # ---- open turtle chart ----
    def open_chart(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("Hey!", "Select a student first!")
            return
        idx = sel[0]
        name = list(students.keys())[idx]
        marks = students[name]
        show_turtle_chart(name, marks)

    # ---- remove student ----
    def remove_student(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("Hey!", "Select a student to remove!")
            return
        idx = sel[0]
        name = list(students.keys())[idx]
        if messagebox.askyesno("Confirm", f"Remove {name}?"):
            del students[name]
            self.refresh_list()
            self.detail_label.config(text="← Select a student to see details", fg=MUTED)

    # ---- show topper ----
    def show_topper(self):
        if not students:
            messagebox.showinfo("Hmm", "No students added yet!")
            return
        topper = max(students, key=lambda n: sum(students[n]) / len(students[n]))
        avg = sum(students[topper]) / len(students[topper])
        grade, _ = self.get_grade(avg)
        messagebox.showinfo("🏆 Class Topper",
                            f"Name: {topper}\nAverage: {avg:.1f}\nGrade: {grade}")

    # ---- clear form ----
    def clear_form(self):
        self.name_var.set("")
        for var in self.mark_vars:
            var.set("")


# ---- run app ----
if __name__ == "__main__":
    root = tk.Tk()
    app = GradeApp(root)
    root.mainloop()
