# -*- coding: utf-8 -*-
"""
LangGraph智能体状态定义
整个流程共享的数据结构
"""

from typing import TypedDict, Optional, List, Dict
from langgraph.graph.message import add_messages
from typing import Annotated


class AgentState(TypedDict):
    """
    智能体状态
    每个节点执行后，会更新这个状态里的字段
    """
    # ===== 用户输入 =====
    user_input: str  # 用户的原始输入
    birth_year: Optional[int]  # 出生年份
    birth_month: Optional[int]  # 出生月份
    birth_day: Optional[int]  # 出生日期
    birth_hour: Optional[str]  # 出生时辰
    gender: Optional[str]  # 性别
    birth_province: Optional[str]  # 出生省份
    current_province: Optional[str]  # 现居省份
    occupation: Optional[str]  # 职业

    # ===== 推演结果 =====
    zang_energy: Optional[Dict[str, int]]  # 五脏能量：{肝: 1, 心: 0, ...}
    constitution: Optional[str]  # 体质类型
    top_symptoms: Optional[List[str]]  # Top5症状
    syndrome_patterns: Optional[List[str]]  # 复合证型

    # ===== 知识库检索 =====
    retrieved_docs: Optional[List]  # 检索到的知识片段

    # ===== 对话历史 =====
    messages: Annotated[list, add_messages]  # 对话历史（LangGraph内置的消息列表）

    # ===== 其他 =====
    current_step: str  # 当前执行到哪一步
    final_answer: Optional[str]  # 最终回答
