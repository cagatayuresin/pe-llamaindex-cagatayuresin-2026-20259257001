# LlamaIndex ile Tam Yığın (Full-Stack) Web Uygulaması Oluşturma Rehberi

LlamaIndex bir Python kütüphanesidir; bu da onu bir tam yığın (full-stack) web uygulamasına entegre etmenin, alışık olduğunuzdan biraz daha farklı olacağı anlamına gelir.

Bu kılavuz, Python ile yazılmış temel bir API servisinin oluşturulması için gereken adımları ve bunun bir TypeScript+React ön ucu (frontend) ile nasıl etkileşime girdiğini göstermeyi amaçlamaktadır.

Buradaki tüm kod örnekleri [llama_index_starter_pack](https://github.com/logan-markewich/llama_index_starter_pack/tree/main/flask_react) içindeki `flask_react` klasöründe mevcuttur.

Bu kılavuzda kullanılan ana teknolojiler şunlardır:

-   python3.11
-   llama_index
-   flask
-   typescript
-   react

## Flask Arka Ucu (Backend)

Bu kılavuz için arka ucumuz, ön uç kodumuzla iletişim kurmak üzere bir [Flask](https://flask.palletsprojects.com/en/2.2.x/) API sunucusu kullanacaktır. İsterseniz bunu kolayca bir [FastAPI](https://fastapi.tiangolo.com/) sunucusuna veya seçtiğiniz başka bir Python sunucu kütüphanesine dönüştürebilirsiniz.

Flask kullanarak bir sunucu kurmak kolaydır. Paketi içe aktarır, uygulama (app) nesnesini oluşturur ve ardından uç noktalarınızı (endpoints) oluşturursunuz. Önce sunucu için temel bir iskelet oluşturalım:

```python
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Merhaba Dünya!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5601)
```

_flask_demo.py_

Bu dosyayı çalıştırırsanız (`python flask_demo.py`), 5601 portunda bir sunucu başlatacaktır. `http://localhost:5601/` adresini ziyaret ederseniz, tarayıcınızda "Merhaba Dünya!" yazısını göreceksiniz. Güzel!

Bir sonraki adım, sunucumuza hangi fonksiyonları dahil etmek istediğimize karar vermek ve LlamaIndex kullanmaya başlamaktır.

Her şeyi basit tutmak gerekirse, sağlayabileceğimiz en temel işlem mevcut bir indeksi sorgulamaktır. LlamaIndex'teki [Paul Graham makalesini](https://github.com/jerryjliu/llama_index/blob/main/examples/paul_graham_essay/data/paul_graham_essay.txt) kullanarak bir `documents` klasörü oluşturun ve makale metin dosyasını indirip içine yerleştirin.

### Temel Flask - Kullanıcı İndeks Sorgularını Yönetme

Şimdi, indeksi başlatmak için bazı kodlar yazalım:

```python
import os
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
)

# NOT: Sadece yerel testler içindir, anahtarınızı kodun içine gömerek yayınlamayın
os.environ["OPENAI_API_KEY"] = "anahtarınız buraya"

index = None


def initialize_index():
    global index
    storage_context = StorageContext.from_defaults()
    index_dir = "./.index"
    if os.path.exists(index_dir):
        index = load_index_from_storage(storage_context)
    else:
        documents = SimpleDirectoryReader("./documents").load_data()
        index = VectorStoreIndex.from_documents(
            documents, storage_context=storage_context
        )
        storage_context.persist(index_dir)
```

Bu fonksiyon indeksi başlatacaktır. Eğer bunu `main` fonksiyonu içinde Flask sunucusunu başlatmadan hemen önce çağırırsak, indeksimiz kullanıcı sorguları için hazır olacaktır!

Sorgu uç noktamız, sorgu metnini bir parametre olarak alan `GET` isteklerini kabul edecektir. İşte tam uç nokta fonksiyonunun nasıl görüneceği:

```python
from flask import request


@app.route("/query", methods=["GET"])
def query_index():
    global index
    query_text = request.args.get("text", None)
    if query_text is None:
        return (
            "Metin bulunamadı, lütfen URL'ye ?text=birşeyler parametresini ekleyin",
            400,
        )
    query_engine = index.as_query_engine()
    response = query_engine.query(query_text)
    return str(response), 200
```

Şimdi sunucumuza birkaç yeni kavram ekledik:

-   Fonksiyon dekoratörü tarafından tanımlanan yeni bir `/query` uç noktası.
-   İstekten parametreleri almak için kullanılan Flask'tan yeni bir içe aktarma: `request`.
-   Eğer `text` parametresi eksikse, bir hata mesajı ve uygun bir HTML yanıt kodu döndürüyoruz.
-   Aksi takdirde, indeksi sorguluyor ve yanıtı dize (string) olarak döndürüyoruz.

Tarayıcınızda test edebileceğiniz tam bir sorgu örneği şuna benzeyebilir: `http://localhost:5601/query?text=yazar büyürken ne yaptı` (Enter tuşuna bastığınızda tarayıcı boşlukları otomatik olarak "%20" karakterlerine dönüştürecektir).

İşler oldukça iyi gidiyor! Artık işlevsel bir API'mız var. Kendi dökümanlarınızı kullanarak, herhangi bir uygulamanın Flask API'ını çağırması ve sorgulara yanıt alması için kolayca bir arayüz sağlayabilirsiniz.

### Gelişmiş Flask - Kullanıcı Döküman Yüklemelerini Yönetme

Her şey harika görünüyor, ancak bunu bir adım daha ileri nasıl taşıyabiliriz? Ya kullanıcıların kendi dökümanlarını yükleyerek kendi indekslerini oluşturmalarına izin vermek istersek? Korkmayın, Flask her şeyi halledebilir :muscle:.

Kullanıcıların döküman yüklemesine izin vermek için bazı ekstra önlemler almamız gerekir. Mevcut bir indeksi sorgulamak yerine, indeks **değişebilir (mutable)** hale gelecektir. Aynı indekse ekleme yapan birçok kullanıcınız varsa, eşzamanlılığı (concurrency) nasıl yöneteceğimizi düşünmemiz gerekir. Flask sunucumuz iş parçacıklıdır (threaded), bu da birden fazla kullanıcının sunucuya aynı anda işlenecek istekler gönderebileceği anlamına gelir.

Bir seçenek, her kullanıcı veya grup için bir indeks oluşturmak ve bunları S3'te saklayıp getirmek olabilir. Ancak bu örnek için, kullanıcıların etkileşimde bulunduğu yerel olarak saklanan tek bir indeks olduğunu varsayacağız.

Eşzamanlı yüklemeleri yönetmek ve indekse sıralı eklemeler yapılmasını sağlamak için, ayrı bir sunucu ve kilitler (locks) kullanarak indekse sıralı erişim sağlamak üzere `BaseManager` Python paketini kullanabiliriz. Bu kulağa korkutucu geliyor ama o kadar da kötü değil! Sadece tüm indeks işlemlerimizi (başlatma, sorgulama, ekleme) Flask sunucumuzdan çağrılacak olan `BaseManager` "index_server" içine taşıyacağız.

Kodumuzu taşıdıktan sonra `index_server.py` dosyamızın nasıl görüneceğine dair temel bir örnek:

```python
import os
from multiprocessing import Lock
from multiprocessing.managers import BaseManager
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Document

# NOT: Sadece yerel testler içindir, anahtarınızı kodun içine gömerek yayınlamayın
os.environ["OPENAI_API_KEY"] = "anahtarınız buraya"

index = None
lock = Lock()


def initialize_index():
    global index
    with lock:
        # eskisi gibi ...
        pass


def query_index(query_text):
    global index
    query_engine = index.as_query_engine()
    response = query_engine.query(query_text)
    return str(response)


if __name__ == "__main__":
    # global indeksi başlat
    print("indeks başlatılıyor...")
    initialize_index()

    # sunucuyu kur
    # NOT: Şifreyi kod içine gömmek yerine daha güvenli bir yol tercih edebilirsiniz
    manager = BaseManager(("", 5602), b"sifre")
    manager.register("query_index", query_index)
    server = manager.get_server()

    print("sunucu başlatılıyor...")
    server.serve_forever()
```

_index_server.py_

Böylece fonksiyonlarımızı taşıdık, global indekse sıralı erişimi garanti eden `Lock` nesnesini ekledik, tek fonksiyonumuzu sunucuya kaydettik ve sunucuyu 5602 portunda `sifre` şifresiyle başlattık.

Ardından, Flask kodumuzu şu şekilde düzenleyebiliriz:

```python
from multiprocessing.managers import BaseManager
from flask import Flask, request

# manager bağlantısını başlat
# NOT: Şifreyi kod içine gömmek yerine daha güvenli bir yol tercih edebilirsiniz
manager = BaseManager(("", 5602), b"sifre")
manager.register("query_index")
manager.connect()


@app.route("/query", methods=["GET"])
def query_index():
    global index
    query_text = request.args.get("text", None)
    if query_text is None:
        return (
            "Metin bulunamadı, lütfen URL'ye ?text=birşeyler parametresini ekleyin",
            400,
        )
    response = manager.query_index(query_text)._getvalue()
    return str(response), 200


@app.route("/")
def home():
    return "Merhaba Dünya!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5601)
```

_flask_demo.py_

İki ana değişiklik; mevcut `BaseManager` sunucumuza bağlanmak ve fonksiyonları kaydetmek, ayrıca `/query` uç noktasında fonksiyonu manager üzerinden çağırmaktır.

Not edilmesi gereken özel bir durum; `BaseManager` sunucuları nesneleri tam olarak beklediğimiz gibi döndürmezler. Dönüş değerini orijinal nesnesine çözümlemek için `_getvalue()` fonksiyonunu çağırırız.

Kullanıcıların kendi dökümanlarını yüklemelerine izin verirsek, muhtemelen Paul Graham makalesini `documents` klasöründen kaldırmalıyız, o yüzden önce bunu yapalım. Ardından, dosya yüklemek için bir uç nokta ekleyelim! Önce Flask uç nokta fonksiyonumuzu tanımlayalım:

```python
...
manager.register("insert_into_index")
...


@app.route("/uploadFile", methods=["POST"])
def upload_file():
    global manager
    if "file" not in request.files:
        return "Lütfen bir dosya ile POST isteği gönderin", 400

    filepath = None
    try:
        uploaded_file = request.files["file"]
        filename = secure_filename(uploaded_file.filename)
        filepath = os.path.join("documents", os.path.basename(filename))
        uploaded_file.save(filepath)

        if request.form.get("filename_as_doc_id", None) is not None:
            manager.insert_into_index(filepath, doc_id=filename)
        else:
            manager.insert_into_index(filepath)
    except Exception as e:
        # geçici dosyayı temizle
        if filepath is not None and os.path.exists(filepath):
            os.remove(filepath)
        return "Hata: {}".format(str(e)), 500

    # geçici dosyayı temizle
    if filepath is not None and os.path.exists(filepath):
        os.remove(filepath)

    return "Dosya eklendi!", 200
```

Fena değil! Dosyayı diske yazdığımızı fark edeceksiniz. Sadece `txt` gibi temel dosya formatlarını kabul etseydik bunu atlayabilirdik, ancak diske yazarak LlamaIndex'in `SimpleDirectoryReader` özelliğinden yararlanıp bir dizi daha karmaşık dosya formatını halledebiliriz. İsteğe bağlı olarak, dosya adını `doc_id` olarak kullanmak veya LlamaIndex'in bizim için bir tane oluşturmasına izin vermek için ikinci bir `POST` parametresi de kullanıyoruz. Bu, ön yüzü (frontend) uyguladığımızda daha mantıklı gelecektir.

Bu daha karmaşık isteklerle [Postman](https://www.postman.com/downloads/?utm_source=postman-home) gibi bir araç kullanmanızı da öneririm. Uç noktalarımızı test etmek için Postman kullanma örnekleri [bu projenin deposunda](https://github.com/logan-markewich/llama_index_starter_pack/tree/main/flask_react/postman_examples) bulunmaktadır.

Son olarak, manager'a yeni bir fonksiyon eklediğimizi fark etmişsinizdir. Bunu `index_server.py` içinde uygulayalım:

```python
def insert_into_index(doc_text, doc_id=None):
    global index
    document = SimpleDirectoryReader(input_files=[doc_text]).load_data()[0]
    if doc_id is not None:
        document.doc_id = doc_id

    with lock:
        index.insert(document)
        index.storage_context.persist()


...
manager.register("insert_into_index", insert_into_index)
...
```

Kolay! Eğer hem `index_server.py` hem de `flask_demo.py` dosyalarını başlatırsak; bir vektör indeksine döküman eklemek için birden fazla isteği yönetebilen ve kullanıcı sorgularına yanıt verebilen bir Flask API sunucumuza sahibiz!

Ön yüzdeki bazı işlevleri desteklemek için, Flask API'ından gelen bazı yanıtların nasıl göründüğünü ayarladım ve indekste hangi dökümanların saklandığını takip etmek için bazı işlevler ekledim (LlamaIndex şu anda bunu kullanıcı dostu bir şekilde desteklemiyor, ancak bunu kendimiz zenginleştirebiliriz!). Son olarak, `Flask-cors` Python paketini kullanarak sunucuya CORS desteği eklemem gerekti.

Son küçük değişiklikler, `requirements.txt` dosyası ve dağıtıma yardımcı olacak örnek bir `Dockerfile` için [depodaki](https://github.com/logan-markewich/llama_index_starter_pack/tree/main/flask_react) tam `flask_demo.py` ve `index_server.py` betiklerini inceleyin.

## React Ön Yüzü (Frontend)

Genel olarak React ve TypeScript, günümüzde web uygulamaları yazmak için en popüler kütüphane ve dillerden biridir. Bu kılavuz, bu araçların nasıl çalıştığına aşina olduğunuzu varsayacaktır, aksi takdirde bu kılavuzun uzunluğu üç katına çıkacaktır :smile:.

[Depoda](https://github.com/logan-markewich/llama_index_starter_pack/tree/main/flask_react), ön uç kodu `react_frontend` klasörü içinde organize edilmiştir.

Ön yüzün en alakalı kısmı `src/apis` klasörü olacaktır. Burası Flask sunucusuna çağrılar yaptığımız yerdir ve aşağıdaki sorguları destekler:

-   `/query`: Mevcut indekse bir sorgu yapar.
-   `/uploadFile`: İndekse eklenmek üzere Flask sunucusuna bir dosya yükler.
-   `/getDocuments`: Mevcut döküman başlıklarını ve metinlerinin bir kısmını listeler.

Bu üç sorguyu kullanarak; kullanıcıların dosyalarını yüklemelerine ve takip etmelerine, indeksi sorgulamalarına, sorgu yanıtını ve yanıtı oluşturmak için hangi metin node'larının kullanıldığına dair bilgileri görüntülemelerine olanak tanıyan sağlam bir ön yüz oluşturabiliriz.

### fetchDocuments.tsx

Tahmin ettiğiniz gibi, bu dosya indeksteki mevcut dökümanların listesini getirme fonksiyonunu içerir. Kod şu şekildedir:

```typescript
export type Document = {
  id: string;
  text: string;
};

const fetchDocuments = async (): Promise<Document[]> => {
  const response = await fetch("http://localhost:5601/getDocuments", {
    mode: "cors",
  });

  if (!response.ok) {
    return [];
  }

  const documentList = (await response.json()) as Document[];
  return documentList;
};
```

Gördüğünüz gibi, Flask sunucusuna bir sorgu yapıyoruz (burada localhost üzerinde çalıştığı varsayılıyor). Harici bir istek yaptığımız için `mode: 'cors'` seçeneğini dahil etmemiz gerektiğini unutmayın.

Ardından, yanıtın tamam olup olmadığını kontrol ediyoruz ve eğer öyleyse, yanıt JSON'ını alıp döndürüyoruz. Burada yanıt JSON'ı, aynı dosyada tanımlanan `Document` nesnelerinden oluşan bir listedir.

### queryIndex.tsx

Bu dosya kullanıcı sorgusunu Flask sunucusuna gönderir ve yanıtı, ayrıca indeksimizdeki hangi node'ların yanıtı sağladığına dair detayları geri alır.

```typescript
export type ResponseSources = {
  text: string;
  doc_id: string;
  start: number;
  end: number;
  similarity: number;
};

export type QueryResponse = {
  text: string;
  sources: ResponseSources[];
};

const queryIndex = async (query: string): Promise<QueryResponse> => {
  const queryURL = new URL("http://localhost:5601/query?text=1");
  queryURL.searchParams.append("text", query);

  const response = await fetch(queryURL, { mode: "cors" });
  if (!response.ok) {
    return { text: "Sorguda hata oluştu", sources: [] };
  }

  const queryResponse = (await response.json()) as QueryResponse;

  return queryResponse;
};

export default queryIndex;
```

Bu, `fetchDocuments.tsx` dosyasına benzerdir; ana fark, sorgu metnini URL'de bir parametre olarak dahil etmemizdir. Ardından yanıtın tamam olup olmadığını kontrol eder ve uygun TypeScript tipiyle döndürürüz.

### insertDocument.tsx

Muhtemelen en karmaşık API çağrısı bir döküman yüklemektir. Buradaki fonksiyon bir dosya nesnesi kabul eder ve `FormData` kullanarak bir `POST` isteği oluşturur.

Asıl yanıt metni uygulamada kullanılmaz ancak dosyanın yüklenip yüklenemediğine dair kullanıcıya geri bildirim sağlamak için kullanılabilir.

```typescript
const insertDocument = async (file: File) => {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("filename_as_doc_id", "true");

  const response = await fetch("http://localhost:5601/uploadFile", {
    mode: "cors",
    method: "POST",
    body: formData,
  });

  const responseText = response.text();
  return responseText;
};

export default insertDocument;
```

### Diğer Tüm Ön Yüz Güzellikleri

Ve bu, ön yüz kısmını hemen hemen tamamlıyor! React ön yüz kodunun geri kalanı, oldukça temel React bileşenlerinden ve en azından biraz güzel görünmesi için gösterdiğim çabadan ibarettir :smile:.

Geri kalan [kod tabanını](https://github.com/logan-markewich/llama_index_starter_pack/tree/main/flask_react/react_frontend) okumanızı ve iyileştirmeler için PR'lar göndermenizi öneririm!

## Sonuç

Bu kılavuz tonlarca bilgi kapsadı. Python ile yazılmış temel bir "Merhaba Dünya" Flask sunucusundan, LlamaIndex destekli tam işlevli bir arka uca ve bunu bir ön uç uygulamasına nasıl bağlayacağımıza kadar geldik.

Gördüğünüz gibi, ön yüzde iyi bir kullanıcı deneyimi sağlamaya yardımcı olmak için LlamaIndex tarafından sunulan hizmetleri kolayca zenginleştirebilir ve sarmalayabiliriz (küçük bir harici döküman takipçisi gibi).

Bunu alıp birçok özellik ekleyebilirsiniz (çoklu indeks/kullanıcı desteği, nesneleri S3'e kaydetme, bir Pinecone vektör sunucusu ekleme vb.). Bunu okuduktan sonra bir uygulama oluşturduğunuzda, sonucu Discord'da paylaşmayı unutmayın! İyi şanslar! :muscle: