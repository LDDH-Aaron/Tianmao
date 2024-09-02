# 短学期项目

天猫商品评论爬取与可视化分析

【问题说明】
我们通过在线购物平台进行购物前，通常都会参考其他用户对已购商品的评论，以便更好地进行购物决策，商家也可以根据用户评论，不断完善商品或调整经营决策，通过人工搜集评论数据耗时费力，因此如何自动搜集用户评论信息并进行分析非常重要。

【任务清单】
本课题要求对天猫商品评论数据进行爬取与可视化分析（也可以对其他在线购物平台的商品评论进行爬取和可视化分析）。具体要求：

- 输入商品名称，提示查看第几个商品的评论信息，获取买家对商品的评论并保存到本地。
- 评论内容分析与可视化：对评论内容进行中文进行分词，根据用户需求如词云形状、颜色、大小等等设置词云；
- 情感分析：对商品评论文本进行情感分析（找出文本中作者对某个实体（包括产品、服务、人、组织机构、事件、话题）的评判态度（支持或反对、喜欢或厌恶等）或情感状态（高兴、愤怒、悲伤、恐惧等））
- 其它数据分析：对爬取的相关数据进行其它分析和图形显示，参考文献，但需有扩展（某商品中、差评预警）；
- 天猫商品评论可视化系统设计与开发
- 自主创新内容

# 任务拆分  

## 模块1

([@NingmengLemon](https://github.com/NingmengLemon))

1. 爬取数据

## 模块2

([@YXZ252426](https://github.com/YXZ252426))

1. 基础数据分析
2. 可视化

## 模块3

([@NingmengLemon](https://github.com/NingmengLemon))

1. 分词
2. 可视化

## 模块4

([@LDDH-Aaron](https://github.com/LDDH-Aaron))

1. 情感分析

## 模块5

([@LDDH-Aaron](https://github.com/LDDH-Aaron))

1. AI问答助手的加入

## 模块6

([@YXZ252426](https://github.com/YXZ252426))
1. 前端设计 

# TODO

- 代码
- 结题报告 yxz 
- ppt gcx
- 汇报答辩 hmy 
## 项目文档

> 此项目可以分成三大模块：1.爬虫与词云统计 2.前端数据展示 3. AI模块

### 爬虫与词云统计

### 前端数据展示

此次前端展示所用到的技术是gradio(Gradio 是一个用于创建机器学习模型和数据科学应用的简单易用的 Python 库。它允许开发者通过几行代码快速构建和共享交互式用户界面，无需前端开发知识。)数据处理用到了pandas库，而绘图用的是matplotlib

#### 代码简析

第一步要读取json文件并将数据转化成DataFrame

在代码里写了三个函数`` plot_bar_chart`` `` plot_pie_chart`` `` plot_cloud_char``分别用于绘制柱状图，饼状图和词云

代码还对时间做了处理，以每五天为一个单位划分以实现更好的展示效果

在前端界面设置了输入框，输入想要查询的评论区链接就并点击按钮就可以开始爬虫

贴心地增加了进度条，当处理完成后就会分别输出不同时间段评论数量统计图，用户评价情感分析图，以及词云

闲来无事的我甚至还为界面的标题设置了CSS样式，至于具体是如何实现的就不展开讲了

#### 操作方式
执行showByGradio文件，点击输出的端口即可进入浏览器前端界面，输入想要爬虫的商品链接，稍等片刻即可输出图表