# -*- coding: utf-8 -*-
"""测试RAG问答接口"""
import requests
import json

url = 'http://localhost:8001/api/chat'
headers = {'Content-Type': 'application/json'}
data = {'question': '五运六气是什么？', 'context': None}

try:
    print("正在调用API接口...")
    response = requests.post(url, headers=headers, json=data, timeout=120)
    print(f"状态码: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print(f"use_rag: {result.get('use_rag')}")
        print(f"参考资料数: {len(result.get('sources', []))}")
        print(f"回答前300字: {result.get('answer', '')[:300]}")

        if result.get('sources'):
            print("\n参考资料:")
            for s in result['sources']:
                print(f"  - {s['source']}: {s['content'][:80]}")
    else:
        print(f"错误响应: {response.text}")

except Exception as e:
    print(f"错误: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
