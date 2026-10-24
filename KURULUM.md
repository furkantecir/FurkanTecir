# FuTe Cyber Arcade v3 — Kurulum

## Bilgisayarındaki mevcut FurkanTecir deposunda PowerShell aç

ZIP dosyasını klasöre ayıkla. Ardından bu komutu çalıştır (farklı klasöre ayıkladıysan yolu değiştir):

```powershell
Copy-Item -Path "D:\indirilneler\FuTe-Cyber-Arcade-v3-Kaynak-Kod\*" -Destination "C:\Users\FuTe\Documents\GitHub\FurkanTecir" -Recurse -Force
```

Ardından:

```powershell
git add -A
git commit -m "feat: FuTe Cyber Arcade v3"
git push origin main
```

GitHub > FurkanTecir deposu > Actions > Refresh FuTe Cyber Arcade > Run workflow.

**Not:** Paketle gelen activity görseli demo olarak işaretlidir. GitHub Actions başarılı tamamlanmadan gerçek veri var diye gösterilmez. `GITHUB_TOKEN` GitHub Actions tarafından otomatik sağlanır; token'ı dosyalara eklemeyin.

- `project-01.svg` … `project-04.svg` ayrı görseller, tıklanınca ilgili depo açılır.
- README avatarı GitHub görsel adresinden hemen gösterir. `avatar.png` ve SVG içindeki gömülü avatar Action çalışınca GitHub avatarından üretilir.
- `hero.svg` görüntüsüne avatar gömülür, ağ bağlantısı yoksa gömülü eski owl çizimi yedek olarak kullanılır.
- Robot, virüs ve katkı kareleri `scripts/generate.py` ile oluşturulur.
- README içinden Pinned / GitHub'ın kendi contributions grafiği kaldırılamaz.
