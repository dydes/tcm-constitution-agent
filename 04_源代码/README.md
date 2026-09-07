# 源代码说明

## 技术栈

- **框架**: React 19 + TypeScript
- **构建工具**: Vite 8
- **样式**: TailwindCSS 4 + shadcn/ui (new-york 风格)
- **图表**: ECharts 5.6 (雷达图、柱状图)
- **路由**: React Router 7
- **动画**: Framer Motion + GSAP
- **图标**: Lucide React
- **平台**: 飞书妙搭 (Lark APaaS)

## 项目目录结构

```
tcm-constitution-app/
├── index.html                          # 入口HTML
├── package.json                        # 依赖配置
├── vite.config.ts                      # Vite配置
├── tsconfig.json                       # TypeScript配置
├── components.json                     # shadcn配置
└── src/
    ├── index.tsx                       # 应用入口
    ├── app.tsx                         # 路由配置
    ├── index.css                       # 全局样式
    ├── tailwind-theme.css              # Tailwind主题（宣纸底+朱砂红+墨色）
    ├── typography.css                  # 字体配置（Noto Serif SC / Noto Sans SC）
    ├── lib/
    │   ├── utils.ts                    # 工具函数（cn类名合并）
    │   └── tcm-calculator.ts           # ★ 核心推演逻辑（约2000+行）
    ├── data/
    │   ├── tcmclassics.ts              # 经典原文知识库（《素问》《灵枢》片段）
    │   ├── food-images.ts              # 食物图片数据（每脏5种，含症状标签）
    │   ├── acupoint-images.ts          # 穴位图片数据（原穴+背俞穴）
    │   ├── exercises.ts                # 运动调理库（12种运动+智能推荐算法）
    │   ├── occupations.ts              # 职业类型定义及对五脏的损益值
    │   └── regions.ts                  # 五方地域与五行五脏对应
    ├── hooks/
    │   └── use-mobile.ts               # 移动端检测Hook
    ├── components/
    │   ├── Layout.tsx                  # 布局组件
    │   ├── InputForm.tsx               # 输入表单组件
    │   ├── ModuleSection.tsx           # 可折叠模块区块容器
    │   ├── SideNav.tsx                 # 右侧锚点导航
    │   ├── PersonAvatar.tsx            # 人物图标剪影（性别+年龄段）
    │   ├── DietBodyDiagram.tsx         # 饮食调理食物展示
    │   ├── ExerciseTreatment.tsx       # 运动调理组件（3张运动卡片）
    │   ├── ui/                         # shadcn UI组件库（57个组件）
    │   └── sections/                   # 各结果区块组件
    │       ├── SummarySection.tsx              # 区块1：结论概览
    │       ├── StepsSection.tsx                # 区块2：先天禀赋推演步骤
    │       ├── ConstitutionDiseaseSection.tsx  # 区块3：体质与健康风险
    │       ├── EnvironmentLifestyleSection.tsx # 区块4：环境与生活方式
    │       ├── LoadMatrixSection.tsx           # 综合负荷矩阵
    │       ├── SymptomsSection.tsx             # 表象清单
    │       ├── TreatmentSection.tsx            # 调理方案（饮食/运动/穴位/起居/情志）
    │       ├── EnergyCompareSection.tsx        # 能量对比图
    │       └── ReferenceSection.tsx            # 参考依据
    └── pages/
        └── TcmConstitutionPage/
            └── TcmConstitutionPage.tsx  # ★ 主页面
```

## 核心推演逻辑（tcm-calculator.ts）

### 核心函数

| 函数 | 功能 |
|---|---|
| `calcGanZhi(year)` | 天干地支推算 |
| `calcZhongYun(tianGan)` | 中运太过/不及判定 |
| `calcSiTianZaiQuan(diZhi)` | 司天在泉推算 |
| `calcZangEnergy(...)` | 五脏能量叠加计算（中运+司天+在泉+生克+地域） |
| `calcShengKeAnalysis(zangEnergy)` | 生克传变分析 |
| `calcConstitutionType(zangEnergy)` | 体质类型判定（九种体质） |
| `calcAgeStage(gender, currentAge)` | 年龄阶段与衰脏判定 |
| `calcRegionEffect(birthRegion, currentRegion)` | 地域影响计算 |
| `calcOccupationEffect(occupationType)` | 职业影响计算 |
| `calcDiseaseRisks(...)` | 高风险疾病列表生成 |
| `calcSymptoms(zangEnergy, loadMatrix)` | 表象清单生成（权重打分） |
| `calcTreatmentPlan(...)` | 调理方案生成 |

### 能量等级制（7级）

| 等级 | 数值 | 标签 |
|---|---|---|
| 过强 | +3 | 🔴 过强 |
| 强 | +2 | 🟠 强 |
| 偏强 | +1 | 🟡 偏强 |
| 平和 | 0 | 🟢 平和 |
| 偏弱 | -1 | 🔵 偏弱 |
| 弱 | -2 | 🟣 弱 |
| 过弱 | -3 | ⚫ 过弱 |

### 组合病机引擎（12种）

1. 风火相煽（肝强+心强）
2. 肺胃热盛（肺强+脾/胃强）
3. 心肾不交（心强+肾弱）
4. 木火刑金（肝强+肺弱）
5. 土虚木乘（脾弱+肝强）
6. 水不涵木（肾弱+肝强/弱）
7. 金水相生不足（肺弱+肾弱）
8. 气血两虚（心弱+脾弱）
9. 痰湿内蕴（脾弱+肺弱）
10. 阴虚火旺（肾弱+心强）
11. 肝郁脾虚（肝强+脾弱）
12. 脾肾阳虚（脾弱+肾弱）

## 本地运行方法

### 前置条件
- Node.js 18+
- npm 或 pnpm

### 运行步骤

```bash
# 1. 安装依赖
npm install

# 2. 开发模式（热更新）
npm run dev

# 3. 构建生产版本
npm run build

# 4. 预览生产构建
npm run preview
```

### 注意事项

本项目原部署于飞书妙搭平台，依赖 `@lark-apaas/client-toolkit-lite` SDK（含 `AppContainer` 组件、沙箱环境等）。在本地独立运行时，需要：

1. **移除飞书SDK依赖**：将 `src/index.tsx` 中的 `AppContainer` 包裹移除，改为普通 React 入口
2. **移除 scopedStorage**：如果代码中使用了飞书沙箱的 `scopedStorage`，替换为普通 `localStorage`
3. **图片资源**：食物、穴位、运动、脏器图片均使用远程 CDN URL（aka.doubaocdn.com），无需本地配置
4. **shadcn组件**：57个UI组件可通过 `npx shadcn@latest add` 一键重装

### 核心文件纯前端化

核心推演逻辑 `tcm-calculator.ts` 和所有数据文件（`data/` 目录）均为纯 TypeScript 实现，不依赖任何平台SDK，可直接在任何 React 项目中使用。

---

*更新日期：2026-09-01*
