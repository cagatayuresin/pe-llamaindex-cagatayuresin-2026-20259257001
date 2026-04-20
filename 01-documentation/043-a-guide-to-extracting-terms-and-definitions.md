# Terim ve Tanımları Çıkarma Kılavuzu

LlamaIndex'in iyi dökümante edilmiş birçok kullanım durumu (anlamsal arama, özetleme vb.) vardır. Ancak bu, LlamaIndex'i çok spesifik kullanım durumlarına uygulayamayacağımız anlamına gelmez!

Bu eğitimde, metinden terimleri ve tanımları çıkarmak için LlamaIndex'i kullanma ve kullanıcıların daha sonra bu terimleri sorgulamasına olanak tanıma tasarım sürecini inceleyeceğiz. [Streamlit](https://streamlit.io/) kullanarak, tüm bunları çalıştırmak ve test etmek için kolayca bir ön yüz oluşturabilir ve tasarımımızla hızlı bir şekilde yineleme yapabiliriz.

Bu eğitim, Python 3.9+ sürümüne ve aşağıdaki paketlerin yüklü olduğuna sahip olduğunuzu varsayar:

-   llama-index
-   streamlit

Temel düzeyde amacımız; bir dökümandan metin almak, terimleri ve tanımları çıkarmak ve ardından kullanıcıların bu terim ve tanım bilgi tabanını sorgulaması için bir yol sağlamaktır. Eğitim, hem LlamaIndex hem de Streamlit özelliklerini inceleyecek ve umarız ortaya çıkan yaygın sorunlar için ilginç çözümler sunacaktır.

Bu eğitimin final sürümü [burada](https://github.com/abdulasiraj/A-Guide-to-Extracting-Terms-and-Definitions) bulunabilir ve canlı olarak barındırılan bir demo [Huggingface Spaces](https://huggingface.co/spaces/Nobody4591/Llama_Index_Term_Extractor) üzerinde mevcuttur.

## Metin Yükleme

İlk adım, kullanıcılara metni manuel olarak girme yolu vermektir. Bunun için arayüz sağlayacak Streamlit kodunu yazalım! Aşağıdaki kodu kullanın ve uygulamayı `streamlit run app.py` ile başlatın.

```python
import streamlit as st

st.title("🦙 Llama Index Terim Çıkarıcı 🦙")

document_text = st.text_area("Ham metni girin")
if st.button("Terimleri ve Tanımları Çıkar") and document_text:
    with st.spinner("Çıkarılıyor..."):
        extracted_terms = document_text  # bu bir yer tutucudur!
    st.write(extracted_terms)
```

Süper basit, değil mi! Ancak uygulamanın henüz yararlı bir şey yapmadığını fark edeceksiniz. LlamaIndex'i kullanmak için OpenAI LLM'imizi de kurmamız gerekiyor. LLM için bir dizi olası ayar vardır, bu yüzden hangisinin en iyi olduğunu kullanıcının belirlemesine izin verebiliriz. Ayrıca kullanıcının terimleri çıkaracak istemi (prompt) ayarlamasına da izin vermeliyiz (bu, neyin en iyi çalıştığını hata ayıklamamıza da yardımcı olacaktır).

## LLM Ayarları

Bu sonraki adım, farklı özellikler sunan farklı bölmelere ayırmak için uygulamamıza bazı sekmeler (tabs) ekler. LLM ayarları ve metin yükleme için birer sekme oluşturalım:

```python
import os
import streamlit as st

DEFAULT_TERM_STR = (
    "Bağlamda tanımlanan terimlerin ve tanımların bir listesini yapın, "
    "her satırda bir çift olsun. "
    "Bir terimin tanımı eksikse, en iyi tahmininizi kullanın. "
    "Her satırı şu şekilde yazın:\nTerim: <terim> Tanım: <tanım>"
)

st.title("🦙 Llama Index Terim Çıkarıcı 🦙")

setup_tab, upload_tab = st.tabs(["Kurulum", "Yükle/Terimleri Çıkar"])

with setup_tab:
    st.subheader("LLM Kurulumu")
    api_key = st.text_input("OpenAI API anahtarınızı buraya girin", type="password")
    llm_name = st.selectbox("Hangi LLM?", ["gpt-3.5-turbo", "gpt-4"])
    model_temperature = st.slider(
        "LLM Sıcaklığı (Temperature)", min_value=0.0, max_value=1.0, step=0.1
    )
    term_extract_str = st.text_area(
        "Terimleri ve tanımları çıkarmak için kullanılacak sorgu.",
        value=DEFAULT_TERM_STR,
    )

with upload_tab:
    st.subheader("Tanımları Çıkar ve Sorgula")
    document_text = st.text_area("Ham metni girin")
    if st.button("Terimleri ve Tanımları Çıkar") and document_text:
        with st.spinner("Çıkarılıyor..."):
            extracted_terms = document_text  # bu bir yer tutucudur!
        st.write(extracted_terms)
```

Artık uygulamamızın iki sekmesi var, bu da organizasyona gerçekten yardımcı oluyor. Ayrıca terimleri çıkarmak için varsayılan bir istem eklediğimi fark edeceksiniz -- bazı terimleri çıkarmayı denedikten sonra bunu değiştirebilirsiniz, bu sadece biraz deneme yaptıktan sonra ulaştığım istemdir.

Terimleri çıkarmaktan bahsetmişken, tam olarak bunu yapacak bazı fonksiyonlar eklemenin zamanı geldi!

## Terimleri Çıkarma ve Saklama

Artık LLM ayarlarını ve girdi metnini tanımlayabildiğimize göre, terimleri bizim için metinden çıkarmak için LlamaIndex'i kullanmayı deneyebiliriz!

Hem LLM'imizi başlatmak hem de giriş metninden terimleri çıkarmak için aşağıdaki fonksiyonları ekleyebiliriz.

```python
from llama_index.core import Document, SummaryIndex, load_index_from_storage
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings


def get_llm(llm_name, model_temperature, api_key, max_tokens=256):
    os.environ["OPENAI_API_KEY"] = api_key
    return OpenAI(
        temperature=model_temperature, model=llm_name, max_tokens=max_tokens
    )


def extract_terms(
    documents, term_extract_str, llm_name, model_temperature, api_key
):
    llm = get_llm(llm_name, model_temperature, api_key, max_tokens=1024)

    temp_index = SummaryIndex.from_documents(
        documents,
    )
    query_engine = temp_index.as_query_engine(
        response_mode="tree_summarize", llm=llm
    )
    terms_definitions = str(query_engine.query(term_extract_str))
    terms_definitions = [
        x
        for x in terms_definitions.split("\n")
        if x and "Terim:" in x and "Tanım:" in x
    ]
    # metni bir sözlüğe dönüştür
    terms_to_definition = {
        x.split("Tanım:")[0]
        .split("Terim:")[-1]
        .strip(): x.split("Tanım:")[-1]
        .strip()
        for x in terms_definitions
    }
    return terms_to_definition
```

Şimdi yeni fonksiyonları kullanarak nihayet terimlerimizi çıkarabiliriz!

```python
...
with upload_tab:
    st.subheader("Tanımları Çıkar ve Sorgula")
    document_text = st.text_area("Ham metni girin")
    if st.button("Terimleri ve Tanımları Çıkar") and document_text:
        with st.spinner("Çıkarılıyor..."):
            extracted_terms = extract_terms(
                [Document(text=document_text)],
                term_extract_str,
                llm_name,
                model_temperature,
                api_key,
            )
        st.write(extracted_terms)
```

Şu anda çok şey oluyor, neler bittiğini incelemek için bir dakikanızı ayıralım.

`get_llm()`, kurulum sekmesindeki kullanıcı yapılandırmasına dayanarak LLM'i somutlaştırıyor.

`extract_terms()`, tüm güzel şeylerin olduğu yerdir. İlk olarak, terimlerimizi ve tanımlarımızı çıkarırken modeli çok fazla kısıtlamak istemediğimiz için `max_tokens=1024` ile `get_llm()` çağırıyoruz (ayarlanmazsa varsayılan değer 256'dır). Ardından, `Settings` nesnemizi tanımlıyoruz; `num_output` değerini `max_tokens` değerimizle hizalıyoruz ve chunk boyutunu çıktıdan daha büyük olmayacak şekilde ayarlıyoruz. Dökümanlar LlamaIndex tarafından indekslendiğinde, büyüklerse parçalara (node olarak da adlandırılır) bölünürler ve `chunk_size` bu parçaların boyutunu belirler.

Sırada, geçici bir özet indeksi (summary index) oluşturuyoruz ve LLM'imizi geçiyoruz. Bir özet indeksi, indeksimizdeki her bir metin parçasını okuyacaktır; bu da terimleri çıkarmak için mükemmeldir. Son olarak, `response_mode="tree_summarize"` kullanarak terimleri çıkarmak için önceden tanımlanmış sorgu metnimizi kullanıyoruz. Bu yanıt modu, aşağıdan yukarıya doğru bir özet ağacı oluşturacaktır; burada her üst öğe (parent) kendi alt öğelerini (children) özetler. Son olarak ağacın tepesi döndürülür; bu tepe tüm çıkarılan terimlerimizi ve tanımlarımızı içerecektir.

Son olarak, küçük bir işlem sonrası (post processing) yapıyoruz. Modelin talimatları takip ettiğini ve her satıra bir terim/tanım çifti koyduğunu varsayıyoruz. Eğer bir satırda `Terim:` veya `Tanım:` etiketleri eksikse, o satırı atlıyoruz. Ardından kolay saklama için bunu bir sözlüğe dönüştürüyoruz!

## Çıkarılan Terimleri Kaydetme

Artık terimleri çıkarabildiğimize göre, onları daha sonra sorgulayabilmemiz için bir yere koymamız gerekiyor. Bir `VectorStoreIndex` şu an için mükemmel bir seçim olacaktır! Ancak ek olarak, uygulamamız daha sonra inceleyebilmemiz için hangi terimlerin indekse eklendiğini de takip etmelidir. `st.session_state` kullanarak, her kullanıcıya özel bir oturum sözlüğünde mevcut terim listesini saklayabiliriz!

Öncelikle küresel bir vektör indeksini başlatmak için bir özellik ve çıkarılan terimleri eklemek için başka bir fonksiyon ekleyelim.

```python
from llama_index.core import Settings, VectorStoreIndex

...
if "all_terms" not in st.session_state:
    st.session_state["all_terms"] = DEFAULT_TERMS
...


def insert_terms(terms_to_definition):
    for term, definition in terms_to_definition.items():
        doc = Document(text=f"Terim: {term}\nTanım: {definition}")
        st.session_state["llama_index"].insert(doc)


@st.cache_resource
def initialize_index(llm_name, model_temperature, api_key):
    """VectorStoreIndex nesnesini oluşturur."""
    Settings.llm = get_llm(llm_name, model_temperature, api_key)

    index = VectorStoreIndex([])

    return index


...

with upload_tab:
    st.subheader("Tanımları Çıkar ve Sorgula")
    if st.button("İndeksi Başlat ve Terimleri Sıfırla"):
        st.session_state["llama_index"] = initialize_index(
            llm_name, model_temperature, api_key
        )
        st.session_state["all_terms"] = {}

    if "llama_index" in st.session_state:
        st.markdown(
            "Bir dökümanın görüntüsünü/ekran görüntüsünü yükleyin veya metni manuel olarak girin."
        )
        document_text = st.text_area("Veya ham metni girin")
        if st.button("Terimleri ve Tanımları Çıkar") and (
            uploaded_file or document_text
        ):
            st.session_state["terms"] = {}
            terms_docs = {}
            with st.spinner("Çıkarılıyor..."):
                terms_docs.update(
                    extract_terms(
                        [Document(text=document_text)],
                        term_extract_str,
                        llm_name,
                        model_temperature,
                        api_key,
                    )
                )
            st.session_state["terms"].update(terms_docs)

        if "terms" in st.session_state and st.session_state["terms"]:
            st.markdown("Çıkarılan terimler")
            st.json(st.session_state["terms"])

            if st.button("Terimler eklensin mi?"):
                with st.spinner("Terimler ekleniyor"):
                    insert_terms(st.session_state["terms"])
                st.session_state["all_terms"].update(st.session_state["terms"])
                st.session_state["terms"] = {}
                st.experimental_rerun()
```

Şimdi Streamlit'in gücünden gerçekten yararlanmaya başlıyorsunuz! Yükleme sekmesinin altındaki kodla başlayalım. Vektör indeksini başlatmak için bir buton ekledik ve onu küresel Streamlit durum sözlüğünde (session state) saklıyoruz; ayrıca mevcut çıkarılan terimleri sıfırlıyoruz. Ardından, girdi metninden terimleri çıkardıktan sonra, çıkarılan terimleri tekrar küresel durumda saklıyoruz ve kullanıcıya eklemeden önce onları inceleme şansı veriyoruz. Eğer ekleme butonuna basılırsa, terim ekleme fonksiyonumuzu çağırıyoruz, eklenen terimlerin küresel takibini güncelliyoruz ve en son çıkarılan terimleri oturum durumundan kaldırıyoruz.

## Çıkarılan Terimler/Tanımlar İçin Sorgulama

Terimler ve tanımlar çıkarılıp kaydedildikten sonra onları nasıl kullanabiliriz? Ve kullanıcı daha önce nelerin kaydedildiğini nasıl hatırlayacak?? Bu özellikleri yönetmek için uygulamaya birkaç sekme daha ekleyebiliriz.

```python
...
setup_tab, terms_tab, upload_tab, query_tab = st.tabs(
    ["Kurulum", "Tüm Terimler", "Yükle/Terimleri Çıkar", "Terimleri Sorgula"]
)
...
with terms_tab:
    st.subheader("Mevcut Çıkarılan Terimler ve Tanımlar")
    st.json(st.session_state["all_terms"])
...
with query_tab:
    st.subheader("Terimleri/Tanımları Sorgulayın!")
    st.markdown(
        (
            "LLM sorgunuzu yanıtlamaya çalışacak ve eklediğiniz terimleri/tanımları kullanarak cevaplarını zenginleştirecektir. "
            "Bir terim indekste yoksa, kendi içsel bilgisiyle yanıt verecektir."
        )
    )
    if st.button("İndeksi Başlat ve Terimleri Sıfırla", key="init_index_2"):
        st.session_state["llama_index"] = initialize_index(
            llm_name, model_temperature, api_key
        )
        st.session_state["all_terms"] = {}

    if "llama_index" in st.session_state:
        query_text = st.text_input("Bir terim veya tanım hakkında soru sorun:")
        if query_text:
            query_text = (
                query_text
                + "\nCevabı bulamazsanız, sorguyu en iyi bildiğiniz şekilde yanıtlayın."
            )
            with st.spinner("Cevap oluşturuluyor..."):
                response = (
                    st.session_state["llama_index"]
                    .as_query_engine(
                        similarity_top_k=5,
                        response_mode="compact",
                        text_qa_template=TEXT_QA_TEMPLATE,
                        refine_template=DEFAULT_REFINE_PROMPT,
                    )
                    .query(query_text)
                )
            st.markdown(str(response))
```

Bu kısım çoğunlukla basit olsa da dikkat edilmesi gereken bazı önemli noktalar:

-   Başlatma butonumuzun diğer butonumuzla aynı metni var. Streamlit buna itiraz edecektir, bu yüzden bunun yerine benzersiz bir anahtar (key) sağlıyoruz.
-   Sorguya ek metin eklendi! Bu, indeksin cevaba sahip olmadığı zamanları telafi etmeye çalışmak içindir.
-   İndeks sorgumuzda iki seçenek belirledik:
    -   `similarity_top_k=5`, indeksin sorguya en yakın eşleşen en iyi 5 terimi/tanımı getireceği anlamına gelir.
    -   `response_mode="compact"`, her LLM çağrısında 5 eşleşen terimden/tanımdan mümkün olduğunca fazla metnin kullanılacağı anlamına gelir. Bu olmasaydı, indeks LLM'e en az 5 çağrı yapardı; bu da kullanıcı için işleri yavaşlatabilir.

## Deneme Testi (Dry Run Test)

Aslında biz ilerlerken sizin test ettiğinizi umuyorum. Ama şimdi, tam bir testi deneyelim.

1.  Uygulamayı yenileyin.
2.  LLM ayarlarınızı girin.
3.  Sorgu sekmesine gidin.
4.  Şunu sorun: `Bunnyhug nedir?`
5.  Uygulama saçma sapan bir cevap vermelidir. Bilmiyorsanız, bunnyhug Kanada Prairies'inden (Kırları) insanların kullandığı bir kapüşonlu (hoodie) sözcüğüdür!
6.  Bu tanımı uygulamaya ekleyelim. Yükleme sekmesini açın ve şu metni girin: `A bunnyhug is a common term used to describe a hoodie. This term is used by people from the Canadian Prairies.`
7.  Çıkar butonuna tıklayın. Birkaç saniye sonra uygulama doğru şekilde çıkarılan terimi/tanımı görüntülemelidir. Kaydetmek için terimi ekle butonuna tıklayın!
8.  Terimler sekmesini açarsak, az önce çıkardığımız terim ve tanım görüntülenmelidir.
9.  Sorgu sekmesine geri dönün ve bir bunnyhug'ın ne olduğunu sormayı deneyin. Şimdi cevap doğru olmalıdır!

## İyileştirme #1 - Bir Başlangıç İndeksi Oluşturun

Temel uygulamamız çalışırken, yararlı bir indeks oluşturmak için çok çaba harcamak gerekiyormuş gibi gelebilir. Ya kullanıcıya uygulamanın sorgu yeteneklerini sergilemek için bir tür başlangıç noktası verseydik? Bunu yapabiliriz! İlk olarak, her yüklemeden sonra indeksi diske kaydetmemiz için uygulamamızda küçük bir değişiklik yapalım:

```python
def insert_terms(terms_to_definition):
    for term, definition in terms_to_definition.items():
        doc = Document(text=f"Terim: {term}\nTanım: {definition}")
        st.session_state["llama_index"].insert(doc)
    # GEÇİCİ - diske kaydet
    st.session_state["llama_index"].storage_context.persist()
```

Şimdi, çıkarım yapacak bir dökümana ihtiyacımız var! Bu projenin deposu New York City hakkındaki Wikipedia sayfasını kullandı ve metni [burada](https://github.com/jerryjliu/llama_index/blob/main/examples/test_wiki/data/nyc_text.txt) bulabilirsiniz.

Metni yükleme sekmesine yapıştırıp çalıştırırsanız (biraz zaman alabilir), çıkarılan terimleri ekleyebiliriz. İndekse eklemeden önce çıkarılan terimlerin metnini bir not defterine veya benzeri bir yere kopyaladığınızdan emin olun! Bunlara bir saniye içinde ihtiyacımız olacak.

Ekledikten sonra, indeksi diske kaydetmek için kullandığımız kod satırını kaldırın. Artık kaydedilmiş bir başlangıç indeksi ile `initialize_index` fonksiyonumuzu şu şekilde görünecek şekilde değiştirebiliriz:

```python
@st.cache_resource
def initialize_index(llm_name, model_temperature, api_key):
    """Index nesnesini yükler."""
    Settings.llm = get_llm(llm_name, model_temperature, api_key)

    index = load_index_from_storage(storage_context)

    return index
```

Not defterine o devasa çıkarılan terim listesini kaydetmeyi hatırladınız mı? Şimdi uygulamamız başladığında, indeksteki varsayılan terimleri küresel terimler durumumuza aktarmak istiyoruz:

```python
...
if "all_terms" not in st.session_state:
    st.session_state["all_terms"] = DEFAULT_TERMS
...
```

Bunu daha önce `all_terms` değerlerini sıfırladığımız her yerde tekrarlayın.

## İyileştirme #2 - (Rafine Etme) Daha İyi İstemler (Prompts)

Şu anda uygulama ile biraz oynarsanız, istemimizi takip etmeyi bıraktığını fark edebilirsiniz! Hatırlarsanız, `query_str` değişkenimize terim/tanım bulunamazsa en iyi bilgisiyle yanıt vermesini eklemiştik. Ancak şimdi rastgele terimler (bunnyhug gibi!) sormayı denerseniz, bu talimatları takip edebilir veya etmeyebilir.

Bu durum, LlamaIndex'teki cevapları "rafine etme" (refining) konseptinden kaynaklanmaktadır. En iyi 5 eşleşen sonuç arasında sorgulama yaptığımız için, bazen tüm sonuçlar tek bir isteme sığmaz! OpenAI modelleri genellikle 4097 token'lık bir maksimum giriş boyutuna sahiptir. Bu nedenle LlamaIndex, eşleşen sonuçları isteme sığacak parçalara ayırarak bunu hesaba katar. LlamaIndex ilk API çağrısından ilk cevabı aldıktan sonra, bir sonraki parçayı API'a bir önceki cevapla birlikte gönderir ve modelden bu cevabı rafine etmesini ister.

Görünüşe göre rafine etme süreci sonuçlarımızı bozuyor! `query_str`'ye fazladan talimatlar eklemek yerine bunu kaldırın; LlamaIndex kendi özel istemlerimizi sağlamamıza izin verecektir! Şimdi [varsayılan istemleri](https://github.com/run-llama/llama_index/blob/main/llama-index-core/llama_index/core/prompts/default_prompts.py) ve [sohbete özel istemleri](https://github.com/run-llama/llama_index/blob/main/llama-index-core/llama_index/core/prompts/chat_prompts.py) kılavuz olarak kullanarak bunları oluşturalım. Yeni bir `constants.py` dosyası kullanarak bazı yeni sorgu şablonları oluşturalım:

```python
from llama_index.core import (
    PromptTemplate,
    SelectorPromptTemplate,
    ChatPromptTemplate,
)
from llama_index.core.prompts.utils import is_chat_model
from llama_index.core.llms import ChatMessage, MessageRole

# Metin Soru-Cevap (QA) şablonları
DEFAULT_TEXT_QA_PROMPT_TMPL = (
    "Bağlam bilgisi aşağıdadır. \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "Bağlam bilgisini dikkate alarak şu soruyu yanıtlayın "
    "(cevabı bilmiyorsanız, en iyi bilginizi kullanın): {query_str}\n"
)
TEXT_QA_TEMPLATE = PromptTemplate(DEFAULT_TEXT_QA_PROMPT_TMPL)

# Rafine Etme (Refine) şablonları
DEFAULT_REFINE_PROMPT_TMPL = (
    "Asıl soru şu şekildedir: {query_str}\n"
    "Mevcut bir cevap sağladık: {existing_answer}\n"
    "Aşağıdaki biraz daha bağlamla mevcut cevabı rafine etme "
    "(sadece gerekiyorsa) fırsatımız var.\n"
    "------------\n"
    "{context_msg}\n"
    "------------\n"
    "Yeni bağlamı ve en iyi bilginizi kullanarak mevcut cevabı iyileştirin. "
    "Mevcut cevabı iyileştiremiyorsanız, aynen tekrarlayın."
)
DEFAULT_REFINE_PROMPT = PromptTemplate(DEFAULT_REFINE_PROMPT_TMPL)

CHAT_REFINE_PROMPT_TMPL_MSGS = [
    ChatMessage(content="{query_str}", role=MessageRole.USER),
    ChatMessage(content="{existing_answer}", role=MessageRole.ASSISTANT),
    ChatMessage(
        content="Yukarıdaki cevabı aşağıdaki biraz daha bağlamla rafine etme "
        "(sadece gerekiyorsa) fırsatımız var.\n"
        "------------\n"
        "{context_msg}\n"
        "------------\n"
        "Yeni bağlamı ve en iyi bilginizi kullanarak mevcut cevabı iyileştirin. "
        "Mevcut cevabı iyileştiremiyorsanız, aynen tekrarlayın.",
        role=MessageRole.USER,
    ),
]

CHAT_REFINE_PROMPT = ChatPromptTemplate(CHAT_REFINE_PROMPT_TMPL_MSGS)

# rafine etme istemi seçicisi (refine prompt selector)
REFINE_TEMPLATE = SelectorPromptTemplate(
    default_template=DEFAULT_REFINE_PROMPT,
    conditionals=[(is_chat_model, CHAT_REFINE_PROMPT)],
)
```

Bu çok fazla kod gibi görünebilir ama o kadar da kötü değil! Varsayılan istemlere baktıysanız, varsayılan istemlerin ve sohbet modellerine özel istemlerin olduğunu fark etmiş olabilirsiniz. Bu eğilimi devam ettirerek, özel istemlerimiz için de aynısını yapıyoruz. Ardından, bir istem seçici kullanarak her iki istemi tek bir nesnede birleştirebiliriz. Kullanılan LLM bir sohbet modeliyse (ChatGPT, GPT-4), sohbet istemleri kullanılır. Aksi takdirde normal istem şablonları kullanılır.

Dikkat edilmesi gereken bir diğer husus da sadece bir tane Soru-Cevap (QA) şablonu tanımlamış olmamızdır. Bir sohbet modelinde bu, tek bir "insan" (human) mesajına dönüştürülecektir.

Şimdi bu istemleri uygulamamıza aktarabilir ve sorgu sırasında kullanabiliriz.

```python
from constants import REFINE_TEMPLATE, TEXT_QA_TEMPLATE

...
if "llama_index" in st.session_state:
    query_text = st.text_input("Bir terim veya tanım hakkında soru sorun:")
    if query_text:
        query_text = query_text  # Eski talimatları kaldırdığımıza dikkat edin
        with st.spinner("Cevap oluşturuluyor..."):
            response = (
                st.session_state["llama_index"]
                .as_query_engine(
                    similarity_top_k=5,
                    response_mode="compact",
                    text_qa_template=TEXT_QA_TEMPLATE,
                    refine_template=DEFAULT_REFINE_PROMPT,
                )
                .query(query_text)
            )
        st.markdown(str(response))
...
```

Sorgularla biraz daha deneme yaparsanız, cevapların artık talimatlarımızı biraz daha iyi takip ettiğini fark edersiniz umarım!

## İyileştirme #3 - Görüntü (Image) Desteği

LlamaIndex görüntüleri de destekler! LlamaIndex kullanarak dökümanların (makaleler, mektuplar vb.) görüntülerini yükleyebiliriz ve LlamaIndex metni çıkarma işlemini halleder. Kullanıcıların dökümanlarının görüntülerini yüklemelerine ve onlardan terim ile tanımları çıkarmalarına olanak tanımak için bundan yararlanabiliriz.

PIL hakkında bir içe aktarma hatası alırsanız, önce `pip install Pillow` kullanarak yükleyin.

```python
from PIL import Image
from llama_index.readers.file import ImageReader


@st.cache_resource
def get_file_extractor():
    image_parser = ImageReader(keep_image=True, parse_text=True)
    file_extractor = {
        ".jpg": image_parser,
        ".png": image_parser,
        ".jpeg": image_parser,
    }
    return file_extractor


file_extractor = get_file_extractor()
...
with upload_tab:
    st.subheader("Tanımları Çıkar ve Sorgula")
    if st.button("İndeksi Başlat ve Terimleri Sıfırla", key="init_index_1"):
        st.session_state["llama_index"] = initialize_index(
            llm_name, model_temperature, api_key
        )
        st.session_state["all_terms"] = DEFAULT_TERMS

    if "llama_index" in st.session_state:
        st.markdown(
            "Bir dökümanın görüntüsünü/ekran görüntüsünü yükleyin veya metni manuel olarak girin."
        )
        uploaded_file = st.file_uploader(
            "Bir dökümanın görüntüsünü/ekran görüntüsünü yükleyin:",
            type=["png", "jpg", "jpeg"],
        )
        document_text = st.text_area("Veya ham metni girin")
        if st.button("Terimleri ve Tanımları Çıkar") and (
            uploaded_file or document_text
        ):
            st.session_state["terms"] = {}
            terms_docs = {}
            with st.spinner("Çıkarılıyor (görüntüler yavaş olabilir)..."):
                if document_text:
                    terms_docs.update(
                        extract_terms(
                            [Document(text=document_text)],
                            term_extract_str,
                            llm_name,
                            model_temperature,
                            api_key,
                        )
                    )
                if uploaded_file:
                    Image.open(uploaded_file).convert("RGB").save("temp.png")
                    img_reader = SimpleDirectoryReader(
                        input_files=["temp.png"], file_extractor=file_extractor
                    )
                    img_docs = img_reader.load_data()
                    os.remove("temp.png")
                    terms_docs.update(
                        extract_terms(
                            img_docs,
                            term_extract_str,
                            llm_name,
                            model_temperature,
                            api_key,
                        )
                    )
            st.session_state["terms"].update(terms_docs)

        if "terms" in st.session_state and st.session_state["terms"]:
            st.markdown("Çıkarılan terimler")
            st.json(st.session_state["terms"])

            if st.button("Terimler eklensin mi?"):
                with st.spinner("Terimler ekleniyor"):
                    insert_terms(st.session_state["terms"])
                st.session_state["all_terms"].update(st.session_state["terms"])
                st.session_state["terms"] = {}
                st.experimental_rerun()
```

Burada Streamlit kullanarak dosya yükleme seçeneğini ekledik. Ardından görüntü açılır ve diske kaydedilir (bu biraz dolambaçlı görünebilir ama işleri basit tutar). Ardından görüntü yolunu okuyucuya (reader) geçeriz, dökümanları/metni çıkarırız ve geçici görüntü dosyamızı kaldırırız.

Artık dökümanlara sahip olduğumuza göre, `extract_terms()` fonksiyonunu daha önce olduğu gibi çağırabiliriz.

## Sonuç / Özet (TLDR)

Bu eğitimde, yolda karşımıza çıkan bazı yaygın sorunları ve problemleri çözerken bir ton bilgiye değindik:

-   Farklı kullanım durumları için farklı indeksler kullanma (Liste ve Vektör indeksi karşılaştırması)
-   Streamlit'in `session_state` konsepti ile küresel durum değerlerini saklama
-   LlamaIndex ile dahili istemleri (prompts) özelleştirme
-   LlamaIndex ile görüntülerden metin okuma

Bu eğitimin final sürümü [burada](https://github.com/abdulasiraj/A-Guide-to-Extracting-Terms-and-Definitions) bulunabilir ve canlı olarak barındırılan bir demo [Huggingface Spaces](https://huggingface.co/spaces/Nobody4591/Llama_Index_Term_Extractor) üzerinde mevcuttur.