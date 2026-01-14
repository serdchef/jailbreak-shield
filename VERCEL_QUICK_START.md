# ⚡ VERCEL DEPLOYMENT - ÖZETİ

## 🎯 Ne Yapacaksın?

Vercel web arayüzüne gidip GitHub repo'nu deployment için bağlayacaksın.

---

## 📋 ADIM ADIM

### 1️⃣ Vercel Dashboard'a Git
**URL:** https://vercel.com/dashboard

### 2️⃣ New Project Oluştur
- Click: "Add New..." → "Project"
- Select: "Import Git Repository"
- Select: `jailbreak-shield` repo'su (GitHub'dan görmeli)
- Click: "Import"

### 3️⃣ Framework & Build Settings
Vercel auto-detect edecek, ama eğer sorun olursa:

**Framework:** Python (or Other)
**Build Command:** `pip install -r demo/requirements.txt`
**Start Command:** `streamlit run demo/app.py`

### 4️⃣ Environment Variables Ekle
"Environment Variables" bölümüne:

```
ANTHROPIC_API_KEY = sk-ant-xxxxx
LAYER2_ENABLED = true
LAYER2_THRESHOLD = 0.5
LOG_LEVEL = INFO
```

⚠️ **API KEY YAZMALISIN** (şu anda demo key var)

### 5️⃣ Deploy
Click: **"Deploy"** button
⏱️ Bekle: 2-3 dakika

### 6️⃣ Live Link Al
Deployment tamamlandığında:
```
https://jailbreak-shield.vercel.app
```

Bu link'i README'ye ekleyeceksin.

---

## ✅ SONRA NE?

- Demo'yu test et: https://jailbreak-shield.vercel.app
- README'yi live link ile güncelle
- GitHub'a push et
- Blog'a paylaş

---

## 🚨 SORUN ÇIKARSA?

**Problem:** "No such file or directory: demo/app.py"
**Çözüm:** Build command'ini şu yap:
```
pip install -r requirements.txt && pip install -r demo/requirements.txt
```

**Problem:** "ANTHROPIC_API_KEY not found"
**Çözüm:** Vercel settings'te env vars'a ekle, sonra redeploy et

**Problem:** Streamlit timeout
**Çözüm:** Vercel settings → Functions → Max Duration → 300 (5 min)

---

## 📌 KÖYNEĞİ

Vercel web arayüzü çok basit - sadece repo'yu bağla ve deploy et.
Otomatik olarak GitHub push'unca redeploy oluyor.

API key olmadan demo kısıtlı çalışacak (sadece Layer 1), ama tamam.

