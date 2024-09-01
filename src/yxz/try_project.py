import json
import pandas as pd
import gradio as gr
import matplotlib.pyplot as plt

# 读取并解析 JSON 文件
with open('commentData.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

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
    plt.tight_layout()
    return plt

with gr.Blocks() as demo:
    gr.Plot(plot_bar_chart)# 启动 Gradio 接口
demo.launch()
