# Python'da Asenkron Programlama

Eğer Python'da asenkron (async) programlamaya yeniyseniz, bu sayfa tam size göre.

Özellikle LlamaIndex'te birçok işlem ve fonksiyon asenkron yürütmeyi destekler. Bu, ana iş parçacığını (main thread) engellemeden aynı anda birden fazla işlemi çalıştırmanıza olanak tanır; bu da çoğu durumda genel veri işleme miktarını (throughput) ve performansı artırmaya yardımcı olur.

Anlamanız gereken bazı temel kavramlar şunlardır:

## 1. `asyncio` Temelleri

- **Olay Döngüsü (Event Loop)**:
  Olay döngüsü, asenkron işlemlerin planlanmasını ve yürütülmesini yönetir. Sürekli olarak görevleri (coroutine'leri) kontrol eder ve yürütür. Tüm asenkron işlemler bu döngü tarafından çalıştırılır ve her iş parçacığı başına yalnızca bir olay döngüsü olabilir.

- **`asyncio.run()`**:
  bu fonksiyon, asenkron bir programı başlatmak için giriş noktasıdır. Olay döngüsünü oluşturur, yönetir ve tamamlandıktan sonra temizler. Unutmayın ki bu fonksiyonun her iş parçacığı için bir kez çağrılması tasarlanmıştır. FastAPI gibi bazı framework'ler olay döngüsünü sizin yerinize çalıştırırken, diğerleri bunu sizin yapmanızı gerektirecektir.

- **Asenkron + Python Notebook'lar**:
  Python notebook'ları, olay döngüsünün zaten çalıştığı özel bir durumdur. Bu, `asyncio.run()` fonksiyonunu kendiniz çağırmanıza gerek olmadığı ve asenkron fonksiyonları doğrudan çağırıp `await` edebileceğiniz anlamına gelir.

## 2. Asenkron Fonksiyonlar ve `await`

- **Asenkron Fonksiyonları Tanımlama**:
  Asenkron bir fonksiyon (coroutine) tanımlamak için `async def` söz dizimini kullanın. Bir asenkron fonksiyon çağrıldığında hemen yürütülmek yerine, planlanması ve çalıştırılması gereken bir coroutine nesnesi döndürür.

- **`await` Kullanımı**:
  Bir asenkron fonksiyonun içinde `await`, beklenen görev tamamlanana kadar o fonksiyonun yürütülmesini duraklatmak için kullanılır. `await some_fn()` yazdığınızda, fonksiyon kontrolü olay döngüsüne geri verir, böylece diğer görevler planlanabilir ve çalıştırılabilir. Aynı anda yalnızca bir asenkron fonksiyon yürütülür ve bunlar `await` ile kontrolü devrederek iş birliği yaparlar.

## 3. Eşzamanlılık (Concurrency) Açıklaması

- **İş Birlikçi Eşzamanlılık (Cooperative Concurrency)**:
  Birden fazla asenkron görevi planlayabilmenize rağmen, aynı anda yalnızca bir görev çalışır. Bu, birden fazla görevin gerçek anlamda aynı anda çalıştığı gerçek paralellikten (parallelism) farklıdır. Bir görev bir `await` ifadesine ulaştığında yürütülmesini askıya alır, böylece başka bir görev çalışabilir. Bu, asenkron programları LLM'lere ve diğer hizmetlere yapılan API çağrıları gibi beklemenin yaygın olduğu I/O-bağımlı görevler için mükemmel kılar.

- **Gerçek Paralellik Değildir**:
  Asyncio eşzamanlılığı (concurrency) mümkün kılar ancak görevleri paralel olarak çalıştırmaz. Paralel yürütme gerektiren CPU-yoğun işler için threading veya multiprocessing (çoklu işlem) kullanmayı düşünün. LlamaIndex genellikle çoğu durumda multiprocessing'den kaçınır ve bunu güvenli ve verimli bir şekilde uygulamanın karmaşık olması nedeniyle kullanıcıya bırakır.

## 4. Engelleyici (Senkron) Kodun İşlenmesi

- **`asyncio.to_thread()`**:
  Bazen asenkron programınızı dondurmadan senkron (engelleyici) kod çalıştırmanız gerekebilir. `asyncio.to_thread()` engelleyici kodu ayrı bir iş parçacığına aktararak olay döngüsünün diğer görevleri işlemeye devam etmesini sağlar. Biraz ek yük getirdiği ve hata ayıklamayı zorlaştırabildiği için bunu dikkatli kullanın.

- **Alternatif: Executor'lar**:
  Engelleyici fonksiyonları yönetmek için `loop.run_in_executor()` kullanımına da rastlayabilirsiniz.

## 5. Pratik Bir Örnek

Aşağıda, `asyncio` ile asenkron fonksiyonların nasıl yazılacağını ve çalıştırılacağını gösteren bir örnek bulunmaktadır:

```python
import asyncio


async def fetch_data(delay):
    print(f"{delay} saniye gecikmeyle veri getirme başladı")

    # Ağ işlemleri gibi I/O-bağımlı işleri simüle eder
    await asyncio.sleep(delay)

    print("Veri getirme tamamlandı")
    return f"{delay} saniye sonraki veri"


async def main():
    print("Ana program başlıyor")

    # İki görevi eş zamanlı olarak planlayın
    task1 = asyncio.create_task(fetch_data(2))
    task2 = asyncio.create_task(fetch_data(3))

    # Her iki görev de tamamlanana kadar bekleyin
    result1, result2 = await asyncio.gather(task1, task2)

    print(result1)
    print(result2)
    print("Ana program tamamlandı")


if __name__ == "__main__":
    asyncio.run(main())
```