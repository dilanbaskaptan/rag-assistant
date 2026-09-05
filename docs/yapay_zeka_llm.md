# Büyük Dil Modelleri (LLM) Nedir?

Büyük Dil Modeli (Large Language Model, LLM), devasa miktarda metin verisiyle eğitilmiş, bir metin dizisinde bir sonraki kelimeyi (daha doğrusu "token"ı) tahmin etmeyi öğrenen bir yapay sinir ağıdır. Bu basit görünen görev, yeterince büyük veri ve parametre sayısıyla birleşince modelin özetleme, çeviri, kod yazma ve soru cevaplama gibi karmaşık yetenekler kazanmasını sağlar.

LLM'ler metni doğrudan işlemez; önce metni "token" adı verilen küçük parçalara (kelime, kelime parçası veya karakter grubu) ayırır ve her token'ı bir sayı dizisine (embedding) çevirir. Modelin "context length" (bağlam uzunluğu) değeri, tek seferde kaç token'ı hafızasında tutabildiğini belirler; bu projede kullanılan phi-3.5-mini modelinin bağlam uzunluğu 131.072 token'dır.

Bu projede kullanılan phi-3.5-mini gibi "küçük dil modelleri" (Small Language Model, SLM), GPT-4 gibi devasa modellere göre çok daha az kaynak (RAM, VRAM) gerektirir ve bu sayede internet bağlantısı olmadan, tamamen yerel donanımda (offline) çalışabilir. Karşılığında, çok genel veya çok karmaşık sorularda büyük modeller kadar başarılı olmayabilirler; RAG mimarisi bu açığı, doğru belgeyi bulup modele vererek kapatmaya çalışır.
