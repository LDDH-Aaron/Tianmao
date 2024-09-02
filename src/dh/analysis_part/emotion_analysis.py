
import json
import threading
from queue import Queue

# 指定文件路径
file_path = 'YourFilePath'
# 读取JSON文件
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# 提取所有'content'字段中的内容
content_list = [entry['content'] for entry in data]

# 以100条为一组分割评论
chunk_size = 100
chunks = [content_list[i:i + chunk_size] for i in range(0, len(content_list), chunk_size)]

# 格式化输出并分批处理
formatted_outputs = []
for index, chunk in enumerate(chunks):
    formatted_output = "\n".join([f"{i + 1}. {content}" for i, content in enumerate(chunk)])
    formatted_outputs.append(formatted_output)

# 打印第一组的内容作为验证（可以替换为其他处理逻辑）
print(formatted_outputs[0])  # 仅显示前500字符以验证格式

# 如果需要保存或进一步处理每组评论，可以在这里添加额外逻辑

from langchain.schema import HumanMessage  # 假设 HumanMessage 来自 langchain
from langchain_core.messages import HumanMessage
import os
import getpass
import os
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    base_url="https://spark-api-open.xf-yun.com/v1",
    api_key="Your_Key",
    model="generalv3.5",
)
#创建实例

def analyze_emotion(reviews):
    # 使用输入的评论内容构建提示
    prompt = f'''
    你是一个评论情绪分析助手，你需要根据用户提供的评论内容，统计每种情绪（正面、负面或中性）评论的数量。请勿输出其他内容
    # 格式：
    正面情绪评论数量: {{正面评论数量}}
    负面情绪评论数量: {{负面评论数量}}
    中性情绪评论数量: {{中性评论数量}}

    # 示例1：
    输入：
    评论内容:
    1. 这个产品真的很好，我非常满意！
    2. 糟糕的服务，我不会再来了。
    3. 质量一般，但价格合理。

    输出：
    正面情绪评论数量: 1
    负面情绪评论数量: 1
    中性情绪评论数量: 1

    # 示例2：
    输入：
    评论内容:
    1. 我很喜欢这家店的环境，但是食物不太合口味。
    2. 客服态度很好，问题也很快解决了。
    3. 从未见过这么糟糕的体验！

    输出：
    正面情绪评论数量: 1
    负面情绪评论数量: 1
    中性情绪评论数量: 1

    请分析以下评论内容并根据格式输出每种情绪的评论数量：
    评论内容:
    {reviews}
    '''

    # 构造用户消息对象
    user_message = HumanMessage(content=prompt)

    # 调用模型生成响应
    response = model([user_message])

    # 返回模型的输出内容
    return response.content

def thread_function(review_chunk, results_queue):
    # 调用情感分析函数并将结果放入队列
    result = analyze_emotion(review_chunk)
    results_queue.put(result)

# 创建线程并运行
def run_multithreaded_analysis(chunks):
    threads = []
    results_queue = Queue()

    # 为每个评论块创建线程
    for chunk in chunks:
        thread = threading.Thread(target=thread_function, args=(chunk, results_queue))
        threads.append(thread)
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    # 从队列中获取结果，按顺序返回
    results = []
    while not results_queue.empty():
        results.append(results_queue.get())

    return results

results = run_multithreaded_analysis(formatted_outputs)

def sum(reviews):
    # 使用输入的评论内容构建提示
    prompt = f'''
    你是一个统计助手，请你将下面的数据做统计，并按照格式输出

    注意：请勿输出无关的内容

    # 示例：
    输入：
    正面情绪评论数量: 2
    负面情绪评论数量: 3
    中性情绪评论数量: 5
    正面情绪评论数量: 2
    负面情绪评论数量: 3
    中性情绪评论数量: 5
    正面情绪评论数量: 5
    负面情绪评论数量: 3
    中性情绪评论数量: 6
    正面情绪评论数量: 2
    负面情绪评论数量: 8
    中性情绪评论数量: 8


    输出：
    正面情绪评论数量: 11
    负面情绪评论数量: 17
    中性情绪评论数量: 24


    输入内容:
    {reviews}
    '''

    # 构造用户消息对象
    user_message = HumanMessage(content=prompt)

    # 调用模型生成响应
    response = model([user_message])

    # 返回模型的输出内容
    return response.content

# 调用情感分析函数并将结果放入队列
result = sum(results)
print(result)

import json
import os

# 定义情绪评论数量的数据
emotion_data = {
    "正面情绪评论数量": 160,
    "负面情绪评论数量": 35,
    "中性情绪评论数量": 7
}

# 构建文件名，检查是否存在同名目录
file_name = 'emotion_data.json'
if os.path.isdir(file_name):
    # 如果存在同名目录，则修改文件名
    file_name = 'emotion_data_new.json'

# 保存数据到 JSON 文件
with open(file_name, 'w', encoding='utf-8') as json_file:
    json.dump(emotion_data, json_file, ensure_ascii=False, indent=4)


import matplotlib.pyplot as plt

# 假设 result 是包含情绪分析结果的字符串
result = "正面情绪评论数量： 160\n负面情绪评论数量： 35\n中性情绪评论数量： 7"

# 提取情绪数量
lines = result.split('\n')
positive_count = int(lines[0].split('：')[-1].strip())
negative_count = int(lines[1].split('：')[-1].strip())
neutral_count = int(lines[2].split('：')[-1].strip())

# 数据准备
categories = ['Positive', 'Negative', 'Neutral']
values = [positive_count, negative_count, neutral_count]

# 创建柱状图
plt.figure(figsize=(8, 6))
plt.bar(categories, values, color=['orange', 'red', 'blue'])
plt.title('Sentiment Analysis Results')
plt.xlabel('Sentiment Type')
plt.ylabel('Number of Comments')
plt.show()