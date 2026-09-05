# Veritabanı Temelleri: SQL ve SQLite

İlişkisel (relational) veritabanları, veriyi satır ve sütunlardan oluşan tablolarda saklar; tablolar arasındaki ilişkiler yabancı anahtarlar (foreign key) ile kurulur. SQL (Structured Query Language), bu tablolara veri eklemek, sorgulamak, güncellemek ve silmek için kullanılan standart bir dildir. `SELECT`, `INSERT`, `UPDATE`, `DELETE` bu dilin en temel dört komutudur.

SQLite, diğer veritabanı sistemlerinden (PostgreSQL, MySQL gibi) farklı olarak ayrı bir sunucu süreci gerektirmez; tüm veritabanı tek bir dosyada saklanır. Bu özellik onu masaüstü uygulamaları, mobil uygulamalar ve bu proje gibi tamamen çevrimdışı (offline) çalışması gereken sistemler için ideal kılar. Python'ın standart kütüphanesinde `sqlite3` modülü hazır geldiği için ek bir kurulum da gerekmez.

Bir veritabanı tasarlarken "şema" (schema), yani hangi tabloların hangi sütunlara ve veri tiplerine sahip olacağı önceden tanımlanır. Örneğin bu projedeki `documents` tablosunda her satır bir belge parçasını (`content`), o parçanın embedding vektörünü (`embedding`) ve hangi kaynaktan geldiğini (`source`) tutar.
