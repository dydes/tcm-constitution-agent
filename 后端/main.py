# -*- coding: utf-8 -*-
"""
中医先天禀赋推演系统 - 后端入口
功能：FastAPI服务 + API Key管理 + 大模型调用
"""

import os
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

# 加载环境变量（开发时从 .env 读取你的 DeepSeek Key）
load_dotenv()

# 创建FastAPI应用
app = FastAPI(
    title="中医先天禀赋推演系统 API",
    description="基于五运六气和大模型的中医体质推演后端服务",
    version="0.1.0"
)

# 允许跨域（前端HTML和后端端口不同，需要跨域）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发时允许所有来源，生产环境可以限制为具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========== 数据模型 ==========

class ChatRequest(BaseModel):
    """对话请求的数据结构"""
    question: str  # 用户的问题
    context: Optional[str] = None  # 可选的上下文信息（如用户的推演结果）


class ChatResponse(BaseModel):
    """对话响应的数据结构"""
    answer: str  # 大模型的回答
    model: str  # 使用的模型
    key_source: str  # key来源：user（用户输入）或 env（环境变量）


class HealthResponse(BaseModel):
    """健康检查响应"""
    status: str
    has_env_key: bool  # 环境变量里是否配置了key


# ========== 工具函数 ==========

def get_llm(api_key: str = None):
    """
    获取大模型实例
    优先级：传入的key > 环境变量里的key
    """
    from langchain_openai import ChatOpenAI

    # 确定用哪个key
    final_key = api_key or os.getenv("DEEPSEEK_API_KEY")
    base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

    if not final_key:
        return None, None, "missing"

    # 动态创建大模型实例（因为每个用户的key可能不同）
    llm = ChatOpenAI(
        model=model,
        api_key=final_key,
        base_url=base_url,
        temperature=0.3,  # 温度低一点，回答更稳定
    )

    # 判断key来源
    key_source = "user" if api_key else "env"

    return llm, model, key_source


# ========== API接口 ==========

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """健康检查接口，测试服务是否正常运行"""
    has_env_key = bool(os.getenv("DEEPSEEK_API_KEY"))
    return HealthResponse(
        status="ok",
        has_env_key=has_env_key
    )


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, x_api_key: str = Header(None)):
    """
    对话接口
    - x_api_key：用户在请求头里传入自己的DeepSeek Key（可选）
    - 如果没传，就用环境变量里的key（开发模式）
    """
    # 获取大模型实例
    llm, model, key_source = get_llm(x_api_key)

    if llm is None:
        raise HTTPException(
            status_code=400,
            detail="未找到API Key。请在前端设置中填写您的DeepSeek API Key，或在后端 .env 文件中配置。"
        )

    try:
        # 构造提示词
        if request.context:
            prompt = f"参考信息：\n{request.context}\n\n用户问题：{request.question}\n\n请用通俗的中文回答："
        else:
            prompt = f"你是一位资深中医专家，请用通俗的中文回答用户的问题。\n\n用户问题：{request.question}"

        # 调用大模型
        response = llm.invoke(prompt)

        return ChatResponse(
            answer=response.content,
            model=model,
            key_source=key_source
        )

    except Exception as e:
        # 大模型调用失败（可能是key无效、额度不足、网络问题等）
        raise HTTPException(
            status_code=500,
            detail=f"大模型调用失败：{str(e)}。请检查您的API Key是否正确，或是否有足够的额度。"
        )


@app.get("/")
async def root():
    """根路径，返回API说明"""
    return {
        "name": "中医先天禀赋推演系统 API",
        "version": "0.1.0",
        "endpoints": {
            "GET /api/health": "健康检查",
            "POST /api/chat": "对话接口（需要在请求头 X-API-Key 中传入DeepSeek Key）"
        },
        "docs": "/docs"
    }


# ========== 启动方式 ==========
# 命令行运行：
# cd 后端
# uvicorn main:app --reload --port 8000
#
# 然后浏览器打开 http://localhost:8000/docs 查看API文档
