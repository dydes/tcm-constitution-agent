# -*- coding: utf-8 -*-
"""
LangGraph图编排
把各个节点串起来，形成完整的智能体流程
"""

from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes import (
    node_parse_input,
    node_calculate_wuyun,
    node_retrieve_knowledge,
    node_generate_answer
)


def build_graph():
    """
    构建LangGraph状态机

    流程：
    解析用户输入 → 计算五运六气 → 检索知识库 → 生成回答 → 结束
    """
    workflow = StateGraph(AgentState)

    # 添加节点
    workflow.add_node("parse_input", node_parse_input)
    workflow.add_node("calculate_wuyun", node_calculate_wuyun)
    workflow.add_node("retrieve_knowledge", node_retrieve_knowledge)
    workflow.add_node("generate_answer", node_generate_answer)

    # 设置入口
    workflow.set_entry_point("parse_input")

    # 设置边（流程顺序）
    workflow.add_edge("parse_input", "calculate_wuyun")
    workflow.add_edge("calculate_wuyun", "retrieve_knowledge")
    workflow.add_edge("retrieve_knowledge", "generate_answer")
    workflow.add_edge("generate_answer", END)

    # 编译
    app = workflow.compile()
    return app


# 全局实例
graph_app = None


def get_graph():
    """获取图实例（懒加载）"""
    global graph_app
    if graph_app is None:
        graph_app = build_graph()
    return graph_app
