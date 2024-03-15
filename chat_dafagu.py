import streamlit as st
from markdown import Markdown
from llama_index import StorageContext, load_index_from_storage
from llama_index.retrievers import VectorIndexRetriever
from llama_index import get_response_synthesizer
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.postprocessor import SimilarityPostprocessor
#from IPython.display import Markdown, display

# ...

storage_context = StorageContext.from_defaults(persist_dir="./storage")
index = load_index_from_storage(storage_context=storage_context)

# configure retriever
retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=6,
)

# configure response synthesizer
response_synthesizer = get_response_synthesizer()

# assemble query engine
query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer,
    node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.8)],
)

# Initialize the conversation history
conversation_history = []

# ...

# Streamlit code
st.title('大法鼓问答')

user_input = st.text_input("问大法鼓：")

if user_input:
    # Add the user input to the conversation history
    conversation_history.append(user_input)

    # Generate the response using the conversation history
    response = query_engine.query(' '.join(conversation_history))

    # Add the response to the conversation history
    conversation_history.append(response)

    st.markdown(f"**{response}**")
    #print(response)
    st.write("-----------------------------------------------------------------")
    st.write("下面是用来产生回答用的大法鼓原文，本程式是用这些和问题相关的原文来产生以上回答。供测试用")
    st.write("-----------------------------------------------------------------")  
    # get the text for top ranking chunck
    top_k = [node.get_text() for node in response.source_nodes]
    for node in top_k:
        st.write(node)