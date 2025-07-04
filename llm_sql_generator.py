# coding=utf8

import requests
from vector_match import find_similar_units
from models import Unit
import re
from unit_association_trigger import expand_units_by_weight
from update_weight import update_association_weights
from get_unit_information import get_unit_info_by_uid
from hybrid_retriever import HybridRetriever


def build_prompt(question: str, related_units: list) -> str:
    parts = [
        "你是一个SQL助手，请根据用户的问题生成SQL查询语句。",
        f"用户问题：{question}",
        "相关信息：",
        "请注意：使用的SQL数据库是SQL Server，所有表都在 [LLM_test].[dbo] 路径下。请对表名或字段名加上中括号 []。",
        "数据库中时间字段类型均为 varchar，格式如 YYYY-MM，例如 2024-11，若需要筛选年份，请操作月份字段。",
        "请避免臆造字段，若字段不在下方信息中，请不要使用。",
        "提供给你的所有Field中都额外添加了一个表名，用来区分"
        "以下是与问题相关的字段、解释与所属表结构："
    ]

    seen_tables = set()

    for uid in related_units:
        info = get_unit_info_by_uid(uid)
        if not info:
            continue

        for record in info:
            try:
                nlp = record.get("nlp") or "（无关键词）"
                exp = record.get("explanation") or "（无解释）"
                field = record.get("field_name").split(".")[1] or "未知字段"
                table = record.get("table_name") or "未知表"

                parts.append(f"- 关键词：{nlp}\n  解释：{exp}\n  字段：[{table}].[{field}]")

                # 附加该字段所在表的全部字段结构（只展示一次）
                if table not in seen_tables:
                    seen_tables.add(table)
                    from models import Table
                    table_node = Table.nodes.get(name=table)
                    table_fields = table_node.fields if hasattr(table_node, 'fields') else []
                    if table_fields:
                        parts.append(f"  [{table}] 表包含字段：")
                        for f in table_fields:
                            parts.append(f"    - {f.name} ({f.type}, 可空: {f.nullable})")
            except Exception as e:
                print(f"[跳过错误记录] {e}")
                continue

    parts.append("请只返回SQL代码，不要做任何解释，也不要输出其他额外信息。")
    return "\n".join(parts)



def call_ollama_llm(prompt: str) -> str:
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "deepseek-r1:8b",
        "prompt": prompt,
        "stream": False
    })
    response.raise_for_status()
    return response.json()["response"].strip()


def generate_sql_from_question(question: str) -> str:
    retriever = HybridRetriever()
    matched_units = retriever.find_units(question)
    if not matched_units:
        return "-- 无匹配单元，无法生成SQL"

    expanded_units = expand_units_by_weight(matched_units, threshold=5)
    prompt = build_prompt(question, expanded_units)
    print(prompt)
    sql = call_ollama_llm(prompt)
    update_association_weights(expanded_units)
    return sql


if __name__ == '__main__':
    q = input("请输入问题：\n> ")
    print("\n生成的SQL：\n")
    print(generate_sql_from_question(q))
