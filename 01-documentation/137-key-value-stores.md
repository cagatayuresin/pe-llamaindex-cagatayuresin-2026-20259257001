# Anahtar-Değer Depoları (Key-Value Stores)

Anahtar-Değer (Key-Value) depoları, [Döküman Depolarımıza](/python/framework/module_guides/storing/docstores) ve [İndeks Depolarımıza](/python/framework/module_guides/storing/index_stores) güç veren temel saklama soyutlamalarıdır (storage abstractions).

Şu anahtar-değer depolarını sağlıyoruz:

-   **Basit Anahtar-Değer Deposu (Simple Key-Value Store)**: Bellek içi (in-memory) bir KV deposu. Kullanıcı, verileri diske kaydetmek için bu kv deposunda `persist` metodunu çağırmayı seçebilir.
-   **MongoDB Anahtar-Değer Deposu (MongoDB Key-Value Store)**: Bir MongoDB KV deposu.
-   **Tablestore Anahtar-Değer Deposu (Tablestore Key-Value Store)**: Bir Tablestore KV deposu.

Daha fazla detay için [API Referansına](/python/framework-api-reference/storage/kvstore) bakın.

Not: Şu anda bu saklama soyutlamaları doğrudan dışa açık (externally facing) değildir.