# Belgeleri Yükleme

---
title: Belgeleri Yükleme
 | LlamaIndex OSS Documentation
---

documents = SimpleDirectoryReader(”./data/paul\_graham/“).load\_data() print(“Document ID:”, len(documents), documents\[0].doc\_id)

````
    Document ID: 1 8d84aefd-ca73-4c1e-b83d-141c1b1b3ba6






```python
from llama_index import ServiceContext
from llama_index.embeddings import HuggingFaceEmbedding
from llama_index.vector_stores import VearchVectorStore


"""
vearch cluster
"""
vector_store = VearchVectorStore(
    path_or_url="http://liama-index-router.vectorbase.svc.sq01.n.jd.local",
    table_name="liama_index_test2",
    db_name="liama_index",
    flag=1,
)


"""
vearch standalone
"""
# vector_store = VearchVectorStore(
#         path_or_url = '/data/zhx/zhx/liama_index/knowledge_base/liama_index_teststandalone',
#         # path_or_url = 'http://liama-index-router.vectorbase.svc.sq01.n.jd.local',
#         table_name = 'liama_index_teststandalone',
#         db_name = 'liama_index',
#         flag = 0)


embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
service_context = ServiceContext.from_defaults(embed_model=embed_model)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, service_context=service_context
)
````

```
Loading checkpoint shards:   0%|          | 0/7 [00:00<?, ?it/s]
```

```
query_engine = index.as_query_engine()
response = query_engine.query("What did the author do growing up?")
display(Markdown(f"<b>{response}</b>"))
```

**Yazar, yetişme dönemi hakkında herhangi bir bilgi vermedi.**

```
query_engine = index.as_query_engine()
response = query_engine.query(
    "What did the author do after his time at Y Combinator?"
)
display(Markdown(f"<b>{response}</b>"))
```

**Yazar, Y Combinator üzerinde çalışmaya devam ederken Y Combinator'ın tüm dahili yazılımlarını Arc'ta yazdı, ancak daha sonra Arc üzerinde çalışmayı bıraktı ve denemeler yazmaya ve Y Combinator üzerinde çalışmaya odaklandı. 2012 yılında yazarın annesi felç geçirdi ve yazar, Y Combinator'ın zamanının çok fazlasını aldığını fark ederek onu başka birine devretmeye karar verdi. Yazar bunu, Y Combinator'ın yazarın yaptığı son harika şey olmadığından emin olması için yazara talep edilmemiş bir tavsiyede bulunan Robert Morris'e önerdi. Yazar nihayetinde 2013 yılında Y Combinator'ın liderliğini Sam Altman'a devretmeye karar verdi.**
