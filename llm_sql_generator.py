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
        "相关信息："
        "请注意，使用的sql数据库基于sQL Server，所有的表都在[LLM_test].[dbo]路径下，对于每个表名或者键名，请在外面加上[]。"
        "此外，整个数据库中所有的时间日期类数据都使用varchar类型，数据库中没有年份相关的列，月份的格式为YYYY-MM（如2024-11），如果需要检索年份，请对月份使用检索。"
        "下面是一个例子： SELECT [月份],[单据类型],[采购总金额] FROM [LLM_test].[dbo].[各单据类型每月采购总额]"
    ]

    for uid in related_units:
        info = get_unit_info_by_uid(uid)
        if not info:
            continue

        # 支持一个unit关联多个field（不常见，但结构允许）
        for record in info:
            try:
                nlp = record.get("nlp") or "（无关键词）"
                exp = record.get("explanation") or "（无解释）"
                field = record.get("field_name") or "未知字段"
                table = record.get("table_name") or "未知表"
                parts.append(f"- 关键词：{nlp}\n  解释：{exp}\n  字段：{table}.{field}")
            except:
                continue

    parts.append("请只返回SQL代码，不要做任何解释，不要换行，也不要输出额外文本。")
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
