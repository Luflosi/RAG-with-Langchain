#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os


# In[2]:


import streamlit as st

from streamlit_jupyter import StreamlitPatcher, tqdm

sp = StreamlitPatcher()
sp.jupyter()  # register streamlit with jupyter-compatible wrappers


# In[3]:


IN_JUPYTER_NOTEOOK = sp.registered_methods != set()
if IN_JUPYTER_NOTEOOK:
    print("We're running inside of a Jupyter Notebook")
else:
    print("We're running outside of a Jupyter Notebook")


# In[4]:


# --- Streamlit Application UI
st.set_page_config(page_title="Nixpkgs RAG Chatbot", page_icon="🤖")
st.title("🤖 Nixpkgs RAG Chatbot")
st.caption("A conversational AI assistant for the Nixpkgs manual.")


# In[5]:


from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
import json

def scrape_and_cache(url, cache_filepath):
  if os.path.exists(cache_filepath):
    with open(cache_filepath, 'r') as f:
      cached_data = json.load(f)
      docs = [Document(page_content=item['page_content'], metadata=item['metadata']) for item in cached_data]
      print("cached Data is found")
      return docs
  else:
    print(f"Caching not found, Scraping from: {url}")
    loader = WebBaseLoader(web_paths=[url]) # edit for the nix page
    docs= loader.load()

    os.makedirs(os.path.dirname(cache_filepath), exist_ok=True)
    serializable_docs = []
    for doc in docs:
      serializable_docs.append({
          'page_content': doc.page_content,
          'metadata' : doc.metadata #check if metadatas
      })

    with open(cache_filepath, 'w') as f:
      json.dump(serializable_docs, f, indent=4, ensure_ascii=False)
    print(f"scraped data is cached to: {cache_filepath}")
    return docs


web_path = "https://nixos.org/manual/nixpkgs/stable/"
cache_dir = "scraped_data_cache"
cache_file = os.path.join(cache_dir, "nix_docs.json")
docs = scrape_and_cache(web_path, cache_file)


# In[6]:


# from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    is_separator_regex=False,
)
splits = text_splitter.split_documents(docs)
# vectorstore_nix = Chroma.from_documents(documents=splits, embedding=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"))
vectorstore_nix = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
retriever = vectorstore_nix.as_retriever()
from langchain_community.vectorstores import Chroma

## Change to HTMLHeaderTextSplitter
# @st.cache_resource
# def setup_vector_store():
#     docs = scrape_and_cache(web_path, cache_file)
#     html_splitter = HTMLHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
#     # Use the embedding model parameters.

#     splits = text_splitter.split_documents(docs)
#     embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
#     vectorstore_nix = Chroma.from_documents(
#         documents=splits,
#         embedding=embedding,
#     )
#     return html_splitter, vectorstore_nix
    # print("the length of the split is", len(splits))
#for i in splits:
#  print(i)


# In[7]:


st.title("Example")


# In[8]:


# # Add docs to vector DB using Chroma DB
# # from langchain_openai import OpenAIEmbeddings

# from langchain.text_splitter import HTMLHeaderTextSplitter, RecursiveCharacterTextSplitter
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.vectorstores import Chroma


# headers_to_split_on = [
#     ("h1", "Header 1"),
#     ("h2", "Header 2"),
#     ("h3", "Header 3"),
# ]
# # chunk_size = MAX_SEQ_LENGTH - HF_EOS_TOKEN_LENGTH
# # chunk_overlap = np.round(chunk_size * 0.10, 0)
# html_splitter = HTMLHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
# child_splitter = RecursiveCharacterTextSplitter(
#     # Set a really small chunk size, just to show.
#     chunk_size=1000,
#     chunk_overlap=200,
#     length_function=len,
#     is_separator_regex=False,
# )

# docs = scrape_and_cache(web_path, cache_file)

# def process_html_splits(html_splitter, headers_to_split_on):
#     html_header_splits = []
#     for doc in docs:
#         splits = html_splitter.split_text(doc.page_content)
#         for split in splits:
#             # Add the source URL and header values to the metadata
#             metadata = {}    
#             new_text = split.page_content    
#             for header_name, metadata_header_name in headers_to_split_on:    
#                 header_value = new_text.split("¶ ")[0].strip()    
#                 metadata[header_name] = header_value    
#                 try:
#                     new_text = new_text.split("¶ ")[1].strip()    
#                 except:
#                     break
#             split.metadata = {
#                 **metadata,
#                 "source": doc.metadata["source"]}
#             split.page_content = split.page_content
#         html_header_splits.extend(splits)
#     return html_header_splits

# processed_splits = process_html_splits(html_splitter, headers_to_split_on)
# splits = child_splitter.split_documents(processed_splits)

# vectorstore_nix = Chroma.from_documents(documents=splits, embedding=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"))
# retriever = vectorstore_nix.as_retriever(search_type="similarity")




# In[9]:


# #Auugmentation
# # fetch the documents from the vector DB and then along with question whcih is a context send it to the

# #https://smith.langchain.com/hub/rlm/rag-prompt?organizationId=05726ff1-dd0c-4484-9c9c-cc8927681d12 # prompt from the lanchain hub

# from langchain import hub
# prompt = hub.pull("rlm/rag-prompt")

# print(prompt)


# In[10]:


#setup LLM
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-3.5-turbo") # default model is being used here

# from langchain_ollama import ChatOllama
# llm = ChatOllama(
#     model="deepseek-r1:1.5b",
#     reasoning=True,
# )

from langchain_core.runnables import RunnablePassthrough # RunnablePassthrough is used when you want to pass the input as it is.
from langchain_core.output_parsers import StrOutputParser # the output from llm has lot of info so to get only the correct content


# In[11]:


from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory


# In[12]:


from langchain.chains import create_history_aware_retriever, create_retrieval_chain

### Contextualize question ###
contextualize_q_system_prompt = """Given a chat history and the latest user question \
which might reference context in the chat history, formulate a standalone question \
which can be understood without the chat history. Do NOT answer the question, \
just reformulate it if needed and otherwise return it as is."""

contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)


# In[13]:


from langchain.chains.combine_documents import create_stuff_documents_chain
### Answer question ###
qa_system_prompt = """As a highly knowledgeable Nix Manual assistant, your role is to accurately interpret Nix related queries and 
provide responses using our specialized Nix Manual database. Follow these directives to ensure optimal user interactions:\
1. Precision in Answers: Respond solely with information directly relevant to the user's query from our Nix Manual database. 
    Refrain from making assumptions or adding extraneous details.\
2. Handling Off-topic Queries: For questions unrelated to Nix Manual (e.g., general knowledge questions like "Why is the sky blue?"), 
    politely inform the user that the query is outside the chatbot’s scope and suggest redirecting to Nix Manual-related inquiries.\
3. Contextual Accuracy: Ensure responses are directly related to the Nix Manual query, utilizing only pertinent 
    information from our database.\
4. Relevance Check: If a query does not align with our Nix Manual database, guide the user to refine their 
    question or politely decline to provide an answer.\
5. Avoiding Duplication: Ensure no response is repeated within the same interaction, maintaining uniqueness and 
    relevance to each user query.\
6. Streamlined Communication: Eliminate any unnecessary comments or closing remarks from responses. Focus on
    delivering clear, concise, and direct answers.\
7. Avoid Non-essential Sign-offs: Do not include any sign-offs like "Best regards" or "NixBot" in responses.\
8. One-time Use Phrases: Avoid using the same phrases multiple times within the same response. Each 
    sentence should be unique and contribute to the overall message without redundancy.\

{context}"""
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)


# In[14]:


from langchain_core.chat_history import BaseChatMessageHistory

rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)


### Statefully manage chat history ###
store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if "messages" not in st.session_state:
        st.session_state.messages = ChatMessageHistory()
    return st.session_state.messages

conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",
)


# In[15]:


# print(conversational_rag_chain.invoke(
#     {"input": "what are the best supported platforms?"},
#     config={
#         "configurable": {"session_id": "abc123"}
#     },
# )["answer"])


# In[17]:


from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage

if "messages" not in st.session_state:
    st.session_state.messages = ChatMessageHistory()
    st.session_state.messages.add_ai_message("Hello! I'm your assistant for the Nixpkgs manual. How can I help you today?")

for message in st.session_state.messages.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

# st.chat_input() is not implemented in streamlit-jupyter, so fall back to input()
input_function = input if IN_JUPYTER_NOTEOOK else st.chat_input
if prompt := input_function("Ask me a question..."):
    st.session_state.messages.add_user_message(prompt)
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = conversational_rag_chain.invoke(
                {"input": prompt},
                config={"configurable": {"session_id": "streamlit_session_id"}}
            )
            st.markdown(response["answer"])
            st.session_state.messages.add_ai_message(response["answer"])


# In[ ]:




