# RAG (Retrieval-Augmented Generation) Nedir?

RAG, bir dil modelinin (LLM) cevap üretirken sadece eğitim sırasında öğrendiği bilgiye değil, sorgu anında dışarıdan getirilen (retrieve edilen) güncel veya özel belgelere de dayanmasını sağlayan bir mimaridir. Bu sayede model, hiç görmediği veya eğitim verisinde bulunmayan belgeler hakkında da doğru cevaplar verebilir.

RAG mimarisinin iki ana adımı vardır: önce kullanıcının sorusuna en alakalı belge parçaları (chunk) bir veritabanından bulunur (retrieval), sonra bu parçalar soruyla birlikte dil modeline bir prompt içinde verilir (generation). Alakalı parçaları bulmak için genellikle embedding vektörleri ve kosinüs benzerliği (cosine similarity) kullanılır.

RAG'ın klasik fine-tuning'e göre en büyük avantajı, modelin ağırlıklarını değiştirmeden yeni bilgi eklenebilmesidir; veritabanına yeni bir belge eklemek yeterlidir. Ayrıca model cevap verirken hangi belgeye dayandığını gösterebildiği için "halüsinasyon" (uydurma bilgi) riski, kaynak gösterilmeyen serbest üretime göre daha kolay fark edilir ve azaltılabilir.
