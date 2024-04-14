import os
from typing import List, Union

from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langserve import add_routes
from openai import BaseModel
from pydantic import Field

_ = load_dotenv(find_dotenv())

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple api server using Langchain's Runnable interfaces",
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

add_routes(
    app,
    ChatOpenAI(model_name="gpt-4", base_url=os.environ['OPENAI_BASE_URL']),
    path="/openai",
)

add_routes(
    app,
    ChatAnthropic(model_name="claude-3-opus-20240229"),
    path="/anthropic",
)

model = ChatAnthropic(model_name="claude-3-sonnet-20240229")
prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")
add_routes(
    app,
    prompt | model,
    path="/joke",
)

# # Declare a chain
# prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", "You are a helpful, professional assistant named Cob."),
#         MessagesPlaceholder(variable_name="messages"),
#     ]
# )
#
# chain = prompt | ChatAnthropic(model="claude-2")
#
#
# class InputChat(BaseModel):
#     """Input for the chat endpoint."""
#
#     messages: List[Union[HumanMessage, AIMessage, SystemMessage]] = Field(
#         ...,
#         description="The chat messages representing the current conversation.",
#     )
#
#
# add_routes(
#     app,
#     chain.with_types(input_type=InputChat),
#     enable_feedback_endpoint=True,
#     enable_public_trace_link_endpoint=True,
#     playground_type="chat",
# )

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
