# VideoDB'ye Bağlanma (connect to VideoDB)

---
title: VideoDB'ye Bağlanma (connect to VideoDB)
 | LlamaIndex OSS Belgeleri
---

```python
conn = connect()
coll = conn.create_collection(name="VideoDB Erişicileri", description="VideoDB Erişicileri")
```

# VideoDB'deki varsayılan koleksiyona videoları yükleyin

```python
print("Video Yükleniyor")
video = coll.upload(url="https://www.youtube.com/watch?v=aRgP3n0XiMc")
print(f"Video şu kimlikle yüklendi: {video.id}")
```

```text
    Video Yükleniyor
    Video şu kimlikle yüklendi: m-a758f9bb-f769-484a-9d54-02417ccfe7e6
```

> * `coll = conn.get_collection()` : Varsayılan koleksiyon nesnesini döndürür.
> * `coll.get_videos()` : Bir koleksiyondaki tüm videoların listesini döndürür.
> * `coll.get_video(video_id)`: Verilen `video_id` değerine sahip Video nesnesini döndürür.

### 🗣️ Adım 2: Konuşulan İçerikten İndeksleme ve Arama (Step 2: Indexing & Search from Spoken Content)

Video, farklı modalitelere sahip veriler olarak görülebilir. İlk olarak `konuşulan içerik` üzerinde çalışacağız.

#### 🗣️ Konuşulan İçeriği İndeksleme (Indexing Spoken Content)

```python
print("Videodaki konuşulan içerik indeksleniyor...")
video.index_spoken_words()
```

```text
Videodaki konuşulan içerik indeksleniyor...

100%|████████████████████████████████████████████████████████████████████████████████████████████████████| 100/100 [00:48<00:00,  2.08it/s]
```

#### 🗣️ Konuşma İndeksinden İlgili Düğümleri Getirme (Retrieving Relevant Nodes from Spoken Index)

İndekslenmiş içeriğimizden ilgili düğümleri getirmek için `VideoDBRetriever` kullanacağız. Video kimliği bir parametre olarak geçilmeli ve `index_type` değeri `IndexType.spoken_word` olarak ayarlanmalıdır.

Deney yaptıktan sonra `score_threshold` ve `result_threshold` değerlerini yapılandırabilirsiniz.

```python
from llama_index.retrievers.videodb import VideoDBRetriever
from videodb import SearchType, IndexType


spoken_retriever = VideoDBRetriever(
    collection=coll.id,
    video=video.id,
    search_type=SearchType.semantic,
    index_type=IndexType.spoken_word,
    score_threshold=0.1,
)


spoken_query = "Ülke çapındaki sınavlar"
nodes_spoken_index = spoken_retriever.retrieve(spoken_query)
```

#### 🗣️ Sonucu Görüntüleme: 💬 Metin (Viewing the result : Text)

İlgili düğümleri kullanacağız ve llamaindex kullanarak yanıtı sentezleyeceğiz.

```python
from llama_index.core import get_response_synthesizer


response_synthesizer = get_response_synthesizer()


response = response_synthesizer.synthesize(
    spoken_query, nodes=nodes_spoken_index
)
print(response)
```

```text
Ülke çapındaki sınavların sonuçları tüm gün merakla beklendi.
```

#### 🗣️ Sonucu Görüntüleme: 🎥 Video Klibi (Viewing the result : Video Clip)

Sorguyla ilgili getirilen her düğüm için, metaverideki `start` (başlangıç) ve `end` (bitiş) alanları düğümün kapsadığı zaman aralığını temsil eder.

Bu düğümlerin zaman damgalarına dayalı ilgili video kliplerinden oluşan bir akış oluşturmak için VideoDB'nin Programlanabilir Akışını (Programmable Stream) kullanacağız.

```python
from videodb import play_stream


results = [
    (node.metadata["start"], node.metadata["end"])
    for node in nodes_spoken_index
]


stream_link = video.generate_stream(results)
play_stream(stream_link)
```

```text
'https://console.videodb.io/player?url=https://dseetlpshk2tb.cloudfront.net/v3/published/manifests/3c108acd-e459-494a-bc17-b4768c78e5df.m3u8'
```

### 📸️ Adım 3: Görsel İçerikten İndeksleme ve Arama (Step 3: Index & Search from Visual Content)

#### 📸 Görsel İçeriği İndeksleme (Indexing Visual Content)

Sahne İndeksi (Scene Index) hakkında daha fazla bilgi edinmek için aşağıdaki kılavuzları inceleyin:

- [Hızlı Başlangıç Kılavuzu](https://github.com/video-db/videodb-cookbook/blob/main/quickstart/Scene%20Index%20QuickStart.ipynb): Sahne İndeksine adım adım giriş sağlar. Hızlıca başlamak ve temel işlevleri anlamak için idealdir.

- [Sahne Çıkarma Seçenekleri Kılavuzu](https://github.com/video-db/videodb-cookbook/blob/main/guides/scene-index/playground_scene_extraction.ipynb): Sahne İndeksi içindeki sahne çıkarma için mevcut çeşitli seçenekleri derinlemesine inceler. Gelişmiş ayarları, özelleştirme özelliklerini ve farklı ihtiyaç ve tercihlere göre sahne çıkarmayı optimize etmek için ipuçlarını kapsar.

```python
from videodb import SceneExtractionType


print("Videodaki Görsel içerik indeksleniyor...")


# Sahne içeriğini indeksle
index_id = video.index_scenes(
    extraction_type=SceneExtractionType.shot_based,
    extraction_config={"frame_count": 3},
    prompt="Sahneyi detaylıca tanımla",
)
video.get_scene_index(index_id)


print(f"Sahne İndeksi şu kimlikle başarılı: {index_id}")
```

```text
Videodaki Görsel içerik indeksleniyor...
Sahne İndeksi şu kimlikle başarılı: 990733050d6fd4f5
```

#### 📸️ Sahne İndeksinden İlgili Düğümleri Getirme (Retrieving Relevant Nodes from Scene Index)

Konuşma indeksi için `VideoDBRetriever`ı nasıl kullandıysak, sahne indeksi için de öyle kullanacağız. Burada, `index_type` değerini `IndexType.scene` olarak ayarlamamız ve `scene_index_id` değerini geçmemiz gerekecektir.

```python
from llama_index.retrievers.videodb import VideoDBRetriever
from videodb import SearchType, IndexType


scene_retriever = VideoDBRetriever(
    collection=coll.id,
    video=video.id,
    search_type=SearchType.semantic,
    index_type=IndexType.scene,
    scene_index_id=index_id,
    score_threshold=0.1,
)


scene_query = "kaza sahneleri"
nodes_scene_index = scene_retriever.retrieve(scene_query)
```

#### 📸️️️ Sonucu Görüntüleme: 💬 Metin (Viewing the result : Text)

```python
from llama_index.core import get_response_synthesizer


response_synthesizer = get_response_synthesizer()


response = response_synthesizer.synthesize(
    scene_query, nodes=nodes_scene_index
)
print(response)
```

```text
Tanımlanan sahneler kazaları tasvir etmiyor, aksine geceleri kentsel ortamlarda hareket, aciliyet ve gerilim içeren dinamik ve yoğun senaryoları betimliyor.
```

#### 📸 ️ Sonucu Görüntüleme: 🎥 Video Klibi (Viewing the result : Video Clip)

```python
from videodb import play_stream


results = [
    (node.metadata["start"], node.metadata["end"])
    for node in nodes_scene_index
]


stream_link = video.generate_stream(results)
play_stream(stream_link)
```

```text
'https://console.videodb.io/player?url=https://dseetlpshk2tb.cloudfront.net/v3/published/manifests/ae74e9da-13bf-4056-8cfa-0267087b74d7.m3u8'
```

### 🛠️ Adım 4: Basit Çok Modlu RAG - Her iki modalitenin sonuçlarını birleştirme (Step 4: Simple Multimodal RAG)

Video kitaplığımızdaki çok modlu sorguların kilidini bu şekilde açmak istiyoruz:

> 📸🗣️ “*Bana şunları göster: 1.Kaza Sahnesi 2.Ülke çapındaki sınavlar hakkındaki tartışma*”

Çok modlu bir RAG oluşturmanın birçok yolu vardır, basitlik açısından basit bir yaklaşım seçiyoruz:

1. 🧩 **Sorgu Dönüşümü (Query Transformation)**: Sorguyu, ilgili sahne ve konuşma indeksleriyle kullanılabilecek iki bölüme ayırın.
2. 🔎 **Her modalite için ilgili düğümleri bulma**: `VideoDBRetriever` kullanarak Konuşma İndeksi ve Sahne İndeksinden ilgili düğümleri bulun.
3. ✏️ **Sonucu görüntüleme: Metin**: Hassas video segmenti tanımlaması için her iki indeksten gelen sonuçları entegre ederek metin tabanlı bir yanıt sentezlemek üzere İlgili Düğümleri kullanın.
4. 🎥 **Sonucu görüntüleme: Video Klibi**: Hassas video segmenti tanımlaması için her iki indeksten gelen sonuçları entegre edin.

> Daha gelişmiş çok modlu teknikleri incelemek için [gelişmiş çok modlu kılavuzlara](https://docs.videodb.io/multimodal-guide-90) göz atın.

#### 🧩 Sorgu Dönüşümü (Query Transformation)

```python
from llama_index.llms.openai import OpenAI


def split_spoken_visual_query(query):
    transformation_prompt = """
    Aşağıdaki sorguyu iki ayrı parçaya bölün: biri konuşulan içerik için, diğeri görsel içerik için. Konuşulan içerik herhangi bir anlatım, diyalog veya sözlü açıklamaya atıfta bulunmalı; görsel içerik ise herhangi bir resim, video veya grafiksel temsile atıfta bulunmalıdır. Yanıtı kesinlikle şu şekilde formatlayın:\nKonuşulan (Spoken): <konuşulan_sorgu>\nGörsel (Visual): <görsel_sorgu>\n\nSorgu: {query}
    """
    prompt = transformation_prompt.format(query=query)
    response = OpenAI(model="gpt-4").complete(prompt)
    divided_query = response.text.strip().split("\n")
    spoken_query = divided_query[0].replace("Konuşulan (Spoken):", "").strip()
    scene_query = divided_query[1].replace("Görsel (Visual):", "").strip()
    return spoken_query, scene_query


query = "Bana şunları göster: 1.Kaza Sahnesi 2.Ülke çapındaki sınavlar hakkındaki tartışma "
spoken_query, scene_query = split_spoken_visual_query(query)
print("Konuşma erişicisi için sorgu: ", spoken_query)
print("Sahne erişicisi için sorgu: ", scene_query)
```

```text
Konuşma erişicisi için sorgu:  Ülke çapındaki sınavlar hakkındaki tartışma
Sahne erişicisi için sorgu:  Kaza Sahnesi
```

##### 🔎 Her modalite için ilgili düğümleri bulma

```python
from videodb import SearchType, IndexType


# Konuşma İndeksi için Erişici
spoken_retriever = VideoDBRetriever(
    collection=coll.id,
    video=video.id,
    search_type=SearchType.semantic,
    index_type=IndexType.spoken_word,
    score_threshold=0.1,
)


# Sahne İndeksi için Erişici
scene_retriever = VideoDBRetriever(
    collection=coll.id,
    video=video.id,
    search_type=SearchType.semantic,
    index_type=IndexType.scene,
    scene_index_id=index_id,
    score_threshold=0.1,
)


# Konuşma indeksi için ilgili düğümleri getir
nodes_spoken_index = spoken_retriever.retrieve(spoken_query)


# Sahne indeksi için ilgili düğümleri getir
nodes_scene_index = scene_retriever.retrieve(scene_query)
```

#### ️💬️ Sonucu Görüntüleme: Metin

```python
response_synthesizer = get_response_synthesizer()


response = response_synthesizer.synthesize(
    query, nodes=nodes_scene_index + nodes_spoken_index
)
print(response)
```

```text
İlk sahne, geceleri kentsel bir ortamda dinamik ve yoğun bir senaryoyu tasvir ediyor; muhtemelen kaçan bir figürün dahil olduğu bir motosiklet kovalamacasını içeriyor. İkinci sahne, büyük bir kamyonun yanında hareket halindeki karakterlerle dramatik bir kaçış veya kurtarma durumunu canlandırıyor. Ülke çapındaki sınavlarla ilgili tartışma, bir karakter ile annesi arasında sınav sonuçları ve ders çalışma üzerine geçen bir konuşmayı içeriyor.
```

#### 🎥 Sonucu Görüntüleme: Video Klibi

Her modaliteden, o modalite içindeki sorguyla ilgili (bu durumda anlamsal ve sahne/görsel) getirilmiş sonuçlarımız var.

Her düğümün metaverisinde, düğümün kapsadığı zaman aralığını temsil eden başlangıç ve bitiş alanları bulunur.

Bu sonuçları sentezlemenin birçok yolu vardır, şimdilik basit bir yöntem kullanacağız:

- `Birleşim (Union)`: Bu yöntem, her düğümdeki tüm zaman damgalarını alarak, bazı zaman damgaları yalnızca bir modalitede görünse bile her ilgili zamanı içeren kapsamlı bir liste oluşturur.

Diğer yollardan biri `Kesişim (Intersection)` olabilir:

- `Kesişim (Intersection)`: Bu yöntem yalnızca her düğümde mevcut olan zaman damgalarını içerir, bu da tüm modalitelerde evrensel olarak ilgili olan zamanların bulunduğu daha küçük bir liste ile sonuçlanır.

```python
from videodb import play_stream


def merge_intervals(intervals):
    if not intervals:
        return []
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for interval in intervals[1:]:
        if interval[0] <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], interval[1])
        else:
            merged.append(interval)
    return merged




# Her iki ilgili düğümden zaman damgalarını çıkar
results = [
    [node.metadata["start"], node.metadata["end"]]
    for node in nodes_spoken_index + nodes_scene_index
]
merged_results = merge_intervals(results)


# İlgili kliplerden oluşan bir akış oluşturmak için Videodb'yi kullanın
stream_link = video.generate_stream(merged_results)
play_stream(stream_link)
```

```text
'https://console.videodb.io/player?url=https://dseetlpshk2tb.cloudfront.net/v3/published/manifests/91b08b39-c72f-4e33-ad1c-47a2ea11ac17.m3u8'
```

## 🛠 Video Koleksiyonu için RAG Oluşturmada VideoDBRetriever Kullanımı (Using VideoDBRetriever to Build RAG for Collection of Videos)

---

### Koleksiyonumuza daha fazla video ekleme

```python
video_2 = coll.upload(url="https://www.youtube.com/watch?v=kMRX3EA68g4")
```

#### 🗣️ Konuşulan İçeriği İndeksleme

```python
video_2.index_spoken_words()
```

#### 📸 Sahneleri İndeksleme

```python
from videodb import SceneExtractionType


print("Videodaki Görsel içerik indeksleniyor...")


# Sahne içeriğini indeksle
index_id = video_2.index_scenes(
    extraction_type=SceneExtractionType.shot_based,
    extraction_config={"frame_count": 3},
    prompt="Sahneyi detaylıca tanımla",
)
video_2.get_scene_index(index_id)


print(f"Sahne İndeksi şu kimlikle başarılı: {index_id}")
```

```text
[Video(id=m-b6230808-307d-468a-af84-863b2c321f05, collection_id=c-4882e4a8-9812-4921-80ff-b77c9c4ab4e7, stream_url=https://dseetlpshk2tb.cloudfront.net/v3/published/manifests/528623c2-3a8e-4c84-8f05-4dd74f1a9977.m3u8, player_url=https://console.dev.videodb.io/player?url=https://dseetlpshk2tb.cloudfront.net/v3/published/manifests/528623c2-3a8e-4c84-8f05-4dd74f1a9977.m3u8, name=Death note - episode 1 (english dubbed) | HD, description=None, thumbnail_url=None, length=1366.006712),
 Video(id=m-f5b86106-4c28-43f1-b753-fa9b3f839dfe, collection_id=c-4882e4a8-9812-4921-80ff-b77c9c4ab4e7, stream_url=https://dseetlpshk2tb.cloudfront.net/v3/published/manifests/4273851a-46f3-4d57-bc1b-9012ce330da8.m3u8, player_url=https://console.dev.videodb.io/player?url=https://dseetlpshk2tb.cloudfront.net/v3/published/manifests/4273851a-46f3-4d57-bc1b-9012ce330da8.m3u8, name=Death note - episode 5 (english dubbed) | HD, description=None, thumbnail_url=None, length=1366.099592)]
```

#### 🧩 Sorgu Dönüşümü

```python
query = "Bana şunları göster: 1.Kaza Sahnesi 2.Kiara konuşuyor "
spoken_query, scene_query = split_spoken_visual_query(query)
print("Konuşma erişicisi için sorgu: ", spoken_query)
print("Sahne erişicisi için sorgu: ", scene_query)
```

```text
Konuşma erişicisi için sorgu:  Kiara konuşuyor
Sahne erişicisi için sorgu:  Kaza Sahnesini göster
```

#### 🔎 İlgili düğümleri bulma

```python
from videodb import SearchType, IndexType


# Konuşma İndeksi için Erişici
spoken_retriever = VideoDBRetriever(
    collection=coll.id,
    search_type=SearchType.semantic,
    index_type=IndexType.spoken_word,
    score_threshold=0.2,
)


# Sahne İndeksi için Erişici
scene_retriever = VideoDBRetriever(
    collection=coll.id,
    search_type=SearchType.semantic,
    index_type=IndexType.scene,
    score_threshold=0.2,
)


# Konuşma indeksi için ilgili düğümleri getir
nodes_spoken_index = spoken_retriever.retrieve(spoken_query)


# Sahne indeksi için ilgili düğümleri getir
nodes_scene_index = scene_retriever.retrieve(scene_query)
```

#### ️💬️ Sonucu Görüntüleme: Metin

```python
response_synthesizer = get_response_synthesizer()


response = response_synthesizer.synthesize(
    "Kiara ne hakkında konuşuyor? Ve bana kaza sahnesinden bahset",
    nodes=nodes_scene_index + nodes_spoken_index,
)
print(response)
```

```text
Kira, otobüsteki ajanla ilgili planları ve niyetleri hakkında konuşuyor. Kaza sahnesi, bir bireyin hasarlı bir arabanın yakınında acilen telefon görüşmesi yaptığı, kurbanın ise yerde hareketsiz yattığı üzücü bir anı yakalıyor. Kaotik sahne, arka plandaki bir otobüsü de içeriyor ve trajik olayın ciddiyetini vurguluyor.
```

#### 🎥 Sonucu Görüntüleme: Video Klibi

Birden fazla videoyu kapsayan bir kurgu akışıyla çalışırken, `VideoAsset` nesnelerinden oluşan bir `Zaman Çizelgesi (Timeline)` oluşturmamız ve ardından bunları derlememiz gerekir.

![](https://codaio.imgix.net/docs/_s5lUnUCIU/blobs/bl-n4vT_dFztl/e664f43dbd4da89c3a3bfc92e3224c8a188eb19d2d458bebe049e780f72506ca6b19421c7168205f7ad307187e73da60c73cdbb9a0ef3fec77cc711927ad26a29a92cd13691fa9375c231f1c006853bacf28e09b3bf0bbcb5f7b76462b354a180fb437ad?auto=format%2Ccompress&fit=max)

```python
from videodb import connect, play_stream
from videodb.timeline import Timeline
from videodb.asset import VideoAsset


# Yeni bir timeline nesnesi oluştur
timeline = Timeline(conn)


for node_obj in nodes_scene_index + nodes_spoken_index:
    node = node_obj.node


    # Her düğüm için bir Video varlığı oluştur
    node_asset = VideoAsset(
        asset_id=node.metadata["video_id"],
        start=node.metadata["start"],
        end=node.metadata["end"],
    )


    # Varlığı zaman çizelgesine ekle
    timeline.add_inline(node_asset)


# Derlenen zaman çizelgesi için akış üret
stream_url = timeline.generate_stream()
play_stream(stream_url)
```

```text
'https://console.videodb.io/player?url=https://dseetlpshk2tb.cloudfront.net/v3/published/manifests/2810827b-4d80-44af-a26b-ded2a7a586f6.m3u8'
```

## `VideoDBRetriever` Yapılandırması (Configuring VideoDBRetriever)

---

### ⚙️ Sadece bir Video için Erişici

Sadece o videoda arama yapmak için video nesnesinin `id` değerini geçebilirsiniz.

```python
VideoDBRetriever(video="video_id_miz")
```

### ⚙️ Bir Video Kümesi / Koleksiyonu için Erişici

Sadece o Koleksiyonda arama yapmak için Koleksiyonun `id` değerini geçebilirsiniz.

```python
VideoDBRetriever(collection="koleksiyon_id_miz")
```

### ⚙️ Farklı İndeks Türleri için Erişici

```python
from videodb import IndexType
konusulan_kelime = VideoDBRetriever(index_type=IndexType.spoken_word)


sahne_ericisi = VideoDBRetriever(index_type=IndexType.scene, scene_index_id="indeks_id_miz")
```

### ⚙️ Erişicinin Arama Türünü Yapılandırma

`search_type`, verilen sorguya karşı düğümleri getirmek için kullanılan arama yöntemini belirler.

```python
from videodb import SearchType, IndexType


anahtar_kelime_konusma_aramasi = VideoDBRetriever(
    search_type=SearchType.keyword,
    index_type=IndexType.spoken_word
)


anlamsal_sahne_aramasi = VideoDBRetriever(
    search_type=SearchType.semantic,
    index_type=IndexType.spoken_word
)
```

### ⚙️ Eşik parametrelerini yapılandırın

- `result_threshold`: Erişici tarafından döndürülen sonuç sayısı eşiğidir; varsayılan değer `5`tir.
- `score_threshold`: Yalnızca puanı `score_threshold` değerinden yüksek olan düğümler erişici tarafından döndürülür; varsayılan değer `0.2`dir.

```python
ozel_ericisi = VideoDBRetriever(result_threshold=2, score_threshold=0.5)
```

## ✨ İndeksleme ve Parçalama Yapılandırması (Configuring Indexing and Chunking)

---

Bu örnekte, video erişimi için VideoDB'nin İndekslemesini kullanıyoruz. Ancak, hem Transkript hem de Sahne Verilerini yükleme ve LlamaIndex kullanarak kendi indeksleme tekniklerinizi uygulama esnekliğine sahipsiniz.

Daha ayrıntılı rehberlik için bu [kılavuza](https://colab.research.google.com/github/run-llama/llama_index/blob/main/docs/examples/multi_modal/multi_modal_videorag_videodb.ipynb) başvurun.

## 🏃‍♂️ Sonraki Adımlar (Next Steps)

---

Bu kılavuzda, VideoDB, LlamaIndex ve OpenAI kullanarak Videolar için Basit Çok Modlu bir RAG oluşturduk.

Aşağıdaki gibi daha gelişmiş teknikleri dahil ederek işleme hattını optimize edebilirsiniz:

- Sorgu Dönüşümünü Optimize Edin
- Farklı modalitelerden getirilen düğümleri birleştirmek için daha fazla yöntem kullanın
- Bilgi Grafiği (Knowledge Graph) gibi farklı RAG işleme hatlarını deneyin

İlgili klibi oluşturmak için kullandığımız Programlanabilir Akış özelliği hakkında daha fazla bilgi edinmek için [Dinamik Video Akışı Kılavuzu](https://docs.videodb.io/dynamic-video-stream-guide-44)na göz atın.

Sahne İndeksi hakkında daha fazla bilgi edinmek için aşağıdaki kılavuzları inceleyin:

- [Hızlı Başlangıç Kılavuzu](https://github.com/video-db/videodb-cookbook/blob/main/quickstart/Scene%20Index%20QuickStart.ipynb)
- [Sahne Çıkarma Seçenekleri](https://github.com/video-db/videodb-cookbook/blob/main/guides/scene-index/playground_scene_extraction.ipynb)
- [Gelişmiş Görsel Arama](https://github.com/video-db/videodb-cookbook/blob/main/guides/scene-index/advanced_visual_search.ipynb)
- [Özel Açıklama İşleme Hattı](https://github.com/video-db/videodb-cookbook/blob/main/guides/scene-index/custom_annotations.ipynb)

## 👨‍👩‍👧‍👦 Destek ve Topluluk (Support & Community)

---

Herhangi bir sorunuz veya geri bildiriminiz varsa, bize ulaşmaktan çekinmeyin 🙌🏼

- [Discord](https://colab.research.google.com/corgiredirector?site=https%3A%2F%2Fdiscord.gg%2Fpy9P639jGz)
- [GitHub](https://github.com/video-db)
- [E-posta](mailto:ashu@videodb.io)
