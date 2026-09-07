# -*- coding: utf-8 -*-
"""
工具封装
把现有的计算逻辑封装成LangChain Tool，供大模型调用
"""

from langchain_core.tools import tool


@tool
def calculate_wuyun_liuqi(birth_year: int, birth_month: int = None,
                           birth_day: int = None, birth_hour: str = None) -> dict:
    """
    根据出生日期计算五运六气和五脏能量。

    Args:
        birth_year: 出生年份（必填）
        birth_month: 出生月份（选填）
        birth_day: 出生日期（选填）
        birth_hour: 出生时辰（选填，如"午"）

    Returns:
        包含五运六气详情和五脏能量的字典
    """
    # TODO: 把前端HTML里的计算逻辑移植到这里
    # 现在先返回占位数据
    return {
        "energy": {"肝": 1, "心": 0, "脾": -1, "肺": 0, "肾": -2},
        "wuyun": "土运",
        "liuqi": "少阴君火司天",
        "note": "这是占位数据，后续需要移植完整的五运六气计算逻辑"
    }


@tool
def search_knowledge(query: str, k: int = 3) -> str:
    """
    从中医知识库中检索相关内容。

    Args:
        query: 检索关键词
        k: 返回结果数量

    Returns:
        检索到的知识片段文本
    """
    try:
        from rag.retriever import retrieve, format_docs
        docs = retrieve(query, k=k)
        return format_docs(docs)
    except Exception as e:
        return f"知识库检索失败：{str(e)}。请先运行 build_knowledge_base.py 构建向量库。"


@tool
def analyze_constitution(answers: dict) -> dict:
    """
    根据体质问卷答案分析体质类型。

    Args:
        answers: 问卷答案字典，格式为 {题号: 分数}

    Returns:
        体质分析结果
    """
    # TODO: 把前端HTML里的体质评分逻辑移植到这里
    return {
        "main_constitution": "平和质",
        "score": 75,
        "note": "这是占位数据，后续需要移植完整的体质评分逻辑"
    }


# 所有工具的列表，供LangGraph使用
ALL_TOOLS = [calculate_wuyun_liuqi, search_knowledge, analyze_constitution]
