# -*- coding: utf-8 -*-
"""
中医先天禀赋推演系统 - 后端入口
功能：FastAPI服务 + API Key管理 + 大模型调用
"""

import os
import sys
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

# 确保当前目录在Python路径中，能正确导入rag和agent模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 加载环境变量（开发时从 .env 读取你的 DeepSeek Key）
load_dotenv()

# 预导入RAG模块（如果导入失败，启动时就会报错，方便排查）
try:
    from rag import retriever as rag_retriever
    print("[启动] RAG模块导入成功")
except Exception as e:
    print(f"[启动] RAG模块导入失败（不影响基础对话功能）：{e}")
    rag_retriever = None

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
    sources: list  # RAG检索到的参考资料列表
    use_rag: bool  # 是否使用了RAG检索


class HealthResponse(BaseModel):
    """健康检查响应"""
    status: str
    has_env_key: bool  # 环境变量里是否配置了key


# ========== 工具函数 ==========

def get_llm(api_key: str = None):
    """
    获取大模型配置
    优先级：传入的key > 环境变量里的key
    返回：(api_key, base_url, model, key_source)
    """
    # 确定用哪个key
    final_key = api_key or os.getenv("DEEPSEEK_API_KEY")
    base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

    if not final_key:
        return None, None, None, "missing"

    # 判断key来源
    key_source = "user" if api_key else "env"

    return final_key, base_url, model, key_source


def call_deepseek(api_key: str, base_url: str, model: str, prompt: str) -> str:
    """
    直接调用DeepSeek API（不经过langchain封装，更稳定）
    """
    from openai import OpenAI

    # 创建客户端（DeepSeek兼容OpenAI接口格式）
    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
    )

    # 调用对话接口
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "你是一位资深中医专家，擅长用通俗的语言解释中医理论和养生建议。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=2000,
    )

    # 返回回答内容
    return response.choices[0].message.content


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
    对话接口（支持RAG知识库检索增强）
    - x_api_key：用户在请求头里传入自己的DeepSeek Key（可选）
    - 如果没传，就用环境变量里的key（开发模式）
    - 自动检索中医知识库，大模型基于知识库内容回答
    """
    import traceback

    # 获取大模型配置
    api_key, base_url, model, key_source = get_llm(x_api_key)

    if api_key is None:
        raise HTTPException(
            status_code=400,
            detail="未找到API Key。请在前端设置中填写您的DeepSeek API Key，或在后端 .env 文件中配置。"
        )

    # 初始化变量
    retrieved_docs = []
    sources = []
    use_rag = False
    knowledge_text = ""

    try:
        # ===== 第一步：RAG知识库检索 =====
        print(f"\n{'='*50}")
        print(f"收到请求，key来源：{key_source}")
        print(f"问题：{request.question}")

        try:
            if rag_retriever is not None:
                print(f"正在检索知识库...")
                retrieved_docs = rag_retriever.retrieve(request.question, k=3)
                if retrieved_docs:
                    use_rag = True
                    knowledge_text = rag_retriever.format_docs(retrieved_docs)
                    # 整理参考资料列表
                    for i, doc in enumerate(retrieved_docs):
                        source_info = doc.metadata.get("一级标题", "") + " " + doc.metadata.get("二级标题", "")
                        sources.append({
                            "index": i + 1,
                            "source": source_info,
                            "content": doc.page_content[:150] + "..."  # 只显示前150字
                        })
                    print(f"检索到 {len(retrieved_docs)} 条相关知识")
                else:
                    print(f"知识库中未找到相关内容")
            else:
                print(f"RAG模块未加载，跳过知识库检索")
        except Exception as e:
            import traceback
            print(f"知识库检索失败（不影响大模型回答）：{type(e).__name__}: {e}")
            print(f"错误详情：")
            traceback.print_exc()
            use_rag = False

        # ===== 第二步：构造提示词 =====
        if use_rag:
            # 有知识库参考：要求大模型基于知识库回答
            prompt = f"""你是一位资深中医专家。请参考以下知识库内容，用通俗的中文回答用户的问题。

【知识库参考内容】
{knowledge_text}

【用户问题】
{request.question}

【回答要求】
1. 优先参考知识库内容回答
2. 如果知识库内容不够，可以补充你的专业知识
3. 回答要通俗易懂，结构清晰
4. 重要结论可以标注参考来源（如"根据知识库第二部分..."）
"""
        elif request.context:
            # 有上下文但没有知识库
            prompt = f"参考信息：\n{request.context}\n\n用户问题：{request.question}\n\n请用通俗的中文回答："
        else:
            # 没有知识库也没有上下文
            prompt = f"你是一位资深中医专家，请用通俗的中文回答用户的问题。\n\n用户问题：{request.question}"

        # ===== 第三步：调用大模型 =====
        print(f"正在调用大模型...")
        answer = call_deepseek(api_key, base_url, model, prompt)

        print(f"大模型返回成功，回答长度：{len(answer)} 字")
        print(f"{'='*50}\n")

        return ChatResponse(
            answer=answer,
            model=model,
            key_source=key_source,
            sources=sources,
            use_rag=use_rag
        )

    except Exception as e:
        # 打印详细错误信息到控制台
        print(f"\n{'='*50}")
        print(f"大模型调用失败！")
        print(f"错误类型：{type(e).__name__}")
        print(f"错误信息：{str(e)}")
        print(f"错误堆栈：")
        traceback.print_exc()
        print(f"{'='*50}\n")

        # 返回友好的错误提示
        raise HTTPException(
            status_code=500,
            detail=f"大模型调用失败：{type(e).__name__}: {str(e)}。请检查您的API Key是否正确，或是否有足够的额度。"
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
