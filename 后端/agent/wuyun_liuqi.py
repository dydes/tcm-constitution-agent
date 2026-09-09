# -*- coding: utf-8 -*-
"""
五运六气计算模块
从前端HTML移植，保持计算逻辑完全一致
"""

# ========== 基础数据定义 ==========

TIAN_GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
DI_ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

GAN_WUXING = {'甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土', '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水'}
GAN_YINYANG = {'甲': '阳', '乙': '阴', '丙': '阳', '丁': '阴', '戊': '阳', '己': '阴', '庚': '阳', '辛': '阴', '壬': '阳', '癸': '阴'}
ZANG_WUXING = {'木': '肝', '火': '心', '土': '脾', '金': '肺', '水': '肾'}
WUXING_ZANG = {'肝': '木', '心': '火', '脾': '土', '肺': '金', '肾': '水'}

# 五行相生：木生火、火生土、土生金、金生水、水生木
SHENG = {'木': '火', '火': '土', '土': '金', '金': '水', '水': '木'}
# 五行相克：木克土、土克水、水克火、火克金、金克木
KE = {'木': '土', '土': '水', '水': '火', '火': '金', '金': '木'}

ZHI_LIUQI = {
    '子': '少阴君火', '午': '少阴君火',
    '丑': '太阴湿土', '未': '太阴湿土',
    '寅': '少阳相火', '申': '少阳相火',
    '卯': '阳明燥金', '酉': '阳明燥金',
    '辰': '太阳寒水', '戌': '太阳寒水',
    '巳': '厥阴风木', '亥': '厥阴风木'
}
LIUQI_WUXING = {
    '厥阴风木': '木', '少阴君火': '火', '少阳相火': '火',
    '太阴湿土': '土', '阳明燥金': '金', '太阳寒水': '水'
}

KE_QI_ORDER = ['厥阴风木', '少阴君火', '太阴湿土', '少阳相火', '阳明燥金', '太阳寒水']

# 主气六步
ZHU_QI = [
    {'name': '初之气', 'qi': '厥阴风木', 'period': '大寒-春分', 'zang': '肝', 'desc': '风气主事，万物始生'},
    {'name': '二之气', 'qi': '少阴君火', 'period': '春分-小满', 'zang': '心', 'desc': '火气主事，万物繁茂'},
    {'name': '三之气', 'qi': '少阳相火', 'period': '小满-大暑', 'zang': '心/心包', 'desc': '暑气主事，炎热极盛'},
    {'name': '四之气', 'qi': '太阴湿土', 'period': '大暑-秋分', 'zang': '脾', 'desc': '湿气主事，长夏养长'},
    {'name': '五之气', 'qi': '阳明燥金', 'period': '秋分-小雪', 'zang': '肺', 'desc': '燥气主事，万物收敛'},
    {'name': '终之气', 'qi': '太阳寒水', 'period': '小雪-大寒', 'zang': '肾', 'desc': '寒气主事，万物闭藏'}
]

# 十二时辰子午流注
SHICHEN_ZANG = {
    '子': '胆', '丑': '肝', '寅': '肺', '卯': '大肠', '辰': '胃', '巳': '脾',
    '午': '心', '未': '小肠', '申': '膀胱', '酉': '肾', '戌': '心包', '亥': '三焦'
}
SHICHEN_ZANG_MAIN = {
    '子': '肾', '丑': '肝', '寅': '肺', '卯': '肺', '辰': '脾', '巳': '脾',
    '午': '心', '未': '心', '申': '膀胱', '酉': '肾', '戌': '心包', '亥': '三焦'
}

# 省份方向映射（简化版，只保留省份和方向）
PROVINCE_DIRECTION = {
    '北京市': '北', '天津市': '北', '河北省': '中', '山西省': '中', '内蒙古自治区': '北',
    '辽宁省': '北', '吉林省': '北', '黑龙江省': '北',
    '上海市': '东', '江苏省': '东', '浙江省': '东', '安徽省': '东', '福建省': '南', '江西省': '中', '山东省': '东',
    '河南省': '中', '湖北省': '中', '湖南省': '南',
    '广东省': '南', '广西壮族自治区': '南', '海南省': '南',
    '重庆市': '南', '四川省': '西', '贵州省': '南', '云南省': '西', '西藏自治区': '西',
    '陕西省': '西', '甘肃省': '西', '青海省': '西', '宁夏回族自治区': '西', '新疆维吾尔自治区': '西',
    '台湾省': '东', '香港特别行政区': '南', '澳门特别行政区': '南'
}

# 职业影响
OCCUPATION_EFFECTS = {
    'it': {'name': '互联网/IT-程序员', 'effects': {'心': -1, '肝': -1, '脾': -1, '肺': 0, '肾': 0}, 'tags': ['久坐', '久视屏幕', '熬夜', '用脑过度', '缺乏运动']},
    'design': {'name': '设计/创意', 'effects': {'心': -1, '肝': -1, '脾': 0, '肺': 0, '肾': 0}, 'tags': ['久坐', '久视', '熬夜', '精神紧张']},
    'finance': {'name': '金融/投资', 'effects': {'心': -1, '肝': -1, '脾': -1, '肺': 0, '肾': 0}, 'tags': ['久坐', '精神高压', '熬夜', '思虑过度']},
    'education': {'name': '教育/培训', 'effects': {'心': 0, '肝': 0, '脾': -1, '肺': -1, '肾': 0}, 'tags': ['久站', '多言', '用嗓过度', '思虑']},
    'medical': {'name': '医疗/健康', 'effects': {'心': -1, '肝': 0, '脾': -1, '肺': 0, '肾': 0}, 'tags': ['倒班', '熬夜', '精神紧张', '久站']},
    'sales': {'name': '销售/市场', 'effects': {'心': 0, '肝': -1, '脾': -1, '肺': 0, '肾': 0}, 'tags': ['应酬', '饮酒', '饮食不规律', '奔波']},
    'manager': {'name': '管理/行政', 'effects': {'心': -1, '肝': -1, '脾': 0, '肺': 0, '肾': 0}, 'tags': ['久坐', '思虑过度', '精神压力', '应酬']},
    'manufacture': {'name': '制造/生产', 'effects': {'心': 0, '肝': 0, '脾': 0, '肺': -1, '肾': -1}, 'tags': ['久站', '体力劳动', '噪音', '粉尘', '倒班']},
    'service': {'name': '服务/餐饮', 'effects': {'心': 0, '肝': 0, '脾': -1, '肺': 0, '肾': -1}, 'tags': ['久站', '多言', '饮食不规律', '熬夜']},
    'student': {'name': '学生', 'effects': {'心': -1, '肝': 0, '脾': -1, '肺': 0, '肾': 0}, 'tags': ['久坐', '久视', '用脑过度', '熬夜', '饮食不规律']},
    'freelance': {'name': '自由职业', 'effects': {'心': 0, '肝': 0, '脾': -1, '肺': 0, '肾': 0}, 'tags': ['作息不规律', '久坐', '饮食不规律']},
    'retired': {'name': '退休', 'effects': {'心': 0, '肝': 0, '脾': 0, '肺': 0, '肾': -1}, 'tags': ['活动减少', '肾气渐衰', '闲逸过度']}
}


# ========== 基础计算函数 ==========

def get_gan_zhi(year):
    """根据年份计算天干地支"""
    gan_index = (year - 4) % 10
    zhi_index = (year - 4) % 12
    return {
        'gan': TIAN_GAN[gan_index],
        'zhi': DI_ZHI[zhi_index],
        'gan_index': gan_index,
        'zhi_index': zhi_index
    }


def get_zhong_yun(gan):
    """计算中运（大运）"""
    wx = GAN_WUXING[gan]
    yy = GAN_YINYANG[gan]
    z = ZANG_WUXING[wx]
    is_tai_guo = (yy == '阳')
    value = 2 if is_tai_guo else -2
    return {
        'wuxing': wx,
        'zang': z,
        'is_tai_guo': is_tai_guo,
        'value': value,
        'desc': f"{gan}为{yy}干，属{wx}，{z}运{'太过' if is_tai_guo else '不及'}"
    }


def get_si_tian_zai_quan(zhi):
    """计算司天在泉"""
    st = ZHI_LIUQI[zhi]
    stwx = LIUQI_WUXING[st]
    stz = ZANG_WUXING[stwx]
    zi = DI_ZHI.index(zhi)
    zqz = DI_ZHI[(zi + 6) % 12]
    zq = ZHI_LIUQI[zqz]
    zqwx = LIUQI_WUXING[zq]
    zqzang = ZANG_WUXING[zqwx]
    return {
        'si_tian': st,
        'si_tian_zang': stz,
        'zai_quan': zq,
        'zai_quan_zang': zqzang,
        'desc': f"{zhi}年司天为{st}（{stz}），在泉为{zq}（{zqzang}）"
    }


def get_direction(province):
    """获取省份所属方向"""
    return PROVINCE_DIRECTION.get(province, '中')


# ========== 五运六气精细化计算 ==========

def calc_detailed_luck_qi(year, month, day, hour=None, calendar_type='solar'):
    """
    五运六气精细化计算
    填写了月日时才执行
    """
    try:
        solar_month = month
        solar_day = day

        # 确定主气（二十四节气划分）
        solar_terms = [
            {'month': 1, 'day': 20, 'qi': '太阳寒水', 'zang': '肾'},
            {'month': 2, 'day': 4, 'qi': '厥阴风木', 'zang': '肝'},
            {'month': 3, 'day': 21, 'qi': '少阴君火', 'zang': '心'},
            {'month': 5, 'day': 21, 'qi': '少阳相火', 'zang': '心/心包'},
            {'month': 7, 'day': 23, 'qi': '太阴湿土', 'zang': '脾'},
            {'month': 9, 'day': 23, 'qi': '阳明燥金', 'zang': '肺'},
            {'month': 11, 'day': 22, 'qi': '太阳寒水', 'zang': '肾'}
        ]

        zhu_qi = '厥阴风木'
        zhu_qi_zang = '肝'
        for i in range(len(solar_terms) - 1, -1, -1):
            if solar_month > solar_terms[i]['month'] or (solar_month == solar_terms[i]['month'] and solar_day >= solar_terms[i]['day']):
                zhu_qi = solar_terms[i]['qi']
                zhu_qi_zang = solar_terms[i]['zang']
                break

        # 确定客气（司天在泉+左右间气）
        ganzhi = get_gan_zhi(year)
        si_tian_qi = ZHI_LIUQI[ganzhi['zhi']]
        si_tian_idx = KE_QI_ORDER.index(si_tian_qi)
        zai_quan_idx = (si_tian_idx + 3) % 6

        # 三之气为司天，六之气为在泉
        ke_qi = si_tian_qi
        ke_qi_zang = ZANG_WUXING[LIUQI_WUXING[si_tian_qi]]
        qi_step = (solar_month - 1) // 2
        if qi_step == 2:
            ke_qi = si_tian_qi
            ke_qi_zang = ZANG_WUXING[LIUQI_WUXING[si_tian_qi]]
        elif qi_step == 5:
            ke_qi = KE_QI_ORDER[zai_quan_idx]
            ke_qi_zang = ZANG_WUXING[LIUQI_WUXING[KE_QI_ORDER[zai_quan_idx]]]
        else:
            offset = qi_step + 4 if qi_step < 2 else qi_step - 3
            ke_idx = (si_tian_idx + offset) % 6
            ke_qi = KE_QI_ORDER[ke_idx]
            ke_qi_zang = ZANG_WUXING[LIUQI_WUXING[ke_qi]]

        # 客主加临顺逆判断
        ke_wuxing = LIUQI_WUXING[ke_qi]
        zhu_wuxing = LIUQI_WUXING[zhu_qi]
        shun_ni = '顺'
        if ke_wuxing == zhu_wuxing:
            shun_ni = '同（天符）'
        elif SHENG[ke_wuxing] == zhu_wuxing:
            shun_ni = '顺（客生主）'
        elif KE[ke_wuxing] == zhu_wuxing:
            shun_ni = '逆（客克主）'
        elif SHENG[zhu_wuxing] == ke_wuxing:
            shun_ni = '逆（主生客）'

        # 运气同化判断
        zhongyun_wuxing = GAN_WUXING[ganzhi['gan']]
        tong_hua = ''
        if zhongyun_wuxing == LIUQI_WUXING[si_tian_qi]:
            tong_hua = '天符'
        if zhongyun_wuxing == LIUQI_WUXING[KE_QI_ORDER[zai_quan_idx]]:
            tong_hua = tong_hua + '同天符' if tong_hua else '岁会（在泉）'

        # 主气修正值（顺则+1，逆则-1，同则+2）
        zhu_qi_adjust = 1
        if '逆' in shun_ni:
            zhu_qi_adjust = -1
        elif '同' in shun_ni:
            zhu_qi_adjust = 2

        # 客气修正值（司天/在泉年份+1，间气0）
        ke_qi_adjust = 1 if qi_step in [2, 5] else 0

        # 出生时辰子午流注禀赋
        shichen = hour
        shichen_zang = None
        if shichen and shichen in SHICHEN_ZANG:
            shichen_zang = SHICHEN_ZANG[shichen]

        return {
            'zhu_qi': zhu_qi,
            'zhu_qi_zang': zhu_qi_zang,
            'zhu_qi_adjust': zhu_qi_adjust,
            'ke_qi': ke_qi,
            'ke_qi_zang': ke_qi_zang,
            'ke_qi_adjust': ke_qi_adjust,
            'shun_ni': shun_ni,
            'tong_hua': tong_hua,
            'shichen': shichen,
            'shichen_zang': shichen_zang
        }
    except Exception as e:
        print(f"精细化计算失败: {e}")
        return None


# ========== 核心：五脏能量综合计算 ==========

def calc_zang_energy(input_data):
    """
    五脏能量综合计算（核心函数）
    input_data: {
        birth_year: int,
        birth_month: int (可选),
        birth_day: int (可选),
        birth_hour: str (可选，如'午'),
        birth_province: str,
        current_province: str,
        occupation: str (可选，如'it'),
        gender: str ('male'/'female'),
        current_age: int
    }
    """
    birth_year = input_data['birth_year']
    birth_month = input_data.get('birth_month')
    birth_day = input_data.get('birth_day')
    birth_hour = input_data.get('birth_hour')
    birth_province = input_data.get('birth_province', '北京市')
    current_province = input_data.get('current_province', '北京市')
    occupation = input_data.get('occupation')
    gender = input_data.get('gender', 'male')
    current_age = input_data.get('current_age', 30)
    calendar_type = input_data.get('calendar_type', 'solar')

    # 基础计算
    ganzhi = get_gan_zhi(birth_year)
    zhongyun = get_zhong_yun(ganzhi['gan'])
    sitian = get_si_tian_zai_quan(ganzhi['zhi'])
    birth_dir = get_direction(birth_province)
    current_dir = get_direction(current_province)
    occ = OCCUPATION_EFFECTS.get(occupation) if occupation else None

    # 初始化能量和详情
    energy = {'肝': 0, '心': 0, '脾': 0, '肺': 0, '肾': 0}
    details = {'肝': [], '心': [], '脾': [], '肺': [], '肾': []}

    # 1. 中运影响
    energy[zhongyun['zang']] += zhongyun['value']
    details[zhongyun['zang']].append(
        f"中运{zhongyun['zang']}{'太过' if zhongyun['is_tai_guo'] else '不及'}"
        f"({'+' if zhongyun['value'] > 0 else ''}{zhongyun['value']})"
    )

    # 2. 司天在泉影响
    energy[sitian['si_tian_zang']] += 1
    details[sitian['si_tian_zang']].append(f"司天{sitian['si_tian']}(+1)")
    energy[sitian['zai_quan_zang']] += 1
    details[sitian['zai_quan_zang']].append(f"在泉{sitian['zai_quan']}(+1)")

    # 3. 五行生克乘侮影响
    zangs = ['肝', '心', '脾', '肺', '肾']
    for z in zangs:
        wx = WUXING_ZANG[z]
        # 母脏（生我者）
        mother_wx = [k for k, v in SHENG.items() if v == wx][0]
        mother_z = ZANG_WUXING[mother_wx]
        # 克我者
        keme_wx = [k for k, v in KE.items() if v == wx][0]
        keme_z = ZANG_WUXING[keme_wx]
        # 我克者
        meke_z = ZANG_WUXING[KE[wx]]

        if energy[mother_z] >= 1:
            energy[z] += 1
            details[z].append(f"母脏{mother_z}偏旺，相生(+1)")
        if energy[mother_z] <= -1:
            energy[z] -= 1
            details[z].append(f"母脏{mother_z}偏弱，生源不足(-1)")
        if energy[keme_z] >= 1:
            energy[z] -= 1
            details[z].append(f"克我之{keme_z}偏旺，相乘(-1)")
        if energy[meke_z] <= -1:
            energy[z] += 1
            details[z].append(f"我克之{meke_z}偏弱，反侮(+1)")

    # 4. 出生地方向影响
    dir_zang_map = {'东': '肝', '南': '心', '中': '脾', '西': '肺', '北': '肾'}
    birth_zang = dir_zang_map[birth_dir]
    energy[birth_zang] += 1
    details[birth_zang].append(f"出生地属{birth_dir}方，{birth_zang}气得地之助(+1)")

    # 保存先天能量（后天影响前）
    congenital = dict(energy)

    # 5. 现居地方向影响
    current_zang = dir_zang_map[current_dir]
    if current_dir != birth_dir:
        energy[current_zang] += 1
        details[current_zang].append(f"现居地属{current_dir}方，{current_zang}气受环境影响(+1)")

    # 6. 职业影响
    if occ:
        for z in zangs:
            if occ['effects'][z] != 0:
                energy[z] += occ['effects'][z]
                details[z].append(
                    f"职业{occ['name']}，{z}{'受益' if occ['effects'][z] > 0 else '受损'}"
                    f"({'+' if occ['effects'][z] > 0 else ''}{occ['effects'][z]})"
                )

    # 7. 年龄生命节律影响
    age = current_age
    is_male = (gender == 'male')
    if is_male:
        if age >= 40:
            energy['肾'] -= 1
            details['肾'].append('年逾四十，肾气渐衰(-1)')
        if age >= 48:
            energy['肝'] -= 1
            details['肝'].append('年近五十，肝气始衰(-1)')
        if age >= 56:
            energy['心'] -= 1
            details['心'].append('年过八八，心气始衰(-1)')
    else:
        if age >= 35:
            energy['脾'] -= 1
            details['脾'].append('五七阳明脉衰，脾气始弱(-1)')
        if age >= 42:
            energy['肝'] -= 1
            details['肝'].append('六七三阳脉衰，肝气始弱(-1)')
        if age >= 49:
            energy['肾'] -= 1
            details['肾'].append('七七任脉虚，肾气衰(-1)')

    # 8. 五运六气精细化（填写了月日时才执行）
    detailed_luck_qi = None
    if birth_month and birth_day:
        detailed_luck_qi = calc_detailed_luck_qi(
            birth_year, birth_month, birth_day, birth_hour, calendar_type
        )
        if detailed_luck_qi:
            # 主气修正
            if detailed_luck_qi['zhu_qi_zang'] and detailed_luck_qi['zhu_qi_zang'] != '心/心包':
                energy[detailed_luck_qi['zhu_qi_zang']] += detailed_luck_qi['zhu_qi_adjust']
                details[detailed_luck_qi['zhu_qi_zang']].append(
                    f"主气{detailed_luck_qi['zhu_qi']}（{detailed_luck_qi['zhu_qi_zang']}）"
                    f"{'+' if detailed_luck_qi['zhu_qi_adjust'] > 0 else ''}{detailed_luck_qi['zhu_qi_adjust']}"
                )
            # 客气修正
            if detailed_luck_qi['ke_qi_zang'] and detailed_luck_qi['ke_qi_zang'] != '心/心包':
                energy[detailed_luck_qi['ke_qi_zang']] += detailed_luck_qi['ke_qi_adjust']
                details[detailed_luck_qi['ke_qi_zang']].append(
                    f"客气{detailed_luck_qi['ke_qi']}（{detailed_luck_qi['ke_qi_zang']}）"
                    f"{'+' if detailed_luck_qi['ke_qi_adjust'] > 0 else ''}{detailed_luck_qi['ke_qi_adjust']}"
                )
            # 出生时辰子午流注禀赋
            if (detailed_luck_qi['shichen_zang'] and
                    detailed_luck_qi['shichen_zang'] not in ['心包', '三焦', '胆', '胃', '大肠', '小肠', '膀胱']):
                energy[detailed_luck_qi['shichen_zang']] += 1
                details[detailed_luck_qi['shichen_zang']].append(
                    f"出生{detailed_luck_qi['shichen']}时，{detailed_luck_qi['shichen_zang']}经当令禀赋(+1)"
                )

    # 9. 能量限制在-3到+3之间
    for z in zangs:
        energy[z] = max(-3, min(3, energy[z]))

    return {
        'energy': energy,
        'congenital': congenital,
        'details': details,
        'ganzhi': ganzhi,
        'zhongyun': zhongyun,
        'sitian': sitian,
        'birth_dir': birth_dir,
        'current_dir': current_dir,
        'occ': occ,
        'detailed_luck_qi': detailed_luck_qi
    }


# ========== 体质判断 ==========

# 体质类型（简化版，只保留名称和描述）
CONSTITUTIONS = [
    {'name': '平和质', 'desc': '阴阳气血调和，体态适中、面色红润、精力充沛'},
    {'name': '气虚质', 'desc': '元气不足，疲乏、气短、自汗'},
    {'name': '阳虚质', 'desc': '阳气不足，畏寒怕冷、手足不温'},
    {'name': '阴虚质', 'desc': '阴液亏少，口燥咽干、手足心热'},
    {'name': '痰湿质', 'desc': '痰湿凝聚，形体肥胖、腹部肥满、口黏苔腻'},
    {'name': '湿热质', 'desc': '湿热内蕴，面垢油光、口苦、苔黄腻'},
    {'name': '血瘀质', 'desc': '血行不畅，肤色晦暗、舌质紫暗'},
    {'name': '气郁质', 'desc': '气机郁滞，神情抑郁、情感脆弱'},
    {'name': '特禀质', 'desc': '先天失常，生理缺陷、过敏反应'}
]


def judge_constitution(energy):
    """根据五脏能量判断体质类型"""
    zangs = ['肝', '心', '脾', '肺', '肾']
    # 全部在-1到1之间为平和质
    if all(-1 <= energy[z] <= 1 for z in zangs):
        return CONSTITUTIONS[0]

    best = None
    best_score = 0
    for c in CONSTITUTIONS[1:]:
        score = 0
        if c['name'] == '气虚质' and (energy['脾'] <= -2 or energy['肺'] <= -2):
            score = 80
        if c['name'] == '阳虚质' and energy['肾'] <= -2 and energy['心'] <= 0:
            score = 75
        if c['name'] == '阴虚质' and energy['肾'] <= -2 and energy['心'] >= 1:
            score = 80
        if c['name'] == '痰湿质' and energy['脾'] <= -1 and energy['肺'] <= -1:
            score = 70
        if c['name'] == '湿热质' and energy['脾'] >= 1 and energy['肝'] >= 1:
            score = 65
        if c['name'] == '血瘀质' and (energy['心'] <= -1 or energy['肝'] >= 1):
            score = 60
        if c['name'] == '气郁质' and (energy['肝'] <= -1 or energy['肝'] >= 2):
            score = 75
        if c['name'] == '特禀质' and (energy['肺'] <= -2 or energy['肾'] <= -2):
            score = 70
        if score > best_score:
            best_score = score
            best = c

    return best or CONSTITUTIONS[0]


# ========== 便捷函数 ==========

def quick_calc(birth_year, birth_province='北京市', current_province='北京市',
               occupation=None, gender='male', current_age=30):
    """快速计算（只填必填项）"""
    input_data = {
        'birth_year': birth_year,
        'birth_province': birth_province,
        'current_province': current_province,
        'occupation': occupation,
        'gender': gender,
        'current_age': current_age
    }
    result = calc_zang_energy(input_data)
    constitution = judge_constitution(result['energy'])
    return {
        'energy': result['energy'],
        'congenital': result['congenital'],
        'constitution': constitution,
        'ganzhi': result['ganzhi'],
        'zhongyun': result['zhongyun'],
        'sitian': result['sitian']
    }
