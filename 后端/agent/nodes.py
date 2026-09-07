# -*- coding: utf-8 -*-
"""
LangGraph节点定义
每个节点是一个函数，输入State，输出更新后的State
"""

from typing import Dict
from .state import AgentState


def node_parse_input(state: AgentState) -> Dict:
    """
    节点1：解析用户输入
    从用户输入中提取出生年份、性别等信息
    """
    # TODO: 用大模型从自然语言中提取结构化信息
    # 现在先直接返回输入
    return {
        "current_step": "parse_input",
        "user_input": state.get("user_input", "")
    }


def node_calculate_wuyun(state: AgentState) -> Dict:
    """
    节点2：计算五运六气
    调用五运六气计算工具
    """
    # TODO: 调用 calculate_wuyun_liuqi 工具
    return {
        "current_step": "calculate_wuyun",
        "zang_energy": {"肝": 1, "心": 0, "脾": -1, "肺": 0, "肾": -2}
    }


def node_retrieve_knowledge(state: AgentState) -> Dict:
    """
    节点3：检索知识库
    根据五脏能量和用户问题检索相关知识
    """
    # TODO: 调用 search_knowledge 工具
    return {
        "current_step": "retrieve_knowledge",
        "retrieved_docs": []
    }


def node_generate_answer(state: AgentState) -> Dict:
    """
    节点4：生成最终回答
    大模型综合所有信息生成回答
    """
    # TODO: 调用大模型生成回答
    return {
        "current_step": "generate_answer",
        "final_answer": "这是占位回答，后续需要实现大模型生成逻辑"
    }
