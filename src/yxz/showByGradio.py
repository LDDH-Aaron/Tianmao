import json
import sys
import time
import pandas as pd
import gradio as gr
import matplotlib.pyplot as plt

from Tianmao.src.lemon.wordfreq import cut_and_generate
# 设置中文字体
plt.rcParams['font.family'] = 'SimHei'  # 设置为黑体

# 读取并解析 JSON 文件
with open('commentData.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
with open('emotion_data.json', 'r', encoding='utf-8') as file:
    emotion_data = json.load(file)

# 将数据转换为 DataFrame
df = pd.DataFrame(data)


# 找到最早和最晚的日期
start_date = df['date'].min()
end_date = df['date'].max()

# 生成时间段索引，从最早日期开始，以5天为间隔
date_range = pd.date_range(start=start_date, end=end_date, freq='5D')

# 为每一行数据分配一个自定义时间段标签
'''
right=False: 这个参数指定区间是否包括右边界。right=False 意味着每个区间是左闭右开的，即 [start, end)，不包含区间的结束日期。

'''
df['period'] = pd.cut(df['date'], bins=date_range, right=False)
comment_counts = df.groupby('period').size().reset_index(name='comment_count')
# 将 period 列格式化为只显示日期部分并转换为字符串
'''
Interval 的构成
一个 Interval 对象由三个主要部分构成：

左边界（left）：区间的起始值。
右边界（right）：区间的结束值。
闭区间类型：表示区间是否包含其边界，可以是左闭右开 [a, b)、左开右闭 (a, b]、闭区间 [a, b] 或开区间 (a, b)。
'''
comment_counts['period'] = comment_counts['period'].apply(lambda x: x.left.strftime('%m-%d')).astype(str)

def plot_bar_chart():
    plt.figure(figsize=(10, 6))
    plt.bar(comment_counts['period'], comment_counts['comment_count'], color='orange')
    plt.xlabel('period')
    plt.ylabel('comment_count')
    plt.title('comment count every 5 day')
    plt.xticks(rotation=45, ha='right')  # 旋转X轴标签并右对齐
    # 保存图片
    file_path = "bar_chart.png"
    plt.savefig(file_path)
    plt.close()  # 确保关闭图形，避免冲突
    return file_path
def plot_pie_chart():
    labels = list(emotion_data.keys())
    sizes = list(emotion_data.values())

    # 绘制饼状图
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)

    # 设置标题
    plt.title('情绪分布图')

    # 保存图片
    file_path = "pie_chart.png"
    plt.savefig(file_path)
    plt.close()  # 确保关闭图形，避免冲突
    return file_path
def plot_cloud_chart():
    textfile = "commentData.json"
    with open(textfile, "r", encoding="utf-8") as fp:
        txt = (
            "\n".join([i["content"] for i in json.load(fp)])
            if textfile.endswith(".json")
            else fp.read()
        )
    c = cut_and_generate(txt,[])

    plt.figure(figsize=(16, 9))
    plt.imshow(c, interpolation="bilinear")
    plt.axis("off")
    return plt
def update_graphs(input_text):
    progress(0, desc="正在执行...")
    time.sleep(1)
    for i in progress.tqdm(range(168)):
        time.sleep(0.1)
    # 返回图表
    return plot_bar_chart(), plot_pie_chart(), plot_cloud_chart()


custom_css = """
@keyframes neon {
    0% {
        text-shadow: 0 0 5px #00FFFF, 0 0 10px #00FFFF, 0 0 20px #00FFFF, 0 0 40px #00FFFF, 0 0 80px #00FFFF, 0 0 90px #00FFFF, 0 0 100px #00FFFF, 0 0 150px #00FFFF;
        color: #00FFFF;
    }
    50% {
        text-shadow: 0 0 10px #1E90FF, 0 0 20px #1E90FF, 0 0 30px #1E90FF, 0 0 60px #1E90FF, 0 0 120px #1E90FF, 0 0 140px #1E90FF, 0 0 180px #1E90FF, 0 0 200px #1E90FF;
        color: #1E90FF;
    }
    100% {
        text-shadow: 0 0 5px #00FFFF, 0 0 10px #00FFFF, 0 0 20px #00FFFF, 0 0 40px #00FFFF, 0 0 80px #00FFFF, 0 0 90px #00FFFF, 0 0 100px #00FFFF, 0 0 150px #00FFFF;
        color: #00FFFF;
    }
}

@keyframes float {
    0% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-10px);
    }
    100% {
        transform: translateY(0);
    }
}

h1 {
    font-family: 'Arial', sans-serif;
    font-size: 48px;
    animation: neon 1.5s infinite, float 3s ease-in-out infinite;
    text-align: center;
    padding: 20px;
    margin: 0;
}
"""

markdown_content = """
<h1>京东评论爬虫系统</h1>
"""
with gr.Blocks(css=custom_css) as demo:
    gr.Markdown(markdown_content)

    # 添加输入栏
    input_text = gr.Textbox(label="输入商品评论链接", placeholder="在这里输入链接...")

    # 用于更新图表的按钮
    update_button = gr.Button("开始爬虫")

    # 进度条
    progress = gr.Progress()
    # 三个图表的展示区域
    with gr.Row():
        with gr.Row():
            plot1 = gr.Image(label="图表 1")
            plot3 = gr.Plot(label="图表 3")
    plot2 = gr.Image(label="图表 2")
    # 定义按钮点击时的行为
    update_button.click(
        update_graphs,
        inputs=input_text,
        outputs=[plot1, plot2, plot3]
    )
demo.launch()
