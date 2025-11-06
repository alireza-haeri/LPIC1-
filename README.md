# راهنمای جامع LPIC-1

مجموعه آموزش LPIC-1 به زبان فارسی

## هدف پروژه

آموزش گواهینامه LPIC-1 (Linux Professional Institute Certification) به زبان فارسی با استفاده از MkDocs و Material theme.

## مشاهده آنلاین

**[https://alireza-haeri.github.io/LPIC1-/](https://alireza-haeri.github.io/LPIC1-/)**

## نحوه اجرا

```bash
cd lpic1-guide
pip install -r requirements.txt
mkdocs serve
```

سپس به `http://127.0.0.1:8000` بروید.

## اضافه کردن درس جدید

1. یک فایل `.md` در پوشه `docs/` ایجاد کنید
2. محتوای درس را به فارسی بنویسید (کدها باید LTR باشند)
3. فایل را به `nav` در `mkdocs.yml` اضافه کنید
4. فایل را به لیست در `docs/lessons.md` اضافه کنید

مثال:

```yaml
nav:
  - خانه: index.md
  - فهرست دروس: lessons.md
  - دروس:
    - مبانی لینوکس: basics.md
    - درس جدید: new-lesson.md
```

## ویژگی‌ها

- پشتیبانی کامل RTL برای متن فارسی
- کدها و دستورات LTR
- حالت روشن و تاریک
- ناوبری بین دروس (قبلی/بعدی)
- جستجوی فارسی

---

**ساخته شده با ❤️ برای جامعه لینوکس ایران**
