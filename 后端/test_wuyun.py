# -*- coding: utf-8 -*-
"""测试五运六气计算模块"""
import sys
sys.path.insert(0, '.')

from agent.wuyun_liuqi import quick_calc, calc_zang_energy, judge_constitution

# 测试1：快速计算（1995年男生，河北石家庄）
print('=' * 60)
print('测试1：1995年男生，出生河北，现居北京，IT行业，30岁')
print('=' * 60)
result = quick_calc(
    birth_year=1995,
    birth_province='河北省',
    current_province='北京市',
    occupation='it',
    gender='male',
    current_age=30
)
print(f"天干地支: {result['ganzhi']['gan']}{result['ganzhi']['zhi']}")
print(f"中运: {result['zhongyun']['desc']}")
print(f"司天在泉: {result['sitian']['desc']}")
print(f"先天能量: {result['congenital']}")
print(f"后天能量: {result['energy']}")
print(f"体质: {result['constitution']['name']} - {result['constitution']['desc']}")

# 测试2：带月日时的精细化计算
print()
print('=' * 60)
print('测试2：1995年6月15日午时出生，精细化计算')
print('=' * 60)
input_data = {
    'birth_year': 1995,
    'birth_month': 6,
    'birth_day': 15,
    'birth_hour': '午',
    'birth_province': '河北省',
    'current_province': '北京市',
    'occupation': 'it',
    'gender': 'male',
    'current_age': 30
}
result2 = calc_zang_energy(input_data)
print(f"主气: {result2['detailed_luck_qi']['zhu_qi']} ({result2['detailed_luck_qi']['zhu_qi_zang']})")
print(f"客气: {result2['detailed_luck_qi']['ke_qi']} ({result2['detailed_luck_qi']['ke_qi_zang']})")
print(f"客主加临: {result2['detailed_luck_qi']['shun_ni']}")
print(f"运气同化: {result2['detailed_luck_qi']['tong_hua']}")
print(f"出生时辰: {result2['detailed_luck_qi']['shichen']}时，{result2['detailed_luck_qi']['shichen_zang']}经当令")
print(f"最终能量: {result2['energy']}")
print()
print('计算详情（每个脏器的影响因素）:')
for zang, details in result2['details'].items():
    print(f"  {zang}: {details}")

print()
print('=' * 60)
print('测试完成！')
print('=' * 60)
