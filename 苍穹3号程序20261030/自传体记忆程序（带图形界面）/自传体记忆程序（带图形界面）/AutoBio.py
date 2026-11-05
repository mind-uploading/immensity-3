import tkinter as tk
from tkinter import ttk, messagebox
import requests
import uuid
import datetime
from typing import List, Dict, Any
import csv
import os

# Tooltip类
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tip_window or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            tw, text=self.text, justify=tk.LEFT,
            background="#ffffe0", relief=tk.SOLID, borderwidth=1,
            font=("Microsoft YaHei", 9)
        )
        label.pack(ipadx=4)

    def hide_tip(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

class AutobiographicalMemory:
    def __init__(self):
        self.memory_bank: List[Dict[str, Any]] = []

    def add_event(self, event_type: str, episodic: str, semantic: str,
                  emotion: str, importance: float, timestamp: datetime.datetime = None, add_to_csv = True):
        """添加自传体记忆事件"""
        event = {
            "id": str(uuid.uuid4()),
            "event_type": event_type,
            "episodic": episodic,   # 具体发生了什么（情节细节）
            "semantic": semantic,   # 抽象意义（涉及的价值观/信念）
            "emotion": emotion,     # 情绪标签（正/负/混合 + 强度描述）
            "importance": importance,
            "timestamp": timestamp if timestamp else datetime.datetime.now()
        }
        self.memory_bank.append(event)
        
        if add_to_csv == True:
            
            # 追加写入到 CSV
            file_exists = os.path.isfile("autobiographical_memory.csv")
            with open("autobiographical_memory.csv", mode="a", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=event.keys())
                if not file_exists:
                    writer.writeheader()  # 首次写入加表头
                writer.writerow(event)

    def load_memories_from_csv(self, file_path="autobiographical_memory.csv"):
        
        if not os.path.exists(file_path):
            return []
        with open(file_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)
    def retrieve_by_context(self, context: str, top_k: int = 3):
        """简单的情境检索，后续可改为向量检索"""
        # 暂时用关键词匹配+重要性排序
        matches = []
        for event in self.memory_bank:
            score = 0
            if context.lower() in event["episodic"].lower():
                score += 1
            if context.lower() in event["semantic"].lower():
                score += 0.5
            score += event["importance"]  # 加权
            if score > 0:
                matches.append((score, event))
        matches.sort(key=lambda x: x[0], reverse=True)
        return [m[1] for m in matches[:top_k]]
    
    def get_all_events(self):
        return self.memory_bank


class ReflectionModule:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

    def reflect_on_memories(self, memories: List[Dict[str, Any]], current_context: str) -> str:
        """调用智谱清言 API 生成反思"""
        if not memories:
            return "没有找到相关记忆进行反思。"

        # 将记忆拼接成输入
        memory_text = "\n\n".join(
            [f"事件ID: {m['id']}\n类型: {m['event_type']}\n情节: {m['episodic']}\n语义: {m['semantic']}\n情绪: {m['emotion']}"
             for m in memories]
        )

        prompt = f"""你是一位基于认知心理学的反思助手。
当前情境是：{current_context}

相关的自传体记忆如下：
{memory_text}

请结合心理学理论，对这些记忆进行反思，包括：
0. 首先总结你看到的自传体记忆，和当前的情境，需要注意自传体记忆的时序特征和重要性的权重。
1. 当时的情绪和反应是否合理？
2. 有哪些模式或信念可能需要调整？
3. 这个经历对当前情境提供了什么启示？
"""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "glm-4",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
        response = requests.post(self.api_url, headers=headers, json=payload)
        result = response.json()
        return result["choices"][0]["message"]["content"]
    
    





# ======= Tkinter GUI =======
class MemoryReflectionApp:
    def __init__(self, root, api_key):
        self.root = root
        self.root.title("自传体记忆反思助手")
        self.root.geometry("1000x600")
        self.root.configure(bg="#2b2b2b")

        self.memory_manager = AutobiographicalMemory()
        self.reflector = ReflectionModule(api_key)

        self.create_widgets()
        self.refresh_memory_list()

    def create_widgets(self):
        # 左侧 - 记忆管理
        left_frame = tk.Frame(self.root, bg="#333333", width=450, padx=10, pady=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(left_frame, text="添加自传体记忆", font=("Microsoft YaHei", 14, "bold"), fg="white", bg="#333333").pack()

        # 输入框
        self.event_type_var = tk.StringVar()
        self.episodic_var = tk.StringVar()
        self.semantic_var = tk.StringVar()
        self.emotion_var = tk.StringVar()
        self.importance_var = tk.DoubleVar(value=0.5)
        
  
        

        fields = [
            ("事件类型", self.event_type_var,"这里输入事件类型，例如：'毕业典礼'，'第一次出国旅行'"),
            ("情节细节", self.episodic_var,"这里输入情节细节，例如：'在海边散步时看到日落'，'和我聊天的朋友经常喋喋不休'，'我开始反思其当时的动机，为什么我要这么做？"),
            ("事件主题/意义", self.semantic_var,"这里输入事件主题/意义，最好以关键词以便检索，例如：'- 事件：第一次一个人旅行 - 主题：自由、成长、独立； 事件：“和朋友在雨中散步”- 主题：友情、温暖、意外的快乐'"),
            ("情绪标签", self.emotion_var,"这里输入当时的情绪标签，例如：'开心'、'紧张'、'怀念'")
        ]

        for label, var, explains in fields:
            tk.Label(left_frame, text=label, fg="white", bg="#333333").pack(anchor="w")
            temp_entry = tk.Entry(left_frame, textvariable=var, width=40)
            temp_entry.pack()
            ToolTip(temp_entry, explains)

        tk.Label(left_frame, text="重要性 (0-1)", fg="white", bg="#333333").pack(anchor="w")
        temp_scale = tk.Scale(left_frame, variable=self.importance_var, from_=0, to=1, resolution=0.1,
                 orient=tk.HORIZONTAL, length=200, bg="#333333", fg="white")
        temp_scale.pack()
        ToolTip(temp_scale,"这里输入你觉得这个事情的重要性，0-1之间，0表示完全不重要，1表示最重要的事件")
        
        

        tk.Button(left_frame, text="添加记忆", command=self.add_memory,
                  bg="#4CAF50", fg="white", font=("Microsoft YaHei", 10, "bold")).pack(pady=10)

        # 记忆列表
        tk.Label(left_frame, text="已存储的记忆（可多选）; 所选数据项可以通过DEL键删除", fg="white", bg="#333333").pack(anchor="w")
        self.memory_listbox = tk.Listbox(left_frame, selectmode=tk.MULTIPLE, width=60, height=15,
                                         bg="#1e1e1e", fg="white", selectbackground="#ff9800")
        self.memory_listbox.pack()

        # 右侧 - 情境与反思
        right_frame = tk.Frame(self.root, bg="#2b2b2b", padx=10, pady=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        tk.Label(right_frame, text="当前情境", font=("Microsoft YaHei", 14, "bold"), fg="white", bg="#2b2b2b").pack()
        self.context_var = tk.StringVar()
        
        entry = tk.Entry(right_frame, textvariable=self.context_var, width=70)
        entry.pack()
    
        
        ToolTip(entry, "这里输入当前情境，例如：'正在准备做饭'、'屋外下着大雨'")
        tk.Button(right_frame, text="生成反思", command=self.generate_reflection,
                  bg="#2196F3", fg="white", font=("Microsoft YaHei", 10, "bold")).pack(pady=10)

        tk.Label(right_frame, text="反思结果(智谱比较慢，要几十秒)", font=("Microsoft YaHei", 14, "bold"), fg="white", bg="#2b2b2b").pack()
        self.reflection_text = tk.Text(right_frame, wrap=tk.WORD, bg="#1e1e1e", fg="white", insertbackground="white")
        self.reflection_text.pack(fill=tk.BOTH, expand=True)
        
        # 列表绑定 Del 键
        self.memory_listbox.bind("<Delete>", lambda event: self.delete_selected_memories())
    def delete_selected_memories(self):
        selected_indices = list(self.memory_listbox.curselection())
        if not selected_indices:
            return
        
        # 载入 CSV
        memories = self.memory_manager.load_memories_from_csv()
        
        # 倒序删除（避免索引错位）
        for index in sorted(selected_indices, reverse=True):
            self.memory_listbox.delete(index)
            if index < len(memories):
                del memories[index]
        
        # 重新写回 CSV
        with open("autobiographical_memory.csv", mode="w", encoding="utf-8", newline="") as f:
            if memories:
                writer = csv.DictWriter(f, fieldnames=memories[0].keys())
                writer.writeheader()
                writer.writerows(memories)
            

    def add_memory(self):
        self.memory_manager.add_event(
            event_type=self.event_type_var.get(),
            episodic=self.episodic_var.get(),
            semantic=self.semantic_var.get(),
            emotion=self.emotion_var.get(),
            importance=self.importance_var.get()
        )
        
        self.refresh_memory_list()
        self.clear_inputs()

    def refresh_memory_list(self):
        self.memory_listbox.delete(0, tk.END)
        # 界面启动时加载历史记忆
        past_memories = self.memory_manager.load_memories_from_csv()
        
        for m in past_memories:
            self.memory_manager.add_event(m['event_type'],m['episodic'],m['semantic'],m['emotion'],m['importance'],m['timestamp'],add_to_csv=False)
            display = f"{m['timestamp']}  [{m['event_type']}] {m['episodic']} | 情绪:{m['emotion']} | 重要性:{m['importance']}"
            self.memory_listbox.insert(tk.END, display)

    def clear_inputs(self):
        self.event_type_var.set("")
        self.episodic_var.set("")
        self.semantic_var.set("")
        self.emotion_var.set("")
        self.importance_var.set(0.5)

    def generate_reflection(self):
        selected_indices = self.memory_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("提示", "请至少选择一条记忆进行反思。")
            return
        print(selected_indices)
        print(self.memory_manager.get_all_events())
        selected_memories = [self.memory_manager.get_all_events()[i] for i in selected_indices]
        
        context = self.context_var.get()

        if not context.strip():
            messagebox.showwarning("提示", "请填写当前情境。")
            return

        reflection = self.reflector.reflect_on_memories(selected_memories, context)
        
        # 存储反思结果到 CSV
        reflection_data = []
        
        reflection_data.append({
            "reflection_time": datetime.datetime.now().isoformat(timespec='seconds'),
            "reflection": reflection
        })

        file_exists = os.path.isfile("reflections.csv")
        with open("reflections.csv", mode="a", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=reflection_data[0].keys())
            if not file_exists:
                writer.writeheader()
            writer.writerows(reflection_data)

        
        self.reflection_text.delete(1.0, tk.END)
        self.reflection_text.insert(tk.END, reflection)



# ========== 使用示例 ==========
if __name__ == "__main__":
    # # 初始化记忆库
    # mem = AutobiographicalMemory()
    # mem.add_event(
    #     event_type="失败经历",
    #     episodic="在大学时一次重要的演讲中，由于准备不足而表现很差",
    #     semantic="准备的重要性，自我效能感",
    #     emotion="负面，高挫败感",
    #     importance=0.9
    # )
    # mem.add_event(
    #     event_type="成就",
    #     episodic="成功组织了一次校内技术分享会",
    #     semantic="团队协作，知识分享的价值",
    #     emotion="正面，高满足感",
    #     importance=0.8
    # )

    # # 检索与“演讲”相关的记忆
    # context = "即将参加一次重要的演讲"
    # related_memories = mem.retrieve_by_context(context)

    # 反思模块
    api_key = "d56358b7bc4a42528d0fb17ef0bfcd28.UXPWECkuoxMRzL8C"  # 这是我的智谱清言的 API Key，你可以使用，但是最好不要让其他人用，额度有限
   
    root = tk.Tk()
    app = MemoryReflectionApp(root, api_key)
    root.mainloop()
    # reflector = ReflectionModule(api_key)
    # reflection_result = reflector.reflect_on_memories(related_memories, context)
    # print(reflection_result)
