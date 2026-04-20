# Döküman Yönetimi (Document Management)

Çoğu LlamaIndex indeks yapısı **ekleme (insertion)**, **silme (deletion)**, **güncelleme (update)** ve **yenileme (refresh)** işlemlerine izin verir.

## Ekleme (Insertion)

İndeksi başlangıçta oluşturduktan sonra, herhangi bir indeks veri yapısına yeni bir Döküman (Document) "ekleyebilirsiniz". Bu döküman node'lara ayrılacak ve indekse dahil edilecektir.

Ekleme işleminin arkasındaki temel mekanizma indeks yapısına bağlıdır. Örneğin, özet indeksi (summary index) için yeni bir Döküman, listedeki ek node(lar) olarak eklenir. Vektör deposu indeksi (vector store index) için yeni bir Döküman (ve embedding'ler) temel döküman/embedding deposuna eklenir.

Aşağıda bir örnek kod parçası verilmiştir:

```python
from llama_index.core import SummaryIndex, Document

index = SummaryIndex([])
text_chunks = ["metin_parçası_1", "metin_parçası_2", "metin_parçası_3"]

doc_chunks = []
for i, text in enumerate(text_chunks):
    doc = Document(text=text, id_=f"doc_id_{i}")
    doc_chunks.append(doc)

# ekle
for doc_chunk in doc_chunks:
    index.insert(doc_chunk)
```

## Silme (Deletion)

Bir `document_id` belirterek çoğu indeks veri yapısından bir Dökümanı "silebilirsiniz". (**NOT**: Ağaç indeksi (tree index) şu an için silme işlemini desteklememektedir). Dökümana karşılık gelen tüm node'lar silinecektir.

```python
index.delete_ref_doc("doc_id_0", delete_from_docstore=True)
```

Aynı döküman deposunu (docstore) kullanan indeksler arasında node paylaşıyorsanız `delete_from_docstore` varsayılan olarak `False` olacaktır. Ancak, sorgulama için hangi node'ların kullanılabileceğini takip eden `index_struct` yapısından silinecekleri için, bu değer `False` olarak ayarlandığında sorgulama sırasında kullanılmayacaklardır.

## Güncelleme (Update)

Bir Döküman zaten bir indekste mevcutsa, aynı döküman `id_` değerine sahip bir dökümanı "güncelleyebilirsiniz" (örneğin, Dökümandaki bilgiler değiştiyse).

```python
# NOT: dökümanın bir `id_` değeri belirtilmiştir
doc_chunks[0].text = "Yepyeni döküman metni"
index.update_ref_doc(doc_chunks[0])
```

## Yenileme (Refresh)

Verilerinizi yüklerken her dökümanın döküman `id_` değerini ayarlarsanız, indeksi otomatik olarak da yenileyebilirsiniz.

`refresh()` fonksiyonu yalnızca döküman `id_` değeri aynı olan ancak metin içeriği farklı olan dökümanları güncelleyecektir. İndekste hiç bulunmayan tüm dökümanlar da eklenecektir.

`refresh()` ayrıca girdideki hangi dökümanların indekste yenilendiğini gösteren boole (boolean) bir liste döndürür.

```python
# aynı doc_id'ye sahip ilk dökümanı değiştirin
doc_chunks[0] = Document(text="Süper yeni döküman metni", id_="doc_id_0")

# yeni bir döküman ekleyin
doc_chunks.append(
    Document(
        text="Bu henüz indekste değil, ama yakında olacak!",
        id_="doc_id_3",
    )
)

# indeksi yenile
refreshed_docs = index.refresh_ref_docs(doc_chunks)

# refreshed_docs[0] ve refreshed_docs[-1] true olmalıdır
```

Yine, dökümanın döküman deposundan silindiğinden emin olmak için bazı ek argümanlar geçtik. Bu elbette isteğe bağlıdır.

`refresh()` çıktısını yazdırırsanız (`print()`), hangi girdi dökümanlarının yenilendiğini görebilirsiniz:

```python
print(refreshed_docs)
# > [True, False, False, True]
```

Bu özellik, sürekli yeni bilgilerle güncellenen bir dizinden okuma yaparken çok kullanışlıdır.

`SimpleDirectoryReader` kullanırken döküman `id_` değerini otomatik olarak ayarlamak için `filename_as_id` bayrağını etkinleştirebilirsiniz. [Dökümanları özelleştirme](/python/framework/module_guides/loading/documents_and_nodes/usage_documents) hakkında daha fazla bilgi edinebilirsiniz.

## Döküman Takibi (Document Tracking)

Döküman deposunu (docstore) kullanan herhangi bir indekste (yani çoğu vektör deposu entegrasyonu dışındaki tüm indekslerde), döküman deposuna hangi dökümanları eklediğinizi görebilirsiniz.

```python
print(index.ref_doc_info)
"""
> {'doc_id_1': RefDocInfo(node_ids=['071a66a8-3c47-49ad-84fa-7010c6277479'], metadata={}),
   'doc_id_2': RefDocInfo(node_ids=['9563e84b-f934-41c3-acfd-22e88492c869'], metadata={}),
   'doc_id_0': RefDocInfo(node_ids=['b53e6c2f-16f7-4024-af4c-42890e945f36'], metadata={}),
   'doc_id_3': RefDocInfo(node_ids=['6bedb29f-15db-4c7c-9885-7490e10aa33f'], metadata={})}
"""
```

Çıktıdaki her giriş, anahtar olarak sisteme dahil edilen döküman `id_`lerini ve bunlarla ilişkili, dökümanların bölündüğü node'ların `node_ids` listesini gösterir.

Son olarak, her giriş dökümanının orijinal `metadata` sözlüğü de takip edilir. `metadata` özniteliği hakkında daha fazla bilgiyi [Dökümanları Özelleştirme](/python/framework/module_guides/loading/documents_and_nodes/usage_documents) bölümünde okuyabilirsiniz.