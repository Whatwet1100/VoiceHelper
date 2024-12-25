import tkinter as tk
from idlelib.iomenu import encoding

from PIL import Image, ImageTk
from openai import OpenAI
import pyttsx3
from tkinter.filedialog import askdirectory

class VoiceHelper:
    def __init__(self, root):
        """tkinter,pyttsx3,API初始配置"""
        # tkinter初始配置
        self.root = root
        self.root.title("VoiceHelper")
        self.root.geometry("600x500")

        # 文件默认目录
        self.avatar = "VoiceHelper/Souls/default/pic.jpg"
        self.soul = "VoiceHelper/Souls/default/soul.txt"

        # 窗口左分区，包含头像图片，回复文字
        self.left_frame = tk.Frame(self.root, width=300, height=400, bg="white")
        self.left_frame.pack(side="left", fill="both", expand=True)
        ## 头像图片
        self.canvas = tk.Canvas(self.left_frame, width=200, height=200, bg="white")
        self.canvas.place(x=50, y=50)
        self.img = Image.open(self.avatar)
        self.img = self.img.resize((200, 200))
        self.img_tk = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(100, 100, image=self.img_tk)
        ## 显示回复文本
        self.output_box = tk.Label(self.left_frame, text="", bg="white", font=("Comicsans", 12),wraplength=250)
        self.output_box.place(x=50, y=260)

        # 窗口右分区，包含输入框，提交按钮
        self.right_frame = tk.Frame(self.root, width=300, height=400, bg="white")
        self.right_frame.pack(side="right", fill="both", expand=True)
        ## 问题输入框
        self.text_input = tk.Text(self.right_frame, width=30, height=5, wrap=tk.WORD)
        self.text_input.place(x=50, y=100)
        ##回复按钮
        self.button = tk.Button(self.right_frame, text="提交", command=self.output_information)
        self.button.place(x=50, y=200)

        # 窗口菜单
        self.top = tk.Menu(self.root)
        self.root.config(menu=self.top)
        ## 开始菜单，设置角色
        self.menu = tk.Menu(self.top)
        self.top.add_cascade(label='开始', menu=self.menu)
        self.menu.add_command(label="设置", command=self.settings)

        # 临时文本
        self.temp = ""
        self.output = ""
        self.path = ""

        # Kimi基础设置
        ## 设置API
        self.get_txt("VoiceHelper/KimiAPI/API.txt")
        self.client = OpenAI(
            api_key=self.temp,
            base_url="https://api.moonshot.cn/v1",
        )
        ## 获取默认角色词条
        self.get_txt(self.soul)
        self.role = self.temp

        self.temp = ""

        # pyttsx3基础配置
        self.engine = pyttsx3.init()

    def get_txt(self,file_path):
        try:
            # 打开文件并读取内容
            with open(file_path, 'r', encoding='utf-8') as file:
                self.temp = file.read()
            return self.temp
        except FileNotFoundError:
            return f"文件 '{file_path}' 未找到"
        except IOError as e:
            return f"读取文件时发生错误: {e}"

    def confirm_pic(self):
        self.img = Image.open(self.avatar)
        self.img = self.img.resize((200, 200))
        self.img_tk = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(100, 100, image=self.img_tk)

    def confirm_role(self):
        """获取角色信息"""
        self.get_txt(self.soul)
        self.role = self.temp
        self.temp = ""


    def settings(self):
        # 获取文件地址
        path = tk.StringVar()
        path_ = askdirectory()
        if path_ == "":
            path.get()
        else:
            path.set(path_)

        self.path = path_

        # 更新avatar头像
        self.avatar = self.path + "/pic.jpg"
        self.confirm_pic()

        # 更新soul文件
        self.soul = self.path + "/soul.txt"
        self.confirm_role()

    def output_information(self):
        """处理信息，输出文本"""
        # 获取输入框中的文本
        text = self.text_input.get("1.0", tk.END).strip()

        # 处理输入的文本
        completion = self.client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=[
                {"role": "system", "content": self.role},
                {"role": "user", "content": text}
            ],
            temperature=0.3,

        )

        # 输出文本
        self.output = completion.choices[0].message.content

        # 显示文本
        self.output_box.config(text=self.output)

        # 阅读文本
        self.engine.say(self.output)
        self.engine.runAndWait()

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceHelper(root)
    root.mainloop()





