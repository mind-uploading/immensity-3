import os

#切换到项目根目录（本脚本位于 辅助工具/意识数据采集/ 下，向上两级；确保意识数据保存在项目根目录的意识数据文件夹中，而不是单开一个文件夹）
os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def main():
    print("=" * 70)
    print("欢迎使用「苍穹3号」意识上传引导程序")
    print("您将用自然语言讲述自己的内心世界，程序会将其转化为苍穹3号可识别的数据。")
    print("请按照提示一步步输入，每一条都会请您确认。")
    print("如果想跳过某部分，请按回车")
    print("=" * 70)

    print("\n本次上传的数据的版本号是:（例如姓名、数字或姓名+数字，将用于文件名）")
    print("(注：若存在同名文档，将直接覆盖)")
    identifier = input().strip()
    if not identifier:
        identifier = "default"

    # 创建所需目录
    dirs = [
        "意识数据/情绪习惯列表/喜习惯列表",
        "意识数据/情绪习惯列表/哀习惯列表",
        "意识数据/行为习惯列表",
        "意识数据/自传体记忆",
        "意识数据/状态转移概率矩阵"
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # 存储各部分的条目（每一条已经是完整的行字符串，格式符合苍穹3号）
    hap_entries = []      # 喜习惯
    sad_entries = []      # 哀习惯
    act_entries = []      # 行为习惯
    memory_entries = []   # 自传体记忆
    trans_entries = []    # 状态转移（意志、价值观、世界观）

    # ---------- 7. 知识与经验 ----------
    print("\n" + "=" * 70)
    print("您的知识与经验（原问卷第七部分）")
    print("\n这部分不单独录入，而是将您的专业知识拆分为：")
    print("  • 规律 → 填写到「世界观」")
    print("  • 操作流程 → 填写到「行为习惯」")
    print("  • 典型案例 → 填写到「自传体记忆」")
    input("请您在接下来填写时，顺便将您的专业知识拆分并填写到上述各部分中。按回车继续...")

    # ---------- 1. 意志 ----------
    print("\n" + "=" * 70)
    print("第一部分：您的核心追求——意志与目标")
    print("\n这部分要上传的是您这辈子最想要的是什么，以及您打算怎么去实现它。")
    print("在苍穹3号里，这被拆解成两个东西：")
    print("  1. 您追求的目标")
    print("  2. 您相信这个目标能带来您想要的终极满足")
    print("没有目标，苍穹3号就不知道该往哪个方向努力。这是您数字人格的“发动机”。")
    print("\n请用几个关键词描述您的核心目标和它带来的终极幸福。")
    while True:
        target = input("\n请描述您的核心目标（请用空格分隔多个关键词，例如“共产主义实现 每个人自由发展”）：").strip()
        if not target:
            break
        ultimate = input("这个目标将带来什么样的终极幸福？（请用空格分隔多个关键词，例如“人类解放 压迫消失”）：").strip()
        if not ultimate:
            print("终极幸福不能为空，请重新输入。")
            continue
        # 将关键词（空格分隔）转换为句号分隔
        target_words = target.split()
        ultimate_words = ultimate.split()
        entry = f"{'。'.join(target_words)}；{'。'.join(ultimate_words)}、1、0"  # 概率默认1，次数0
        print(f"\n您录入的是：\n  目标：{target}\n  终极幸福：{ultimate}")
        if input("确认录入？(y/n): ").lower() == 'y':
            trans_entries.append(entry)
            print("已录入。")
        else:
            print("已取消。")
        if input("是否继续录入新的目标？(y/n): ").lower() != 'y':
            break

    # ---------- 2. 情绪习惯 ----------
    print("\n" + "=" * 70)
    print("第二部分：您的情绪反应——情绪习惯")
    print("\n这部分要上传的是什么东西会让您开心，什么东西会让您难过。")
    print("这是苍穹3号的“情感内核”，决定了您的数字人格在面对不同情境时会产生怎样的情绪。")
    
    # 喜习惯
    print("\n--- 喜习惯（让您开心的事物） ---")
    print("请用几个关键词描述一个让您感到开心或幸福的场景或事物。")
    while True:
        scene = input("\n描述开心的场景（请用空格分隔多个关键词，例如“和爱的人在一起 看到夕阳 坐在沙滩上”）：").strip()
        if not scene:
            break
        intensity = input("这个场景让您开心的强度如何？请从1（有点）到5（极其强烈）打分：").strip()
        if not intensity.isdigit() or not (1 <= int(intensity) <= 5):
            print("请输入1~5之间的整数。")
            continue
        scene_words = scene.split()
        entry = f"{'。'.join(scene_words)}；{intensity}"
        print(f"\n您录入的是：\n  场景：{scene}\n  强度：{intensity}")
        if input("确认录入？(y/n): ").lower() == 'y':
            hap_entries.append(entry)
            print("已录入。")
        else:
            print("已取消。")
        if input("是否继续录入新的喜习惯？(y/n): ").lower() != 'y':
            break

    # 哀习惯
    print("\n--- 哀习惯（让您难过的事物） ---")
    print("请用几个关键词描述一个让您感到难过或痛苦的事物。")
    while True:
        scene = input("\n描述难过的场景（请用空格分隔多个关键词，例如“被他人责怪 孤独”）：").strip()
        if not scene:
            break
        intensity = input("这个场景让您难过的强度如何？请从1（有点）到5（极其强烈）打分：").strip()
        if not intensity.isdigit() or not (1 <= int(intensity) <= 5):
            print("请输入1~5之间的整数。")
            continue
        scene_words = scene.split()
        entry = f"{'。'.join(scene_words)}；{intensity}"
        print(f"\n您录入的是：\n  场景：{scene}\n  强度：{intensity}")
        if input("确认录入？(y/n): ").lower() == 'y':
            sad_entries.append(entry)
            print("已录入。")
        else:
            print("已取消。")
        if input("是否继续录入新的哀习惯？(y/n): ").lower() != 'y':
            break

    # ---------- 3. 价值观 ----------
    print("\n" + "=" * 70)
    print("第三部分：您的价值观——行为与后果的因果信念")
    print("\n这部分是您认为“做某件事”会带来“某种结果”，而这种结果会让您产生某种情绪。")
    print("它让苍穹3号能够“规划”和“决策”，主动去做那些它相信会带来好结果的事情。")
    print("请回忆一个您生活中重要的因果信念：在什么情况下，您做了什么，导致了什么结果？")
    while True:
        situation = input("\n请描述当时的情况（请用空格分隔多个关键词，例如“空闲 感到无聊”）：").strip()
        if not situation:
            break
        action = input("您当时做了什么？（请用空格分隔多个关键词，例如“玩战争雷霆 玩我的世界”）：").strip()
        if not action:
            print("行为不能为空，请重新输入。")
            continue
        result = input("这个行为导致了什么结果？（请用空格分隔多个关键词，例如“交到朋友”）：").strip()
        if not result:
            print("结果不能为空。")
            continue
        next_action = input("结果发生后，您又做了什么？（如果没有，直接回车；如有，请用空格分隔多个关键词）：").strip()
        prob = input("您认为这个因果发生的可能性有多大？请用0到1之间的小数表示（默认1）：").strip() or "1"
        # 构建状态：前序状态 = situation + action，结果状态 = action + result + next_action（如果有）
        sit_words = situation.split()
        act_words = action.split()
        res_words = result.split()
        next_words = next_action.split() if next_action else []
        pre_state = '。'.join(sit_words + act_words)
        post_state = '。'.join(act_words + res_words + next_words)
        entry = f"{pre_state}；{post_state}、{prob}、0"
        print(f"\n您录入的是：\n  情况：{situation}\n  行为：{action}\n  结果：{result}" + (f"\n  后续行为：{next_action}" if next_action else ""))
        print(f"  确信度：{prob}")
        if input("确认录入？(y/n): ").lower() == 'y':
            trans_entries.append(entry)
            print("已录入。")
        else:
            print("已取消。")
        if input("是否继续录入新的价值观条目？(y/n): ").lower() != 'y':
            break

    # ---------- 4. 自传体记忆 ----------
    print("\n" + "=" * 70)
    print("第四部分：您的人生故事——自传体记忆")
    print("\n这部分是您人生中那些塑造了今天的您的“关键时刻”。")
    print("每一条记忆包含三个要素：")
    print("  1. 当时您感知到了什么？（知觉）")
    print("  2. 您当时做了什么？（行为）")
    print("  3. 这件事给您带来了什么样的整体感受？（价值，正数表示积极，负数表示消极）")
    print("请按时间顺序从以前到现在依次录入各条记忆")
    while True:
        sen = input("\n请描述当时您感知到的核心信息（请用空格分隔多个关键词）：").strip()
        if not sen:
            break
        act = input("您当时做出了什么关键行为或决定？（请用空格分隔多个关键词，如无直接回车）：").strip()
        val = input("这件事带给您的整体感受如何？请用-5到5之间的整数表示（-5极其痛苦，+5极其幸福）：").strip()
        if not val.lstrip('-').isdigit() or not (-5 <= int(val) <= 5):
            print("请输入-5到5之间的整数。")
            continue
        sen_words = sen.split()
        act_words = act.split() if act else []
        entry = f"{'。'.join(sen_words)}；{'。'.join(act_words)}；{val}"
        print(f"\n您录入的是：\n  知觉：{sen}\n  行为：{act if act else '无'}\n  感受评分：{val}")
        if input("确认录入？(y/n): ").lower() == 'y':
            memory_entries.append(entry)
            print("已录入。")
        else:
            print("已取消。")
        if input("是否继续录入新的自传体记忆？(y/n): ").lower() != 'y':
            break

    # ---------- 5. 世界观 ----------
    print("\n" + "=" * 70)
    print("第五部分：您对世界的理解——世界观")
    print("\n这部分是您认为这个世界是如何运转的，有哪些基本的规律。")
    print("它让苍穹3号能够“理解”世界，知道社会、自然、事物发展的基本规律，做出符合您认知的决策。")
    print("请写下一条您认为重要的世界规律，例如“技术进步会推动生产力发展”。")
    while True:
        condition = input("\n请描述规律的前提条件（请用空格分隔多个关键词，例如“技术进步”）：").strip()
        if not condition:
            break
        consequence = input("这个前提会导致什么结果？（请用空格分隔多个关键词，例如“生产力 发展”）：").strip()
        if not consequence:
            print("结果不能为空。")
            continue
        prob = input("这个规律发生的可能性有多大？请用0到1之间的小数表示（默认1）：").strip() or "1"
        cond_words = condition.split()
        cons_words = consequence.split()
        entry = f"{'。'.join(cond_words)}；{'。'.join(cons_words)}、{prob}、0"
        print(f"\n您录入的是：\n  前提：{condition}\n  结果：{consequence}\n  确信度：{prob}")
        if input("确认录入？(y/n): ").lower() == 'y':
            trans_entries.append(entry)
            print("已录入。")
        else:
            print("已取消。")
        if input("是否继续录入新的世界观规律？(y/n): ").lower() != 'y':
            break

    # ---------- 6. 行为习惯 ----------
    print("\n" + "=" * 70)
    print("第六部分：您的行为习惯——自动化的反应模式")
    print("\n这部分是您在特定情境下会自动做出的行为，也就是您的“习惯”或“本能反应”。")
    print("这是苍穹3号的“肌肉记忆”，当它遇到某些情境时，不需要思考就能自动做出反应。")
    while True:
        trigger = input("\n请描述触发这个习惯的情境（请用空格分隔多个关键词，例如“饥饿”）：").strip()
        if not trigger:
            break
        action = input("您在这个情境下会不假思索地做什么？（请用空格分隔多个关键词，例如“吃饭”）：").strip()
        if not action:
            print("行为不能为空。")
            continue
        feeling = input("做完这件事后，您的感受如何？请从1（感觉非常难受）到5（感觉非常好）打分：").strip()
        if not feeling.isdigit() or not (1 <= int(feeling) <= 5):
            print("请输入1~5之间的整数。")
            continue
        trigger_words = trigger.split()
        action_words = action.split()
        entry = f"{'。'.join(trigger_words)}；{'。'.join(action_words)}；{feeling}"
        print(f"\n您录入的是：\n  触发情境：{trigger}\n  行为：{action}\n  感受评分：{feeling}")
        if input("确认录入？(y/n): ").lower() == 'y':
            act_entries.append(entry)
            print("已录入。")
        else:
            print("已取消。")
        if input("是否继续录入新的行为习惯？(y/n): ").lower() != 'y':
            break


    # ---------- 写入文件 ----------
    print("\n" + "=" * 70)
    print("正在保存数据...")

    if hap_entries:
        path = f"意识数据/情绪习惯列表/喜习惯列表/喜习惯列表{identifier}.txt"
        with open(path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(hap_entries))
        print(f"✓ 保存 {len(hap_entries)} 条喜习惯 -> {path}")
    else:
        print("⚠ 未录入喜习惯，跳过。")

    if sad_entries:
        path = f"意识数据/情绪习惯列表/哀习惯列表/哀习惯列表{identifier}.txt"
        with open(path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(sad_entries))
        print(f"✓ 保存 {len(sad_entries)} 条哀习惯 -> {path}")
    else:
        print("⚠ 未录入哀习惯，跳过。")

    if act_entries:
        path = f"意识数据/行为习惯列表/行为习惯列表{identifier}.txt"
        with open(path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(act_entries))
        print(f"✓ 保存 {len(act_entries)} 条行为习惯 -> {path}")
    else:
        print("⚠ 未录入行为习惯，跳过。")

    if memory_entries:
        path = f"意识数据/自传体记忆/自传体记忆{identifier}.txt"
        with open(path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(memory_entries))
        print(f"✓ 保存 {len(memory_entries)} 条自传体记忆 -> {path}")
    else:
        print("⚠ 未录入自传体记忆，跳过。")

    if trans_entries:
        path = f"意识数据/状态转移概率矩阵/状态转移概率矩阵{identifier}.txt"
        with open(path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(trans_entries))
        print(f"✓ 保存 {len(trans_entries)} 条状态转移（意志、价值观、世界观）-> {path}")
    else:
        print("⚠ 未录入状态转移条目，跳过。")

    print("\n所有数据已保存完毕！")
    print("您可以将这些文件放置到苍穹3号系统对应的目录下，供系统加载。")
    print("感谢使用，祝您在数字世界的新旅程中找到属于自己的答案。")

if __name__ == "__main__":
    main()