"""# 接入Langchain"""
from chromadb.app import server
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from langchain.schema import HumanMessage  # 假设 HumanMessage 来自 langchain
from langchain_core.messages import HumanMessage
from langchain_community.tools.tavily_search import TavilySearchResults
import os
from langgraph.prebuilt import create_react_agent
import getpass
import os
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    base_url="https://spark-api-open.xf-yun.com/v1",
    api_key="your_api_key",
    model="generalv3.5",
)
#创建实例

"""#数据处理"""

import json
from collections import Counter

# 加载 JSON 文件内容到一个变量中
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# 统计词频并格式化输出，去掉词频小于4的词
def count_word_frequency(data):
    # 使用 Counter 统计词频
    word_counter = Counter(data)
    # 过滤掉词频小于4的词
    filtered_word_count = {word: count for word, count in word_counter.items() if count >= 4}
    # 将统计结果转换为按词频排序的列表
    sorted_word_count = sorted(filtered_word_count.items(), key=lambda x: x[1], reverse=True)
    return sorted_word_count

# 将词频统计结果格式化为指定格式
def format_word_frequency(word_count):
    formatted_output = "词频统计结果：\n"
    for word, count in word_count:
        formatted_output += f"{word}：{count}\n"
    return formatted_output

# 文件路径
file_path = 'sample.txt.washed.json'

# 加载 JSON 数据
data = load_json(file_path)

# 统计词频
word_count = count_word_frequency(data)

# 格式化输出并保存到变量
formatted_output = format_word_frequency(word_count)

# 格式化数据的函数
def format_emotion_data(data):
    formatted_data = "情绪评论统计：\n"
    for key, value in data.items():
        formatted_data += f"{key}：{value}\n"
    return formatted_data

def format_daily_comment_counts(data):
    formatted_data = "\n每日评论统计：\n"
    for entry in data:
        formatted_data += f"日期：{entry['date']}，评论数量：{entry['comment_count']}\n"
    return formatted_data

# 加载 JSON 文件内容到一个变量中
def load_json(file_path): # Define the load_json function within this file as well.
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# 文件路径
emotion_data_path = 'emotion_data(1).json'
daily_comment_counts_path = 'daily_comment_counts(1).json'

# 加载 JSON 数据
emotion_data = load_json(emotion_data_path)
daily_comment_counts = load_json(daily_comment_counts_path)

# 格式化数据并保存在变量中
formatted_emotion_data = format_emotion_data(emotion_data)
formatted_daily_comments = format_daily_comment_counts(daily_comment_counts)

"""# 生成报告
获取：
好评差评数量
数据分析（浏览量）
产品名称与描述
关键词云


输出：
针对评论区的总结报告

"""

final_output = formatted_emotion_data + formatted_daily_comments + formatted_output
print(final_output)

def report_maker(content):
    prompt = f'''
    你是一个评论区分析助手，你将根据用户提供的评论统计数据、词频分析结果和关键词分析，为产品改进和市场策略提供建议。请根据用户提供的数据进行详细分析，并按照指定格式输出结果

#格式：
情绪分析结果：
1、总体情绪分析
2、正面情绪分析
3、负面情绪分析
4、中性情绪分析

每日评论趋势分析：
1、热点评论时间段
2、评论量增加或减少的原因
3、关键词分析：

主要关键词：
列出频率最高的关键词，并解释其背后的用户需求或关注点
负面关键词：
列出负面情绪中频率较高的关键词，并分析其对用户体验的影响

产品建议：
基于情绪分析的建议
基于词频和关键词分析的建议
综合建议

#注意：
不要输出情绪评论统计、每日评论数量、关键词数量，直接输出报告

#示例输入：
情绪评论统计：
正面情绪评论数量：160
负面情绪评论数量：35
中性情绪评论数量：7

每日评论统计：
日期：2024-05-26，评论数量：2
日期：2024-05-27，评论数量：4
...
（更多日期和评论数量）

词频统计结果：
喜欢：55
内容：47
包装：45
发货：33
...
（更多词频统计）

#示例输出：
情绪分析结果：

总体情绪分析：总体来说，评论区情绪以正面为主，占总评论量的70%以上，表明大多数用户对产品体验较为满意。
正面情绪分析：正面评论主要集中在“喜欢”、“好看”、“值得”等关键词，说明用户对产品设计和价值感到满意。
负面情绪分析：负面评论占比约为15%，主要涉及“发货”问题和“包装”质量等，表明在物流和包装方面存在一定的用户不满。
中性情绪分析：中性评论数量较少，占总量的不到5%，可能表示一些用户对产品体验没有特别的感受或是持观望态度。
每日评论趋势分析：

热点评论时间段：7月7日至7月14日为评论高峰期，可能与产品活动或促销相关。
评论量增加或减少的原因：7月7日的评论量激增，可能与当天的促销活动或新品发布相关；7月15日之后评论量有所下降，可能是活动结束或产品关注度减弱导致。
关键词分析：

主要关键词：

“喜欢”（55次）：用户对产品的整体设计、使用体验感到满意，产品的视觉吸引力较强。
“内容”（47次）：可能反映出用户对产品的实质内容（如说明书、附加资料等）的重视，表明需要继续丰富产品内容。
“包装”（45次）：虽然高频出现，但其中夹杂了正面和负面的反馈，需要在包装设计和质量上作进一步改进。
负面关键词：

“发货”（33次）：与物流和交付时间相关的负面评论较多，需要加强供应链和物流管理，减少发货延迟。
“瑕疵”（6次）：表明用户对产品质量有一定不满，可能涉及细节处理或材料问题，建议提高产品质量控制标准。
产品建议：

基于情绪分析的建议：
加强物流环节的管理，减少发货延迟；优化包装质量，减少负面评论和用户不满。

基于词频和关键词分析的建议：

强化产品设计和内容质量，突出用户喜欢的设计元素和内容丰富度。
解决负面情绪集中反映的问题，如提升包装质量和优化发货流程。
综合建议：
考虑在未来的促销活动中更好地利用用户的正面情绪反馈，扩大宣传力度；同时，针对用户反馈的负面意见（特别是物流和包装方面），制定相应的改进计划，以提升整体用户满意度。

以下是输入
'''

    user_message = HumanMessage(content=prompt)

    response = model([user_message])

    return response.content

print(report_maker(final_output))

"""#多轮对话"""

def continue_conversation(user_input, chat_history):
    # 格式化聊天记录为自然语言文本
    formatted_history = "\n".join([f"用户: {user}\nAI: {bot}" for user, bot in chat_history])

    # 构建提示语句
    prompt = f"之前的聊天记录是：\n{formatted_history}\n你需要结合之前的聊天记录，回答的问题是：{user_input}"

    # 创建一个 HumanMessage 对象
    user_message = HumanMessage(content=prompt)

    # 调用模型生成回复
    ai_response = model([user_message]).content

    # 更新聊天记录
    chat_history.append((user_input, ai_response))

    # 返回更新后的聊天记录和 AI 的回复
    return chat_history, ai_response

"""# 前端"""

import gradio as gr

def gradio_interface():
    # 生成初始报告内容
    initial_content = "这里是您的初始输入数据..."
    initial_report = report_maker(final_output)

     # 定义 Gradio 界面
    with gr.Blocks() as interface:
        gr.Markdown("### ❤AI报告")

        # 报告输出区域
        report_output = gr.Textbox(label="生成的报告", value=initial_report, lines=10)

        # 聊天区域
        chatbot = gr.Chatbot(label="你还可以问我更多关于评论的问题", height=400)
        user_message_input = gr.Textbox(label="你的问题", placeholder="在这里输入你的问题")
        chat_button = gr.Button("发送")

        # 全局变量：存储聊天历史记录
        chat_history = gr.State([])

        # 继续对话
        def on_continue_conversation(user_input, chat_history):
            updated_history, ai_response = continue_conversation(user_input, chat_history)
            return updated_history, updated_history, ""

        # 设置事件处理
        chat_button.click(
            on_continue_conversation,
            inputs=[user_message_input, chat_history],
            outputs=[chatbot, chat_history, user_message_input]
        )

    # 启动 Gradio 界面
    interface.launch()

# 运行界面
gradio_interface()