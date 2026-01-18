# 🚀 Manuel Vercel Deployment

Browser agent sistem limitlerine takıldığı için, son adımı manuel yapman gerekiyor.

### 1. Environment Variable Ekle
👉 [Vercel Env Vars Sayfasına Git](https://vercel.com/serdars-projects-a7056390/jailbreak-shield/settings/environment-variables)

**Key:** `ANTHROPIC_API_KEY`  
**Value:** `[SANA VERDİĞİM API KEY]` (Buraya yazmıyorum güvenlik için)

Seçenekler:
- [x] Production
- [x] Preview
- [x] Development

**Save** butonuna tıkla.

### 2. Redeploy Et
1. [Deployments Sayfasına Git](https://vercel.com/serdars-projects-a7056390/jailbreak-shield/deployments)
2. En üstteki (muhtemelen fail eden) deployment yanındaki **3 nokta** ikonuna tıkla.
3. **Redeploy** seçeneğini seç.
4. "Use existing Build Cache" kutusunu **BOŞ BIRAK**.
5. **Redeploy** butonuna bas.

İşlem tamamlanınca yeni URL'i paylaşabilirsin.
