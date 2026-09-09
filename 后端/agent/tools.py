# -*- coding: utf-8 -*-
"""
工具封装
把现有的计算逻辑封装成LangChain Tool，供大模型调用
"""

from langchain_core.tools import tool


@tool
def calculate_wuyun_liuqi(
    birth_year: int,
    birth_province: str = "北京市",
    current_province: str = "北京市",
    occupation: str = None,
    gender: str = "male",
    current_age: int = 30,
    birth_month: int = None,
    birth_day: int = None,
    birth_hour: str = None
) -> dict:
    """
    根据出生信息计算五运六气和五脏能量格局。
    这是中医体质推演的核心工具，能算出先天禀赋和后天受影响后的五脏能量。

    Args:
        birth_year: 出生年份（必填），如1995
        birth_province: 出生省份（选填），如"河北省"、"广东省"
        current_province: 现居省份（选填），如"北京市"、"上海市"
        occupation: 职业类型（选填），可选值：it/design/finance/education/medical/sales/manager/manufacture/service/student/freelance/retired
        gender: 性别（选填），"male"或"female"，默认"male"
        current_age: 当前年龄（选填），默认30
        birth_month: 出生月份（选填，1-12），填写后启用五运六气精细化计算
        birth_day: 出生日期（选填，1-31），填写后启用精细化计算
        birth_hour: 出生时辰（选填），如"子"、"丑"、"寅"、"卯"、"辰"、"巳"、"午"、"未"、"申"、"酉"、"戌"、"亥"

    Returns:
        包含五运六气详情和五脏能量的字典，包括：
        - ganzhi: 天干地支
        - zhongyun: 中运（大运）
        - sitian: 司天在泉
        - congenital_energy: 先天能量（出生时的五脏能量）
        - current_energy: 当前能量（受后天环境、职业、年龄影响后）
        - constitution: 体质类型判断
        - details: 每个脏器的影响因素详情
        - detailed_luck_qi: 五运六气精细化计算结果（填写了月日时才有）
    """
    from agent.wuyun_liuqi import calc_zang_energy, judge_constitution

    input_data = {
        'birth_year': birth_year,
        'birth_province': birth_province,
        'current_province': current_province,
        'occupation': occupation,
        'gender': gender,
        'current_age': current_age
    }

    # 如果填写了月日，加入精细化计算
    if birth_month and birth_day:
        input_data['birth_month'] = birth_month
        input_data['birth_day'] = birth_day
        if birth_hour:
            input_data['birth_hour'] = birth_hour

    # 执行计算
    result = calc_zang_energy(input_data)
    constitution = judge_constitution(result['energy'])

    # 整理返回结果
    return {
        'ganzhi': f"{result['ganzhi']['gan']}{result['ganzhi']['zhi']}",
        'zhongyun': result['zhongyun']['desc'],
        'sitian': result['sitian']['desc'],
        'congenital_energy': result['congenital'],
        'current_energy': result['energy'],
        'constitution': {
            'name': constitution['name'],
            'desc': constitution['desc']
        },
        'details': result['details'],
        'detailed_luck_qi': result['detailed_luck_qi']
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
