# -*- coding: utf-8 -*-
"""
知识库向量化脚本
功能：把中医养生知识库markdown文件切分、向量化，存入Chroma向量库

使用方法：
    cd 后端
    python -m rag.build_knowledge_base
"""

import os
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


def build_knowledge_base(
    markdown_path: str = "../01_知识库/中医养生知识库_完整版.md",
    persist_directory: str = "./chroma_db"
):
    """
    构建知识库向量库

    Args:
        markdown_path: 知识库markdown文件路径
        persist_directory: 向量库保存路径
    """
    print("=" * 50)
    print("开始构建知识库向量库...")
    print("=" * 50)

    # 1. 读取知识库文件
    print(f"\n[1/4] 读取知识库文件：{markdown_path}")
    with open(markdown_path, "r", encoding="utf-8") as f:
        markdown_text = f.read()
    print(f"  文件大小：{len(markdown_text)} 字符")

    # 2. 按标题切分文档
    print("\n[2/4] 按标题切分文档...")
    headers_to_split_on = [
        ("#", "一级标题"),
        ("##", "二级标题"),
        ("###", "三级标题"),
    ]
    splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    docs = splitter.split_text(markdown_text)
    print(f"  切分成 {len(docs)} 个文档片段")

    # 3. 初始化嵌入模型
    print("\n[3/4] 初始化嵌入模型（第一次运行会自动下载模型，约400MB）...")
    embeddings = HuggingFaceEmbeddings(
        model_name="shibing624/text2vec-base-chinese",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    print("  嵌入模型加载完成")

    # 4. 存入向量数据库
    print(f"\n[4/4] 存入向量数据库：{persist_directory}")
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    print("  向量库构建完成！")

    # 测试检索
    print("\n" + "=" * 50)
    print("测试检索：查询'肝火旺的症状'")
    print("=" * 50)
    results = vectorstore.similarity_search("肝火旺的症状", k=2)
    for i, doc in enumerate(results):
        print(f"\n--- 结果 {i+1} ---")
        print(f"来源：{doc.metadata}")
        print(f"内容：{doc.page_content[:100]}...")

    return vectorstore


if __name__ == "__main__":
    build_knowledge_base()
