from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import uvicorn

# 导入你已有模块
from hybrid_retriever import HybridRetriever
from get_unit_information import get_unit_info_by_uid
from llm_sql_generator import build_prompt  # 你提供的 prompt 构建函数

app = FastAPI(title="Prompt API for SQL Generator", description="输入自然语言问题，自动生成 Prompt")

retriever = HybridRetriever()  # 初始化混合检索器


# 请求体格式
class PromptRequest(BaseModel):
    question: str


# 响应接口
@app.post("/generate_prompt")
def generate_prompt(payload: PromptRequest):
    # 步骤 1：调用混合检索器获取相关 unit uid（含联想）
    unit_uids = retriever.find_units(payload.question)

    # 步骤 2：构建 prompt
    prompt = build_prompt(payload.question, unit_uids)

    return {"prompt": prompt, "matched_units": unit_uids}


# 可选本地运行
if __name__ == "__main__":
    uvicorn.run("prompt_api:app", host="0.0.0.0", port=8083, reload=True)
