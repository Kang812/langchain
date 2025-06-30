from fastapi import FastAPI
from langserve import add_routes
#from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
# LangSmith API Key 설정
os.environ["LANGSMITH_TRACING"] = os.getenv("LANGSMITH_TRACING")  # LangSmith 활성화
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")  # API Key 불러오기
os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT")   # 프로젝트 이름 설정
os.environ["LANGSMITH_ENDPOINT"] = os.getenv("LANGSMITH_ENDPOINT")   # EndPoint 설정

# .env 파일 로드
load_dotenv(".env")

# 환경 변수에서 API 키 가져오기
#api_key = os.getenv("OPENAI_API_KEY")

# FastAPI 애플리케이션 생성
app = FastAPI(title="LangServe API with .env")

# LLM 모델 생성 (API 키 적용)
#llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=api_key)
llm = llm = ChatOpenAI(
    base_url="https://api.groq.com/openai/v1",  # Groq API 엔드포인트
    model="meta-llama/llama-4-scout-17b-16e-instruct",  # Spring AI와 동일한 모델
    temperature=0.7
)

# LangChain 프롬프트 설정
prompt = PromptTemplate.from_template("질문: {question}\n답변:")
#chain = LLMChain(llm=llm, prompt=prompt)
chain = prompt | llm

# LangServe를 이용해 API 엔드포인트 추가
add_routes(app, chain, path="/chat")

# FastAPI 서버 실행 (uvicorn 사용)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)