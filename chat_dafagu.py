import time
import streamlit as st
from llama_index import StorageContext, load_index_from_storage
from llama_index.retrievers import VectorIndexRetriever
from llama_index import get_response_synthesizer
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.postprocessor import SimilarityPostprocessor
import sys
# Start timing
#start_time = time.time()

@st.cache_data
def load_index():
    print("Loading the index...")
    start_time = time.time()
    storage_context = StorageContext.from_defaults(persist_dir="./storage")
    print("Time taken to load the storage context: %s seconds" % (time.time() - start_time))
    start_time = time.time()
    ix = load_index_from_storage(storage_context=storage_context)
    print("Time taken to load index: %s seconds" % (time.time() - start_time))
    start_time = time.time()
 
    print(f"Done Loading the index...")
    print(f"Size of index: {sys.getsizeof(ix)} bytes")
    print(f"Size of index: {sys.getsizeof(storage_context)} bytes")
    
    return ix

# Load the index
index = load_index()


# Reset the timer
start_time = time.time()

# configure retriever
retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=6,
)

# Print time taken to configure the retriever
print("Time taken to configure the retriever: %s seconds" % (time.time() - start_time))

# Reset the timer
start_time = time.time()

# configure response synthesizer
response_synthesizer = get_response_synthesizer()

# Print time taken to configure the response synthesizer
print("Time taken to configure the response synthesizer: %s seconds" % (time.time() - start_time))

# Reset the timer
start_time = time.time()

# assemble query engine
query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer,
    node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.8)],
)

# Print time taken to assemble the query engine
print("Time taken to assemble the query engine: %s seconds" % (time.time() - start_time))

# Initialize the conversation history
conversation_history = []

# ...

# Streamlit code
st.title('大法鼓问答')

user_input = st.text_input("问大法鼓：")

if user_input:
    # Add the user input to the conversation history
    conversation_history.append(user_input)
    print(user_input)

    # Generate the response using the conversation history
    #response = query_engine.query(' '.join(conversation_history))
    response = query_engine.query(user_input)

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