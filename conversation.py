from langchain_core.messages import HumanMessage, AIMessage
import time


# Store conversations for each session
conversation_store = {}



# --------------------------Get conversation history----------------------


def get_history(session_id):

    if session_id not in conversation_store:

        conversation_store[session_id] = []

    return conversation_store[session_id]



# -------------------Convert messages into text-------------


def format_history(messages):

    history = []

    for message in messages:

        if isinstance(message, HumanMessage):

            history.append(
                f"User: {message.content}"
            )

        elif isinstance(message, AIMessage):

            if message.content:

                history.append(
                    f"Assistant: {message.content}"
                )

    return "\n".join(history)



# -----------------Clean rewritten question-------------


def clean_rewritten_question(text):

    text = text.strip()


    # Remove reasoning if model returns it
    if "What would be a good standalone question?" in text:

        text = text.split(
            "What would be a good standalone question?"
        )[-1].strip()


    # Remove common labels
    prefixes = [
        "Rewritten question:",
        "Standalone question:",
        "Final question:"
    ]

    for prefix in prefixes:

        if text.startswith(prefix):

            text = text[len(prefix):].strip()


    return text


#------------------------ Run one complete chat interaction------------------


def run_chat(
    query,
    session_id,
    agent,
    rewrite_chain
):

    


    
    #------------------------- Get conversation history-----------------------
    

    messages = get_history(session_id)

    history = format_history(messages)


    
    # --------------------Rewrite follow-up questions------------------
    

    if history:

       


        rewritten = rewrite_chain.invoke({

            "history": history,

            "question": query

        })


        standalone_query = clean_rewritten_question(
            rewritten
        )


        
    else:

        standalone_query = query


        print(
            "\nRewrite skipped (first question)"
        )



    #---------------- Run controlled agent------------------
    

     answer = agent(
        standalone_query
    )



    
    # ------------------Save original conversation-----------------

    messages.append(
        HumanMessage(
            content=query
        )
    )

    messages.append(
        AIMessage(
            content=answer
        )
    )




    return answer
