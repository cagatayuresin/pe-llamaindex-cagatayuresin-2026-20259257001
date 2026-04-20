# Durumu (State) Koruma

Varsayılan olarak `AgentWorkflow`, her çalışma arasında durumsuzdur (stateless). Bu, ajanın önceki çalışmalara dair herhangi bir hafızasının olmayacağı anlamına gelir.

Durumu korumak için önceki durumu takip etmemiz gerekir. LlamaIndex'te, İş Akışları (Workflows), çalışmaların içinde ve arasında durumu korumak için kullanılabilecek bir `Context` sınıfına sahiptir. `AgentWorkflow` aslında önceden oluşturulmuş bir İş Akışı olduğu için, onu şimdi de kullanabiliriz.

```python
from llama_index.core.workflow import Context
```

Çalışmalar arasında durumu korumak için `ctx` adında yeni bir Context oluşturacağız. Bu Context nesnesini kullanacak olan iş akışı için düzgün bir şekilde yapılandırmak amacıyla iş akışımızı ona parametre olarak geçiyoruz.

```python
ctx = Context(workflow)
```

Yapılandırılmış Context nesnemizi ilk çalışmamıza geçebiliriz.

```python
response = await workflow.run(user_msg="Merhaba, benim adım Laurie!", ctx=ctx)
print(response)
```

Bu bize şunu verecektir:

```text
Merhaba Laurie! Bugün size nasıl yardımcı olabilirim?
```

Ve şimdi bir takip sorusu sormak için iş akışını tekrar çalıştırırsak, bu bilgiyi hatırlayacaktır:

```python
response2 = await workflow.run(user_msg="Benim adım ne?", ctx=ctx)
print(response2)
```

Bu bize şunu verir:

```text
Adınız Laurie!
```

## Durumu Daha Uzun Süre Koruma

Context nesnesi serileştirilebilir (serializable) olduğundan bir veritabanına, dosyaya vb. kaydedilebilir ve daha sonra tekrar yüklenebilir.

`JsonSerializer`, bağlamı serileştirmek ve serileştirmeden geri döndürmek için `json.dumps` ve `json.loads` kullanan basit bir serileştiricidir.

`JsonPickleSerializer`, bağlamı serileştirmek ve geri yüklemek için `pickle` kullanan bir serileştiricidir. Bağlamınızda serileştirilemeyen nesneler varsa bu serileştiriciyi kullanabilirsiniz.

Serileştiricilerimizi herhangi bir import gibi dahil ederiz:

```python
from llama_index.core.workflow import JsonPickleSerializer, JsonSerializer
```

Ardından bağlamımızı bir sözlüğe (dictionary) serileştirebilir ve bir dosyaya kaydedebiliriz:

```python
ctx_dict = ctx.to_dict(serializer=JsonSerializer())
```

Bunu tekrar bir Context nesnesine dönüştürebilir (deserialize) ve daha önce olduğu gibi sorular sorabiliriz:

```python
restored_ctx = Context.from_dict(
    workflow, ctx_dict, serializer=JsonSerializer()
)

response3 = await workflow.run(user_msg="Benim adım ne?", ctx=restored_ctx)
```

Bu örneğin [kodlarının tamamını](https://github.com/run-llama/python-agents-tutorial/blob/main/3_state.py) inceleyebilirsiniz.

## Araçlar ve Durum (State)

İş akışı bağlamına erişimi olan araçlar da tanımlanabilir. Bu, bağlamdan değişkenler ayarlayıp alabileceğiniz ve bunları araçta kullanabileceğiniz veya araçlar arasında bilgi aktarabileceğiniz anlamına gelir.

`AgentWorkflow`, her ajanın erişebildiği `state` adında bir bağlam değişkeni kullanır. Bilgileri açıkça aktarmak zorunda kalmadan `state` içindeki bilgilere güvenebilirsiniz.

Bağlam'a (Context) erişmek için, Context parametresi aracın ilk parametresi olmalıdır. Burada sadece duruma bir isim ekleyen bir araçta yaptığımız gibi:

```python
async def set_name(ctx: Context, name: str) -> str:
    async with ctx.store.edit_state() as ctx_state:
        ctx_state["state"]["name"] = name

    return f"İsim {name} olarak ayarlandı"
```

Artık bu aracı kullanan bir ajan oluşturabiliriz. Opsiyonel olarak ajanın başlangıç durumunu (initial state) sağlayabilirsiniz, burada da yapacağımız gibi:

```python
workflow = AgentWorkflow.from_tools_or_functions(
    [set_name],
    llm=llm,
    system_prompt="Siz isim ayarlayabilen yardımcı bir asistansınız.",
    initial_state={"name": "unset"},
)
```

Şimdi bir Context oluşturabilir ve ajana durumu sorabiliriz:

```python
ctx = Context(workflow)

# Ayarlamadan önce bir isim bilip bilmediğini kontrol edin
response = await workflow.run(user_msg="Benim adım ne?", ctx=ctx)
print(str(response))
```

Bu bize şunu verir:

```text
Adınız "unset" (ayarlanmamış) olarak belirlenmiş.
```

Ardından ajanın yeni bir çalışmasında ismi açıkça ayarlayabiliriz:

```python
response2 = await workflow.run(user_msg="Benim adım Laurie", ctx=ctx)
print(str(response2))
```

Çıktı:

```text
Adınız "Laurie" olarak güncellendi.
```

Artık ajana ismini tekrar sorabiliriz veya durum değerine doğrudan erişebiliriz:

```python
state = await ctx.store.get("state")
print("Durumda saklanan isim: ", state["name"])
```

Bu bize şunu verir:

```text
Durumda saklanan isim: Laurie
```

Bu örneğin [kodlarının tamamını](https://github.com/run-llama/python-agents-tutorial/blob/main/3a_tools_and_state.py) inceleyebilirsiniz.

Sırada [çıkış ve olay akışı (streaming)](/python/framework/understanding/agent/streaming) hakkında bilgi edineceğiz.