# -*- coding: utf-8 -*-
"""测试LangChain工具"""
import sys
sys.path.insert(0, '.')

from agent.tools import calculate_wuyun_liuqi, ALL_TOOLS

print('=' * 60)
print('测试1：直接调用五运六气计算工具')
print('=' * 60)

# 直接调用工具（传入字典）
result = calculate_wuyun_liuqi.invoke({
    'birth_year': 1995,
    'birth_province': '河北省',
    'current_province': '北京市',
    'occupation': 'it',
    'gender': 'male',
    'current_age': 30
})

print(f"天干地支: {result['ganzhi']}")
print(f"中运: {result['zhongyun']}")
print(f"司天在泉: {result['sitian']}")
print(f"先天能量: {result['congenital_energy']}")
print(f"当前能量: {result['current_energy']}")
print(f"体质: {result['constitution']['name']} - {result['constitution']['desc']}")
print(f"精细化计算: {'有' if result['detailed_luck_qi'] else '无（未填写月日）'}")

print()
print('=' * 60)
print('测试2：带月日时的精细化计算')
print('=' * 60)

result2 = calculate_wuyun_liuqi.invoke({
    'birth_year': 1995,
    'birth_month': 6,
    'birth_day': 15,
    'birth_hour': '午',
    'birth_province': '河北省',
    'current_province': '北京市',
    'occupation': 'it',
    'gender': 'male',
    'current_age': 30
})

print(f"天干地支: {result2['ganzhi']}")
print(f"当前能量: {result2['current_energy']}")
print(f"体质: {result2['constitution']['name']}")
if result2['detailed_luck_qi']:
    dq = result2['detailed_luck_qi']
    print(f"主气: {dq['zhu_qi']} ({dq['zhu_qi_zang']})")
    print(f"客气: {dq['ke_qi']} ({dq['ke_qi_zang']})")
    print(f"客主加临: {dq['shun_ni']}")
    print(f"运气同化: {dq['tong_hua']}")

print()
print('=' * 60)
print('测试3：查看所有可用工具')
print('=' * 60)
for tool in ALL_TOOLS:
    print(f"  - {tool.name}: {tool.description[:80]}...")

print()
print('所有测试完成！')
