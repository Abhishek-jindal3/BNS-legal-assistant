

from vector_store import get_retriever, format_docs
from agent import create_bns_agent
from conversation import run_chat


# Load the retriever
retriever = get_retriever()


# Create the agent and rewrite chain
agent, rewrite_chain = create_bns_agent(
    retriever,
    format_docs
)


# Keep asking questions
while True:

    query = input("\nAsk a BNS question (type 'exit' to quit): ")

    if query.lower() == "exit":
        break

    answer = run_chat(
        query=query,
        session_id="test",
        agent=agent,
        rewrite_chain=rewrite_chain
    )

    print("\nAnswer:")
    print(answer)