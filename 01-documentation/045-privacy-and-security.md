# Gizlilik ve Güvenlik

Varsayılan olarak LlamaIndex; embedding'ler (vektör temsilleri) ve doğal dil yanıtları oluşturmak için verilerinizi OpenAI'a gönderir. Ancak bunun tercihlerine göre yapılandırılabileceğini unutmamak önemlidir. LlamaIndex, isterseniz kendi embedding modelinizi kullanma veya yerel olarak bir büyük dil modeli çalıştırma esnekliğini sağlar.

## Veri Gizliliği

Veri gizliliğiyle ilgili olarak, LlamaIndex'i OpenAI ile birlikte kullanırken verilerinizin gizlilik ayrıntıları ve işlenmesi OpenAI'ın politikalarına tabidir. OpenAI dışındaki her bir özel servisin de kendi politikaları bulunmaktadır.

## Vektör Depoları (Vector Stores)

LlamaIndex, embedding'leri saklamak için indeksler içindeki diğer vektör depolarına bağlanacak modüller sunar. Her vektör deposunun kendi gizlilik politikaları ve uygulamaları olduğunu ve LlamaIndex'in verilerinizin nasıl işlendiği veya kullanıldığı konusunda sorumluluk kabul etmediğini unutmamak gerekir. Ayrıca varsayılan olarak LlamaIndex, embedding'lerinizi yerel olarak saklamak için varsayılan bir seçeneğe sahiptir.