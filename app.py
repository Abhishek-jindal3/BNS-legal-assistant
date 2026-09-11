
import streamlit as st

from vector_store import (
    get_retriever,
    format_docs
)

from agent import create_bns_agent

from conversation import run_chat


# -----------------Page configuration-----------------

st.set_page_config(
    page_title="BNS Legal Assistant",
    page_icon="⚖️",
    layout="centered"
)



# -----------------Load AI resources----------------


@st.cache_resource
def load_resources():

    # Load existing Chroma database
    retriever = get_retriever()


    # Create agent and rewrite chain
    agent, rewrite_chain = create_bns_agent(
        retriever,
        format_docs
    )


    return retriever, agent, rewrite_chain






# -------------------Page title---------------

st.title("⚖️ BNS Legal Assistant")

st.caption(
    "Ask questions about the Bharatiya Nyaya Sanhita, 2023."
)



# --------------------Initialize Streamlit chat history-----------------------

if "messages" not in st.session_state:

    st.session_state.messages = []


# ---------------------Display previous messages-------------------


for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )



# -------------------User input-----------------


query = st.chat_input(
    "Ask a question about the BNS..."
)



# --------------------------Process user question------------

if query:

    # Load BNS resources only when the user asks a question
    retriever, agent, rewrite_chain = load_resources()


    # Display user message
    with st.chat_message("user"):

        st.markdown(query)


    # Save user message
    st.session_state.messages.append({

        "role": "user",

        "content": query

    })


    # Generate answer
    with st.chat_message("assistant"):

        answer = run_chat(

            query=query,

            session_id="default",

            agent=agent,

            rewrite_chain=rewrite_chain

        )


        st.markdown(answer)


    # Save assistant message
    st.session_state.messages.append({

        "role": "assistant",

        "content": answer

    })
