---
title: Jaguar Vektör Deposu (Vector Store)
 | LlamaIndex OSS Belgeleri
---

# Jaguar Vektör Deposu

Bu belge, LlamaIndex'in Jaguar vektör deposu ile nasıl çalıştığını göstermektedir.

- Çok sayıda vektörü saklayabilen dağıtık bir vektör veritabanıdır.
- ZeroMove özelliği, anlık yatay ölçeklendirmeye olanak tanır.
- Gömmeleri (embeddings), metinleri, görselleri, videoları, PDF'leri, sesleri, zaman serilerini ve mekansal verileri destekler.
- Tümü-ana sunucu (all-master) mimarisi, hem paralel okumaya hem de paralel yazmaya izin verir.
- Anomali tespiti yetenekleri, veri kümesindeki aykırı değerleri ayırt edebilir.
- RAG desteği, LLM'leri özel ve gerçek zamanlı verilerle birleştirebilir.
- Meta verilerin birden fazla vektör indeksi arasında paylaşılması veri tutarlılığını artırır.
- Mesafe metrikleri arasında Euclidean, Cosine, InnerProduct, Manhatten, Chebyshev, Hamming, Jeccard ve Minkowski bulunur.
- Benzerlik araması, zaman sınırı (time cutoff) ve zamanla aşınma (time decay) etkileriyle gerçekleştirilebilir.

## Ön Koşullar

Bu dosyadaki örnekleri çalıştırmak için iki gereksinim vardır.

JaguarDB sunucusunu ve HTTP ağ geçidi (gateway) sunucusunu kurmalı ve ayarlamalısınız. Referans olarak [Jaguar Kurulumu](http://www.jaguardb.com/docsetup.html) bölümündeki talimatları izleyin.

`llama-index` ve `jaguardb-http-client` paketlerini kurmalısınız.

**Birinci Yöntem: Docker**

```bash
docker pull jaguardb/jaguardb
docker run -d -p 8888:8888 -p 8080:8080 --name jaguardb jaguardb/jaguardb
pip install -U llama-index
pip install -U jaguardb-http-client
```

**İkinci Yöntem: Hızlı Kurulum (Linux)**

```bash
curl -fsSL http://jaguardb.com/install.sh | sh
pip install -U llama-index
pip install -U jaguardb-http-client
```

```bash
%pip install llama-index-vector-stores-jaguar
```

```bash
!pip install -U jaguardb-http-client
```

## İçe Aktarmalar

Aşağıdaki paketler içe aktarılmalıdır. Örnek olarak `OpenAIEmbedding` kullanıyoruz. Uygulamanızda diğer gömme modellerini seçebilirsiniz.

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import StorageContext
from llama_index.vector_stores.jaguar import JaguarVectorStore
from jaguardb_http_client.JaguarHttpClient import JaguarHttpClient
```

## İstemci Nesnesi (Client Object)

Şimdi bir jaguar vektör deposu istemci nesnesi oluşturuyoruz. `url`, ağ geçidi sunucusunun http uç noktasıdır. URL, ortam ayarlarınızla değiştirilmelidir. `pod`, Pod (veya veritabanı) adıdır. `store`, vektör deposunun adıdır. Bir pod'un birden fazla deposu olabilir. `vector_index`, depodaki vektör indeksinin adıdır. Bir deponun birden fazla vektör indeksi olabilir. Ancak, depo istemci nesnesi yalnızca bir vektör indeksine bağlıdır. `vector_type`, vektör indeksinin niteliklerini belirtir. "cosine_fraction_short" dizesinde `cosine`, iki vektör arasındaki mesafenin kosinüs mesafesiyle hesaplandığı anlamına gelir. `fraction`, vektör bileşenlerinin kesirli sayılar olduğu anlamına gelir. `short`, vektör bileşenlerinin saklama biçiminin 16 bitlik işaretli tam sayılar olduğu anlamına gelir. Saklama biçimi 32 bitlik kayan noktalı sayılar (`float`) olabilir. Ayrıca 8 bitlik işaretli tam sayılar (`byte`) da olabilir. `vector_dimension`, sağlanan gömme modeli tarafından oluşturulan vektörün boyutudur.

```python
url = "http://127.0.0.1:8080/fwww/"
pod = "vdb"
store = "llamaindex_jaguar_store"
vector_index = "v"
vector_type = "cosine_fraction_float"
# vector_type = "cosine_fraction_short"  # float'a kıyasla bellek kullanımının yarısı
# vector_type = "cosine_fraction_byte" # float'a kıyasla bellek kullanımının dörtte biri
vector_dimension = 1536  # OpenAIEmbedding modeline göre
jaguarstore = JaguarVectorStore(
    pod,
    store,
    vector_index,
    vector_type,
    vector_dimension,
    url,
)
```

## Kimlik Doğrulama

İstemci, sistem güvenliği ve kullanıcı kimlik doğrulaması için arka uç jaguar sunucusuna giriş yapmalı veya bağlanmalıdır. `JAGUAR_API_KEY` ortam değişkeni veya `$HOME/.jagrc` dosyası, sistem yöneticiniz tarafından verilen jaguar api anahtarını içermelidir. `login()` yöntemi `True` veya `False` döndürür. `False` döndürürse, jaguar api anahtarınız geçersiz olabilir veya http ağ geçidi sunucusu çalışmıyor olabilir veya jaguar sunucusu düzgün çalışmıyor olabilir.

```python
true_or_false = jaguarstore.login()
print(f"giriş sonucu: {true_or_false}")
```

```text
giriş sonucu: True
```

## Vektör Deposu Oluşturma

Metin tutmak için 1024 bayt boyutunda 'v:text' alanı ve iki ek meta veri alanı olan 'author' (yazar) ve 'category' (kategori) içeren bir vektör deposu oluşturuyoruz.

```python
metadata_str = "author char(32), category char(16)"
text_size = 1024
jaguarstore.create(metadata_str, text_size)
```

## Belgeleri Yükleme

Aşağıdaki kod, örnek Paul Graham belgelerini açar ve belleğe okur.

```python
documents = SimpleDirectoryReader("../data/paul_graham/").load_data()
print(f"{len(documents)} belge yükleniyor")
```

## İndeks Oluşturma

Depolama bağlamını hazırlayın ve bir indeks nesnesi oluşturun. `from_documents()` çağrısından sonra vektör deposuna kaydedilmiş 22 vektör olacaktır.

```python
### vektör depomuzu kullanarak bir depolama bağlamı oluşturun
storage_context = StorageContext.from_defaults(vector_store=jaguarstore)


### vektör deposundaki tüm vektörleri temizleyin
jaguarstore.clear()


### belgeler ve depolama bağlamı ile bir indeks oluşturun
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)


### Vektör deposuna daha fazla belge ekleyebilirsiniz:
# jaguarstore.add_documents(bazı_belgeler)
# jaguarstore.add_documents(daha_fazla_belge, text_tag="bu belgelere etiket")


### jaguar vektör deposundaki belge sayısını yazdırın
num = jaguarstore.count()
print(f"Jaguar vektör deposunda {num} vektör var")
```

## Soru Sorun

Bir sorgu motoru alıyoruz ve motora bazı sorular soruyoruz.

```python
query_engine = index.as_query_engine()
q = "Yazar büyürken neler yaptı?"
print(f"Soru: {q}")
response = query_engine.query(q)
print(f"Cevap: {str(response)}\n")


q = "Yazar Viaweb'deki zamanından sonra neler yaptı?"
print(f"Soru: {q}")
response = query_engine.query(q)
print(f"Cevap: {str(response)}")
```

```text
Soru: Yazar büyürken neler yaptı?
Cevap: Yazar büyürken okul dışında iki ana konu üzerinde çalıştığını belirtti: yazarlık ve programlama. Kısa hikayeler yazdı ve bir IBM 1401 bilgisayarında programlar yazmayı denedi.


Soru: Yazar Viaweb'deki zamanından sonra neler yaptı?
Cevap: Viaweb'deki zamanından sonra yazar, sanat galerilerini çevrimiçi hale getirmek için bir şirket kurdu. Ancak sanat galerileri çevrimiçi olmak istemediği için bu fikir başarılı olmadı.
```

## Sorgu Seçeneklerini İletme

Jaguar vektör deposundan yalnızca verilerin bir alt kümesini seçmek için sorgu motoruna ekstra argümanlar iletebiliriz. Bu, `vector_store_kwargs` argümanı kullanılarak gerçekleştirilebilir. `day_cutoff` parametresi, metnin yoksayılacağı gün sayısıdır. `day_decay_rate`, benzerlik puanları için günlük aşınma oranıdır.

```python
qkwargs = {
    "args": "day_cutoff=365,day_decay_rate=0.01",
    "where": "category='startup' or category=''",
}
query_engine_filter = index.as_query_engine(vector_store_kwargs=qkwargs)
q = "Yazarın yaşam tarzı nasıldı?"
print(f"Soru: {q}")
response = query_engine_filter.query(q)
print(f"Cevap: {str(response)}")
```

**Cevap: Yazarın yaşam tarzı, Accademia'ya bir öğrenci olarak devam etmeyi ve geceleri yatak odasında natürmort resimler yapmayı içeriyordu. Ayrıca denemeler yazdı ve başkaları için ilginç ve cesaret verici olacağını düşündüğü dağınık bir hayatı vardı.**

## Temizlik ve Çıkış Yapma

Vektör deposundaki tüm vektörler ve ilgili veriler silinebilir ve testi bitirmek için vektör deposu tamamen kaldırılabilir. `logout` çağrısı, istemci tarafından kullanılan kaynakların serbest bırakılmasını sağlar.

```python
### isterseniz vektör deposundaki tüm verileri kaldırın
jaguarstore.clear()


### isterseniz veritabanındaki tüm vektörü silin
jaguarstore.drop()


### jaguar sunucusuyla olan bağlantıyı kesin ve kaynakları temizleyin
jaguarstore.logout()
```
