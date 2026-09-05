# API ve REST Nedir?

API (Application Programming Interface), iki yazılımın birbiriyle konuşmasını sağlayan bir sözleşmedir. Bir uygulama, başka bir uygulamanın iç detaylarını bilmeden onun sunduğu fonksiyonları belirli bir arayüz üzerinden çağırabilir. Bu, Java'daki bir arayüz (interface) tanımının farklı sınıflar tarafından implemente edilmesine benzer: çağıran taraf sadece arayüzü bilir, iç uygulamayı bilmesine gerek yoktur.

REST (Representational State Transfer), web üzerinden çalışan API'ler için en yaygın kullanılan mimari stildir. REST API'ler HTTP protokolünü kullanır; `GET` veri okumak, `POST` yeni veri oluşturmak, `PUT`/`PATCH` güncellemek, `DELETE` silmek için kullanılır. Veri genellikle JSON formatında gönderilip alınır.

Bu projede Foundry Local, bilgisayarda yerel olarak çalışan bir REST API sunar ve bu API, OpenAI'nin bulut servisiyle aynı JSON formatını kullanır. Bu sayede resmi `openai` Python kütüphanesi, sadece hedef adresi (`base_url`) değiştirilerek yerel modelle konuşturulabilir; kod tarafında ekstra bir uyarlama gerekmez.
