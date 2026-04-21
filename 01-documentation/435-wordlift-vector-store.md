# **WordLift** Vektör Deposu

---
title: **WordLift** Vektör Deposu
 | LlamaIndex OSS Documentation
---

## Giriş

Bu komut dosyası, bir ürün web sitesinin nasıl taranacağını, ilgili bilgilerin nasıl çıkarılacağını, SEO dostu bir Bilgi Grafiği (Knowledge Graph - PDP'lerin ve PLP'lerin yapılandırılmış bir temsili) oluşturulacağını ve bunu geliştirilmiş arama ve kullanıcı deneyimi için nasıl kullanılacağını göstermektedir.

### Temel Özellikler ve Kütüphaneler:

- Web scraping (Advertools)
- Knowledge Graph creation for Product Detail Pages (PDPs) and Product Listing Pages (PLPs) - WordLift
- Product recommendations (WordLift Neural Search)
- Shopping assistant creation (WordLift + LlamaIndex 🦙)

Bu yaklaşım, e-ticaret siteleri için SEO performansını ve kullanıcı etkileşimini artırır.

Nasıl çalıştığı hakkında daha fazlasını buradan öğrenin:

- <https://www.youtube.com/watch?v=CH-ir1MTAwQ>
- <https://wordlift.io/academy-entries/mastering-serp-analysis-knowledge-graphs>

|                                                                                                    |                                                                                                                                                                                                   |
| -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [![](https://wordlift.io/wp-content/uploads/2018/07/logo-assets-510x287.png)](https://wordlift.io) | by [Andrea Volpini ](https://wordlift.io/blog/en/entity/andrea-volpini)and [David Riccitelli](https://wordlift.io/blog/en/entity/david-riccitelli) MIT License *Last updated: **Jul 31st, 2024*** |



# Kurulum

```
!pip install advertools -q
!pip install -U wordlift-client # 🎉 first time on stage 🎉
!pip install rdflib -q
```

```
# Standart kütüphane içe aktarmaları
import json
import logging
import os
import re
import urllib.parse
import requests
from typing import List, Optional


# Üçüncü taraf içe aktarmalar
import advertools as adv
import pandas as pd
import nest_asyncio


# RDFLib içe aktarmaları
from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import SDO, Namespace, DefinedNamespace


# WordLift istemci içe aktarmaları
import wordlift_client
from wordlift_client import Configuration, ApiClient
from wordlift_client.rest import ApiException
from wordlift_client.api.dataset_api import DatasetApi
from wordlift_client.api.entities_api import EntitiesApi
from wordlift_client.api.graph_ql_api import GraphQLApi
from wordlift_client.models.graphql_request import GraphqlRequest
from wordlift_client.models.page_vector_search_query_response_item import (
    PageVectorSearchQueryResponseItem,
)
from wordlift_client.models.vector_search_query_request import (
    VectorSearchQueryRequest,
)
from wordlift_client.api.vector_search_queries_api import (
    VectorSearchQueriesApi,
)




# Asenkron programlama
import asyncio


# Günlük kaydını (logging) ayarlama
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# nest_asyncio uygula
nest_asyncio.apply()
```

```
WORDLIFT_KEY = os.getenv("WORDLIFT_KEY")
OPENAI_KEY = os.getenv("OPENAI_KEY")
```

# Advertools ile Web Sitesini Tarama

```
# Adım 1: Web sitesi yapısını tanımlayın
# -----------------------------------


# İki tür sayfa ile çalışıyoruz:
 # 1. Ürün Listeleme Sayfaları (PLP): https://product-finder.wordlift.io/product-category/bags/
 # 2. Ürün Detay Sayfaları (PDP): https://product-finder.wordlift.io/product/1980s-marco-polo-crossbody-bag-in-black/
 
 # Ürün açıklaması bu XPath'te bulunabilir:
 # /html/body/div[1]/div/div/div/div/div[1]/div/div[3]/div/div[2]/div[2]/div[1]/p/text()
 # Fiyat burada:
 # /html/body/div[1]/div/div/div/div/div[1]/div/div[3]/div/div[2]/p/span/bdi/text()
 # Kategori burada:
 # //span[contains(@class, 'breadcrumb')]/a/text()


# Adım 2: Taramayı ayarlayın
# ------------------------




def crawl_website(url, output_file, num_pages=10):
    logger.info(f"Starting crawl of {url}")
    adv.crawl(
        url,
        output_file,
        follow_links=True,
        custom_settings={
            "CLOSESPIDER_PAGECOUNT": num_pages,
            "USER_AGENT": "WordLiftBot/1.0 (Maven Project)",
            "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
            "DOWNLOAD_DELAY": 1,
            "ROBOTSTXT_OBEY": False,
        },
        xpath_selectors={
            "product_description": "/html/body/div[1]/div/div/div/div/div[1]/div/div[3]/div/div[2]/div[2]/div[1]/p/text()",
            "product_price": "/html/body/div[1]/div/div/div/div/div[1]/div/div[3]/div/div[2]/p/span/bdi/text()",
            "product_category": "//span[@class='posted_in']/a/text()",
        },
    )
    logger.info(f"Crawl completed. Results saved to {output_file}")




# Adım 3: URL kalıplarını analiz edin
# ----------------------------




def analyze_url_patterns(df):
    df["page_type"] = df["url"].apply(
        lambda x: "PLP"
        if "/product-category/" in x
        else ("PDP" if "/product/" in x else "Other")
    )
    logger.info(
        f"Found {(df['page_type'] == 'PLP').sum()} PLPs and {(df['page_type'] == 'PDP').sum()} PDPs"
    )
    return df




# Adım 4: Sayfa verilerini çıkarın
# ----------------------------




def extract_page_data(df):
    extracted_data = []
    for _, row in df.iterrows():
        page = {
            "url": row["url"],
            "title": row["title"],
            "page_type": row["page_type"],
            "meta_description": row.get("meta_description", ""),
            "og_title": row.get("og_title", ""),
            "og_description": row.get("og_description", ""),
            "h1": ", ".join(row.get("h1", []))
            if isinstance(row.get("h1"), list)
            else row.get("h1", ""),
            "h2": ", ".join(row.get("h2", []))
            if isinstance(row.get("h2"), list)
            else row.get("h2", ""),
        }


        if row["page_type"] == "PDP":
            page.update(
                {
                    "product_description": ", ".join(
                        row.get("product_description", [])
                    )
                    if isinstance(row.get("product_description"), list)
                    else row.get("product_description", ""),
                    "product_price": ", ".join(row.get("product_price", []))
                    if isinstance(row.get("product_price"), list)
                    else row.get("product_price", ""),
                    "product_category": ", ".join(
                        row.get("product_category", [])
                    )
                    if isinstance(row.get("product_category"), list)
                    else row.get("product_category", ""),
                }
            )
        elif row["page_type"] == "PLP":
            # H1 içeriğinden kategoriyi ayıkla (parse et)
            h1_content = (
                row.get("h1", [""])[0]
                if isinstance(row.get("h1"), list)
                else row.get("h1", "")
            )
            category = (
                h1_content.split("@@")[-1]
                if "@@" in h1_content
                else h1_content.replace("Category: ", "").strip()
            )
            page["category_name"] = category


        extracted_data.append(page)


    return pd.DataFrame(extracted_data)
```

# WordLift ile Bilgi Grafiği (KG) Oluşturma 🕸

```
# Adım 5: WordLift istemcisini yapılandırın
# ----------------------------


# WordLift anahtarınızı kullanarak WordLift API istemcisi için bir yapılandırma nesnesi oluşturun.
configuration = Configuration(host="https://api.wordlift.io")
configuration.api_key["ApiKey"] = WORDLIFT_KEY
configuration.api_key_prefix["ApiKey"] = "Key"


EXAMPLE_PRIVATE_NS = Namespace("https://ns.example.org/private/")


BASE_URI = "http://data.wordlift.io/[dataset_id]/"
```

```
# Adım 6: Bilgi Grafiği'ni (KG) ve yerleştirmeleri (embeddings) oluşturun
# ----------------------------




async def cleanup_knowledge_graph(api_client):
    dataset_api = wordlift_client.DatasetApi(api_client)
    try:
        # Hepsini sil
        await dataset_api.delete_all_entities()
    except Exception as e:
        print(
            "Exception when calling DatasetApi->delete_all_entities: %s\n" % e
        )




async def create_entity(entities_api, entity_data):
    g = Graph().parse(data=json.dumps(entity_data), format="json-ld")
    body = g.serialize(format="application/rdf+xml")
    await entities_api.create_or_update_entities(
        body=body, _content_type="application/rdf+xml"
    )




def replace_url(original_url: str) -> str:
    old_domain = "https://product-finder.wordlift.io/"
    new_domain = "https://data-science-with-python-for-seo.wordlift.dev/"


    if original_url.startswith(old_domain):
        return original_url.replace(old_domain, new_domain, 1)
    else:
        return original_url




def create_entity_uri(url):
    parsed_url = urllib.parse.urlparse(url)
    path = parsed_url.path.strip("/")
    path_parts = path.split("/")
    fragment = parsed_url.fragment


    if "product" in path_parts:
        # Bu bir ürün sayfası veya ürün teklifidir
        product_id = path_parts[-1]  # Get the last part of the path
        if fragment == "offer":
            return f"{BASE_URI}offer_{product_id}"
        else:
            return f"{BASE_URI}product_{product_id}"
    elif "product-category" in path_parts:
        # Bu bir ürün listeleme sayfasıdır (PLP)
        category = path_parts[-1]  # Get the last part of the path
        return f"{BASE_URI}plp_{category}"
    else:
        # Diğer her türlü sayfa için
        safe_path = "".join(c if c.isalnum() else "_" for c in path)
        if fragment == "offer":
            return f"{BASE_URI}offer_{safe_path}"
        else:
            return f"{BASE_URI}page_{safe_path}"




def clean_price(price_str):
    if not price_str or price_str == "N/A":
        return None
    if isinstance(price_str, (int, float)):
        return float(price_str)
    try:
        # Ondalık nokta dışındaki sayısal olmayan karakterleri kaldırın
        cleaned_price = "".join(
            char for char in str(price_str) if char.isdigit() or char == "."
        )
        return float(cleaned_price)
    except ValueError:
        logger.warning(f"Could not convert price: {price_str}")
        return None




def create_product_entity(row, dataset_uri):
    url = replace_url(row["url"])
    product_entity_uri = create_entity_uri(url)


    entity_data = {
        "@context": "http://schema.org",
        "@type": "Product",
        "@id": product_entity_uri,
        "url": url,
        "name": row["title"]
        if not pd.isna(row["title"])
        else "Untitled Product",
        "urn:meta:requestEmbeddings": [
            "http://schema.org/name",
            "http://schema.org/description",
        ],
    }


    if not pd.isna(row.get("product_description")):
        entity_data["description"] = row["product_description"]


    if not pd.isna(row.get("product_price")):
        price = clean_price(row["product_price"])
        if price is not None:
            # Create offer ID as a sub-resource of the product ID
            offer_entity_uri = f"{product_entity_uri}/offer_1"
            entity_data["offers"] = {
                "@type": "Offer",
                "@id": offer_entity_uri,
                "price": str(price),
                "priceCurrency": "GBP",
                "availability": "http://schema.org/InStock",
                "url": url,
            }


    if not pd.isna(row.get("product_category")):
        entity_data["category"] = row["product_category"]


    custom_attributes = {
        key: row[key]
        for key in [
            "meta_description",
            "og_title",
            "og_description",
            "h1",
            "h2",
        ]
        if not pd.isna(row.get(key))
    }
    if custom_attributes:
        entity_data[str(EXAMPLE_PRIVATE_NS.attributes)] = json.dumps(
            custom_attributes
        )


    return entity_data




def create_collection_entity(row, dataset_uri):
    url = replace_url(row["url"])
    entity_uri = create_entity_uri(url)


    entity_data = {
        "@context": "http://schema.org",
        "@type": "CollectionPage",
        "@id": entity_uri,
        "url": url,
        "name": row["category_name"] or row["title"],
    }


    custom_attributes = {
        key: row[key]
        for key in [
            "meta_description",
            "og_title",
            "og_description",
            "h1",
            "h2",
        ]
        if row.get(key)
    }
    if custom_attributes:
        entity_data[str(EXAMPLE_PRIVATE_NS.attributes)] = json.dumps(
            custom_attributes
        )


    return entity_data




async def build_knowledge_graph(df, dataset_uri, api_client):
    entities_api = EntitiesApi(api_client)


    for _, row in df.iterrows():
        try:
            if row["page_type"] == "PDP":
                entity_data = create_product_entity(row, dataset_uri)
            elif row["page_type"] == "PLP":
                entity_data = create_collection_entity(row, dataset_uri)
            else:
                logger.warning(
                    f"Skipping unknown page type for URL: {row['url']}"
                )
                continue


            if entity_data is None:
                logger.warning(
                    f"Skipping page due to missing critical data: {row['url']}"
                )
                continue


            await create_entity(entities_api, entity_data)
            logger.info(
                f"Created entity for {row['page_type']}: {row['title']}"
            )
        except Exception as e:
            logger.error(
                f"Error creating entity for {row['page_type']}: {row['title']}"
            )
            logger.error(f"Error: {str(e)}")
```

# Gösteriyi Başlat / Çalıştırma

```
# ----------------------------
# Ana Yürütme (Main Execution)
# ----------------------------


# Global yapılandırma değişkenleri
CRAWL_URL = "https://product-finder.wordlift.io/"
OUTPUT_FILE = "crawl_results.jl"




async def main():
    # Adım 1: Web sitesini tara
    crawl_website(CRAWL_URL, OUTPUT_FILE)


    # Adım 2: Taranan verileri yükle
    df = pd.read_json(OUTPUT_FILE, lines=True)


    # Adım 3: URL kalıplarını analiz et
    df = analyze_url_patterns(df)


    # Adım 4: Sayfa verilerini çıkar
    pages_df = extract_page_data(df)


    async with ApiClient(configuration) as api_client:
        # Mevcut bilgi grafiğini temizle
        try:
            await cleanup_knowledge_graph(api_client)
            logger.info(f"Knowledge Graph Cleaned Up")
        except Exception as e:
            logger.error(
                f"Failed to clean up the existing Knowledge Graph: {str(e)}"
            )
            return  # Exit if cleanup fails


        # Yeni bilgi grafiğini oluşturun
        await build_knowledge_graph(pages_df, CRAWL_URL, api_client)


    logger.info("Knowledge graph building completed.")




if __name__ == "__main__":
    asyncio.run(main())
```

## Şimdi GraphQL kullanarak KG'deki ürünleri sorgulayalım

```
async def perform_graphql_query(api_client):
    graphql_api = GraphQLApi(api_client)
    query = """
    {
        products(rows: 20) {
            id: iri
            category: string(name:"schema:category")
            name: string(name:"schema:name")
            description: string(name:"schema:description")
            url: string(name:"schema:url")
        }
    }
    """
    request = GraphqlRequest(query=query)


    try:
        response = await graphql_api.graphql_using_post(body=request)
        print("GraphQL Query Results:")
        print(json.dumps(response, indent=2))
    except Exception as e:
        logger.error(f"An error occurred during GraphQL query: {e}")




async with ApiClient(configuration) as api_client:
    # Adım 6: GraphQL sorgusunu gerçekleştirin
    await perform_graphql_query(api_client)
    logger.info("Knowledge graph building and GraphQL query completed.")
```

# Bilgi Grafiğini (Knowledge Graph) Değerlendirme

E-ticaret web sitemiz için ürün yerleştirmeleriyle tamamlanmış bir Bilgi Grafiği'ni (Knowledge Graph) başarıyla oluşturduğumuza göre, kullanıcı deneyimini ve işlevselliği artırmak için bundan yararlanabiliriz. Her bir ürün için oluşturduğumuz yerleştirmeler, anlamsal benzerlik aramaları yapmamıza ve daha akıllı sistemler kurmamıza olanak tanır.

## Web Sayfalarınıza Yapılandırılmış Veri Ekleme

Bu bölümde, WordLift'in veri API'si üzerinde basit bir test gerçekleştireceğiz. Bu API, Bilgi Grafiği'nden (KG) gelen yapılandırılmış veri işaretlemesini web sayfalarınıza eklemek için kullanılır. Yapılandırılmış veriler, arama motorlarının içeriğinizi daha iyi anlamasına yardımcı olur, bu da potansiyel olarak arama sonuçlarında zengin snippet'lere ve gelişmiş SEO'ya yol açar.
 
 Bu not defteri için, bir demo e-ticaret web sitesinde önceden yapılandırılmış bir KG kullanıyoruz. Fiktif bir URL'yi referans alacağız: `https://data-science-with-python-for-seo.wordlift.dev`.
 
 WordLift'in veri API'sini çağırırken, sadece bir URL iletiriz ve karşılık gelen JSON-LD (JavaScript Object Notation for Linked Data) çıktısını alırız. Bu yapılandırılmış veriler tipik olarak e-ticaret siteleri için ürün ayrıntıları, fiyatlandırma ve stok durumu gibi bilgileri içerir.
 
 Aşağıdaki `get_json_ld_from_url()` işlevi bu süreci göstermektedir. Girdi olarak bir URL alır ve yapılandırılmış veriyi web sayfanıza eklenmeye hazır JSON-LD formatında döndürür.

```
def get_json_ld_from_url(url):
    # 'https://api.wordlift.io/data/https/' öneki ile API URL'sini oluşturun
    api_url = "https://api.wordlift.io/data/https/" + url.replace(
        "https://", ""
    )


    # API'ye GET isteği gönderin
    response = requests.get(api_url)


    # İsteğin başarılı olup olmadığını kontrol edin
    if response.status_code == 200:
        # Yanıttan JSON-LD verisini ayrıştırın
        json_ld = response.json()
        return json_ld
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None




def pretty_print_json(json_obj):
    # JSON nesnesini güzelce yazdırın (pretty print)
    print(json.dumps(json_obj, indent=4))
```

```
# Hadi bir test çalıştıralım
url = "https://data-science-with-python-for-seo.wordlift.dev/product/100-pure-deluxe-travel-pack-duo-2/"
json_ld = get_json_ld_from_url(url)
json_ld
```

## WordLift Neural Search Kullanarak Benzer Ürünlerin Bağlantılarını Oluşturma

Ürün yerleştirmelerimiz hazır olduğunda, kullanıcılara benzer ürünler önermek için artık WordLift'in Nöral Arama (Neural Search) yeteneklerinden yararlanabiliriz. Bu özellik, kullanıcı etkileşimini önemli ölçüde artırır ve anlamsal benzerliğe dayalı ilgili ürünleri göstererek satışları potansiyel olarak yükseltebilir.
 
 Geleneksel anahtar kelime eşleştirmesinin aksine, anlamsal benzerlik ürün açıklamalarının bağlamını ve anlamını dikkate alır. Bu yaklaşım, ürünler tam olarak aynı anahtar kelimeleri paylaşmasa bile daha incelikli ve doğru önerilere olanak tanır.
 
 Daha önce tanımladığımız `get_top_k_similar_urls` işlevi bu işlevselliği uygular. Bir ürün URL'si alır ve benzerlik puanlarına göre sıralanmış anlamsal olarak benzer ürünlerin bir listesini döndürür.
 
 Örneğin, bir kullanıcı kırmızı bir pamuklu tişört görüntülüyorsa, bu özellik farklı renklerdeki diğer pamuklu tişörtleri veya farklı malzemelerden yapılmış benzer stillerdeki üstleri önerebilir. Bu, kullanıcı için daha sezgisel ve ilgi çekici bir alışveriş deneyimi oluşturur.
 
 Bu Nöral Arama özelliğini uygulayarak, daha kişiselleştirilmiş ve verimli bir alışveriş deneyimi yaratabiliyoruz, bu da potansiyel olarak artan kullanıcı memnuniyetine ve daha yüksek dönüşüm oranlarına yol açar.

```
async def get_top_k_similar_urls(configuration, query_url: str, top_k: int):
    request = VectorSearchQueryRequest(
        query_url=query_url,
        similarity_top_k=top_k,
    )


    async with wordlift_client.ApiClient(configuration) as api_client:
        api_instance = VectorSearchQueriesApi(api_client)
        try:
            page = await api_instance.create_query(
                vector_search_query_request=request
            )
            return [
                {
                    "url": item.id,
                    "name": item.text.split("\n")[0],
                    "score": item.score,
                }
                for item in page.items
                if item.id and item.text
            ]
        except Exception as e:
            logger.error(f"Error querying for entities: {e}", exc_info=True)
            return None
```

```
top_k = 10
url = "https://data-science-with-python-for-seo.wordlift.dev/product/100-mineral-sunscreen-spf-30/"
similar_urls = await get_top_k_similar_urls(
    configuration, query_url=url, top_k=top_k
)
print(json.dumps(similar_urls, indent=2))
```

## LlamaIndex Kullanarak E-ticaret Web Sitesi için Chatbot Oluşturma 🦙

Oluşturduğumuz Bilgi Grafiği, akıllı bir chatbot oluşturmak için mükemmel bir temel görevi görür. LlamaIndex (eski adıyla GPT Index), Büyük Dil Modellerinde (LLM'ler) özel veya alan özgü verileri almamıza, yapılandırmamıza ve bunlara erişmemize olanak tanıyan güçlü bir veri çerçevesidir. LlamaIndex ile, ürün kataloğumuzu anlayan ve müşterilere etkili bir şekilde yardımcı olabilen, bağlam duyarlı bir chatbot oluşturabiliriz.
 
 Bilgi Grafiğimizle birlikte LlamaIndex'ten yararlanarak, doğrudan sorgulara yanıt veren bir chatbot geliştirebiliriz. Bu chatbot, ürün kataloğu hakkında bir anlayışa sahip olacak ve aşağıdakileri yapabilecektir:
 
 1. Ürün özellikleri, stok durumu ve fiyatlandırma hakkındaki soruları yanıtlamak
 2. Müşteri tercihlerine göre kişiselleştirilmiş ürün önerileri yapmak
 3. Benzer ürünler arasında karşılaştırmalar sağlamak
 
 Bu yaklaşım, müşterilerle daha doğal ve yardımcı etkileşimlere yol açarak alışveriş deneyimlerini geliştirir. Chatbot, Bilgi Grafiğimizdeki yapılandırılmış verilerden yararlanabilir ve LLM aracılığıyla ilgili bilgileri verimli bir şekilde getirmek ve sunmak için LlamaIndex'i kullanabilir.
 
 İzleyen bölümlerde, Bilgi Grafiği verilerimizle LlamaIndex'i kurma ve e-ticaret müşterilerimize akıllıca yardımcı olabilecek bir chatbot oluşturma sürecini inceleyeceğiz.

### `LlamaIndex` ve `WordLiftVectorStore` Kurulumu 💪

```
%%capture
!pip install llama-index
!pip install -U 'git+https://github.com/wordlift/llama_index.git#egg=llama-index-vector-stores-wordlift&subdirectory=llama-index-integrations/vector_stores/llama-index-vector-stores-wordlift'
!pip install llama-index-embeddings-nomic
```

```
# gerekli modülleri içe aktarın
from llama_index.vector_stores.wordlift import WordliftVectorStore
from llama_index.core import VectorStoreIndex
```

### Sorgu Motorumuz için NomicEmbeddings'i Ayarlama

Nomic, metin yerleştirme (text embedding) yeteneklerine önemli iyileştirmeler getiren yerleştirme modellerinin v1.5 🪆🪆🪆 sürümünü yayınladı. Yerleştirmeler, metnin anlamsal anlamını yakalayan sayısal temsillerdir ve sistemimizin sorguların ve belgelerin içeriğini anlamasına ve karşılaştırmasına olanak tanır.
 
 **Nomic v1.5**'in temel özellikleri şunları içerir:
 
 - 64 ile 768 boyut arasında değişen değişken boyutlu yerleştirmeler
 - İç içe geçmiş temsillere izin veren Matryoshka öğrenimi
 - 8192 token'lık genişletilmiş bir bağlam boyutu
 
 WordLift'te bu gelişmiş özellikler nedeniyle NomicEmbeddings kullanıyoruz ve şimdi LlamaIndex'i kullanıcı sorgularını kodlarken de bunu kullanacak şekilde yapılandırıyoruz. Tüm yapımızdaki yerleştirme modellerindeki bu tutarlılık, Bilgi Grafiğimiz ile sorgu anlama süreci arasında daha iyi bir uyum sağlar.
 
 NomicEmbeddings hakkında daha fazla bilgi [burada](https://www.nomic.ai/blog/posts/nomic-embed-matryoshka) bulunabilir.

Ücretsiz anahtarınızı almak için [buraya gidin](https://atlas.nomic.ai/).

```
from llama_index.embeddings.nomic import NomicEmbedding


nomic_api_key = os.getenv("NOMIC_KEY")


embed_model = NomicEmbedding(
    api_key=nomic_api_key,
    dimensionality=128,
    model_name="nomic-embed-text-v1.5",
)


embedding = embed_model.get_text_embedding("Hey Ho SEO!")
len(embedding)
```

Yanıt oluşturmak için varsayılan LLM olarak OpenAI kullanacağız. Elbette mevcut diğer herhangi bir LLM'i de kullanabilirdik.

```
# Çevre değişkenini (environment variable) ayarla
os.environ["OPENAI_API_KEY"] = OPENAI_KEY
```

Şimdi Bilgi Grafiğimizden gelen verileri kullanarak WordliftVectorStore'u kuralım.

```
# WL Anahtarımızı kullanarak WordliftVectorStore'u yapılandıralım
vector_store = WordliftVectorStore(key=API_KEY)


# Vektör deposundan bir indeks oluşturun
index = VectorStoreIndex.from_vector_store(
    vector_store, embed_model=embed_model
)


# Bir sorgu motoru oluşturun
query_engine = index.as_query_engine()
```

```
query1 = "Can you give me a product similar to the facial puff? Please add the URL also"
result1 = query_engine.query(query1)


print(result1)
```

```
# Sorguları işlemek için işlev (function)
def query_engine(query):
    # Vektör deposundan bir indeks oluşturun
    index = VectorStoreIndex.from_vector_store(
        vector_store, embed_model=embed_model
    )


    # Bir sorgu motoru oluşturun
    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    return response




# Etkileşimli sorgu döngüsü
while True:
    user_query = input("Enter your query (or 'quit' to exit): ")
    if user_query.lower() == "quit":
        break
    result = query_engine(user_query)
    print(result)
    print("\n---\n")
```
