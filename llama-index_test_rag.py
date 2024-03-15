# %%
import os

print(os.getcwd())

print(os.getenv('OPENAI_API_KEY')) 


# %%
from llama_index.llms import OpenAI
from llama_index import ServiceContext, set_global_service_context
from llama_index import SimpleDirectoryReader
from llama_index import VectorStoreIndex

#llm = OpenAI(model="text-embedding-3-small", temperature=0.2, max_tokens=256)
llm = OpenAI(model="gpt-4", temperature=0.1, max_tokens=512)

# configure service context
service_context = ServiceContext.from_defaults(llm=llm, chunk_size=512, chunk_overlap=20)
documents = SimpleDirectoryReader("../../../data/dafagu/data_final").load_data()
index = VectorStoreIndex.from_documents(documents, service_context=service_context)
index.storage_context.persist()

# %%

from llama_index import StorageContext, load_index_from_storage
from llama_index.retrievers import VectorIndexRetriever
from llama_index import get_response_synthesizer
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.postprocessor import SimilarityPostprocessor
from IPython.display import Markdown, display

storage_context = StorageContext.from_defaults(persist_dir="./storage")
index = load_index_from_storage(storage_context=storage_context)

#%%
# configure retriever
retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=5,
)

# configure response synthesizer
response_synthesizer = get_response_synthesizer()

# assemble query engine
query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer,
    node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.8)],
)

#%%
response = query_engine.query("人对宗教的信仰的需求")
display(Markdown(f"<b>{response}</b>"))


#%%
# get the text for top ranking chunck
top_k = [node.get_text() for node in response.source_nodes]
for node in top_k:
    print(node)
    print("=======================\n")
    with open('chunks.txt', 'a') as f:
        f.write(node)
        f.write('\n-----------------------------------------\n')


# %% 
response = query_engine.query("明天天气如何？")
if response=='':
    display(Markdown(f"<b>{response}</b>"))
else:
    display(Markdown(f"<b>I do not know</b>"))
    

# %%
