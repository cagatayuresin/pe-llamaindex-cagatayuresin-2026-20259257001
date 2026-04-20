# Uzun Bağlamlı Gömme Modelleri ile Parça + Belge Hibrit Erişimi (Together.ai)

---
title: Uzun Bağlamlı Gömme Modelleri ile Parça + Belge Hibrit Erişimi (Together.ai)
 | LlamaIndex OSS Belgeleri
---

Bu not defteri, gelişmiş RAG süreci için uzun bağlamlı together.ai gömme (embedding) modellerinin nasıl kullanılacağını gösterir. Gömme modelini hem tüm belge metni üzerinde hem de her bir parça (chunk) üzerinde çalıştırarak her belgeyi indeksliyoruz. Daha sonra hem düğüm (node) benzerliğini hem de belge benzerliğini hesaplayabilen özel bir erişici tanımlıyoruz.

API anahtarı almak için <https://together.ai> adresini ziyaret edin ve kaydolun.

## Kurulum ve Veri İndirme (Setup and Download Data)

Belgelerimizi yüklüyoruz. Hız açısından sadece 10 sayfa yüklüyoruz, ancak modelinizi stres testine tabi tutmak isterseniz tamamını yüklemelisiniz.

```bash
%pip install llama-index-embeddings-together
%pip install llama-index-llms-openai
%pip install llama-index-embeddings-openai
%pip install llama-index-readers-file
```

```python
domain = "docs.llamaindex.ai"
docs_url = "https://docs.llamaindex.ai/en/latest/"
!wget -e robots=off --recursive --no-clobber --page-requisites --html-extension --convert-links --restrict-file-names=windows --domains {domain} --no-parent {docs_url}
```

```python
from llama_index.readers.file import UnstructuredReader
from pathlib import Path
from llama_index.llms.openai import OpenAI
from llama_index.core import Document
```

```python
reader = UnstructuredReader()
# all_files_gen = Path("./docs.llamaindex.ai/").rglob("*")
# all_files = [f.resolve() for f in all_files_gen]
# all_html_files = [f for f in all_files if f.suffix.lower() == ".html"]


# bir alt küme seç
all_html_files = [
    "docs.llamaindex.ai/en/latest/index.html",
    "docs.llamaindex.ai/en/latest/contributing/contributing.html",
    "docs.llamaindex.ai/en/latest/understanding/understanding.html",
    "docs.llamaindex.ai/en/latest/understanding/using_llms/using_llms.html",
    "docs.llamaindex.ai/en/latest/understanding/using_llms/privacy.html",
    "docs.llamaindex.ai/en/latest/understanding/loading/llamahub.html",
    "docs.llamaindex.ai/en/latest/optimizing/production_rag.html",
    "docs.llamaindex.ai/en/latest/module_guides/models/llms.html",
]
```

```python
# YAPILACAK: daha fazla belge istiyorsanız daha yüksek bir değer ayarlayın
doc_limit = 10


docs = []
for idx, f in enumerate(all_html_files):
    if idx > doc_limit:
        break
    print(f"Dizin (Idx) {idx}/{len(all_html_files)}")
    loaded_docs = reader.load_data(file=f, split_documents=True)
    # Sabit Kodlanmış İndeks. Bundan önceki her şey tüm sayfalar için İçindekiler'dir (ToC)
    # Bu start_idx değerini ihtiyaçlarınıza göre ayarlayın
    start_idx = 64
    loaded_doc = Document(
        id_=str(f),
        text="\n\n".join([d.get_content() for d in loaded_docs[start_idx:]]),
        metadata={"path": str(f)},
    )
    print(str(f))
    docs.append(loaded_doc)
```

```text
[nltk_data] Downloading package punkt to /Users/jerryliu/nltk_data...
[nltk_data]   Package punkt is already up-to-date!
[nltk_data] Downloading package averaged_perceptron_tagger to
[nltk_data]     /Users/jerryliu/nltk_data...
[nltk_data]   Package averaged_perceptron_tagger is already up-to-
[nltk_data]       date!


Idx 0/8
docs.llamaindex.ai/en/latest/index.html
Idx 1/8
docs.llamaindex.ai/en/latest/contributing/contributing.html
Idx 2/8
docs.llamaindex.ai/en/latest/understanding/understanding.html
Idx 3/8
docs.llamaindex.ai/en/latest/understanding/using_llms/using_llms.html
Idx 4/8
docs.llamaindex.ai/en/latest/understanding/using_llms/privacy.html
Idx 5/8
docs.llamaindex.ai/en/latest/understanding/loading/llamahub.html
Idx 6/8
docs.llamaindex.ai/en/latest/optimizing/production_rag.html
Idx 7/8
docs.llamaindex.ai/en/latest/module_guides/models/llms.html
```

## Parça Gömme + Üst Belge Gömme ile Hibrit Erişim Oluşturma (Building Hybrid Retrieval with Chunk Embedding + Parent Embedding)

Aşağıdaki adımları gerçekleştiren özel bir erişici tanımlayın:

- Önce gömme benzerliğine dayalı ilgili parçaları getirin.
- Her parça için kaynak belgenin gömme değerine bakın.
- Bir alfa değeri ile ağırlıklandırın.

Bu, temel olarak düğüm (node) benzerliklerini yeniden ağırlıklandıran bir yeniden sıralama (reranking) adımına sahip vektör erişimidir.

```python
# API anahtarını gömme modelleri içinde veya env içinde ayarlayabilirsiniz
# import os
# os.environ["TOGETHER_API_KEY"] = "api-anahtarınız"


from llama_index.embeddings.together import TogetherEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI


api_key = "<api_anahtarı>"


embed_model = TogetherEmbedding(
    model_name="togethercomputer/m2-bert-80M-32k-retrieval", api_key=api_key
)


llm = OpenAI(temperature=0, model="gpt-3.5-turbo")
```

### Belge Deposu (Document Store) Oluşturma

Orijinal belgeler için bir Belge Deposu (docstore) oluşturun. Her bir belgeyi gömme (embed) işleminden geçirin ve belge deposuna ekleyin.

Daha sonra hibrit erişim algoritmamızda buna başvuracağız!

```python
from llama_index.core.storage.docstore import SimpleDocumentStore


for doc in docs:
    embedding = embed_model.get_text_embedding(doc.get_content())
    doc.embedding = embedding


docstore = SimpleDocumentStore()
docstore.add_documents(docs)
```

### Vektör İndeksi Oluşturma (Build Vector Index)

Parçaların vektör indeksini oluşturalım. Her bir parça, `index_id` aracılığıyla kaynak belgesine bir referansa sahip olacaktır (bu daha sonra belge deposunda kaynak belgeyi aramak için kullanılabilir).

```python
from llama_index.core.schema import IndexNode
from llama_index.core import (
    load_index_from_storage,
    StorageContext,
    VectorStoreIndex,
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import SummaryIndex
from llama_index.core.retrievers import RecursiveRetriever
import os
from tqdm.notebook import tqdm
import pickle




def build_index(docs, out_path: str = "storage/chunk_index"):
    nodes = []


    splitter = SentenceSplitter(chunk_size=512, chunk_overlap=70)
    for idx, doc in enumerate(tqdm(docs)):
        # print('Parçalanıyor: ' + str(idx))


        cur_nodes = splitter.get_nodes_from_documents([doc])
        for cur_node in cur_nodes:
            # Kimlik (ID), temel + üst belge şeklinde olacaktır
            file_path = doc.metadata["path"]
            new_node = IndexNode(
                text=cur_node.text or "Yok",
                index_id=str(file_path),
                metadata=doc.metadata
                # obj=doc
            )
            nodes.append(new_node)
    print("düğüm sayısı: " + str(len(nodes)))


    # indeksi diske kaydet
    if not os.path.exists(out_path):
        index = VectorStoreIndex(nodes, embed_model=embed_model)
        index.set_index_id("simple_index")
        index.storage_context.persist(f"./{out_path}")
    else:
        # depolama bağlamını (storage context) yeniden oluştur
        storage_context = StorageContext.from_defaults(
            persist_dir=f"./{out_path}"
        )
        # indeksi yükle
        index = load_index_from_storage(
            storage_context, index_id="simple_index", embed_model=embed_model
        )


    return index


index = build_index(docs)
```

### Hibrit Erişicinin Tanımlanması (Define Hybrid Retriever)

Vektör benzerliğine göre önce parçaları getirebilen ve ardından bunları ana belgeyle benzerliğe dayalı olarak (bir alfa parametresi kullanarak) yeniden ağırlıklandırabilen hibrit bir erişici tanımlıyoruz.

```python
from llama_index.core.retrievers import BaseRetriever
from llama_index.core.indices.query.embedding_utils import get_top_k_embeddings
from llama_index.core import QueryBundle
from llama_index.core.schema import NodeWithScore
from typing import List, Any, Optional




class HybridRetriever(BaseRetriever):
    """Hibrit erişici."""


    def __init__(
        self,
        vector_index,
        docstore,
        similarity_top_k: int = 2,
        out_top_k: Optional[int] = None,
        alpha: float = 0.5,
        **kwargs: Any,
    ) -> None:
        """Parametreleri başlat (Init)."""
        super().__init__(**kwargs)
        self._vector_index = vector_index
        self._embed_model = vector_index._embed_model
        self._retriever = vector_index.as_retriever(
            similarity_top_k=similarity_top_k
        )
        self._out_top_k = out_top_k or similarity_top_k
        self._docstore = docstore
        self._alpha = alpha


    def _retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        """Sorgu verildiğinde düğümleri getirir."""


        # önce parçaları getir
        nodes = self._retriever.retrieve(query_bundle.query_str)


        # belgeleri ve sorgu ile belgeler arasındaki gömme benzerliğini al


        ## belge gömme değerlerini al
        docs = [self._docstore.get_document(n.node.index_id) for n in nodes]
        doc_embeddings = [d.embedding for d in docs]
        query_embedding = self._embed_model.get_query_embedding(
            query_bundle.query_str
        )


        ## belge benzerliklerini hesapla
        doc_similarities, doc_idxs = get_top_k_embeddings(
            query_embedding, doc_embeddings
        )


        ## belge benzerlikleri ve orijinal düğüm benzerliği ile nihai benzerliği hesapla
        result_tups = []
        for doc_idx, doc_similarity in zip(doc_idxs, doc_similarities):
            node = nodes[doc_idx]
            # ağırlık = alfa * düğüm benzerliği + (1-alfa) * belge benzerliği
            full_similarity = (self._alpha * node.score) + (
                (1 - self._alpha) * doc_similarity
            )
            print(
                f"Belge (Doc) {doc_idx} (düğüm puanı, belge benzerliği, tam benzerlik): {(node.score, doc_similarity, full_similarity)}"
            )
            result_tups.append((full_similarity, node))


        result_tups = sorted(result_tups, key=lambda x: x[0], reverse=True)
        # puanları güncelle
        for full_score, node in result_tups:
            node.score = full_score


        return [n for _, n in result_tups][:self._out_top_k]
```

```python
top_k = 10
out_top_k = 3
hybrid_retriever = HybridRetriever(
    index, docstore, similarity_top_k=top_k, out_top_k=3, alpha=0.5
)
base_retriever = index.as_retriever(similarity_top_k=out_top_k)
```

```python
def show_nodes(nodes, out_len: int = 200):
    for idx, n in enumerate(nodes):
        print(f"\n\n >>>>>>>>>>>> Kimlik (ID) {n.id_}: {n.metadata['path']}")
        print(n.get_content()[:out_len])
```

```python
query_str = "Bana LLM arayüzü ve nerelerde kullanıldıkları hakkında daha fazla bilgi ver"
```

```python
nodes = hybrid_retriever.retrieve(query_str)
```

```text
Belge 0 (düğüm puanı, belge benzerliği, tam benzerlik): (0.8951729860296237, 0.888711859390314, 0.8919424227099688)
Belge 3 (düğüm puanı, belge benzerliği, tam benzerlik): (0.7606735418349336, 0.888711859390314, 0.8246927006126239)
Belge 1 (düğüm puanı, belge benzerliği, tam benzerlik): (0.8008658562229534, 0.888711859390314, 0.8447888578066337)
Belge 4 (düğüm puanı, belge benzerliği, tam benzerlik): (0.7083936595542725, 0.888711859390314, 0.7985527594722932)
Belge 2 (düğüm puanı, belge benzerliği, tam benzerlik): (0.7627518988051541, 0.7151744680533735, 0.7389631834292638)
Belge 5 (düğüm puanı, belge benzerliği, tam benzerlik): (0.6576277615091234, 0.6506473659825045, 0.654137563745814)
Belge 7 (düğüm puanı, belge benzerliği, tam benzerlik): (0.6141130778320664, 0.6159139530209246, 0.6150135154264955)
Belge 6 (düğüm puanı, belge benzerliği, tam benzerlik): (0.6225339833394525, 0.24827341793941335, 0.43540370063943296)
Belge 8 (düğüm puanı, belge benzerliği, tam benzerlik): (0.5672766061523489, 0.24827341793941335, 0.4077750120458811)
Belge 9 (düğüm puanı, belge benzerliği, tam benzerlik): (0.5671131641337652, 0.24827341793941335, 0.4076932910365893)
```

```python
show_nodes(nodes)
```

```text
 >>>>>>>>>>>> Kimlik (ID) 2c7b42d3-520c-4510-ba34-d2f2dfd5d8f5: docs.llamaindex.ai/en/latest/module_guides/models/llms.html
Katkıda Bulunma: Belgelere yeni LLM'ler eklemek için herkes davetlidir. Mevcut bir not defterini kopyalayın, kendi LLM'nizi kurun ve test edin, ardından sonuçlarınızla birlikte bir PR açın.


Eğer bunu iyileştirecek yollarınız varsa...




 >>>>>>>>>>>> Kimlik (ID) 72cc9101-5b36-4821-bd50-e707dac8dca1: docs.llamaindex.ai/en/latest/module_guides/models/llms.html
LLM'leri Kullanma


Kavram


Verileriniz üzerinde herhangi bir LLM uygulaması oluştururken dikkate almanız gereken ilk adımlardan biri, uygun Büyük Dil Modelini (LLM) seçmektir.


LLM'ler LlamaIndex'in temel bir bileşenidir...




 >>>>>>>>>>>> Kimlik (ID) 7c2be7c7-44aa-4f11-b670-e402e5ac35a5: docs.llamaindex.ai/en/latest/module_guides/models/llms.html
Eğer LLM'i değiştirirseniz, doğru token sayımı, parçalama (chunking) ve yönlendirmeyi sağlamak için bu tokenleştiriciyi güncellemeniz gerekebilir.


Bir tokenleştirici için tek gereksinim, çağrılabilir bir fonksiyon olmasıdır...
```

```python
base_nodes = base_retriever.retrieve(query_str)
```

```python
show_nodes(base_nodes)
```

```text
 >>>>>>>>>>>> Kimlik (ID) 2c7b42d3-520c-4510-ba34-d2f2dfd5d8f5: docs.llamaindex.ai/en/latest/module_guides/models/llms.html
Katkıda Bulunma: Belgelere yeni LLM'ler eklemek için herkes davetlidir. Mevcut bir not defterini kopyalayın, kendi LLM'nizi kurun ve test edin, ardından sonuçlarınızla birlikte bir PR açın.


Eğer bunu iyileştirecek yollarınız varsa...




 >>>>>>>>>>>> Kimlik (ID) 72cc9101-5b36-4821-bd50-e707dac8dca1: docs.llamaindex.ai/en/latest/module_guides/models/llms.html
LLM'leri Kullanma


Kavram


Verileriniz üzerinde herhangi bir LLM uygulaması oluştururken dikkate almanız gereken ilk adımlardan biri, uygun Büyük Dil Modelini (LLM) seçmektir.


LLM'ler LlamaIndex'in temel bir bileşenidir...




 >>>>>>>>>>>> Kimlik (ID) 252fc99b-2817-4913-bcbf-4dd8ef509b8c: docs.llamaindex.ai/en/latest/index.html
Bunlar API'ler, PDF'ler, SQL ve (çok) daha fazlası olabilir.


Veri indeksleri, verilerinizi LLM'lerin tüketmesi için kolay ve performanslı aramalar sağlayan ara temsillere göre yapılandırır.


Motorlar doğal dilde erişim sağlar...
```

## Bazı Sorgular Çalıştırın (Run Some Queries)

```python
from llama_index.core.query_engine import RetrieverQueryEngine


query_engine = RetrieverQueryEngine(hybrid_retriever)
base_query_engine = index.as_query_engine(similarity_top_k=out_top_k)
```

```python
response = query_engine.query(query_str)
print(str(response))
```

```text
Belge 0 (düğüm puanı, belge benzerliği, tam benzerlik): (0.8951729860296237, 0.888711859390314, 0.8919424227099688)
Belge 3 (düğüm puanı, belge benzerliği, tam benzerlik): (0.7606735418349336, 0.888711859390314, 0.8246927006126239)
Belge 1 (düğüm puanı, belge benzerliği, tam benzerlik): (0.8008658562229534, 0.888711859390314, 0.8447888578066337)
Belge 4 (düğüm puanı, belge benzerliği, tam benzerlik): (0.7083936595542725, 0.888711859390314, 0.7985527594722932)
Belge 2 (düğüm puanı, belge benzerliği, tam benzerlik): (0.7627518988051541, 0.7151744680533735, 0.7389631834292638)
Belge 5 (düğüm puanı, belge benzerliği, tam benzerlik): (0.6576277615091234, 0.6506473659825045, 0.654137563745814)
Belge 7 (düğüm puanı, belge benzerliği, tam benzerlik): (0.6141130778320664, 0.6159139530209246, 0.6150135154264955)
Belge 6 (düğüm puanı, belge benzerliği, tam benzerlik): (0.6225339833394525, 0.24827341793941335, 0.43540370063943296)
Belge 8 (düğüm puanı, belge benzerliği, tam benzerlik): (0.5672766061523489, 0.24827341793941335, 0.4077750120458811)
Belge 9 (düğüm puanı, belge benzerliği, tam benzerlik): (0.5671131641337652, 0.24827341793941335, 0.4076932910365893)
LLM arayüzü, OpenAI, Hugging Face veya LangChain gibi farklı kaynaklardan Büyük Dil Modellerini (LLM'ler) tanımlamak için LlamaIndex tarafından sağlanan birleşik bir arayüzdür. Bu arayüz, LLM arayüzünü tanımlamak için gerekli olan kalıplaşmış (boilerplate) kodları yazma ihtiyacını ortadan kaldırır. LLM arayüzü metin tamamlama (text completion) ve sohbet (chat) uç noktalarının yanı sıra akış (streaming) olan ve olmayan uç noktaları da destekler. Ayrıca hem senkron hem de asenkron uç noktaları destekler.


LLM'ler LlamaIndex'in temel bileşenlerinden biridir ve bağımsız modüller olarak kullanılabilirler veya indeksler, erişiciler ve sorgu motorları gibi diğer temel LlamaIndex modüllerine takılabilirler. Öncelikle erişimden sonra gerçekleşen yanıt sentezi (response synthesis) adımında kullanılırlar. Kullanılan indeks türüne bağlı olarak, LLM'ler indeks oluşturma, ekleme ve sorgu gezintisi (query traversal) sırasında da kullanılabilir.


LLM'leri kullanmak için gerekli modülleri içe aktarabilir ve LLM nesnesini oluşturabilirsiniz. Daha sonra yanıtlar oluşturmak veya metin istemlerini tamamlamak için LLM nesnesini kullanabilirsiniz. LlamaIndex, LLM'leri kullanmaya başlamanıza yardımcı olacak örnekler ve kod parçacıkları sunar.


Tokenleştirmenin LLM'lerde çok önemli bir rol oynadığını unutmamak gerekir. LlamaIndex varsayılan olarak global bir tokenleştirici (tokenizer) kullanır, ancak LLM'i değiştirirseniz doğru token sayımı, parçalama ve yönlendirme sağlamak için tokenleştiriciyi güncellemeniz gerekebilir. LlamaIndex, tiktoken veya Hugging Face’in AutoTokenizer’ı gibi kütüphaneleri kullanarak global bir tokenleştiricinin nasıl ayarlanacağına dair talimatlar sağlar.


Genel olarak LLM'ler, LlamaIndex uygulamaları oluşturmak için güçlü araçlardır ve LlamaIndex soyutlamaları (abstractions) dahilinde özelleştirilebilirler. OpenAI ve Anthropic gibi ücretli API'lerden alınan LLM'ler genel olarak daha güvenilir kabul edilse de, yerel açık kaynaklı modeller özelleştirilebilirlikleri ve şeffaflıkları sayesinde popülerlik kazanmaktadır. LlamaIndex çeşitli LLM'lerle entegrasyonlar sunar ve uyumlulukları ile performansları hakkında belgeler sağlar. Mevcut LLM'lerin kurulumunu ve performansını iyileştirmek veya yeni LLM'ler eklemek için yapılacak katkılar memnuniyetle karşılanır.
```

```python
base_response = base_query_engine.query(query_str)
print(str(base_response))
```

```text
LLM arayüzü, OpenAI, Hugging Face veya LangChain gibi farklı sağlayıcılardan gelen Büyük Dil Modeli (LLM) modüllerini tanımlamak için LlamaIndex tarafından sağlanan birleşik bir arayüzdür. Kullanıcıların, LLM arayüzünü tanımlamak için gereken kalıplaşmış kodları yazmak zorunda kalmadan farklı sağlayıcılardan gelen LLM'leri uygulamalarına kolayca entegre etmelerini sağlar.


LLM'ler LlamaIndex'in temel bileşenlerinden biridir ve bağımsız modüller olarak kullanılabilirler veya indeksler, erişiciler ve sorgu motorları gibi diğer temel LlamaIndex modüllerine takılabilirler. Öncelikle erişimden sonra gerçekleşen yanıt sentezi adımında kullanılırlar. Kullanılan indeks türüne bağlı olarak, LLM'ler indeks oluşturma, ekleme ve sorgu gezintisi sırasında da kullanılabilir.


LLM arayüzü, metin tamamlama ve sohbet uç noktaları da dahil olmak üzere çeşitli işlevleri destekler. Ayrıca akış olan ve olmayan uç noktaların yanı sıra senkron ve asenkron uç noktalar için de destek sağlar.


LLM'leri kullanmak için gerekli modülleri içe aktarabilir ve sağlanan fonksiyonlardan yararlanabilirsiniz. Örneğin, gpt-3.5-turbo LLM ile etkileşime girmek için `OpenAI()` fonksiyonunu çağırarak OpenAI modülünü kullanabilirsiniz. Daha sonra verilen bir isteme dayalı tamamlamalar oluşturmak için `complete()` fonksiyonunu kullanabilirsiniz.


LlamaIndex'in tüm token sayımları için varsayılan olarak tiktoken'dan cl100k adlı global bir tokenleştirici kullandığını unutmamak önemlidir. Kullanılan LLM'i değiştirirseniz, doğru token sayımı, parçalama ve yönlendirme sağlamak için tokenleştiriciyi güncellemeniz gerekebilir.


Genel olarak LLM'ler ve LlamaIndex tarafından sağlanan LLM arayüzü, LLM uygulamaları oluşturmak ve bunları LlamaIndex ekosistemine entegre etmek için gereklidir.
```
