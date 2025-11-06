# مجوزهای فایل و دایرکتوری

مجوزهای فایل یکی از مهم‌ترین مفاهیم امنیتی در لینوکس است که مشخص می‌کند چه کسی می‌تواند به فایل‌ها دسترسی داشته باشد.

## درک مجوزها

هر فایل و دایرکتوری در لینوکس دارای سه نوع مجوز است:

- **r** (read): خواندن
- **w** (write): نوشتن
- **x** (execute): اجرا

این مجوزها برای سه گروه تعریف می‌شوند:

1. **Owner**: مالک فایل
2. **Group**: گروه مالک
3. **Others**: سایر کاربران

## نمایش مجوزها

با دستور `ls -l` می‌توانید مجوزهای فایل‌ها را مشاهده کنید:

```bash
ls -l myfile.txt
```

خروجی:
```
-rw-r--r-- 1 username groupname 1024 Nov 06 10:30 myfile.txt
```

### تفسیر خروجی

```
-rw-r--r--
│││││││││└─── Others: Read
│││││││└───── Others: Write (-)
││││││└────── Others: Execute (-)
│││││└─────── Group: Read
││││└──────── Group: Write (-)
│││└───────── Group: Execute (-)
││└────────── Owner: Read
│└─────────── Owner: Write
└──────────── File Type (- = file, d = directory)
```

## تغییر مجوزها با chmod

دستور `chmod` (Change Mode) برای تغییر مجوزهای فایل استفاده می‌شود.

### روش نمادی (Symbolic)

```bash
# اضافه کردن مجوز اجرا برای مالک
chmod u+x script.sh

# حذف مجوز نوشتن از گروه
chmod g-w file.txt

# اضافه کردن مجوز خواندن برای همه
chmod a+r document.txt

# تنظیم مجوزهای دقیق
chmod u=rwx,g=rx,o=r file.txt
```

نمادها:
- `u` = user (مالک)
- `g` = group (گروه)
- `o` = others (دیگران)
- `a` = all (همه)

عملیات:
- `+` = اضافه کردن
- `-` = حذف کردن
- `=` = تنظیم دقیق

### روش عددی (Numeric)

مجوزها به صورت اعداد اُکتال نیز قابل نمایش هستند:

| مجوز | عدد |
|------|-----|
| --- | 0 |
| --x | 1 |
| -w- | 2 |
| -wx | 3 |
| r-- | 4 |
| r-x | 5 |
| rw- | 6 |
| rwx | 7 |

مثال‌ها:

```bash
# rwxr-xr-x (755)
chmod 755 script.sh

# rw-r--r-- (644)
chmod 644 document.txt

# rwx------ (700)
chmod 700 private-script.sh

# rw-rw-r-- (664)
chmod 664 shared-file.txt
```

## تغییر مالکیت با chown

دستور `chown` (Change Owner) برای تغییر مالک فایل استفاده می‌شود:

```bash
# تغییر مالک
sudo chown newuser file.txt

# تغییر مالک و گروه
sudo chown newuser:newgroup file.txt

# تغییر بازگشتی برای دایرکتوری
sudo chown -R newuser:newgroup directory/
```

## تغییر گروه با chgrp

دستور `chgrp` (Change Group) برای تغییر گروه مالک استفاده می‌شود:

```bash
# تغییر گروه
chgrp newgroup file.txt

# تغییر بازگشتی
chgrp -R newgroup directory/
```

## مجوزهای پیش‌فرض با umask

`umask` مجوزهای پیش‌فرض برای فایل‌ها و دایرکتوری‌های جدید را تعیین می‌کند:

```bash
# مشاهده umask فعلی
umask

# تنظیم umask
umask 022
```

چگونه umask کار می‌کند:
- مجوزهای پایه: فایل = 666, دایرکتوری = 777
- مجوزهای نهایی = مجوزهای پایه - umask
- مثال: با umask 022 → فایل = 644, دایرکتوری = 755

## مجوزهای ویژه

### SUID (Set User ID) - 4000

```bash
chmod u+s executable
chmod 4755 executable
```

فایل با مجوزات مالک اجرا می‌شود نه کاربر فعلی.

### SGID (Set Group ID) - 2000

```bash
chmod g+s directory
chmod 2755 directory
```

فایل‌های ایجاد شده در دایرکتوری گروه پدر را ارث می‌برند.

### Sticky Bit - 1000

```bash
chmod +t directory
chmod 1777 directory
```

فقط مالک فایل می‌تواند آن را حذف کند (معمولاً برای /tmp).

## مثال‌های کاربردی

### اسکریپت قابل اجرا

```bash
# ایجاد اسکریپت
echo '#!/bin/bash' > script.sh
echo 'echo "Hello World"' >> script.sh

# قابل اجرا کردن
chmod +x script.sh

# اجرا
./script.sh
```

### دایرکتوری اشتراکی

```bash
# ایجاد دایرکتوری برای تیم
mkdir /shared/teamwork
chmod 775 /shared/teamwork
chgrp developers /shared/teamwork
chmod g+s /shared/teamwork  # SGID
```

### فایل فقط‌خواندنی

```bash
chmod 444 important-config.conf
```

## تمرین عملی

1. یک فایل متنی ایجاد کنید
2. مجوزهای آن را به `rw-r--r--` تنظیم کنید (به دو روش)
3. یک اسکریپت ایجاد و قابل اجرا کنید
4. یک دایرکتوری با SGID ایجاد کنید
5. مجوزهای فایل‌ها را با `ls -l` بررسی کنید

## نکات امنیتی

⚠️ **توصیه‌های امنیتی:**

- هرگز بدون دلیل از `chmod 777` استفاده نکنید
- فایل‌های حساس را با مجوز `600` یا `400` نگه دارید
- از SUID با احتیاط استفاده کنید
- مجوزهای دایرکتوری `/home` را بررسی کنید

## خلاصه

در این بخش یاد گرفتید:

- ✅ مفهوم مجوزهای فایل (rwx)
- ✅ تغییر مجوزها با chmod (نمادی و عددی)
- ✅ تغییر مالکیت با chown و chgrp
- ✅ umask و مجوزهای پیش‌فرض
- ✅ مجوزهای ویژه (SUID, SGID, Sticky Bit)

با تسلط بر این مفاهیم، می‌توانید امنیت سیستم لینوکس خود را مدیریت کنید.
