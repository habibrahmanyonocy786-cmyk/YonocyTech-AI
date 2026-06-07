# Plane (برنامهٔ کاری و تغییرات اعمال‌شده)

این فایل برنامهٔ اصلاحات و تغییراتی است که برای دیباگ، بهبود و آماده‌سازی پروژه YonocyTech-AI انجام شد یا باید انجام شود. فایلِ اصلی در شاخه feature/modern-frontend-signup به‌روز شده و این نسخه در ریپازیتوری ذخیره شده است. لطفاً اگر نیاز دارید این فایل را در مسیر محلی `F:\AI Coder\YonocyTechAgent\YonocyTech` ذخیره کنید، می‌توانید آن را از این مخزن دانلود و به آن مسیر منتقل کنید.

تاریخ: 2026-06-07
نویسنده: Copilot (automated changes)

خلاصهٔ هدف:
- رفع مشکلات اجرا و build
- فعال‌سازی صحیح Tailwind و PostCSS
- سازگار کردن Dev proxy Vite با مسیرهای API
- استفاده از متغیر محیطی برای URL API
- اصلاح Dockerfile برای ساخت پایدار
- اضافه کردن health endpoint

تغییرات اعمال‌شده (فایل‌ها):
1. vite.config.js
   - حذف rewrite در proxy تا مسیرهای /api/* بدون تغییر فوروارد شوند.
2. src/index.css
   - جایگزینی `@import 'tailwindcss/...';` با دستورات استاندارد Tailwind: `@tailwind base; @tailwind components; @tailwind utilities;`
3. postcss.config.cjs
   - فایل جدید برای فعال‌سازی tailwindcss و autoprefixer.
4. Dockerfile
   - تغییر `npm ci` به `npm install` تا ساخت بدون package-lock.json نیز کار کند.
5. src/store/authStore.js
   - تغییر fetchها برای استفاده از مقدار پایه API از متغیر محیطی `VITE_API_URL` (فولدبک به '' اگر تنظیم نشده باشد).
6. server.js
   - اضافه شدن endpoint: GET /api/health برای health check.
7. package.json
   - اضافه شدن devDependencies: postcss و autoprefixer.
8. plane.md (این فایل)
   - شامل راهنمای تست، چک‌لیست و مراحل بعدی.

راهنمای تست محلی (پس از pull):
1. نصب وابستگی‌ها:
   npm install

2. اجرای در حالت توسعه:
   npm run dev    # frontend روی http://localhost:5173
   npm start      # backend روی http://localhost:3000

3. تست فرانت‌اند:
   - به http://localhost:5173 بروید.
   - فرم ثبت‌نام را تکمیل کنید؛ در DevTools -> Network درخواست باید به http://localhost:3000/api/auth/signup ارسال شود.

4. تست build:
   npm run build
   npm start
   - بازدید از http://localhost:3000

5. تست Docker:
   docker build -t yonocytech-ai .
   docker run -p 3000:3000 yonocytech-ai

مواردی که هنوز نیاز به کار بیشتری دارند:
- جایگزین کردن auth mock با دیتابیس واقعی و رمزنگاری (bcrypt + JWT).
- اضافه کردن rate limiting و helmet برای امنیت بیشتر.
- افزودن تست‌های واحد و e2e و pipeline CI (GitHub Actions).

درخواست‌های احتمالی بعدی:
- می‌خواهم که شما همین تغییرات را در مخزن اعمال کنید و سپس به من اطلاع دهید تا تست کنم. (انجام شده)
- می‌خواهم این فایل plane.md را در مسیر محلی `F:\AI Coder\YonocyTechAgent\YonocyTech` داشته باشم — نمی‌توانم مستقیم به فایل‌های محلی شما دسترسی داشته باشم؛ می‌توانم این فایل را در مخزن GitHub قرار دهم تا دانلود کنید یا آن را در یک zip برای شما آماده کنم.

لینک commit: https://github.com/habibrahmanyonocy786-cmyk/YonocyTech-AI/commit/6f8d7d31cd1db83df1901cf40055826509908a30

اگر می‌خواهید من همین حالا این تغییرات را merge به main کنم، یا Pull Request بسازم، دستور دهید: "Create PR" یا "Merge to main".
