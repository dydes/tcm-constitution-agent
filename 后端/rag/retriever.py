# -*- coding: utf-8 -*-
"""
知识库检索模块
功能：从向量库中检索与问题相关的知识片段
"""

import os
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


# 全局变量，懒加载向量库
_vectorstore = None


def get_vectorstore(persist_directory: str = "./chroma_db"):
    """
    获取向量库实例（懒加载，只初始化一次）
    """
    global _vectorstore
    if _vectorstore is None:
        if not os.path.exists(persist_directory):
            raise FileNotFoundError(
                f"向量库不存在：{persist_directory}。请先运行 build_knowledge_base.py 构建知识库。"
            )

        embeddings = HuggingFaceEmbeddings(
            model_name="shibing624/text2vec-base-chinese",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        _vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings
        )
    return _vectorstore


def retrieve(query: str, k: int = 3) -> list:
    """
    检索与问题相关的知识片段

    Args:
        query: 用户的问题
        k: 返回最相关的k条结果

    Returns:
        文档片段列表，每个元素包含 page_content 和 metadata
    """
    vectorstore = get_vectorstore()
    results = vectorstore.similarity_search(query, k=k)
    return results


def format_docs(docs: list) -> str:
    """
    把检索到的文档片段格式化成文本，用于拼接到提示词中
    """
    formatted = []
    for i, doc in enumerate(docs):
        source = doc.metadata.get("一级标题", "") + " " + doc.metadata.get("二级标题", "")
        formatted.append(f"【参考{i+1}】来源：{source}\n{doc.page_content}")
    return "\n\n".join(formatted)
