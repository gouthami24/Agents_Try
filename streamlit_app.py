#import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain.chains import create_retrieval_chain
from langchain_core.messages import HumanMessage, AIMessage
from langchain.tools.retriever import create_retriever_tool
from langchain_community.tools.tavily_search import TavilySearchResults

openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')
#tavily_api_key = st.sidebar.text_input('Tavily API Key', type='password')

if not openai_api_key.startswith('sk-'):
   st.warning('Please enter your OpenAI API key!', icon='⚠')

#if not tavily_api_key.startswith('tvly-'):
#   st.warning('Please enter your Tavily API key!', icon='⚠')


# Create Retriever
loader = WebBaseLoader("https://python.langchain.com/docs/expression_language/")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=20
)
splitDocs = splitter.split_documents(docs)

embedding = OpenAIEmbeddings(api_key = openai_api_key)
vectorStore = FAISS.from_documents(docs, embedding=embedding)
retriever = vectorStore.as_retriever(search_kwargs={"k": 3})

model = ChatOpenAI(
    model='gpt-3.5-turbo-1106',
    temperature=0.7,
    api_key = openai_api_key
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a friendly assistant called Max."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

#search = TavilySearchResults()

retriever_tools = create_retriever_tool(
    retriever,
    "lcel_search",
    "Use this tool when searching for information about Langchain Expression Language (LCEL)."
)
#tools = [search, retriever_tools]
tools = [retriever_tools]

agent = create_openai_functions_agent(
    llm=model,
    prompt=prompt,
    tools=tools
)

agentExecutor = AgentExecutor(
    agent=agent,
    tools=tools
)

def process_chat(agentExecutor, user_input, chat_history):
    response = agentExecutor.invoke({
        "input": user_input,
        "chat_history": chat_history
    })
    #st.write("Response:",response["output"])
    return response["output"]
   
def submit():
    st.session_state.my_text = st.session_state.widget
    st.session_state.widget = ""
   
if __name__ == '__main__':
    chat_history = []
    # st.text_input("Enter text here", key="widget", on_change=submit)
   
# Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

# Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
             st.markdown(message["content"])

# Accept user input
    if user_input := st.chat_input("What is up?"):
    # Add user message to chat history
       st.session_state.messages.append({"role": "user", "content": user_input})
    # Display user message in chat message container
       with st.chat_message("user"):
            st.markdown(user_input)

    # Display assistant response in chat message container
       with st.chat_message("assistant"):
            stream = client.chat.completions.create(
               model=st.session_state["openai_model"],
               messages=[
                   {"role": m["role"], "content": m["content"]}
                   for m in st.session_state.messages
               ],
            stream=True,
            )
      response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
