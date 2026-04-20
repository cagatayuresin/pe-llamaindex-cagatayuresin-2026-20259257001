# Delphic ile Tam Yığın (Full-Stack) LlamaIndex Web Uygulaması Oluşturma Rehberi

Bu kılavuz, LlamaIndex'i [Delphic](https://github.com/JSv4/Delphic) adı verilen üretime hazır bir web uygulaması başlangıç şablonuyla kullanma sürecinde size rehberlik etmeyi amaçlamaktadır. Buradaki tüm kod örnekleri [Delphic](https://github.com/JSv4/Delphic) deposunda mevcuttur.

## Ne İnşa Ediyoruz?

İşte Delphic'in kutudan çıktığı haliyle sunduğu işlevselliğin kısa bir demosu:

https://user-images.githubusercontent.com/5049984/233236432-aa4980b6-a510-42f3-887a-81485c9644e6.mp4

## Mimari Genel Bakış

Delphic, kullanıcıların kendi döküman koleksiyonlarını oluşturmalarına ve ardından bunları duyarlı bir ön yüzde sorgulamalarına olanak tanımak için LlamaIndex Python kütüphanesinden yararlanır.

Karmaşık Python işleme görevlerini yönetebilen (1), modern ve duyarlı bir ön yüz (2) ile üzerine ek işlevler inşa edilebilecek güvenli bir arka uç (3) sağlayan sağlam bir teknoloji yığını seçtik.

Temel kütüphaneler şunlardır:

1. [Django](https://www.djangoproject.com/)
2. [Django Channels](https://channels.readthedocs.io/en/stable/)
3. [Django Ninja](https://django-ninja.rest-framework.com/)
4. [Redis](https://redis.io/)
5. [Celery](https://docs.celeryq.dev/en/stable/getting-started/introduction.html)
6. [LlamaIndex](https://gpt-index.readthedocs.io/en/latest/)
7. [Langchain](https://python.langchain.com/en/latest/index.html)
8. [React](https://github.com/facebook/react)
9. Docker & Docker Compose

Süper kararlı Django web çerçevesi üzerine inşa edilen bu modern yığın sayesinde, başlangıç aşamasındaki Delphic uygulaması; kolaylaştırılmış bir geliştirici deneyimi, yerleşik kimlik doğrulama ve kullanıcı yönetimi, asenkron vektör deposu işleme ve duyarlı bir kullanıcı arayüzü için web-socket tabanlı sorgu bağlantılarına sahiptir. Ayrıca, ön ucumuz TypeScript ile yazılmıştır ve modern bir kullanıcı arayüzü için MUI React tabanlıdır.

## Sistem Gereksinimleri

Celery, Windows üzerinde çalışmaz. WSL (Windows Subsystem for Linux) ile dağıtılabilir olabilir ancak bunu yapılandırmak bu eğitimin kapsamı dışındadır. Bu nedenle, bu eğitimi yalnızca Linux veya OSX kullanıyorsanız takip etmenizi öneririz. Uygulamayı dağıtmak için Docker ve Docker Compose yüklü olmalıdır. Yerel geliştirme için node sürüm yöneticisi (nvm) gerekecektir.

## Django Arka Ucu (Backend)

### Proje Dizini Genel Bakışı

Delphic uygulaması, yaygın Django projesi kurallarına uyan yapılandırılmış bir arka uç dizin organizasyonuna sahiptir. Depo kök dizinindeki `./delphic` alt klasöründe ana klasörler şunlardır:

1. `contrib`: Django'nun yerleşik `contrib` uygulamalarına yapılan özel değişiklikleri veya eklemeleri içerir.
2. `indexes`: Döküman indeksleme ve LLM entegrasyonu ile ilgili temel işlevleri içerir. Şunları kapsar:
    - `admin.py`: Uygulama için Django yönetim paneli yapılandırması.
    - `apps.py`: Uygulama yapılandırması.
    - `models.py`: Uygulamanın veritabanı modellerini içerir.
    - `migrations`: Veritabanı şeması geçişlerini (migrations) içeren dizin.
    - `signals.py`: Uygulama için sinyalleri tanımlar.
    - `tests.py`: Uygulama için birim testleri.
3. `tasks`: Celery kullanarak asenkron işleme için görevleri içerir. `index_tasks.py` dosyası vektör indeksleri oluşturma görevlerini içerir.
4. `users`: Kullanıcı yönetimine ayrılmış dizindir.
5. `utils`: Uygulama genelinde kullanılan özel depolama arka uçları, yol yardımcıları ve koleksiyonla ilgili yardımcılar gibi yardımcı modülleri ve fonksiyonları içerir.

### Veritabanı Modelleri

Delphic uygulamasının iki temel modeli vardır: `Document` ve `Collection`. Bu modeller, dökümanları LLM kullanarak indekslerken ve sorgularken uygulamanın ele aldığı merkezi varlıkları temsil eder. Bunlar [`./delphic/indexes/models.py`](https://github.com/JSv4/Delphic/blob/main/delphic/indexes/models.py) dosyasında tanımlanmıştır.

1. `Collection`:
    - `api_key`: Bir koleksiyonu bir API anahtarına bağlayan yabancı anahtar (foreign key).
    - `title`: Koleksiyon için bir başlık sağlayan karakter alanı.
    - `description`: Koleksiyonun açıklamasını sağlayan metin alanı.
    - `status`: `CollectionStatus` numaralandırmasını kullanarak koleksiyonun işleme durumunu saklayan karakter alanı.
    - `created`: Koleksiyonun ne zaman oluşturulduğunu kaydeden tarih-saat alanı.
    - `modified`: Koleksiyonun son değiştirilme zamanını kaydeden tarih-saat alanı.
    - `model`: Koleksiyonla ilişkili modeli saklayan bir dosya alanı.
    - `processing`: Koleksiyonun şu anda işlenip işlenmediğini gösteren bir boolean alan.

2. `Document`:
    - `collection`: Bir dökümanı bir koleksiyona bağlayan yabancı anahtar. Bu, dökümanlar ve koleksiyonlar arasındaki ilişkiyi temsil eder.
    - `file`: Yüklenen döküman dosyasını saklayan bir dosya alanı.
    - `description`: Dökümanın açıklamasını sağlayan metin alanı.
    - `created`: Dökümanın ne zaman oluşturulduğunu kaydeden tarih-saat alanı.
    - `modified`: Dökümanın son değiştirilme zamanını kaydeden tarih-saat alanı.

Bu modeller, LlamaIndex ile döküman koleksiyonları ve onlardan oluşturulan indeksler için sağlam bir temel sağlar.

### Django Ninja API

Django Ninja, Django ve Python 3.7+ tip ipuçları (type hints) ile API'lar oluşturmak için kullanılan bir web çerçevesidir. Girdi doğrulamayı, serileştirmeyi ve dökümantasyonu otomatik olarak oluşturmak için Python'un tip ipuçlarından yararlanarak API uç noktalarını tanımlamanın basit, sezgisel ve etkileyici bir yolunu sunar.

Delphic deposunda, [`./config/api/endpoints.py`](https://github.com/JSv4/Delphic/blob/main/config/api/endpoints.py) dosyası API rotalarını ve mantığını içerir. Şimdi, `endpoints.py` dosyasındaki her bir uç noktanın amacını kısaca ele alalım:

1. `/heartbeat`: API'ın çalışır durumda olup olmadığını kontrol etmek için basit bir GET uç noktası. API'a erişilebiliyorsa `True` döner. Bu, konteynerinizin çalışıp çalışmadığını sorgulamak isteyen Kubernetes kurulumları için yararlıdır.

2. `/collections/create`: Yeni bir `Collection` oluşturmak için kullanılan bir POST uç noktası. `title`, `description` ve bir `files` listesi gibi form parametrelerini kabul eder. Her dosya için yeni bir `Collection` ve `Document` örnekleri oluşturur ve bir indeks oluşturmak için bir Celery görevi planlar.

```python
@collections_router.post("/create")
async def create_collection(
    request,
    title: str = Form(...),
    description: str = Form(...),
    files: list[UploadedFile] = File(...),
):
    key = None if getattr(request, "auth", None) is None else request.auth
    if key is not None:
        key = await key

    collection_instance = Collection(
        api_key=key,
        title=title,
        description=description,
        status=CollectionStatusEnum.QUEUED,
    )

    await sync_to_async(collection_instance.save)()

    for uploaded_file in files:
        doc_data = uploaded_file.file.read()
        doc_file = ContentFile(doc_data, uploaded_file.name)
        document = Document(collection=collection_instance, file=doc_file)
        await sync_to_async(document.save)()

    create_index.si(collection_instance.id).apply_async()

    return await sync_to_async(CollectionModelSchema)(...)
```

3. `/collections/query`: LLM kullanarak bir döküman koleksiyonunu sorgulamak için bir POST uç noktası. `collection_id` ve `query_str` içeren bir JSON veri yükü kabul eder ve koleksiyonu sorgulayarak oluşturulan bir yanıt döndürür. Sohbet arayüzümüzde aslında bu uç noktayı kullanmıyoruz (bir websocket kullanıyoruz - aşağıya bakın), ancak belirli bir koleksiyonu sorgulamak için bu REST uç noktasına entegre olacak bir uygulama inşa edebilirsiniz.

```python
@collections_router.post(
    "/query",
    response=CollectionQueryOutput,
    summary="Döküman koleksiyonuna bir soru sorun",
)
def query_collection_view(
    request: HttpRequest, query_input: CollectionQueryInput
):
    collection_id = query_input.collection_id
    query_str = query_input.query_str
    response = query_collection(collection_id, query_str)
    return {"response": response}
```

4. `/collections/available`: Kullanıcının API anahtarıyla oluşturulan tüm koleksiyonların listesini döndüren bir GET uç noktası. Çıktı, `CollectionModelSchema` kullanılarak serileştirilir.

```python
@collections_router.get(
    "/available",
    response=list[CollectionModelSchema],
    summary="Benim api_key değerimle oluşturulan tüm koleksiyonların listesini getir",
)
async def get_my_collections_view(request: HttpRequest):
    key = None if getattr(request, "auth", None) is None else request.auth
    if key is not None:
        key = await key

    collections = Collection.objects.filter(api_key=key)

    return [{...} async for collection in collections]
```

5. `/collections/{collection_id}/add_file`: Mevcut bir koleksiyona dosya eklemek için kullanılan bir POST uç noktası. Bir `collection_id` yol parametresini ve `file` ile `description` gibi form parametrelerini kabul eder. Dosyayı, belirtilen koleksiyonla ilişkilendirilmiş bir `Document` örneği olarak ekler.

```python
@collections_router.post(
    "/{collection_id}/add_file", summary="Koleksiyona dosya ekle"
)
async def add_file_to_collection(
    request,
    collection_id: int,
    file: UploadedFile = File(...),
    description: str = Form(...),
):
    collection = await sync_to_async(Collection.objects.get)(id=collection_id)
```

### Web Sockets'e Giriş

WebSockets, tek ve uzun ömürlü bir bağlantı üzerinden istemci ile sunucu arasında çift yönlü (bidirectional) ve tam çift yönlü (full-duplex) iletişim sağlayan bir iletişim protokolüdür. WebSocket protokolü, HTTP ve HTTPS ile aynı portlar (sırasıyla 80 ve 443 numaralı portlar) üzerinden çalışacak şekilde tasarlanmıştır ve bir bağlantı kurmak için benzer bir el sıkışma (handshake) süreci kullanır. Bağlantı kurulduktan sonra; veriler, geleneksel HTTP isteklerinin aksine, her seferinde bağlantıyı yeniden kurmaya gerek kalmadan "frame"ler olarak her iki yönde de gönderilebilir.

Özellikle belleğe yüklenmesi uzun süren ancak yüklendikten sonra hızlı çalışan kodlarla çalışırken WebSocket kullanmanın birkaç nedeni vardır:

1. **Performans**: WebSocket'ler, her istek için birden fazla bağlantı açma ve kapama ile ilişkili yükü ortadan kaldırarak gecikmeyi azaltır.
2. **Verimlilik**: WebSocket'ler, sürekli sorgulama (polling) gerektirmeden gerçek zamanlı iletişime olanak tanıyarak kaynakların daha verimli kullanılmasını ve daha iyi yanıt verme sürelerini sağlar.
3. **Ölçeklenebilirlik**: WebSocket'ler çok sayıda eşzamanlı bağlantıyı yönetebilir; bu da onu yüksek eşzamanlılık gerektiren uygulamalar için ideal hale getirir.

Delphic uygulaması durumunda, LLM'lerin belleğe yüklenmesi maliyetli olabileceğinden WebSocket kullanmak mantıklıdır. Bir WebSocket bağlantısı kurularak, LLM bellekte yüklü kalabilir ve modelin her seferinde yeniden yüklenmesine gerek kalmadan sonraki isteklerin hızlı bir şekilde işlenmesine olanak tanır.

ASGI yapılandırma dosyası [`./config/asgi.py`](https://github.com/JSv4/Delphic/blob/main/config/asgi.py), gelen bağlantıların nasıl işleneceğini tanımlar ve bağlantıları protokol türlerine göre yönlendirmek için Django Channels `ProtocolTypeRouter` kullanır. Bu durumda iki protokol türümüz var: "http" ve "websocket".

"http" protokol türü, HTTP isteklerini işlemek için standart Django ASGI uygulamasını kullanırken; "websocket" protokol türü, WebSocket bağlantılarını doğrulamak için özel bir `TokenAuthMiddleware` kullanır. `TokenAuthMiddleware` içindeki `URLRouter`, döküman koleksiyonlarını sorgulamayla ilgili WebSocket bağlantılarını yönetmekten sorumlu olan `CollectionQueryConsumer` için bir URL kalıbı tanımlar.

```python
application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": TokenAuthMiddleware(
            URLRouter(
                [
                    re_path(
                        r"ws/collections/(?P<collection_id>\w+)/query/$",
                        CollectionQueryConsumer.as_asgi(),
                    ),
                ]
            )
        ),
    }
)
```

Bu yapılandırma, istemcilerin döküman koleksiyonlarını LLM kullanarak verimli bir şekilde sorgulamak için Delphic uygulamasıyla WebSocket bağlantıları kurmasına olanak tanır ve her istek için modellerin yeniden yüklenmesine gerek kalmaz.

### Websocket İşleyicisi (Handler)

[`config/api/websockets/queries.py`](https://github.com/JSv4/Delphic/blob/main/config/api/websockets/queries.py) dosyasındaki `CollectionQueryConsumer` sınıfı, döküman koleksiyonlarını sorgulamayla ilgili WebSocket bağlantılarını yönetmekten sorumludur. Django Channels tarafından sağlanan `AsyncWebsocketConsumer` sınıfından miras alır.

`CollectionQueryConsumer` sınıfı üç ana metoda sahiptir:

1. `connect`: WebSocket bağlantı sürecinin bir parçası olarak el sıkışırken çağrılır.
2. `disconnect`: WebSocket herhangi bir nedenle kapandığında çağrılır.
3. `receive`: Sunucu WebSocket üzerinden bir mesaj aldığında çağrılır.

#### Websocket connect dinleyicisi

`connect` metodu bağlantıyı kurmaktan, koleksiyon ID'sini bağlantı yolundan çıkarmaktan, koleksiyon modelini yüklemekten ve bağlantıyı kabul etmekten sorumludur.

```python
async def connect(self):
    try:
        self.collection_id = extract_connection_id(self.scope["path"])
        self.index = await load_collection_model(self.collection_id)
        await self.accept()

    except ValueError as e:
        await self.accept()
        await self.close(code=4000)
    except Exception as e:
        pass
```

#### Websocket disconnect dinleyicisi

WebSocket kapatıldığında yapılması gereken ek bir işlem olmadığı için `disconnect` metodu bu durumda boştur.

#### Websocket receive dinleyicisi

`receive` metodu, WebSocket'ten gelen mesajları işlemekten sorumludur. Gelen mesajı alır, kodunu çözer ve ardından sağlanan sorguyu kullanarak yüklü koleksiyon modelini sorgular. Yanıt daha sonra bir markdown dizesi olarak formatlanır ve WebSocket bağlantısı üzerinden istemciye geri gönderilir.

```python
async def receive(self, text_data):
    text_data_json = json.loads(text_data)

    if self.index is not None:
        query_str = text_data_json["query"]
        modified_query_str = f"Lütfen bu isteğe güzel formatlanmış bir markdown dizesi döndürün:\n\n{query_str}"
        query_engine = self.index.as_query_engine()
        response = query_engine.query(modified_query_str)

        markdown_response = f"## Yanıt\n\n{response}\n\n"
        if response.source_nodes:
            markdown_sources = (
                f"## Kaynaklar\n\n{response.get_formatted_sources()}"
            )
        else:
            markdown_sources = ""

        formatted_response = f"{markdown_response}{markdown_sources}"

        await self.send(json.dumps({"response": formatted_response}, indent=4))
    else:
        await self.send(
            json.dumps(
                {"error": "Bu bağlantı için yüklü bir indeks bulunamadı."}, indent=4
            )
        )
```

Koleksiyon modelini yüklemek için [`delphic/utils/collections.py`](https://github.com/JSv4/Delphic/blob/main/delphic/utils/collections.py) dosyasında bulunan `load_collection_model` fonksiyonu kullanılır. Bu fonksiyon; verilen ID'ye sahip koleksiyon nesnesini getirir, koleksiyon modeli için bir JSON dosyası olup olmadığını kontrol eder ve yoksa bir tane oluşturur. Ardından, önbellek dosyasını kullanarak `VectorStoreIndex`'i yüklemeden önce `LLM` ve `Settings` ayarlarını yapar.

```python
from llama_index.core import Settings


async def load_collection_model(collection_id: str | int) -> VectorStoreIndex:
    """
    Koleksiyon modelini önbellekten veya veritabanından yükler ve indeksi döndürür.

    Args:
        collection_id (Union[str, int]): Koleksiyon model örneğinin ID'si.

    Returns:
        VectorStoreIndex: Yüklenen indeks.

    Bu fonksiyon şu adımları gerçekleştirir:
    1. Verilen collection_id ile Koleksiyon nesnesini getirir.
    2. '/cache/model_{collection_id}.json' adında bir JSON dosyası olup olmadığını kontrol eder.
    3. JSON dosyası mevcut değilse, JSON'ı Koleksiyon.model FileField'ından yükler ve 
       '/cache/model_{collection_id}.json' olarak kaydeder.
    4. cache_file_path ile VectorStoreIndex.load_from_disk metodunu çağırır.
    """
    # Koleksiyon nesnesini getir
    collection = await Collection.objects.aget(id=collection_id)
    logger.info(f"load_collection_model() - koleksiyon {collection_id} yüklendi")

    # Bir model olduğundan emin ol
    if collection.model.name:
        logger.info("load_collection_model() - Yerel json indeks dosyası kuruluyor")

        # JSON dosyasının varlığını kontrol et
        cache_dir = Path(settings.BASE_DIR) / "cache"
        cache_file_path = cache_dir / f"model_{collection_id}.json"
        if not cache_file_path.exists():
            cache_dir.mkdir(parents=True, exist_ok=True)
            with collection.model.open("rb") as model_file:
                with cache_file_path.open(
                    "w+", encoding="utf-8"
                ) as cache_file:
                    cache_file.write(model_file.read().decode("utf-8"))

        # LLM tanımla
        logger.info(
            f"load_collection_model() - Settings, {settings.MAX_TOKENS} token ve "
            f"{settings.MODEL_NAME} modeliyle kuruluyor"
        )
        Settings.llm = OpenAI(
            temperature=0, model="gpt-3.5-turbo", max_tokens=512
        )

        # VectorStoreIndex.load_from_disk çağrısı yap
        logger.info("load_collection_model() - Llama index yükleniyor")
        index = VectorStoreIndex.load_from_disk(
            cache_file_path,
        )
        logger.info(
            "load_collection_model() - Llamaindex yüklendi ve sorgu için hazır..."
        )

    else:
        logger.error(
            f"load_collection_model() - koleksiyon {collection_id}'in modeli yok!"
        )
        raise ValueError("Bu koleksiyon için bir model mevcut değil!")

    return index
```

## React Ön Yüzü (Frontend)

### Genel Bakış

Delphic projesinin ön ucu için TypeScript, React ve Material-UI (MUI) kullanmayı birkaç nedenden dolayı tercih ettik. İlk olarak; en popüler bileşen kütüphanesi (MUI) ve en popüler ön uç çerçevesi (React) olduğundan, bu seçim projeyi devasa bir geliştirici topluluğu için erişilebilir kılıyor. İkinci olarak; React, sanal DOM (virtual DOM) formunda değerli soyutlamalar sunan, görece kararlı ve bize göre öğrenmesi oldukça kolay olan bir çerçevedir.

### Ön Yüz Proje Yapısı

Ön uç, reponun [`/frontend`](https://github.com/JSv4/Delphic/tree/main/frontend) dizininde, React ile ilgili bileşenler ise `/frontend/src` dizininde bulunabilir. `frontend` dizininde bir Dockerfile ve ön uç web sunucumuz olan Nginx'i yapılandırmakla ilgili birkaç klasör ve dosya olduğunu fark edeceksiniz.

`/frontend/src/App.tsx` dosyası uygulamanın giriş noktasıdır. Giriş formu, çekmece düzeni (drawer layout) ve koleksiyon oluşturma modalı gibi ana bileşenleri tanımlar. Ana bileşenler; kullanıcının oturum açıp açmadığına ve bir kimlik doğrulama tokenine sahip olup olmadığına bağlı olarak koşullu olarak oluşturulur.

`DrawerLayout2` bileşeni `DrawerLayout2.tsx` dosyasında tanımlanmıştır. Bu bileşen, uygulamanın düzenini yönetir; navigasyon ve ana içerik alanlarını sağlar.

Uygulama nispeten basit olduğu için, Redux gibi karmaşık bir durum yönetimi (state management) çözümü kullanmadan sadece React'ın `useState` hook'larını kullanarak süreci yürütebiliriz.

### Arka Uçtan Koleksiyonları Almak

Oturum açmış kullanıcıya açık olan koleksiyonlar, `DrawerLayout2` bileşeninde alınır ve görüntülenir. Süreç şu adımlara ayrılabilir:

1. Durum değişkenlerini başlatma:

```tsx
const [collections, setCollections] = useState<CollectionModelSchema[]>([]);
const [loading, setLoading] = useState(true);
```

Burada; koleksiyon listesini saklamak için `collections` ve koleksiyonların getirilip getirilmediğini takip etmek için `loading` olmak üzere iki durum değişkeni başlatıyoruz.

2. `fetchCollections()` fonksiyonu ile oturum açmış kullanıcı için koleksiyonlar getirilir:

```tsx
const fetchCollections = async () => {
  try {
    const accessToken = localStorage.getItem("accessToken");
    if (accessToken) {
      const response = await getMyCollections(accessToken);
      setCollections(response.data);
    }
  } catch (error) {
    console.error(error);
  } finally {
    setLoading(false);
  }
};
```

`fetchCollections` fonksiyonu, kullanıcının erişim tokeniyle `getMyCollections` API fonksiyonunu çağırarak oturum açmış kullanıcı için koleksiyonları alır. Ardından `collections` durumunu alınan verilerle günceller ve getirmenin tamamlandığını belirtmek için `loading` durumunu `false` yapar.

### Koleksiyonları Görüntüleme

En güncel koleksiyonlar çekmecede şu şekilde görüntülenir:

```tsx
<List>
  {collections.map((collection) => (
    <div key={collection.id}>
      <ListItem disablePadding>
        <ListItemButton
          disabled={
            collection.status !== CollectionStatus.COMPLETE ||
            !collection.has_model
          }
          onClick={() => handleCollectionClick(collection)}
          selected={
            selectedCollection &&
            selectedCollection.id === collection.id
          }
        >
          <ListItemText primary={collection.title} />
          {collection.status === CollectionStatus.RUNNING ? (
            <CircularProgress
              size={24}
              style={{ position: "absolute", right: 16 }}
            />
          ) : null}
        </ListItemButton>
      </ListItem>
    </div>
  ))}
</List>
```

Bir koleksiyonun `ListItemButton` bileşeninin `disabled` özelliğinin; koleksiyon durumunun `CollectionStatus.COMPLETE` olmamasına veya koleksiyonun bir modeli olmamasına (`!collection.has_model`) göre ayarlandığını fark edeceksiniz. Eğer bu koşullardan biri doğruysa buton devre dışı bırakılır ve kullanıcıların tamamlanmamış veya modelsiz bir koleksiyonu seçmesi engellenir. `CollectionStatus` değerinin `RUNNING` olduğu durumlarda buton üzerinde bir yükleme çarkı da gösteriyoruz.

Ayrı bir `useEffect` hook'u içinde, `collections` durumundaki herhangi bir koleksiyonun durumunun `CollectionStatus.RUNNING` veya `CollectionStatus.QUEUED` olup olmadığını kontrol ediyoruz. Eğer öyleyse, koleksiyon durumlarını güncellemek için `fetchCollections` fonksiyonunu her 15 saniyede bir (15.000 milisaniye) çağırmak üzere bir aralık (interval) kuruyoruz. Bu şekilde, uygulama periyodik olarak tamamlanan koleksiyonları kontrol eder ve işlem tamamlandığında kullanıcı arayüzü buna göre güncellenir.

```tsx
useEffect(() => {
  let interval: NodeJS.Timeout;
  if (
    collections.some(
      (collection) =>
        collection.status === CollectionStatus.RUNNING ||
        collection.status === CollectionStatus.QUEUED
    )
  ) {
    interval = setInterval(() => {
      fetchCollections();
    }, 15000);
  }
  return () => clearInterval(interval);
}, [collections]);
```

### Sohbet Görünümü (Chat View) Bileşeni

`frontend/src/chat/ChatView.tsx` dosyasındaki `ChatView` bileşeni, bir kullanıcının bir koleksiyonla etkileşime girmesi için bir sohbet arayüzünü yönetmekten ve görüntülemekten sorumludur. Bileşen, sunucuyla gerçek zamanlı iletişim kurmak (mesaj göndermek ve almak) için bir WebSocket bağlantısı kurar.

`ChatView` bileşeninin temel özellikleri şunlardır:

1. Sunucu ile WebSocket bağlantısını kurmak ve yönetmek.
2. Kullanıcıdan ve sunucudan gelen mesajları sohbet formatında görüntülemek.
3. Sunucuya mesaj göndermek için kullanıcı girişini işlemek.
4. Sunucudan alınan mesajlara göre mesaj durumunu ve kullanıcı arayüzünü güncellemek.
5. Mesajların yüklenmesi, sunucuya bağlanılması veya bir koleksiyon yüklenirken hatalarla karşılaşılması gibi durumları ve bağlantı durumunu görüntülemek.

Tüm bunlar, kullanıcıların seçtikleri koleksiyonla oldukça pürüzsüz ve düşük gecikmeli bir deneyimle etkileşime girmesini sağlar.

#### Sohbet Websocket İstemcisi

`ChatView` bileşenindeki WebSocket bağlantısı, istemci ile sunucu arasında gerçek zamanlı iletişim kurmak için kullanılır. WebSocket bağlantısı `ChatView` bileşeninde şu şekilde kurulur ve yönetilir:

Öncelikle WebSocket referansını başlatmak istiyoruz:

`const websocket = useRef<WebSocket | null>(null);`

`useRef` kullanılarak, iletişim için kullanılacak WebSocket nesnesini tutan bir `websocket` referansı oluşturulur. `useRef`, React'ta render'lar arasında kalıcı olan değişebilir bir referans nesnesi oluşturmanıza olanak tanıyan bir hook'tur. Özellikle WebSocket bağlantısı gibi değişebilir bir nesneye referans tutmanız gerektiğinde, gereksiz yeniden render'lara neden olmadan oldukça kullanışlıdır.

`ChatView` bileşeninde WebSocket bağlantısının bileşenin ömrü boyunca kurulması ve sürdürülmesi gerekir ve bağlantı durumu değiştiğinde yeniden render tetiklememelidir. `useRef` kullanarak WebSocket bağlantısının bir referans olarak tutulmasını sağlarsınız ve bileşen yalnızca mesajların güncellenmesi veya hataların görüntülenmesi gibi gerçek durum değişiklikleri olduğunda yeniden render edilir.

`setupWebsocket` fonksiyonu, WebSocket bağlantısını kurmaktan ve farklı WebSocket olaylarını yönetmek için olay işleyicileri (event handlers) ayarlamaktan sorumludur.

Genel olarak `setupWebsocket` fonksiyonu şu şekildedir:

```tsx
const setupWebsocket = () => {
  setConnecting(true);
  // Burada, seçilen koleksiyonun ID'sini ve kullanıcının kimlik doğrulama tokenini 
  // içeren belirtilen URL kullanılarak yeni bir WebSocket nesnesi oluşturulur.

  websocket.current = new WebSocket(
    `ws://localhost:8000/ws/collections/${selectedCollection.id}/query/?token=${authToken}`
  );

  websocket.current.onopen = (event) => {
    //...
  };

  websocket.current.onmessage = (event) => {
    //...
  };

  websocket.current.onclose = (event) => {
    //...
  };

  websocket.current.onerror = (event) => {
    //...
  };

  return () => {
    websocket.current?.close();
  };
};
```

Birçok yerde, web socket istemcisinden gelen bilgilere dayanarak GUI güncellemelerini tetiklediğimizi fark edin.

Bileşen ilk açıldığında ve bir bağlantı kurmaya çalıştığımızda `onopen` dinleyicisi tetiklenir. Geri çağırma (callback) işlevinde, bileşen bağlantının kurulduğunu yansıtacak şekilde durumları günceller, önceki hatalar temizlenir ve yanıt bekleyen mesaj kalmaz:

```tsx
websocket.current.onopen = (event) => {
  setError(false);
  setConnecting(false);
  setAwaitingMessage(false);

  console.log("WebSocket bağlandı:", event);
};
```

`onmessage`, WebSocket bağlantısı üzerinden sunucudan yeni bir mesaj alındığında tetiklenir. Geri çağırmada, alınan veriler ayrıştırılır ve `messages` durumu sunucudan gelen yeni mesajla güncellenir:

```tsx
websocket.current.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log("WebSocket mesajı alındı:", data);
  setAwaitingMessage(false);

  if (data.response) {
    // Mesaj durumunu sunucudan gelen yeni mesajla güncelle
    setMessages((prevMessages) => [
      ...prevMessages,
      {
        sender_id: "server",
        message: data.response,
        timestamp: new Date().toLocaleTimeString(),
      },
    ]);
  }
};
```

`onclose`, WebSocket bağlantısı kapatıldığında tetiklenir. Geri çağırmada, bileşen belirli bir kapanış kodunu (`4000`) kontrol ederek bir uyarı ekranı (toast) gösterir ve bileşen durumlarını buna göre günceller. Ayrıca kapanış olayını loglar:

```tsx
websocket.current.onclose = (event) => {
  if (event.code === 4000) {
    toast.warning(
      "Seçilen koleksiyonun modeli mevcut değil. Doğru şekilde oluşturuldu mu?"
    );
    setError(true);
    setConnecting(false);
    setAwaitingMessage(false);
  }
  console.log("WebSocket kapatıldı:", event);
};
```

Son olarak `onerror`, WebSocket bağlantısında bir hata oluştuğunda tetiklenir. Geri çağırmada bileşen, hatayı yansıtacak şekilde durumları günceller ve hata olayını loglar:

```tsx
websocket.current.onerror = (event) => {
  setError(true);
  setConnecting(false);
  setAwaitingMessage(false);

  console.error("WebSocket hatası:", event);
};
```

#### Sohbet Mesajlarımızı Oluşturma (Rendering)

`ChatView` bileşeninde düzen, CSS stilleri ve Material-UI bileşenleri kullanılarak belirlenir. Ana düzen; `flex` görüntüleme ve sütun yönelimli bir `flexDirection` içeren bir konteynerden oluşur. Bu, konteyner içindeki içeriğin dikey olarak düzenlenmesini sağlar.

Düzende üç ana bölüm vardır:

1. Sohbet mesajları alanı: Bu bölüm mevcut alanın çoğunu kaplar ve kullanıcı ile sunucu arasında gidip gelen mesajların listesini görüntüler. İçerik mevcut alanı aştığında kaydırmaya olanak tanıyan bir `overflow-y: auto` özelliğine sahiptir. Mesajlar, her mesaj için `ChatMessage` bileşeni ve bir sunucu yanıtı beklenirken yükleme durumunu göstermek için `ChatMessageLoading` bileşeni kullanılarak oluşturulur.
2. Ayırıcı (Divider): Sohbet mesajları alanını giriş alanından ayırmak için bir Material-UI `Divider` bileşeni kullanılır ve iki bölüm arasında net bir görsel ayrım oluşturur.
3. Giriş alanı: Bu bölüm en altta bulunur ve kullanıcının mesaj yazıp göndermesine olanak tanır. Material-UI'dan maksimum 2 satırlık çok satırlı girişi kabul edecek şekilde ayarlanmış bir `TextField` bileşeni içerir. Giriş alanı ayrıca mesajı göndermek için bir `Button` bileşeni içerir. Kullanıcı mesajı göndermek için ya "Gönder" butonuna tıklayabilir ya da klavyesindeki "Enter" tuşuna basabilir.

`ChatView` bileşeninde kabul edilen kullanıcı girişleri, kullanıcının `TextField` alanına yazdığı metin mesajlarıdır. Bileşen bu metin girişlerini işler ve WebSocket bağlantısı üzerinden sunucuya gönderir.

## Dağıtım (Deployment)

### Ön Gereksinimler

Uygulamayı dağıtmak için Docker ve Docker Compose yüklü olması gerekir. Ubuntu veya başka bir yaygın Linux dağıtımı kullanıyorsanız; DigitalOcean'ın [harika bir Docker eğitimi](https://www.digitalocean.com/community/tutorial_collections/how-to-install-and-use-docker) ve takip edebileceğiniz [Docker Compose için başka bir harika eğitimi](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04) mevcuttur. Eğer bunlar sizin için uygun değilse, [resmi Docker dökümantasyonunu](https://docs.docker.com/engine/install/) deneyin.

### İnşa Etme ve Dağıtma

Proje `django-cookiecutter` tabanlıdır; bir VM üzerinde dağıtılması ve belirli bir alan adı için HTTPs trafiğine hizmet verecek şekilde yapılandırılması oldukça kolaydır. Ancak yapılandırma biraz zahmetlidir; bu projenin kendisinden dolayı değil, sadece sertifikalarınızı, DNS ayarlarınızı vb. yapılandırmak karmaşık bir konu olduğu içindir.

Bu kılavuzun amaçları doğrultusunda, şimdilik sadece yerel olarak çalıştıralım. Belki ileride üretim dağıtımı üzerine bir döküman yayınlarız. Bu sırada, başlangıç için [Django Cookiecutter projesi dökümanlarına](https://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html) göz atın.

Bu kılavuz, amacınızın uygulamayı kullanım için ayağa kaldırmak olduğunu varsayar. Eğer geliştirme yapmak istiyorsanız, muhtemelen compose yığınını `--profiles fullstack` bayrağıyla başlatmak yerine, React ön ucunu node geliştirme sunucusunu kullanarak başlatmak isteyeceksiniz.

Dağıtım için önce depoyu kopyalayın:

```bash
git clone https://github.com/kullaniciadinız/delphic.git
```

Proje dizinine girin:

```bash
cd delphic
```

Örnek ortam (environment) dosyalarını kopyalayın:

```bash
mkdir -p ./.envs/.local/
cp -a ./docs/sample_envs/local/.frontend ./frontend
cp -a ./docs/sample_envs/local/.django ./.envs/.local
cp -a ./docs/sample_envs/local/.postgres ./.envs/.local
```

`.django` ve `.postgres` yapılandırma dosyalarını; OpenAI API anahtarınızı içerecek ve veritabanı kullanıcınız için benzersiz bir şifre ayarlayacak şekilde düzenleyin. Ayrıca `.django` dosyasında yanıt token limitini ayarlayabilir veya hangi OpenAI modelini kullanmak istediğinizi seçebilirsiniz. Erişime yetkiniz olduğunu varsayarsak GPT-4 desteklenmektedir.

Docker compose yığınını `--profiles fullstack` bayrağıyla inşa edin:

```bash
sudo docker-compose --profiles fullstack -f local.yml build
```

`fullstack` bayrağı; compose'a `frontend` klasöründen bir Docker konteyneri inşa etmesini söyler ve bu konteyner gereken tüm arka uç konteynerleriyle birlikte başlatılır. Ancak bir üretim React konteyneri inşa etmek uzun zaman alır, bu yüzden bu şekilde geliştirme yapmanızı önermiyoruz. Geliştirme ortamı kurulum talimatları için [proje readme.md dosyasındaki talimatları](https://github.com/JSv4/Delphic#development) takip edin.

Son olarak uygulamayı ayağa kaldırın:

```bash
sudo docker-compose -f local.yml up
```

Şimdi, ön ucu görmek ve Delphic uygulamasını yerel olarak kullanmak için tarayıcınızdan `localhost:3000` adresini ziyaret edin.

## Uygulamayı Kullanma

### Kullanıcıları Kurma

Uygulamayı gerçekten kullanabilmek için (şu anda belirli modelleri kimliği doğrulanmamış kullanıcılarla paylaşmayı mümkün kılmayı planlıyoruz), bir girişe ihtiyacınız var. Süper kullanıcı (superuser) veya normal kullanıcı kullanabilirsiniz. Her iki durumda da, birinin önce konsol kullanarak bir süper kullanıcı oluşturması gerekir:

**Neden bir Django süper kullanıcısı kurulmalı?** Bir Django süper kullanıcısı, uygulamada tüm izinlere sahiptir ve kullanıcıları, koleksiyonları ve diğer verileri oluşturma, değiştirme ve silme dahil olmak üzere sistemin tüm yönlerini yönetebilir. Bir süper kullanıcı kurmak, uygulamayı tam olarak kontrol etmenizi ve yönetmenizi sağlar.

**Django süper kullanıcısı nasıl oluşturulur:**

1. Süper kullanıcı oluşturmak için aşağıdaki komutu çalıştırın:

`sudo docker-compose -f local.yml run django python manage.py createsuperuser`

2. Süper kullanıcı için bir kullanıcı adı, e-posta adresi ve şifre sağlamanız istenecektir. Gerekli bilgileri girin.

**Django admin kullanarak ek kullanıcılar nasıl oluşturulur:**

1. Dağıtım talimatlarını izleyerek Delphic uygulamanızı yerel olarak başlatın.
2. Tarayıcınızda `http://localhost:8000/admin` adresine giderek Django yönetim arayüzünü ziyaret edin.
3. Daha önce oluşturduğunuz süper kullanıcı kimlik bilgileriyle giriş yapın.
4. "Authentication and Authorization" bölümündeki "Users" seçeneğine tıklayın.
5. Sağ üst köşedeki "Add user +" butonuna tıklayın.
6. Yeni kullanıcı için kullanıcı adı ve şifre gibi gerekli bilgileri girin. Kullanıcıyı oluşturmak için "Save" butonuna tıklayın.
7. Yeni kullanıcıya ek izinler vermek veya onları süper kullanıcı yapmak için kullanıcı listesinde kullanıcı adlarına tıklayın, "Permissions" bölümüne gidin ve izinlerini buna göre yapılandırın. Değişikliklerinizi kaydedin.