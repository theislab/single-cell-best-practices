این کتاب از [lamindb](https://github.com/laminlabs/lamindb) برای ذخیره، اشتراک‌گذاری و بارگیری مجموعه‌داده‌ها و نوت‌بوک‌ها با استفاده از [نمونهٔ theislab/sc-best-practices](https://lamin.ai/theislab/sc-best-practices) استفاده می‌کند.
از [Lamin Labs](https://lamin.ai/) برای میزبانی رایگان سپاسگزاریم.

1. **نصب lamindb**
   - بستهٔ Python به نام lamindb را نصب کنید:

   ```bash
   pip install lamindb
   ```

2. **ایجاد اختیاری حساب lamin**
   - با پیروی از [دستورالعمل‌ها](https://docs.lamin.ai/setup#sign-up-log-in)، ثبت‌نام کنید و وارد حساب شوید.

3. **بررسی راه‌اندازی**
   - دستور `lamin connect` را اجرا کنید:

   ```python
   import lamindb as ln

   ln.Artifact.connect("theislab/sc-best-practices").df()
   ```

   اکنون باید حداکثر ۱۰۰ مجموعه‌دادهٔ ذخیره‌شده را ببینید.

4. **دسترسی به مجموعه‌داده‌ها (Artifacts)**
   - مجموعه‌داده‌ها را در [صفحهٔ Artifacts](https://lamin.ai/theislab/sc-best-practices/artifacts) جست‌وجو کنید.
   - یک Artifact و شیء متناظر با آن را بارگیری کنید:

   ```python
   import lamindb as ln

   af = ln.Artifact.connect("theislab/sc-best-practices").get(
       key="key_of_dataset", is_latest=True
   )
   obj = af.load()
   ```

   اکنون شیء در حافظه در دسترس و آمادهٔ تحلیل است.
   پسوند [`lamindb.Artifact.connect("theislab/sc-best-practices").get("SOMEIDXXXX")`](xref:lamindb#lamindb.Artifact.connect) را برای دریافت نسخهٔ موردنظر تغییر دهید.

5. **دسترسی به نوت‌بوک‌ها (Transforms)**
   - نوت‌بوک را در [صفحهٔ Transforms](https://lamin.ai/theislab/sc-best-practices/transforms) جست‌وجو کنید.
   - نوت‌بوک را بارگیری کنید:

   ```bash
   lamin load <notebook url>
   ```

   این دستور نوت‌بوک را در پوشهٔ کاری فعلی دریافت می‌کند.
   همانند `Artifacts`، می‌توانید با تغییر شناسهٔ پسوند، نسخه‌های قدیمی‌تر را دریافت کنید.
