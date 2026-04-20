# Yapılandırılmış Girdi (Structured Input)

Yapılandırılmış verinin çıktı ötesindeki diğer tarafı girdidir: Birçok komut verme (prompting) kılavuzu ve en iyi uygulama, LLM'in girdiyi daha iyi anlamasını sağlamak için girdi komutunun XML etiketleriyle işaretlenmesi gibi bazı teknikler içerir.

LlamaIndex size, [banks](https://masci.github.io/banks) ve [Jinja](https://jinja.palletsprojects.com/en/stable/) kütüphanelerinden yararlanarak girdilerinizi yerel olarak XML parçacıkları şeklinde formatlama imkanı sunar (`llama-index>=0.12.34` kurulu olduğundan emin olun).

## Yapılandırılmış Girdiyi Tek Başına Kullanma

Pydantic modelleriyle yapılandırılmış girdilerin nasıl kullanılacağına dair basit bir örnek:

```python
from pydantic import BaseModel
from llama_index.core.prompts import RichPromptTemplate
from llama_index.llms.openai import OpenAI
from typing import Dict

template_str = "Lütfen aşağıdaki XML kodundan kullanıcının iletişim bilgilerini çıkarın:\n\n```xml\n{{ user | to_xml }}\n```\n\n"
prompt = RichPromptTemplate(template_str)


class User(BaseModel):
    name: str
    surname: str
    age: int
    email: str
    phone: str
    social_accounts: Dict[str, str]


user = User(
    name="John",
    surname="Doe",
    age=30,
    email="john.doe@example.com",
    phone="123-456-7890",
    social_accounts={"bluesky": "john.doe", "instagram": "johndoe1234"},
)

## komutun nasıl görüneceğini kontrol edin
prompt.format(user=user)

llm = OpenAI()

response = llm.chat(prompt.format_messages(user=user))

print(response.message.content)
```

Gördüğünüz gibi, yapılandırılmış girdiyi kullanmak için `to_xml` filtresiyle (filtreleme operatörü `|` işaretidir) bir Jinja ifadesi (`{{}}` ile sınırlanmış) kullanmamız gerekiyor.

## Yapılandırılmış Girdiyi Yapılandırılmış Çıktı ile Birleştirme

Yapılandırılmış girdi ve yapılandırılmış çıktının kombinasyonu, LLM'in çıktısının tutarlılığını (ve dolayısıyla güvenilirliğini) gerçekten artırabilir.

Aşağıdaki kod parçacığı ile veri yapılandırmanın bu iki adımını nasıl zincirleyebileceğinizi görebilirsiniz.

```python
from pydantic import Field
from typing import Optional


class SocialAccounts(BaseModel):
    instagram: Optional[str] = Field(default=None)
    bluesky: Optional[str] = Field(default=None)
    x: Optional[str] = Field(default=None)
    mastodon: Optional[str] = Field(default=None)


class ContactDetails(BaseModel):
    email: str
    phone: str
    social_accounts: SocialAccounts


sllm = llm.as_structured_llm(ContactDetails)

structured_response = await sllm.achat(prompt.format_messages(user=user))

print(structured_response.raw.email)
print(structured_response.raw.phone)
print(structured_response.raw.social_accounts.instagram)
print(structured_response.raw.social_accounts.bluesky)
```

Yapılandırılmış girdi hakkında daha derinlemesine bir döküman istiyorsanız, bu [örnek notebook'u](https://docs.llamaindex.ai/en/latest/examples/prompts/structured_input) inceleyin.