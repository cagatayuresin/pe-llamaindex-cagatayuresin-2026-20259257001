# Her İndeksin Çalışma Mantığı

Bu kılavuz, diyagramlar eşliğinde her bir indeksin nasıl çalıştığını açıklamaktadır.

Bazı terminolojiler:

-   **Node (Düğüm)**: Bir Dökümandan (Document) alınan bir metin parçasına karşılık gelir. LlamaIndex, Döküman nesnelerini alır ve bunları dahili olarak Node nesnelerine ayrıştırır/parçalar.
-   **Yanıt Sentezleme (Response Synthesis)**: Getirilen Node verildiğinde bir yanıt sentezleyen modülümüz. [Farklı yanıt modlarını belirtme](/python/framework/module_guides/deploying/query_engine/response_modes) yöntemlerini inceleyebilirsiniz.

## Özet İndeksi (Summary Index - Eskiden List Index)

Özet indeksi, Node'ları basitçe ardışık bir zincir olarak saklar.

![Özet İndeksi](./../../_static/indices/list.png)

### Sorgulama

Sorgulama sırasında, başka bir sorgu parametresi belirtilmezse LlamaIndex, listedeki tüm Node'ları Yanıt Sentezleme modülümüze yükler.

![Özet İndeksi Sorgulama](./../../_static/indices/list_query.png)

Özet indeksi; en yakın k komşuyu getirecek embedding tabanlı bir sorgudan, aşağıda görüldüğü gibi bir anahtar kelime filtresi eklemeye kadar bir özet indeksini sorgulamanın sayısız yolunu sunar:

![Özet İndeksi Filtre Sorgulama](./../../_static/indices/list_filter_query.png)

## Vektör Deposu İndeksi (Vector Store Index)

Vektör deposu indeksi, her bir Node'u ve ilgili bir embedding'i bir [Vektör Deposunda (Vector Store)](/python/framework/community/integrations/vector_stores#using-a-vector-store-as-an-index) saklar.

![Vektör Deposu İndeksi](./../../_static/indices/vector_store.png)

### Sorgulama

Bir vektör deposu indeksini sorgulamak, en benzer k Node'un getirilmesini ve bunların Yanıt Sentezleme modülümüze aktarılmasını içerir.

![Vektör Deposu İndeksi Sorgulama](./../../_static/indices/vector_store_query.png)

## Ağaç İndeksi (Tree Index)

Ağaç indeksi, bir dizi Node'dan (bu ağaçta yaprak node'lar haline gelirler) hiyerarşik bir ağaç oluşturur.

![Ağaç İndeksi](./../../_static/indices/tree.png)

### Sorgulama

Bir ağaç indeksini sorgulamak, kök node'lardan aşağıya, yaprak node'lara doğru inmeyi içerir. Varsayılan olarak (`child_branch_factor=1`), bir sorgu bir üst node verildiğinde bir alt node seçer. Eğer `child_branch_factor=2` ise sorgu seviye başına iki alt node seçer.

![Ağaç İndeksi Sorgulama](./../../_static/indices/tree_query.png)

## Anahtar Kelime Tablosu İndeksi (Keyword Table Index)

Anahtar kelime tablosu indeksi, her bir Node'dan anahtar kelimeler çıkarır ve her bir anahtar kelimeden o anahtar kelimenin ilgili Node'larına bir eşleme (mapping) oluşturur.

![Anahtar Kelime Tablosu İndeksi](./../../_static/indices/keyword.png)

### Sorgulama

Sorgulama sırasında, sorgudan ilgili anahtar kelimeleri çıkarırız ve ilgili Node'ları getirmek için bunları önceden çıkarılmış Node anahtar kelimeleriyle eşleştiririz. Çıkarılan Node'lar Yanıt Sentezleme modülümüze aktarılır.

![Anahtar Kelime Tablosu İndeksi Sorgulama](./../../_static/indices/keyword_query.png)

## Özellik Grafiği İndeksi (Property Graph Index)

Özellik Grafiği İndeksi, öncelikle etiketli node'lar ve ilişkiler içeren bir bilgi grafiği oluşturarak çalışır. Bu grafiğin inşası; LLM'in istediği her şeyi çıkarmasına izin vermekten, katı bir şema kullanarak çıkarmaya ve hatta kendi çıkarma modüllerinizi uygulamanıza kadar son derece özelleştirilebilirdir.

İsteğe bağlı olarak, node'lar daha sonra getirilmek üzere gömülebilir (embedded).

Ayrıca oluşturma adımını atlayabilir ve Neo4j gibi bir entegrasyon kullanarak mevcut bir bilgi grafiğine bağlanabilirsiniz.

### Sorgulama

Bir Özellik Grafiği İndeksini sorgulamak da oldukça esnektir. Getirme işlemi, birkaç alt getirici (sub-retriever) kullanarak ve sonuçları birleştirerek çalışır. Varsayılan olarak; ilgili üçlüleri (triples) getirmek için anahtar kelime + eş anlamlı genişletmesi ve (grafiğiniz gömülüyse) vektör getirme yöntemi kullanılır.

Ayrıca, getirilen üçlülere ek olarak kaynak metni de dahil etmeyi seçebilirsiniz (LlamaIndex dışında oluşturulan grafikler için mevcut değildir).

Daha fazlasını [Özellik Grafikleri (Property Graphs) için tam kılavuzda](/python/framework/module_guides/indexing/lpg_index_guide) görebilirsiniz.