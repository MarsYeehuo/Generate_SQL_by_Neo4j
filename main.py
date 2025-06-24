# coding=utf8

from add_unit import create_new_unit
from embed import update_all_nlp_embeddings
from clear_links import clear_associations
from llm_sql_generator import generate_sql_from_question
from hybrid_retriever import HybridRetriever
import re

def main():
    print("KG SQL Agent 已启动（help 查看指令）")
    retriever = HybridRetriever()

    while True:
        cmd = input("指令 > ").strip().lower()

        if cmd in ('exit', 'quit'):
            print("已退出系统。")
            break

        elif cmd == 'help':
            print("""
可用指令：
  ask     - 输入自然语言问题，唤起相关单元（不生成SQL）
  sql     - 输入自然语言问题，直接生成SQL（并联想、更新权重）
  create  - 添加新知识单元（自然语言 + 解释 + 表字段）
  embed   - 初始化或刷新 NLP 节点向量表示
  reset   - 清空所有 Unit 单元之间的联想边
  help    - 查看帮助信息
  exit    - 退出系统
            """)

        elif cmd == 'ask':
            q = input("请输入问题：\n> ")
            units = retriever.find_units(q)
            print("唤起单元：", units)

        elif cmd == 'sql':
            q = input("请输入问题：\n> ")
            sql = generate_sql_from_question(q)
            cleaned = re.sub(r"<think>.*?</think>", "", sql, flags=re.DOTALL)
            print("\n 生成的SQL语句：\n" + cleaned)

        elif cmd == 'create':
            create_new_unit()

        elif cmd == 'embed':
            update_all_nlp_embeddings()
            print("NLP 向量已更新")

        elif cmd == 'reset':
            clear_associations()

        else:
            print("未知指令，输入 help 查看所有选项。")

if __name__ == '__main__':
    main()
