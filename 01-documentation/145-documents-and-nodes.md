# Dökümanlar ve Node'lar (Documents and Nodes)

##### SSS (FAQ)

1. [Bir Node nesnesinin varsayılan `chunk_size` değeri nedir?](#1-bir-node-nesnesinin-varsayılan-chunk_size-değeri-nedir)
2. [Bir `Document` nesnesine isim, url gibi bilgiler nasıl eklenir?](#2-bir-document-nesnesine-isim-url-gibi-bilgiler-nasıl-eklenir)
3. [Bir İndeks içindeki mevcut döküman nasıl güncellenir?](#3-bir-indeks-içindeki-mevcut-döküman-nasıl-güncellenir)

---

##### 1. Bir Node nesnesinin varsayılan `chunk_size` değeri nedir?

Varsayılan olarak 1024'tür. Eğer `chunk_size` değerini özelleştirmek isterseniz, [Node Özelleştirme](/python/framework/module_guides/loading/node_parsers#customization) kılavuzunu takip edebilirsiniz.

---

##### 2. Bir `Document` nesnesine isim, url gibi bilgiler nasıl eklenir?

Döküman nesnesini özelleştirebilir ve meta veri (metadata) formunda ek bilgiler ekleyebilirsiniz. Bu konuda daha fazla bilgi edinmek için [Döküman Özelleştirme](/python/framework/module_guides/loading/documents_and_nodes/usage_documents#customizing-documents) kılavuzunu takip edin.

---

##### 3. Bir İndeks içindeki mevcut döküman nasıl güncellenir?

Bir İndeks içindeki mevcut dökümanı `doc_id` yardımıyla güncelleyebilir veya silebilirsiniz. Mevcut bir İndekse yeni dökümanlar da ekleyebilirsiniz. Daha fazlasını öğrenmek için [Döküman Yönetimi](/python/framework/module_guides/indexing/document_management) dökümanına göz atın.

---