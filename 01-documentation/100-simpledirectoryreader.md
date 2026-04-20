# SimpleDirectoryReader

`SimpleDirectoryReader`, yerel dosyalardan LlamaIndex'e veri yüklemenin en basit yoludur. Üretim kullanım durumları için muhtemelen [LlamaHub](https://llamahub.ai/) üzerinde bulunan birçok Okuyucudan (Reader) birini kullanmak isteyeceksiniz, ancak `SimpleDirectoryReader` başlamak için harika bir yoldur.

## Desteklenen dosya türleri

Varsayılan olarak `SimpleDirectoryReader`, bulduğu tüm dosyaları metin olarak değerlendirerek okumaya çalışacaktır. Düz metne ek olarak, dosya uzantısına göre otomatik olarak algılanan aşağıdaki dosya türlerini açıkça destekler:

-   .csv - virgülle ayrılmış değerler
-   .docx - Microsoft Word
-   .epub - EPUB e-kitap formatı
-   .hwp - Hangul Kelime İşlemci
-   .ipynb - Jupyter Notebook
-   .jpeg, .jpg - JPEG görsel
-   .mbox - MBOX e-posta arşivi
-   .md - Markdown
-   .mp3, .mp4 - ses ve video
-   .pdf - Taşınabilir Belge Biçimi
-   .png - Portable Network Graphics
-   .ppt, .pptm, .pptx - Microsoft PowerPoint

Burada bulmayı bekleyebileceğiniz bir dosya türü JSON'dur; bunun için [JSON Yükleyicimizi](https://llamahub.ai/l/readers/llama-index-readers-json) kullanmanızı öneririz.

## Kullanım

En temel kullanım, bir `input_dir` (giriş dizini) geçirmektir ve bu dizindeki desteklenen tüm dosyaları yükleyecektir:

```python
from llama_index.core import SimpleDirectoryReader

reader = SimpleDirectoryReader(input_dir="yol/dizin/adi")
documents = reader.load_data()
```

Bir dizinden çok sayıda dosya yükleniyorsa, dökümanlar paralel işleme ile de yüklenebilir. Windows ve Linux/MacOS makinelerinde `multiprocessing` kullanımı arasında farklılıklar olduğunu ve bunun `multiprocessing` dökümantasyonunda açıklandığını unutmayın (örneğin [buraya](https://docs.python.org/3/library/multiprocessing.html?highlight=process#the-spawn-and-forkserver-start-methods) bakın). Sonuç olarak, Windows kullanıcıları daha az performans artışı görebilir veya hiç görmeyebilirken, Linux/MacOS kullanıcıları tam olarak aynı dosya setini yüklerken bu artışları görecektir.

```python
...
documents = reader.load_data(num_workers=4)
```

### Alt dizinlerden okuma

Varsayılan olarak, `SimpleDirectoryReader` yalnızca dizinin en üst seviyesindeki dosyaları okuyacaktır. Alt dizinlerden de okumak için `recursive=True` olarak ayarlayın:

```python
SimpleDirectoryReader(input_dir="yol/dizin/adi", recursive=True)
```

### Dosyalar yüklenirken üzerlerinde döngü kurma

Dosyalar yüklenirken üzerlerinde döngü kurmak ve onları işlemek için `iter_data()` metodunu da kullanabilirsiniz:

```python
reader = SimpleDirectoryReader(input_dir="yol/dizin/adi", recursive=True)
all_docs = []
for docs in reader.iter_data():
    # <dosya başına dökümanlarla bir şeyler yapın>
    all_docs.extend(docs)
```

### Yüklenen dosyaları kısıtlama

Tüm dosyalar yerine bir dosya yolları listesi geçirebilirsiniz:

```python
SimpleDirectoryReader(input_files=["yol/dosya1", "yol/dosya2"])
```

veya `exclude` kullanarak **hariç tutulacak** dosya yollarının bir listesini geçirebilirsiniz:

```python
SimpleDirectoryReader(
    input_dir="yol/dizin/adi", exclude=["yol/dosya1", "yol/dosya2"]
)
```

Yalnızca belirli uzantılara sahip dosyaları yüklemek için `required_exts` parametresine bir dosya uzantıları listesi de atayabilirsiniz:

```python
SimpleDirectoryReader(
    input_dir="yol/dizin/adi", required_exts=[".pdf", ".docx"]
)
```

Ve `num_files_limit` ile yüklenecek maksimum dosya sayısını sınırlayabilirsiniz:

```python
SimpleDirectoryReader(input_dir="yol/dizin/adi", num_files_limit=100)
```

### Dosya kodlamasını (encoding) belirtme

`SimpleDirectoryReader` dosyaların `utf-8` kodlu olmasını bekler, ancak bunu `encoding` parametresini kullanarak geçersiz kılabilirsiniz:

```python
SimpleDirectoryReader(input_dir="yol/dizin/adi", encoding="latin-1")
```

### Meta verileri çıkarma

`SimpleDirectoryReader`, her `Document` nesnesine otomatik olarak bir `metadata` sözlüğü ekleyecektir. Varsayılan olarak bu sözlük şu öğelere sahiptir:

-   `file_path`: dosyanın tam sistem yolu, dosya adı dahil (string)
-   `file_name`: dosya adı, uzantısı dahil (string)
-   `file_type`: [`mimetypes.guess_type()`](https://docs.python.org/3/library/mimetypes.html#mimetypes.guess_type) tarafından tahmin edilen dosyanın MIME türü (string)
-   `file_size`: dosyanın bayt cinsinden boyutu (integer)
-   `creation_date`, `last_modified_date`, `last_accessed_date`: dosyanın oluşturulma, değiştirilme ve erişilme tarihleri, UTC zaman dilimine normalize edilmiş olarak. Aşağıdaki [Tarih ve saat meta verileri](#date-and-time-metadata) bölümüne bakın (string)

Ancak, meta veri sözlüğünü oluşturmak için kullanılan mantığı değiştirebilirsiniz. Bir dosya yolu dizesini alan ve bir sözlük döndüren özel bir fonksiyon oluşturun, ardından bu fonksiyonu `SimpleDirectoryReader` yapılandırıcısına `file_metadata` olarak geçirin:

```python
def get_meta(file_path):
    return {"foo": "bar", "file_path": file_path}


reader = SimpleDirectoryReader(
    input_dir="yol/dizin/adi", file_metadata=get_meta
)

docs = reader.load_data()
print(docs[0].metadata["foo"])  # "bar" yazdırır
```

#### Tarih ve saat meta verileri

`SimpleDirectoryReader` içindeki varsayılan meta veri fonksiyonu, tarihleri `%Y-%m-%d` [formatında](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes) bir dize olarak verir.

Tutarlılığı sağlamak için zaman damgaları UTC zaman dilimine normalize edilir. Çıktı tarihleri gerçek tarihten bir gün farklı görünüyorsa, bu durum UTC gece yarısı ile olan farkla açıklanabilir.

### Diğer dosya türlerine genişletme

`SimpleDirectoryReader`'ı diğer dosya türlerini okuyacak şekilde genişletmek için, `file_extractor` olarak `BaseReader` örneklerine eşlenen bir dosya uzantıları sözlüğü geçirebilirsiniz. Bir `BaseReader`, dosyayı okumalı ve bir Döküman listesi döndürmelidir. Örneğin, `.myfile` dosyaları için özel destek eklemek için:

```python
from llama_index.core import SimpleDirectoryReader
from llama_index.core.readers.base import BaseReader
from llama_index.core import Document


class MyFileReader(BaseReader):
    def load_data(self, file, extra_info=None):
        with open(file, "r") as f:
            text = f.read()
        # load_data, Document nesnelerinden oluşan bir liste döndürür
        return [Document(text=text + "Foobar", extra_info=extra_info or {})]


reader = SimpleDirectoryReader(
    input_dir="./data", file_extractor={".myfile": MyFileReader()}
)

documents = reader.load_data()
print(documents)
```

Belirttiğiniz dosya türleri için bu eşlemenin varsayılan dosya çıkarıcıları geçersiz kılacağını unutmayın; bu nedenle onları desteklemeye devam etmek istiyorsanız geri eklemeniz gerekecektir.

### Harici Dosya Sistemleri Desteği

Diğer modüllerde olduğu gibi, `SimpleDirectoryReader` uzak dosya sistemlerini taramak için kullanılabilecek isteğe bağlı bir `fs` parametresi alır.

Bu, [`fsspec`](https://filesystem-spec.readthedocs.io/en/latest/) protokolü tarafından uygulanan herhangi bir dosya sistemi nesnesi olabilir.
`fsspec` protokolü; [AWS S3](https://github.com/fsspec/s3fs), [Azure Blob & DataLake](https://github.com/fsspec/adlfs), [Google Drive](https://github.com/fsspec/gdrivefs), [SFTP](https://github.com/fsspec/sshfs) ve [diğer pek çoğu](https://github.com/fsspec/) dahil olmak üzere çeşitli uzak dosya sistemleri için açık kaynaklı uygulamalara sahiptir.

İşte S3'e bağlanan bir örnek:

```python
from s3fs import S3FileSystem

s3_fs = S3FileSystem(key="...", secret="...")
bucket_name = "belge-bucketim"

reader = SimpleDirectoryReader(
    input_dir=bucket_name,
    fs=s3_fs,
    recursive=True,  # tüm alt dizinleri özyinelemeli olarak arar
)

documents = reader.load_data()
print(documents)
```

Tam bir örnek notebook [burada](https://github.com/run-llama/llama_index/blob/main/docs/examples/data_connectors/simple_directory_reader_remote_fs.ipynb) bulunabilir.