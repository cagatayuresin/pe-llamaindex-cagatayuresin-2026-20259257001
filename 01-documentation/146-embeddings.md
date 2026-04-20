# Embedding'ler (Embeddings)

##### SSS (FAQ)

1. [Özel/yerel bir embedding modeli nasıl kullanılır?](#1-özelyerel-bir-embedding-modeli-nasıl-kullanılır)
2. [Yerel bir Hugging Face embedding modeli nasıl kullanılır?](#2-yerel-bir-hugging-face-embedding-modeli-nasıl-kullanılır)
3. [Metin için embedding oluşturmak amacıyla embedding modeli nasıl kullanılır?](#3-metin-için-embedding-oluşturmak-amacıyla-embedding-modeli-nasıl-kullanılır)
4. [HuggingFace Metin-Embedding Çıkarımı (Inference) LlamaIndex ile nasıl kullanılır?](#4-huggingface-metin-embedding-çıkarımı-inference-llamaindex-ile-nasıl-kullanılır)

---

##### 1. Özel/yerel bir embedding modeli nasıl kullanılır?

Kendi özelleştirilmiş embedding sınıfınızı oluşturmak için [Özel Embedding'ler (Custom Embeddings)](/python/examples/embeddings/custom_embeddings) kılavuzunu takip edebilirsiniz.

---

##### 2. Yerel bir Hugging Face embedding modeli nasıl kullanılır?

Yerel bir HuggingFace embedding modeli kullanmak için [HuggingFace ile Yerel Embedding'ler](/python/examples/embeddings/huggingface) kılavuzunu takip edebilirsiniz.

---

##### 3. Metin için embedding oluşturmak amacıyla embedding modeli nasıl kullanılır?

Aşağıdaki kod parçasıyla metinler için embedding oluşturabilirsiniz.

```python
text_embedding = embed_model.get_text_embedding("METNİNİZ")
```

---

##### 4. HuggingFace Metin-Embedding Çıkarımı (Inference) LlamaIndex ile nasıl kullanılır?

HuggingFace Metin-Embedding Çıkarımı'nı kullanmak için [Metin-Embedding-Çıkarımı (Text-Embedding-Inference)](/python/examples/embeddings/text_embedding_inference) eğitimini takip edebilirsiniz.