# Oracle AI Vector Search: Gömmeler (Embeddings) Oluşturma

Oracle AI Vector Search, anahtar kelimeler yerine anlambilime (semantics) dayalı olarak verileri sorgulamanıza olanak tanıyan Yapay Zeka (AI) iş yükleri için tasarlanmıştır.
Oracle AI Vector Search'ün en büyük avantajlarından biri, yapılandırılmamış veriler üzerindeki anlamsal aramanın, iş verileri üzerindeki ilişkisel arama ile tek bir sistemde birleştirilebilmesidir.
Bu sadece güçlü olmakla kalmaz, aynı zamanda önemli ölçüde daha etkilidir çünkü özel bir vektör veritabanı eklemenize gerek kalmaz ve birden fazla sistem arasındaki veri parçalanması sorununu ortadan kaldırır.

Buna ek olarak vektörleriniz, Oracle Database'in aşağıdakiler gibi en güçlü özelliklerinden yararlanabilir:

 * [Bölümleme Desteği (Partitioning Support)](https://www.oracle.com/database/technologies/partitioning.html)
 * [Real Application Clusters ölçeklenebilirliği](https://www.oracle.com/database/real-application-clusters/)
 * [Exadata akıllı taramaları (smart scans)](https://www.oracle.com/database/technologies/exadata/software/smartscan/)
 * [Coğrafi olarak dağıtılmış veritabanları genelinde Shard işleme](https://www.oracle.com/database/distributed-database/)
 * [İşlemler (Transactions)](https://docs.oracle.com/en/database/oracle/oracle-database/23/cncpt/transactions.html)
 * [Paralel SQL](https://docs.oracle.com/en/database/oracle/oracle-database/21/vldbg/parallel-exec-intro.html#GUID-D28717E4-0F77-44F5-BB4E-234C31D4E4BA)
 * [Olağanüstü Durum Kurtarma (Disaster recovery)](https://www.oracle.com/database/data-guard/)
 * [Güvenlik](https://www.oracle.com/security/database-security/)
 * [Oracle Machine Learning](https://www.oracle.com/artificial-intelligence/database-machine-learning/)
 * [Oracle Graph Database](https://www.oracle.com/database/integrated-graph-database/)
 * [Oracle Spatial and Graph](https://www.oracle.com/database/spatial/)
 * [Oracle Blockchain](https://docs.oracle.com/en/database/oracle/oracle-database/23/arpls/dbms_blockchain_table.html#GUID-B469E277-978E-4378-A8C1-26D3FF96C9A6)
 * [JSON](https://docs.oracle.com/en/database/oracle/oracle-database/23/adjsn/json-in-oracle-database.html)


Bu kılavuz, OracleEmbeddings kullanarak belgeleriniz için gömmeler oluşturmak amacıyla Oracle AI Vector Search içindeki Gömme Yeteneklerinin nasıl kullanılacağını göstermektedir.

Oracle Database'e yeni başlıyorsanız, veritabanı ortamınızı kurmaya yönelik harika bir giriş sağlayan [ücretsiz Oracle 23 AI](https://www.oracle.com/database/free/#resources) sürümünü keşfetmeyi düşünebilirsiniz. Veritabanıyla çalışırken, varsayılan olarak sistem kullanıcısını (system user) kullanmaktan kaçınmanız genellikle tavsiye edilir; bunun yerine gelişmiş güvenlik ve özelleştirme için kendi kullanıcınızı oluşturabilirsiniz. Kullanıcı oluşturmaya ilişkin ayrıntılı adımlar için, Oracle'da bir kullanıcının nasıl kurulacağını da gösteren [uçtan uca kılavuzumuza](https://github.com/run-llama/llama_index/blob/main/docs/examples/cookbooks/oracleai_demo.ipynb) bakabilirsiniz. Ek olarak, veritabanı güvenliğini etkili bir şekilde yönetmek için kullanıcı yetkilerini (privileges) anlamak çok önemlidir. Kullanıcı hesaplarını ve güvenliğini yönetme konusundaki resmi [Oracle kılavuzundan](https://docs.oracle.com/en/database/oracle/oracle-database/19/admqs/administering-user-accounts-and-security.html#GUID-36B21D72-1BBB-46C9-A0C9-F0D2A8591B8D) bu konu hakkında daha fazla bilgi edinebilirsiniz.

### Ön Koşullar

Llama_index'in Oracle AI Vector Search ile entegrasyonunu kolaylaştırmak için Oracle Python Client sürücüsünün kurulu olduğundan emin olun.


```python
%pip install llama-index-embeddings-oracleai
```

### Oracle Database'e Bağlanma
Aşağıdaki örnek kod, Oracle Database'e nasıl bağlanılacağını gösterecektir. Varsayılan olarak python-oracledb, doğrudan Oracle Database'e bağlanan 'Thin' modunda çalışır. Bu mod Oracle Client kütüphanelerine ihtiyaç duymaz. Ancak python-oracledb bu kütüphaneleri kullandığında bazı ek işlevler kullanılabilir hale gelir. Oracle Client kütüphaneleri kullanıldığında python-oracledb'nin 'Thick' modunda olduğu söylenir. Her iki mod da Python Database API v2.0 Spesifikasyonunu destekleyen kapsamlı işlevselliğe sahiptir. Her modda desteklenen özellikleri anlatan şu [kılavuza](https://python-oracledb.readthedocs.io/en/latest/user_guide/appendix_a.html#featuresummary) bakabilirsiniz. Thin modunu kullanamıyorsanız Thick moduna geçmek isteyebilirsiniz.


```python
import sys

import oracledb

# Aşağıdaki değişkenleri Oracle veritabanı kimlik bilgileriniz ve bağlantı ayrıntılarınızla güncelleyin
username = "<kullanıcı_adı>"
password = "<şifre>"
dsn = "<ana_makine_adı>/<servis_adı>"

try:
    conn = oracledb.connect(user=username, password=password, dsn=dsn)
    print("Bağlantı başarılı!")
except Exception as e:
    print("Bağlantı başarısız!")
    sys.exit(1)
```

Gömme oluşturma için, veritabanı içinde gömme oluşturma ve OcigenAI, Hugging Face ve OpenAI gibi üçüncü taraf hizmetler dahil olmak üzere kullanıcılara çeşitli sağlayıcı seçenekleri sunulur. Üçüncü taraf sağlayıcıları tercih eden kullanıcılar, gerekli kimlik doğrulama bilgilerini içeren kimlik bilgileri oluşturmalıdır. Alternatif olarak, kullanıcılar sağlayıcı olarak 'database' seçeneğini belirlerlerse, gömmeleri kolaylaştırmak için Oracle Database'e bir ONNX modeli yüklemeleri gerekir.

### ONNX Modelini Yükleme

Oracle, kullanıcılara tescilli veritabanı çözümleri ile OCIGENAI ve HuggingFace gibi üçüncü taraf hizmetler arasında seçim yapma imkanı vererek çeşitli gömme sağlayıcılarını destekler. Bu seçim, gömmelerin oluşturulması ve yönetilmesi metodolojisini belirler.

***Önemli***: Kullanıcılar veritabanı seçeneğini tercih ederlerse, Oracle Database'e bir ONNX modeli yüklemeleri gerekir. Aksine, gömme oluşturma için üçüncü taraf bir sağlayıcı seçilirse, Oracle Database'e bir ONNX modeli yüklemek gerekli değildir.

Bir ONNX modelini doğrudan Oracle içinde kullanmanın önemli bir avantajı, verileri dış taraflara iletme ihtiyacını ortadan kaldırarak sunduğu gelişmiş güvenlik ve performanstır. Ek olarak bu yöntem, genellikle ağ veya REST API çağrılarıyla ilişkili olan gecikmeleri (latency) önler.

Aşağıda, Oracle Database'e bir ONNX modeli yüklemek için örnek kod verilmiştir:


```python
from llama_index.embeddings.oracleai import OracleEmbeddings

# Lütfen ilgili bilgilerinizle güncelleyin
# Sistemde onnx dosyanız olduğundan emin olun
onnx_dir = "DEMO_DIR"
onnx_file = "tinybert.onnx"
model_name = "demo_model"

try:
    OracleEmbeddings.load_onnx_model(conn, onnx_dir, onnx_file, model_name)
    print("ONNX modeli yüklendi.")
except Exception as e:
    print("ONNX modeli yükleme başarısız!")
    sys.exit(1)
```

### Kimlik Bilgisi Oluşturma (Create Credential)

Gömmeler oluşturmak için üçüncü taraf sağlayıcılar seçildiğinde, sağlayıcının uç noktalarına güvenli bir şekilde erişmek için kullanıcıların kimlik bilgileri oluşturması gerekir.

***Önemli:*** Gömme oluşturmak için 'database' sağlayıcısını seçtiğinizde herhangi bir kimlik bilgisine (credentials) gerek yoktur. Ancak, kullanıcılar üçüncü taraf bir sağlayıcıyı kullanmaya karar verirlerse, seçilen sağlayıcıya özgü kimlik bilgileri oluşturmalıdırlar.

Aşağıda açıklayıcı bir örnek verilmiştir:


```python
try:
    cursor = conn.cursor()
    cursor.execute(
        """
       declare
           jo json_object_t;
       begin
           -- HuggingFace
           dbms_vector_chain.drop_credential(credential_name  => 'HF_CRED');
           jo := json_object_t();
           jo.put('access_token', '<erişim_belirteci>');
           dbms_vector_chain.create_credential(
               credential_name   =>  'HF_CRED',
               params            => json(jo.to_string));

           -- OCIGENAI
           dbms_vector_chain.drop_credential(credential_name  => 'OCI_CRED');
           jo := json_object_t();
           jo.put('user_ocid','<user_ocid>');
           jo.put('tenancy_ocid','<tenancy_ocid>');
           jo.put('compartment_ocid','<compartment_ocid>');
           jo.put('private_key','<private_key>');
           jo.put('fingerprint','<fingerprint>');
           dbms_vector_chain.create_credential(
               credential_name   => 'OCI_CRED',
               params            => json(jo.to_string));
       end;
       """
    )
    cursor.close()
    print("Kimlik bilgileri oluşturuldu.")
except Exception as ex:
    cursor.close()
    raise
```

### Gömmeler Oluşturma (Generate Embeddings)

Oracle AI Vector Search, yerel olarak barındırılan ONNX modellerini veya üçüncü taraf API'lerini kullanarak gömmeler oluşturmak için birden fazla yöntem sunar. Bu alternatiflerin yapılandırılmasına ilişkin kapsamlı talimatlar için lütfen [Oracle AI Vector Search Kılavuzuna](https://docs.oracle.com/en/database/oracle/oracle-database/23/arpls/dbms_vector_chain1.html#GUID-C6439E94-4E86-4ECD-954E-4B73D53579DE) bakın.

***Not:*** Kullanıcıların, ONNX modeli kullanan 'database' sağlayıcısı hariç, üçüncü taraf gömme oluşturma sağlayıcılarını kullanmak için bir ara sunucu (proxy) yapılandırması gerekebilir.


```python
# özet ve gömücü nesnesini örneklendirirken kullanılacak proxy
proxy = "<ara_sunucu>"
```

Aşağıdaki örnek kod, gömmelerin nasıl oluşturulacağını gösterecektir:


```python
from llama_index.embeddings.oracleai import OracleEmbeddings

"""
# ocigenai kullanarak
embedder_params = {
    "provider": "ocigenai",
    "credential_name": "OCI_CRED",
    "url": "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/20231130/actions/embedText",
    "model": "cohere.embed-english-light-v3.0",
}

# huggingface kullanarak
embedder_params = {
    "provider": "huggingface", 
    "credential_name": "HF_CRED", 
    "url": "https://api-inference.huggingface.co/pipeline/feature-extraction/", 
    "model": "sentence-transformers/all-MiniLM-L6-v2", 
    "wait_for_model": "true"
}
"""

# Oracle Database'e yüklenen ONNX modelini kullanarak
embedder_params = {"provider": "database", "model": "demo_model"}

# Gerekli değilse proxy'yi kaldırın
embedder = OracleEmbeddings(conn=conn, params=embedder_params, proxy=proxy)
embed = embedder._get_text_embedding("Merhaba Dünya!")

""" doğrulama """
print(f"OracleEmbeddings tarafından oluşturulan gömme: {embed}")
```

### Uçtan Uca Demo
Oracle AI Vector Search yardımıyla uçtan uca bir RAG boru hattı (pipeline) oluşturmak için lütfen tam demo kılavuzumuza bakın: [Oracle AI Vector Search Uçtan Uca Demo Kılavuzu](https://github.com/run-llama/llama_index/blob/main/docs/examples/cookbooks/oracleai_demo.ipynb).