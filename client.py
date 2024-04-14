import asyncio

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableMap
from langserve import RemoteRunnable

openai = RemoteRunnable("http://localhost:8000/openai/")
anthropic = RemoteRunnable("http://localhost:8000/anthropic/")
joke_chain = RemoteRunnable("http://localhost:8000/joke/")


# Method-1
joke_response = joke_chain.invoke({"topic": "parrots"})
print(f"{joke_response.content=}")


# or async
# Method-2
# async def joke_chain_async():
#     try:
#         response = await joke_chain.ainvoke({"topic": "parrots"})
#         print(response.content, end="", flush=True)
#     finally:
#         # 在 finally 块中确保无论如何都尝试关闭连接
#         await joke_chain.async_client.aclose()
#
#
# if __name__ == "__main__":
#     asyncio.run(joke_chain_async())

# Method-3
# prompt = [
#     SystemMessage(content='Act like either a cat or a parrot.'),
#     HumanMessage(content='Hello!')
# ]


# Supports astream
# async def astream_anthropic():
#     async for msg in anthropic.astream(prompt):
#         print(msg.content, end="", flush=True)
#
# if __name__ == "__main__":
#     asyncio.run(astream_anthropic())


# Method-4
prompt = ChatPromptTemplate.from_messages(
    [("system", "Tell me a long story about {topic}")]
)

# Can define custom chains
chain = prompt | RunnableMap({
    "openai": openai,
    # "anthropic": anthropic,
})

# chain.batch([{"topic": "parrots"}, {"topic": "cats"}])

for response in chain.batch([{"topic": "parrots"}, {"topic": "cats"}]):
    if "openai" in response:
        print(response["openai"].content, end="", flush=True)
    if "anthropic" in response:
        print(response, end="", flush=True)
#
# if __name__ == "__main__":
#     asyncio.run(main())
#     asyncio.run(main())
