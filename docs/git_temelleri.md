# Git Temelleri

Git, Linus Torvalds tarafından 2005 yılında geliştirilen, dağıtık (distributed) bir versiyon kontrol sistemidir. Merkezi sistemlerden farklı olarak her geliştiricinin bilgisayarında projenin tüm geçmişinin bir kopyası bulunur; bu sayede internet bağlantısı olmadan da commit, branch ve log gibi işlemler yapılabilir.

Bir Git deposunda (repository) değişiklikler önce `git add` komutuyla "staging area"ya eklenir, sonra `git commit` ile kalıcı hale getirilir. Bu iki aşamalı yapı, bir commit'e hangi değişikliklerin dahil edileceğini seçme esnekliği sağlar. `git push` ve `git pull` komutları ise yerel depoyu uzak (remote) bir depoyla senkronize etmeye yarar.

Branch (dal) kavramı, ana koddan bağımsız olarak yeni bir özellik üzerinde çalışmayı mümkün kılar. Bir branch üzerindeki değişiklikler tamamlandığında `git merge` veya `git rebase` ile ana branch'e (genellikle `main`) entegre edilir. Çakışan (conflict) değişiklikler olduğunda Git bunları otomatik çözemez ve geliştiricinin elle müdahale etmesi gerekir.
