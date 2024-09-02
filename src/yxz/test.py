import json
import pandas as pd
import gradio as gr
import matplotlib.pyplot as plt
# 设置中文字体
plt.rcParams['font.family'] = 'SimHei'  # 设置为黑体

# 读取并解析 JSON 文件
with open('resource/id740205035942_【明日方舟】《明日方舟官方美术设定集VOL.2》套装礼盒.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
with open('resource/emotion_data.json', 'r', encoding='utf-8') as file:
    emotion_data = json.load(file)

# 将数据转换为 DataFrame
df = pd.DataFrame(data)

# 将 'date' 列解析为 datetime 对象
df['date'] = pd.to_datetime(df['date'], format='%Y年%m月%d日')

# 找到最早和最晚的日期
start_date = df['date'].min()
end_date = df['date'].max()

# 生成时间段索引，从最早日期开始，以5天为间隔
date_range = pd.date_range(start=start_date, end=end_date, freq='10D')

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
    plt.xlabel('时间')
    plt.ylabel('评论数')
    plt.title('每十天评论数量')
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
with gr.Blocks() as demo:
    with gr.Row():
        gr.Image(plot_bar_chart())
        gr.Image(plot_pie_chart())
demo.launch()
