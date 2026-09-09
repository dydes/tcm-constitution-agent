# -*- coding: utf-8 -*-
"""
测试大模型调用工具的能力
用DeepSeek + LangGraph create_react_agent测试
"""
import sys
import os
sys.path.insert(0, '.')

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from agent.tools import ALL_TOOLS

# 初始化大模型（DeepSeek兼容OpenAI接口）
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    temperature=0.3
)

# 系统提示词
system_prompt = """你是一个中医健康咨询助手。
当用户询问体质、五脏能量、先天禀赋等问题时，你需要调用五运六气计算工具来获取准确的数据。
当用户询问中医知识、养生方法时，你可以调用知识库检索工具来获取参考资料。
请用通俗易懂的语言回答用户的问题，不要使用太多专业术语。"""

# 创建agent（LangChain 1.x新API）
agent = create_agent(
    model=llm,
    tools=ALL_TOOLS,
    system_prompt=system_prompt
)

print('=' * 60)
print('测试1：询问1995年出生的人的体质')
print('（大模型应该调用calculate_wuyun_liuqi工具）')
print('=' * 60)

result1 = agent.invoke({
    "messages": [
        ("human", "我是1995年出生的，男生，出生在河北省，现在住在北京，做IT行业，今年30岁。帮我看看我的体质和五脏能量情况。")
    ]
})

print()
print("大模型回答：")
print(result1["messages"][-1].content)

print()
print('=' * 60)
print('测试2：询问中医知识')
print('（大模型应该调用search_knowledge工具）')
print('=' * 60)

result2 = agent.invoke({
    "messages": [
        ("human", "肝火旺的人有什么症状？应该怎么调理？")
    ]
})

print()
print("大模型回答：")
print(result2["messages"][-1].content)

print()
print('=' * 60)
print('测试完成！')
print('=' * 60)
