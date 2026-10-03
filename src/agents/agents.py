import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser,JsonOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from src.tools.tools import web_search,scrape_url
from langchain.agents import create_agent
from pydantic import BaseModel,Field

load_dotenv()
llm=ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite-preview",temperature=0.5,google_api_key=os.getenv("GEMINI_API_KEY"))
# llm=ChatGroq(model="openai/gpt-oss-20b",temperature=0.5,groq_api_key=os.getenv("GROQ_API_KEY"))

# 1.search agent
def search_agent():
    return create_agent(model=llm,tools=[web_search])

# 2.reader agent
class ReaderOutput(BaseModel):
    picked_urls: list[str] = Field(description="The URLs selected by the reader")
    scraped_content: str = Field(description="The content scraped from the selected URL")

def reader_agent():
    return create_agent(model=llm,tools=[scrape_url],response_format=ReaderOutput)

#writer chain 
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()

#critic_chain 

class Critique(BaseModel):
    score: int = Field(description="Score the report from 0 to 10.")
    strengths: str = Field(description="Strengths of the report.")
    areas_to_improve: str = Field(description="Specific improvements needed in the report.")
    verdict: str = Field(description="One-line overall verdict.")
    needs_new_source: bool = Field(
        description="""
        Set True ONLY if the current source itself must be replaced because
        it is clearly irrelevant, unreliable, unverifiable, or fundamentally
        insufficient to answer the topic.

        Do NOT set True merely because the report needs more detail, examples,
        better structure, a stronger conclusion, or other writing improvements.
        """)
    source_credibility_concern: bool = Field(
        description="""
        Set True ONLY when there is a clear credibility or reliability concern
        with the source, such as an unverifiable, misleading, unauthorized,
        or clearly unreliable source.
        """)

JSONparser=JsonOutputParser(pydantic_object=Critique)

critic_prompt = ChatPromptTemplate.from_messages([
     ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}
Return a JSON Object in this exact format:
{format}
"""),
]).partial(format=JSONparser.get_format_instructions())

critic_chain = critic_prompt | llm | JsonOutputParser(pydantic_object=Critique)
