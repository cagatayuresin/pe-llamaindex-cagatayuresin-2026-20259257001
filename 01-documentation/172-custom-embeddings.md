# Özel (Custom) Embedding'ler

LlamaIndex; OpenAI, Azure ve Langchain'den gelen embedding'leri destekler. Ancak bu yeterli değilse, herhangi bir embedding modelini de uygulayabilirsiniz!

Aşağıdaki örnekte Instructor Embeddings ([kurulum/kurulum ayrıntıları burada](https://huggingface.co/hkunlp/instructor-large)) kullanılmış ve özel bir embedding sınıfı uygulanmıştır. Instructor embedding'leri; metnin yanı sıra, gömülecek (embed) metnin alanı (domain) hakkında "talimatlar" (instructions) sağlayarak çalışır. Bu, çok spesifik ve uzmanlaşmış bir konu hakkındaki metni gömerken (embedding) yardımcı olur.

Bu not defterini Colab'da açıyorsanız, muhtemelen LlamaIndex'i 🦙 kurmanız gerekecektir.

```python
!pip install llama-index
```

```python
# Bağımlılıkları kurun
# !pip install InstructorEmbedding torch transformers sentence-transformers
```

```python
import openai
import os

os.environ["OPENAI_API_KEY"] = "API_ANAHTARINIZ"
openai.api_key = os.environ["OPENAI_API_KEY"]
```

## Özel Embedding Uygulaması

```python
from typing import Any, List
from InstructorEmbedding import INSTRUCTOR

from llama_index.core.bridge.pydantic import PrivateAttr
from llama_index.core.embeddings import BaseEmbedding


class InstructorEmbeddings(BaseEmbedding):
    _model: INSTRUCTOR = PrivateAttr()
    _instruction: str = PrivateAttr()

    def __init__(
        self,
        instructor_model_name: str = "hkunlp/instructor-large",
        instruction: str = "Semantik arama için bir dökümanı temsil et:",
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self._model = INSTRUCTOR(instructor_model_name)
        self._instruction = instruction

    @classmethod
    def class_name(cls) -> str:
        return "instructor"

    async def _aget_query_embedding(self, query: str) -> List[float]:
        return self._get_query_embedding(query)

    async def _aget_text_embedding(self, text: str) -> List[float]:
        return self._get_text_embedding(text)

    def _get_query_embedding(self, query: str) -> List[float]:
        embeddings = self._model.encode([[self._instruction, query]])
        return embeddings[0]

    def _get_text_embedding(self, text: str) -> List[float]:
        embeddings = self._model.encode([[self._instruction, text]])
        return embeddings[0]

    def _get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        embeddings = self._model.encode(
            [[self._instruction, text] for text in texts]
        )
        return embeddings
```

## Kullanım Örneği

```python
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core import Settings
```

#### Veriyi İndir

```python
!mkdir -p 'data/paul_graham/'
!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
```

#### Dökümanları Yükle

```python
documents = SimpleDirectoryReader("./data/paul_graham/").load_data()
```

```python
embed_model = InstructorEmbeddings(embed_batch_size=2)

Settings.embed_model = embed_model
Settings.chunk_size = 512

# İlk kez çalıştırılıyorsa, önce model ağırlıkları indirilecektir!
index = VectorStoreIndex.from_documents(documents)
```

    load INSTRUCTOR_Transformer
    max_seq_length  512

```python
response = index.as_query_engine().query("Yazar büyürken ne yaptı?")
print(response)
```

    Yazar kısa hikayeler yazdı ve ayrıca programlama üzerine çalıştı, özellikle 9. sınıfta bir IBM 1401 bilgisayarında. Fortran'ın erken bir versiyonunu kullandılar ve programları delikli kartlara yazmak zorundaydılar. Daha sonra bir mikrobilgisayar olan TRS-80 aldılar ve basit oyunlar ve bir kelime işlemci yazarak daha kapsamlı bir şekilde programlama yapmaya başladılar. Başlangıçta üniversitede felsefe okumayı planladılar ancak sonunda yapay zekaya (AI) geçiş yaptılar.