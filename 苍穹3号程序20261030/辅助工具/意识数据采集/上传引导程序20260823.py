import os
import numpy as np
import pandas as pd

#切换到项目根目录（本脚本位于 辅助工具/意识数据采集/ 下，向上两级；确保意识数据保存在项目根目录的意识数据文件夹中，而不是单开一个文件夹）
os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def main():
    print("=" * 70)
    print("欢迎使用「苍穹3号」意识上传引导程序（完整版）")
    print("您将用自然语言讲述自己的内心世界，程序会将其转化为苍穹3号可识别的数据。")
    print("请按照提示一步步输入，每一条都会请您确认。")
    print("如果想跳过某部分，请直接按回车（Enter）跳过。")
    print("=" * 70)

    print("\n本次上传的数据的版本号（例如姓名、数字或组合，将用于文件名）")
    print("(注：若存在同名文档，将直接覆盖；若不输入，将使用默认版本号 'default')")
    identifier = input().strip()
    if not identifier:
        identifier = "default"
        print(f"已使用默认版本号: {identifier}")

    # 创建所有需要的目录
    dirs = [
        "意识数据/情绪习惯列表/喜习惯列表",
        "意识数据/情绪习惯列表/哀习惯列表",
        "意识数据/行为习惯列表",
        "意识数据/自传体记忆",
        "意识数据/状态转移概率矩阵",
        "意识数据/行为空间",
        "意识数据/词典",
        "意识数据/词转移概率矩阵",
        "意识数据/ART"
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # 存储各部分的条目
    hap_entries = []         # 喜习惯
    sad_entries = []         # 哀习惯
    allact_entries = []      # 行为空间
    act_entries = []         # 行为习惯
    trans_entries = []       # 状态转移（意志、价值观、世界观）
    memory_entries = []      # 自传体记忆
    dict_entries = []        # 词典
    word_trans_entries = []  # 词转移概率矩阵

    # ============================================================
    # 0. 知识与经验提醒（前置，详细提醒）
    # ============================================================
    print("\n" + "=" * 70)
    print("温馨提示：您的知识与经验（原问卷第七部分）")
    print("\n这部分不单独录入，而是请您将专业知识拆分为：")
    print("  • 规律 → 填写到「世界观」")
    print("  • 操作流程 → 填写到「行为习惯」")
    print("  • 典型案例 → 填写到「自传体记忆」")
    print("\n在接下来的录入中，请有意识地回忆您擅长的领域（如编程、种植、烹饪、政治经济学等），")
    print("并将相关知识填入对应的部分。例如：")
    print("  - 如果您擅长螺旋藻养殖，可将“螺旋藻变黄→加肥料”的规律填到世界观，")
    print("    将“水位低→加水”的操作填到行为习惯，")
    print("    将一次成功收获的经历填到自传体记忆。")
    input("按回车继续...")

    # ============================================================
    # 1. 情绪习惯（独立）
    # ============================================================
    print("\n" + "=" * 70)
    print("第一部分：您的情绪反应——情绪习惯")
    print("\n这部分要上传的是什么东西会让您开心，什么东西会让您难过。")
    print("这是苍穹3号的“情感内核”，决定了您的数字人格在面对不同情境时会产生怎样的情绪。")
    print("\n⚠️ 特别提醒：请在喜习惯中录入您的“终极幸福”及其强度，稍后的“意志”部分您需要再次输入它。")
    print("（如果暂时没有要录入的，直接回车跳过）")
    
    # 喜习惯
    print("\n--- 喜习惯（让您开心的事物） ---")
    print("请用几个关键词描述一个让您感到开心或幸福的场景或事物。")
    while True:
        scene = input("\n描述开心的场景（请用空格分隔多个关键词，例如“和爱的人在一起 看到夕阳”）：").strip()
        if not scene:
            break
        intensity = input("这个场景让您开心的强度如何？请从1（有点）到5（极其强烈）打分：").strip()
        if not intensity.isdigit() or not (1 <= int(intensity) <= 5):
            print("请输入1~5之间的整数。")
            continue
        # 询问是否为终极幸福
        is_ultimate = input("这个场景是您的“终极幸福”吗？（y/n）：").strip().lower()
        if is_ultimate == 'y':
            print("💡 好的。稍后的“意志”部分您需要再次输入这个终极幸福（与目标关联）。")
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

    # ============================================================
    # 2. 行为空间（独立）
    # ============================================================
    print("\n" + "=" * 70)
    print("第二部分：行为空间——所有可能的行为")
    print("\n行为空间是苍穹3号可以执行的所有动作的集合，例如“加肥料”、“吃饭”、“报告意识体验”等。")
    print("您的行为习惯中将引用这些行为。请列出您常用的行为名称。")
    print("（如果暂时没有要录入的行为，直接回车跳过）")
    while True:
        act_name = input("\n请输入一个行为名称（例如“加肥料”）：").strip()
        if not act_name:
            break
        print(f"您录入的是：{act_name}")
        if input("确认录入？(y/n): ").lower() == 'y':
            allact_entries.append(act_name)
            print("已录入。")
        else:
            print("已取消。")
        if input("是否继续录入新的行为？(y/n): ").lower() != 'y':
            break

    # ============================================================
    # 3. 意志（状态转移，依赖行为空间，但格式与原程序一致）
    # ============================================================
    print("\n" + "=" * 70)
    print("第三部分：您的核心追求——意志与目标")
    print("\n这部分要上传的是您这辈子最想要的是什么，以及您打算怎么去实现它。")
    print("在苍穹3号里，这被拆解成两个东西：")
    print("  1. 您追求的目标（作为一个状态）")
    print("  2. 您相信这个目标能带来您想要的终极满足（作为结果状态）")
    print("💡 提示：您刚才在喜习惯中可能已经输入了终极幸福，现在请您再次输入它，以便与目标关联。")
    print("（如果暂时没有要录入的，直接回车跳过）")
    while True:
        target = input("\n请描述您的核心目标（请用空格分隔多个关键词，例如“共产主义实现 每个人自由发展”）：").strip()
        if not target:
            break
        ultimate = input("这个目标将带来什么样的终极幸福？（请用空格分隔多个关键词，例如“人类解放 压迫消失”）：").strip()
        if not ultimate:
            print("终极幸福不能为空，请重新输入。")
            continue
        target_words = target.split()
        ultimate_words = ultimate.split()
        # 与原程序一致：直接 目标；终极幸福、1、0
        entry = f"{'。'.join(target_words)}；{'。'.join(ultimate_words)}、1、0"
        print(f"\n您录入的是：\n  目标：{target}\n  终极幸福：{ultimate}")
        if input("确认录入？(y/n): ").lower() == 'y':
            trans_entries.append(entry)
            print("已录入。")
        else:
            print("已取消。")
        if input("是否继续录入新的目标？(y/n): ").lower() != 'y':
            break

    # ============================================================
    # 4. 价值观（状态转移，依赖行为空间）
    # ============================================================
    print("\n" + "=" * 70)
    print("第四部分：您的价值观——行为与后果的因果信念")
    print("\n这部分是您认为“做某件事”会带来“某种结果”，而这种结果会让您产生某种情绪。")
    print("它让苍穹3号能够“规划”和“决策”，主动去做那些它相信会带来好结果的事情。")
    print("请回忆一个您生活中重要的因果信念：在什么情况下，您做了什么，导致了什么结果？")
    print("（如果暂时没有要录入的，直接回车跳过）")
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
        # 组合状态：前序 = 情况 + 行为，结果 = 行为 + 结果 + 后续行为
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

    # ============================================================
    # 5. 世界观（状态转移，依赖行为空间）
    # ============================================================
    print("\n" + "=" * 70)
    print("第五部分：您对世界的理解——世界观")
    print("\n这部分是您认为这个世界是如何运转的，有哪些基本的规律。")
    print("它让苍穹3号能够“理解”世界，知道社会、自然、事物发展的基本规律，做出符合您认知的决策。")
    print("请写下一条您认为重要的世界规律，例如“技术进步会推动生产力发展”。")
    print("（如果暂时没有要录入的，直接回车跳过）")
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
        # 世界观中通常没有行为，直接状态变化
        entry = f"{'。'.join(cond_words)}；{'。'.join(cons_words)}、{prob}、0"
        print(f"\n您录入的是：\n  前提：{condition}\n  结果：{consequence}\n  确信度：{prob}")
        if input("确认录入？(y/n): ").lower() == 'y':
            trans_entries.append(entry)
            print("已录入。")
        else:
            print("已取消。")
        if input("是否继续录入新的世界观规律？(y/n): ").lower() != 'y':
            break

    # ============================================================
    # 6. 行为习惯（依赖行为空间）
    # ============================================================
    print("\n" + "=" * 70)
    print("第六部分：您的行为习惯——自动化的反应模式")
    print("\n这部分是您在特定情境下会自动做出的行为，也就是您的“习惯”或“本能反应”。")
    print("这是苍穹3号的“肌肉记忆”，当它遇到某些情境时，不需要思考就能自动做出反应。")
    print("（如果暂时没有要录入的，直接回车跳过）")
    while True:
        trigger = input("\n请描述触发这个习惯的情境（请用空格分隔多个关键词，例如“饥饿 没吃饭”）：").strip()
        if not trigger:
            break
        action = input("您在这个情境下会不假思索地做什么？（请用空格分隔多个关键词，例如“吃饭 找食物”）：").strip()
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

    # ============================================================
    # 7. 自传体记忆（独立）
    # ============================================================
    print("\n" + "=" * 70)
    print("第七部分：您的人生故事——自传体记忆")
    print("\n这部分是您人生中那些塑造了今天的您的“关键时刻”。")
    print("每一条记忆包含三个要素：")
    print("  1. 当时您感知到了什么？（知觉）")
    print("  2. 您当时做了什么？（行为）")
    print("  3. 这件事给您带来了什么样的整体感受？（价值，正数表示积极，负数表示消极）")
    print("请按时间顺序从以前到现在依次录入各条记忆。")
    print("（如果暂时没有要录入的，直接回车跳过）")
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

    # ============================================================
    # 8. 词典（独立）
    # ============================================================
    print("\n" + "=" * 70)
    print("第八部分：词典——自然语言到知觉概念的映射")
    print("\n词典帮助苍穹3号理解您输入的自然语言，将其转换为内部的知觉概念。")
    print("例如，您可以说“螺旋藻发黄了”，词典会将其映射为“螺旋藻 黄色”等知觉概念。")
    print("（如果暂时没有要录入的，直接回车跳过）")
    while True:
        word = input("\n请输入一个词或短语（例如“发黄”）：").strip()
        if not word:
            break
        sen = input("这个词对应的知觉概念是什么？请用空格分隔多个关键词（例如“黄色”）虚词的知觉概念直接设为空（即什么都不输入直接回车）：").strip()
        weight = input("该映射的权重（默认1，可不填）：").strip() or "1"
        sen_words = sen.split()
        sen_str = '。'.join(sen_words)
        entry = f"{word}；{sen_str}；{weight}"
        print(f"\n您录入的是：\n  词：{word}\n  知觉概念：{sen}\n  权重：{weight}")
        if input("确认录入？(y/n): ").lower() == 'y':
            dict_entries.append(entry)
            print("已录入。")
        else:
            print("已取消。")
        if input("是否继续录入词典条目？(y/n): ").lower() != 'y':
            break

    # ============================================================
    # 9. 词转移概率矩阵（独立）
    # ============================================================
    print("\n" + "=" * 70)
    print("第九部分：词转移概率矩阵——用于生成自然语言")
    print("\n这个矩阵记录了在苍穹3号生成句子时，一个词后面通常跟哪个词的规律。")
    print("您可以手动输入一些常见的词对转移，例如“天气” → “真好” 的概率为0.8。")
    print("用“<sent_start>”表示句首符号，引出句子第一个词。例如“<sent_start>” → “今天”意味着“今天”作为句子开头第一个词；“<sent_start>” → “今天”的概率为0.1 意味着 “今天”作为句首的概率为0.1")
    print("（如果暂时没有要录入的，直接回车跳过）")
    while True:
        word1 = input("\n请输入前一个词（若想输入句首符号，输入“<sent_start>”）：").strip()
        if not word1:
            break
        word2 = input("请输入后一个词：").strip()
        if not word2:
            print("后一个词不能为空。")
            continue
        prob = input("这个转移的概率是多少？（0~1之间的小数，默认0.5）：").strip() or "0.5"
        try:
            prob = float(prob)
            if prob < 0 or prob > 1:
                raise ValueError
        except:
            print("请输入0~1之间的数字。")
            continue
        entry = f"{word1}；{word2}；{prob}"
        print(f"\n您录入的是：\n  前词：{word1}\n  后词：{word2}\n  概率：{prob}")
        if input("确认录入？(y/n): ").lower() == 'y':
            word_trans_entries.append(entry)
            print("已录入。")
        else:
            print("已取消。")
        if input("是否继续录入词转移？(y/n): ").lower() != 'y':
            break

    # ============================================================
    # 10. ART 网络原型（自动生成，CSV）
    # ============================================================
    print("\n" + "=" * 70)
    print("第十部分：ART网络原型——用于视觉识别")
    print("\nART网络是苍穹3号用来识别图像中物体类别的模块。它需要一组原型向量来表示不同的类别。")
    print("程序将自动为您生成一组默认的随机原型（100个类别，每个512维），以确保系统正常运行。")
    print("您也可以稍后用自己的训练数据替换该文件。")
    print("详情请咨询苍穹3号项目开发组，苍穹3号项目开发组QQ群：645423602")
    input("按回车继续生成默认ART原型...")
    # 生成100个类别，512维，归一化
    num_categories = 100
    dim = 512
    np.random.seed(42)  # 保证可重复
    prototypes = np.random.randn(num_categories, dim)
    norms = np.linalg.norm(prototypes, axis=1, keepdims=True)
    prototypes = prototypes / norms
    art_path = f"意识数据/ART/ART{identifier}.csv"
    df = pd.DataFrame(prototypes)
    df.to_csv(art_path, index=False, header=False)
    print(f"✓ 已生成默认ART原型并保存到 {art_path}")

    # ============================================================
    # 保存所有数据文件（若某部分无数据，生成空文件）
    # ============================================================
    print("\n" + "=" * 70)
    print("正在保存所有数据...")

    # 喜习惯
    hap_path = f"意识数据/情绪习惯列表/喜习惯列表/喜习惯列表{identifier}.txt"
    with open(hap_path, 'w', encoding='utf-8') as f:
        if hap_entries:
            f.write('\n'.join(hap_entries))
            print(f"✓ 保存 {len(hap_entries)} 条喜习惯 -> {hap_path}")
        else:
            f.write('')
            print(f"⚠ 未录入喜习惯，已生成空文件 -> {hap_path}")

    # 哀习惯
    sad_path = f"意识数据/情绪习惯列表/哀习惯列表/哀习惯列表{identifier}.txt"
    with open(sad_path, 'w', encoding='utf-8') as f:
        if sad_entries:
            f.write('\n'.join(sad_entries))
            print(f"✓ 保存 {len(sad_entries)} 条哀习惯 -> {sad_path}")
        else:
            f.write('')
            print(f"⚠ 未录入哀习惯，已生成空文件 -> {sad_path}")

    # 行为空间
    allact_path = f"意识数据/行为空间/行为空间{identifier}.txt"
    with open(allact_path, 'w', encoding='utf-8') as f:
        if allact_entries:
            f.write('\n'.join(allact_entries))
            print(f"✓ 保存 {len(allact_entries)} 个行为 -> {allact_path}")
        else:
            f.write('')
            print(f"⚠ 未录入行为空间，已生成空文件 -> {allact_path}")

    # 行为习惯
    act_path = f"意识数据/行为习惯列表/行为习惯列表{identifier}.txt"
    with open(act_path, 'w', encoding='utf-8') as f:
        if act_entries:
            f.write('\n'.join(act_entries))
            print(f"✓ 保存 {len(act_entries)} 条行为习惯 -> {act_path}")
        else:
            f.write('')
            print(f"⚠ 未录入行为习惯，已生成空文件 -> {act_path}")

    # 状态转移概率矩阵（价值观、世界观、意志）
    trans_path = f"意识数据/状态转移概率矩阵/状态转移概率矩阵{identifier}.txt"
    with open(trans_path, 'w', encoding='utf-8') as f:
        if trans_entries:
            f.write('\n'.join(trans_entries))
            print(f"✓ 保存 {len(trans_entries)} 条状态转移（意志、价值观、世界观）-> {trans_path}")
        else:
            f.write('')
            print(f"⚠ 未录入状态转移条目，已生成空文件 -> {trans_path}")

    # 自传体记忆
    if len(memory_entries) < 5:
        need = 5 - len(memory_entries)
        filler = ["无关内容。；无关内容。；0"] * need
        # 填充内容放在记忆最早期（列表最前面）
        memory_entries = filler + memory_entries
        print(f"⚠ 自传体记忆不足5条，已在最早期填充 {need} 条占位内容，以确保系统正常运行。")

    memory_path = f"意识数据/自传体记忆/自传体记忆{identifier}.txt"
    with open(memory_path, 'w', encoding='utf-8') as f:
        if memory_entries:
            f.write('\n'.join(memory_entries))
            print(f"✓ 保存 {len(memory_entries)} 条自传体记忆 -> {memory_path}")
        else:
            f.write('')
            print(f"⚠ 未录入自传体记忆，已生成空文件 -> {memory_path}")

    # 词典
    dict_path = f"意识数据/词典/词典{identifier}.txt"
    with open(dict_path, 'w', encoding='utf-8') as f:
        if dict_entries:
            f.write('\n'.join(dict_entries))
            print(f"✓ 保存 {len(dict_entries)} 条词典条目 -> {dict_path}")
        else:
            f.write('')
            print(f"⚠ 未录入词典，已生成空文件 -> {dict_path}")

    # 词转移概率矩阵
    word_trans_path = f"意识数据/词转移概率矩阵/词转移概率矩阵{identifier}.txt"
    with open(word_trans_path, 'w', encoding='utf-8') as f:
        if word_trans_entries:
            f.write('\n'.join(word_trans_entries))
            print(f"✓ 保存 {len(word_trans_entries)} 条词转移 -> {word_trans_path}")
        else:
            f.write('')
            print(f"⚠ 未录入词转移，已生成空文件 -> {word_trans_path}")

    # ART 已保存
    print(f"✓ ART原型已保存到 {art_path}")

    print("\n所有数据已保存完毕！")
    print("在您启动苍穹3号时，当系统询问您要同步的数据的版本号时，请输入您本次上传时的版本号，以使系统加载本次上传的数据。")
    print("感谢使用，祝您在数字世界的新旅程中找到属于自己的答案。")

if __name__ == "__main__":
    main()