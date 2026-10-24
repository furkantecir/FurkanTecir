# FuTe // Cyber Arcade — Kurulum

**GitSkins gerekmez.** Bu paketin içindeki bütün SVG tasarımları ve GIF animasyonu açık, değiştirilebilir kaynak kodla üretilir.

## 1. Profil deposunu aç

GitHub kullanıcı adın `furkantecir`, profil README deposunun adı `furkantecir` olmalıdır: **`https://github.com/furkantecir/furkantecir`**.

> NOT: Önceki tasarımın dosyalarını kaybetmemek için README ve `assets/` klasörünü yedekle. Profil deposunu yoksa oluştur: public repo, tam adı `furkantecir`, README eklensin.

## 2. ZIP içeriğini depoya at

`README.md`, `config.json`, `requirements.txt`, `assets/`, `scripts/`, `.github/` dosyalarını aynen depo köküne yükle. Gizli klasör olan `.github` içindeki `workflows/refresh.yml` dosyasının yerinde olduğuna dikkat et.

İlk yüklemede `activity.gif` üstünde **DEMO / NOT LIVE**, istatistikte **SYNC: PENDING** yazar. Bu bir hata değil: gerçek verileri uydurmamak için önizleme verisini belirgin şekilde işaretledik.

## 3. Gerçek GitHub katkı verilerine geç

Repo > **Settings > Actions > General** kısmından Actions çalışma iznini kontrol et. `Workflow permissions` alanında `Read and write permissions` gerekiyorsa aç.

Sonra **Actions > Refresh FuTe Cyber Arcade > Run workflow** seç. İlgili workflow **`secrets.GITHUB_TOKEN`** kullanır; ayrıca kendi PAT tokenını dosyaya yazman gerekmez.

Action çalışınca gerçek GitHub katkı grafiği ve herkese açık stats ile `assets/` dosyaları güncellenir. Her gün UTC 04:27'de yenilenir.

**Not:** GitHub GraphQL katkı verisini güvenlik veya erişim nedeniyle döndürmezse workflow hata verip demo verisini canlıymış gibi yayınlamaz. Actions logunu kontrol et. Kişisel PAT gerekirse tokenı README veya workflow'a yapıştırma; GitHub Secrets üzerinden kullan.

## 4. Tasarımı düzenle

- `config.json`: Kullanıcı adı, renkler, proje adları, proje bilgileri.
- `scripts/generate.py`: SVG bileşenleri, piksel font, baykuş, robot, virüs, lazer animasyonu.
- `assets/`: Oluşturulmuş SVG ve GIF çıktıları.
- `README.md`: Profil düzeni, gerçek ve tıklanabilir proje bağlantıları.

Yerel önizleme:

```bash
python -m pip install -r requirements.txt
python scripts/generate.py --demo
```

**ÖNEMLİ:** `--demo` yüklenirse GitHub'daki canlı verilerin üzerine DEMO yazılır. Gerçek profil için Action'ın `--live` üretimini kullan.

## 5. Sınırlamalar

GitHub README sayfasında keyfi JavaScript, canvas oyun döngüsü veya HTML etkileşimi çalıştırılamaz. Bu nedenle robotlar GIF içinde hareket eder: **izlenebilir oyun animasyonu**, gerçek tıklanabilir oyun değildir. GIF katkıları silmez, değiştirmez; sadece görsel olarak üzerlerinde hareket eder.

GitHub, görüntüleri önbelleğe alabilir: Action başarılı olduğu halde yenilik görünmüyorsa bir süre sonra yeniden kontrol et.

## Önizleme

`preview.html` dosyasını tarayıcıda aç. Üstte FuTe kimlik kartı, proje kartları, istatistikler ve hareketli activity GIF yer alır. Yerel HTML önizleme kodu GitHub profilinde çalışmak zorunda değildir.
