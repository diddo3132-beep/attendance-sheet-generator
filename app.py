#!/usr/bin/env python3
"""
考勤表生成助手 - 图形界面版
"""
import os
import sys
import json
import re
import subprocess
import platform
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from datetime import date

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, 'data')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'template')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
COURSES_JSON = os.path.join(DATA_DIR, 'courses.json')
CONFIG_JSON = os.path.join(DATA_DIR, 'config.json')
DEFAULT_TEMPLATE = os.path.join(TEMPLATE_DIR, '考勤表模板.docx')

for d in [DATA_DIR, TEMPLATE_DIR, OUTPUT_DIR]:
    os.makedirs(d, exist_ok=True)


def load_config():
    if os.path.exists(CONFIG_JSON):
        with open(CONFIG_JSON, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'template_path': DEFAULT_TEMPLATE}


def save_config(cfg):
    with open(CONFIG_JSON, 'w', encoding='utf-8') as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


def open_folder(path):
    folder = os.path.dirname(path) if os.path.isfile(path) else path
    if platform.system() == 'Windows':
        os.startfile(folder)
    elif platform.system() == 'Darwin':
        subprocess.run(['open', folder])
    else:
        subprocess.run(['xdg-open', folder])


class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("考勤表生成助手")
        self.root.geometry("720x680")
        self.root.resizable(True, True)

        self.config = load_config()
        self.courses = []
        self._load_courses()

        style = ttk.Style()
        style.configure('Title.TLabel', font=('Microsoft YaHei', 14, 'bold'))
        style.configure('Section.TLabelframe.Label', font=('Microsoft YaHei', 10, 'bold'))

        notebook = ttk.Notebook(root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        self.tab_generate = ttk.Frame(notebook)
        self.tab_import = ttk.Frame(notebook)
        self.tab_settings = ttk.Frame(notebook)

        notebook.add(self.tab_generate, text='  生成考勤表  ')
        notebook.add(self.tab_import, text='  导入大纲  ')
        notebook.add(self.tab_settings, text='  设置  ')

        self._build_generate_tab()
        self._build_import_tab()
        self._build_settings_tab()

        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(root, textvariable=self.status_var, relief='sunken', anchor='w')
        status_bar.pack(fill='x', side='bottom', padx=10, pady=(0, 5))

    def _load_courses(self):
        if os.path.exists(COURSES_JSON):
            try:
                from course_db import load_courses
                self.courses = load_courses(COURSES_JSON)
            except Exception:
                self.courses = []

    def _build_generate_tab(self):
        frame = self.tab_generate
        pad = {'padx': 8, 'pady': 4}

        info_frame = ttk.LabelFrame(frame, text="培训信息", style='Section.TLabelframe')
        info_frame.pack(fill='x', **pad)

        ttk.Label(info_frame, text="课程代码：").grid(row=0, column=0, sticky='e', **pad)
        self.course_var = tk.StringVar()
        self.course_combo = ttk.Combobox(info_frame, textvariable=self.course_var, width=40)
        self._update_course_list()
        self.course_combo.grid(row=0, column=1, columnspan=3, sticky='w', **pad)
        self.course_combo.bind('<<ComboboxSelected>>', self._on_course_selected)

        ttk.Label(info_frame, text="课程名称：").grid(row=1, column=0, sticky='e', **pad)
        self.name_var = tk.StringVar()
        ttk.Entry(info_frame, textvariable=self.name_var, width=43, state='readonly').grid(row=1, column=1, columnspan=3, sticky='w', **pad)

        ttk.Label(info_frame, text="培训日期：").grid(row=2, column=0, sticky='e', **pad)
        self.date_var = tk.StringVar(value=date.today().strftime('%Y-%m-%d'))
        ttk.Entry(info_frame, textvariable=self.date_var, width=18).grid(row=2, column=1, sticky='w', **pad)

        ttk.Label(info_frame, text="培训时间：").grid(row=2, column=2, sticky='e', **pad)
        self.time_var = tk.StringVar(value="08:30-11:30")
        ttk.Entry(info_frame, textvariable=self.time_var, width=18).grid(row=2, column=3, sticky='w', **pad)

        ttk.Label(info_frame, text="教员姓名：").grid(row=3, column=0, sticky='e', **pad)
        self.instructor_var = tk.StringVar()
        ttk.Entry(info_frame, textvariable=self.instructor_var, width=18).grid(row=3, column=1, sticky='w', **pad)

        ttk.Label(info_frame, text="培训地点：").grid(row=3, column=2, sticky='e', **pad)
        self.location_var = tk.StringVar()
        ttk.Entry(info_frame, textvariable=self.location_var, width=18).grid(row=3, column=3, sticky='w', **pad)

        stu_frame = ttk.LabelFrame(frame, text="学员名单（每行：工号 TAB 姓名，可从 Excel 直接粘贴）", style='Section.TLabelframe')
        stu_frame.pack(fill='both', expand=True, **pad)

        self.students_text = scrolledtext.ScrolledText(stu_frame, height=12, font=('Consolas', 10))
        self.students_text.pack(fill='both', expand=True, padx=5, pady=5)
        self.students_text.insert('1.0', "1001\t李雷\n1002\t韩梅梅\n1003\t王明")

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill='x', **pad)

        ttk.Button(btn_frame, text="生成考勤表", command=self._generate).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="清空学员", command=lambda: self.students_text.delete('1.0', 'end')).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="打开输出文件夹", command=lambda: open_folder(OUTPUT_DIR)).pack(side='right', padx=5)

    def _build_import_tab(self):
        frame = self.tab_import
        pad = {'padx': 8, 'pady': 4}

        ttk.Label(frame, text="从维修工程教学大纲 PDF 导入课程数据", style='Title.TLabel').pack(**pad)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill='x', **pad)

        ttk.Button(btn_frame, text="选择 PDF 文件并导入", command=self._import_pdf).pack(side='left', padx=5)

        info_frame = ttk.LabelFrame(frame, text="当前课程数据库", style='Section.TLabelframe')
        info_frame.pack(fill='both', expand=True, **pad)

        self.courses_listbox = tk.Listbox(info_frame, font=('Microsoft YaHei', 9))
        scrollbar = ttk.Scrollbar(info_frame, orient='vertical', command=self.courses_listbox.yview)
        self.courses_listbox.configure(yscrollcommand=scrollbar.set)
        self.courses_listbox.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        scrollbar.pack(side='right', fill='y', pady=5)
        self._refresh_courses_list()

    def _build_settings_tab(self):
        frame = self.tab_settings
        pad = {'padx': 8, 'pady': 8}

        ttk.Label(frame, text="设置", style='Title.TLabel').pack(**pad)

        tpl_frame = ttk.LabelFrame(frame, text="考勤表模板", style='Section.TLabelframe')
        tpl_frame.pack(fill='x', **pad)

        self.template_var = tk.StringVar(value=self.config.get('template_path', DEFAULT_TEMPLATE))
        ttk.Entry(tpl_frame, textvariable=self.template_var, width=60).pack(side='left', padx=5, pady=8)
        ttk.Button(tpl_frame, text="浏览", command=self._browse_template).pack(side='left', padx=5, pady=8)

        dir_frame = ttk.LabelFrame(frame, text="文件路径", style='Section.TLabelframe')
        dir_frame.pack(fill='x', **pad)

        for label, path in [("数据目录", DATA_DIR), ("模板目录", TEMPLATE_DIR), ("输出目录", OUTPUT_DIR)]:
            row = ttk.Frame(dir_frame)
            row.pack(fill='x', padx=5, pady=2)
            ttk.Label(row, text=f"{label}：", width=10).pack(side='left')
            ttk.Label(row, text=path, foreground='gray').pack(side='left')

        ttk.Button(frame, text="保存设置", command=self._save_settings).pack(**pad)

    def _update_course_list(self):
        values = [f"{c['code']} - {c['name']}" for c in self.courses]
        self.course_combo['values'] = values

    def _refresh_courses_list(self):
        self.courses_listbox.delete(0, 'end')
        for c in self.courses:
            self.courses_listbox.insert('end', f"{c['code']}  |  {c['name']}  |  {c['hours']}课时")

    def _on_course_selected(self, event=None):
        sel = self.course_var.get()
        code = sel.split(' - ')[0].strip() if ' - ' in sel else sel.strip()
        from course_db import get_course_by_code
        course = get_course_by_code(code, self.courses)
        if course:
            self.name_var.set(course['name'])

    def _parse_students(self):
        text = self.students_text.get('1.0', 'end').strip()
        students = []
        for line in text.split('\n'):
            line = line.strip()
            if not line:
                continue
            parts = re.split(r'[\t ]+', line)
            if len(parts) >= 2:
                students.append({'id': parts[0], 'name': parts[1]})
        return students

    def _generate(self):
        sel = self.course_var.get()
        if not sel:
            messagebox.showwarning("提示", "请先选择课程代码")
            return

        code = sel.split(' - ')[0].strip() if ' - ' in sel else sel.strip()
        from course_db import get_course_by_code
        course = get_course_by_code(code, self.courses)
        if not course:
            messagebox.showerror("错误", f"未找到课程代码：{code}")
            return

        students = self._parse_students()
        if not students:
            messagebox.showwarning("提示", "请输入学员名单")
            return

        training_date = self.date_var.get().strip()
        if not training_date:
            messagebox.showwarning("提示", "请输入培训日期")
            return

        user_info = {
            'code': code,
            'date': training_date,
            'time': self.time_var.get().strip(),
            'instructor': self.instructor_var.get().strip(),
            'location': self.location_var.get().strip(),
            'students': students,
        }

        template_path = self.template_var.get()
        if not os.path.exists(template_path):
            messagebox.showerror("错误", f"模板文件不存在：{template_path}\n请在设置中指定正确的模板路径")
            return

        filename = f"{training_date}_{code}_考勤表.docx"
        output_path = os.path.join(OUTPUT_DIR, filename)

        try:
            self.status_var.set("正在生成...")
            self.root.update()
            from generate_docx import fill_attendance_template
            fill_attendance_template(template_path, output_path, course, user_info)
            self.status_var.set(f"生成成功：{filename}")
            result = messagebox.askyesno("生成成功", f"考勤表已生成：\n{filename}\n\n{len(students)} 名学员\n\n是否打开输出文件夹？")
            if result:
                open_folder(output_path)
        except Exception as e:
            self.status_var.set("生成失败")
            messagebox.showerror("生成失败", str(e))

    def _import_pdf(self):
        pdf_path = filedialog.askopenfilename(
            title="选择维修工程教学大纲 PDF",
            filetypes=[("PDF 文件", "*.pdf")]
        )
        if not pdf_path:
            return

        try:
            self.status_var.set("正在解析 PDF...")
            self.root.update()
            from parse_outline import extract_courses_from_pdf, save_courses
            courses = extract_courses_from_pdf(pdf_path)
            if not courses:
                messagebox.showwarning("提示", "未能从 PDF 中提取到课程数据，请检查 PDF 格式")
                self.status_var.set("导入失败：未找到课程数据")
                return
            save_courses(courses, COURSES_JSON)
            self.courses = courses
            self._update_course_list()
            self._refresh_courses_list()
            self.status_var.set(f"导入成功：{len(courses)} 门课程")
            messagebox.showinfo("导入成功", f"从大纲中提取了 {len(courses)} 门课程")
        except Exception as e:
            self.status_var.set("导入失败")
            messagebox.showerror("导入失败", str(e))

    def _browse_template(self):
        path = filedialog.askopenfilename(
            title="选择考勤表模板",
            filetypes=[("Word 文件", "*.docx")],
            initialdir=TEMPLATE_DIR
        )
        if path:
            self.template_var.set(path)

    def _save_settings(self):
        self.config['template_path'] = self.template_var.get()
        save_config(self.config)
        messagebox.showinfo("保存成功", "设置已保存")


def main():
    root = tk.Tk()
    AttendanceApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
