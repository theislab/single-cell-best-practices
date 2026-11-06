1. **نصب conda**:
   - پیش از ایجاد محیط، مطمئن شوید [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) روی سامانهٔ شما نصب است.

2. **ذخیرهٔ محتوای yml**:
   - محتوای زبانهٔ yml را در فایلی با نام `environment.yml` کپی کنید.

3. **ایجاد محیط**:
   - یک ترمینال یا خط فرمان باز کنید.
   - دستور زیر را اجرا کنید:
     ```bash
     conda env create -f environment.yml
     ```

4. **فعال‌سازی محیط**:
   - پس از ایجاد محیط، آن را با دستور زیر فعال کنید:
     ```bash
     conda activate <environment_name>
     ```
   - به‌جای `<environment_name>`، نام مشخص‌شده در فایل `environment.yml` را قرار دهید. در فایل yml، این بخش به‌شکل زیر خواهد بود:
     ```yaml
     name: <environment_name>
     ```

5. **بررسی نصب**:
   - با اجرای دستور زیر بررسی کنید که محیط با موفقیت ایجاد شده است:
     ```bash
     conda env list
     ```
