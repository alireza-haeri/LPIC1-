
# 101.2 - راه‌اندازی سیستم (Boot)

## اهداف یادگیری

در این فصل با موارد زیر آشنا می‌شوید:

- ارسال دستورات رایج به bootloader و گزینه‌های کرنل در زمان بوت
- درک فرآیند بوت از BIOS/UEFI تا اتمام راه‌اندازی
- آشنایی با SysVinit و systemd
- آگاهی از Upstart
- بررسی رویدادهای بوت در فایل‌های لاگ

## کلیدواژه‌ها

`dmesg`, `journalctl`, `BIOS`, `UEFI`, `bootloader`, `kernel`, `initramfs`, `init`, `SysVinit`, `systemd`

---

## فرآیند بوت (Boot Process)

درک فرآیند بوت بسیار مهم است چرا که در این مرحله کنترل کمی روی سیستم دارید و نمی‌توانید دستورات زیادی برای عیب‌یابی اجرا کنید. باید درک خوبی از اتفاقات داشته باشید.

**مراحل بوت به ترتیب:**

1. میان‌افزار مادربورد تست POST را انجام می‌دهد
2. مادربورد bootloader را بارگذاری می‌کند
3. Bootloader کرنل لینوکس را بر اساس تنظیمات خود بارگذاری می‌کند
4. کرنل بارگذاری شده و سیستم فایل root را آماده می‌کند و برنامه init را اجرا می‌کند
5. برنامه init سرویس‌ها مانند وب سرور، رابط گرافیکی، شبکه و... را راه‌اندازی می‌کند

همان‌طور که در فصل قبل (101.1) بحث شد، میان‌افزار مادربورد می‌تواند BIOS یا UEFI باشد.

---

## BIOS

**BIOS** (سیستم ورودی/خروجی پایه):

- فناوری قدیمی
- محدود به یک سکتور دیسک و نیاز به bootloader چند مرحله‌ای دارد
- می‌تواند از هارد داخلی/خارجی، CD/DVD، فلش USB یا سرور شبکه بوت کند
- هنگام بوت از هارد، از Master Boot Record استفاده می‌کند (1 سکتور)

## UEFI

**UEFI** (رابط میان‌افزار توسعه‌یافته یکپارچه):

- مدرن و پیشرفته
- پارتیشن مخصوصی برای bootloader تعریف می‌کند به نام EFI System Partition (ESP)
- ESP از سیستم فایل FAT استفاده می‌کند و روی `/boot/efi` mount می‌شود
- فایل‌های bootloader پسوند `.efi` دارند

**بررسی استفاده از UEFI:**

```bash
ls /sys/firmware/efi
```

!!! note "نکته"
    اگر این مسیر وجود داشته باشد، سیستم شما از UEFI استفاده می‌کند.

---

## Bootloader

Bootloader حداقل سخت‌افزار لازم برای بوت سیستم را راه‌اندازی می‌کند، سپس سیستم عامل را پیدا کرده و اجرا می‌کند.

از نظر فنی می‌توانید UEFI را برای اجرای هر برنامه‌ای تنظیم کنید، اما معمولاً در سیستم‌های گنو/لینوکس از **GRUB** استفاده می‌شود. GRUB می‌تواند هر برنامه مشخصی را اجرا کند اما معمولاً سیستم عامل را اجرا می‌کند.

---

## Kernel (هسته)

کرنل هسته اصلی سیستم عامل است و در واقع خود لینوکس است. Bootloader کرنل را در حافظه بارگذاری کرده و اجرا می‌کند.

کرنل برای شروع به اطلاعات اولیه نیاز دارد، مانند درایورهای ضروری برای کار با سخت‌افزار. این اطلاعات در **initrd** یا **initramfs** در کنار کرنل ذخیره شده و در زمان بوت استفاده می‌شوند.

### پارامترهای کرنل

می‌توانید با استفاده از تنظیمات GRUB، پارامترهایی به کرنل ارسال کنید:

| پارامتر | توضیح |
|---------|-------|
| `1` یا `S` | بوت در حالت تک‌کاربره (recovery) |
| `vga=792` | اجبار گرافیک به حالت 1024×768×24 |

---

## بررسی لاگ‌های بوت

### dmesg

لینوکس در حین بوت لاگ‌های فرآیند را نمایش می‌دهد. برخی سیستم‌های دسکتاپ این لاگ‌ها را پشت صفحه splash پنهان می‌کنند که می‌توانید با کلید `Esc` یا `Ctrl+Alt+F1` آن را ببینید.

کرنل لاگ‌های خود را در **Kernel Ring Buffer** ذخیره می‌کند. پس از اتمام بوت، سرویس syslog این لاگ‌ها را جمع‌آوری کرده و در `/var/log/dmesg` ذخیره می‌کند.

**مشاهده تمام لاگ‌ها:**

```bash
dmesg
```

**مشاهده لاگ‌های اخیر:**

```bash
dmesg | tail -50
```

**مشاهده لاگ‌ها به صورت زنده:**

```bash
dmesg -w
```

**پاک کردن ring buffer:**

```bash
sudo dmesg -c
```

### journalctl

**بررسی لاگ‌های کرنل:**

```bash
journalctl -k
```

**بررسی لاگ‌های بوت فعلی:**

```bash
journalctl -b
```

**بررسی تمام لاگ‌های بوت قبلی:**

```bash
journalctl -u kernel
```

### فایل‌های لاگ

اکثر سیستم‌ها لاگ‌های بوت را در فایل‌های متنی نیز نگه می‌دارند:

- **دبیان:** `/var/log/boot`
- **Red Hat:** `/var/log/boot.log`

---

## /var/log/messages

پس از اجرای فرآیند init، سرویس syslog پیام‌ها را لاگ می‌کند. این لاگ‌ها دارای timestamp هستند و پس از ریبوت نیز باقی می‌مانند.

!!! info "نکات مهم"
    - کرنل همچنان پیام‌های خود را در Kernel Ring Buffer ثبت می‌کند
    - در برخی سیستم‌ها `/var/log/syslog` نامیده می‌شود
    - لاگ‌های بسیار دیگری در `/var/log` وجود دارند

**مشاهده لاگ:**

```bash
tail -f /var/log/messages
```

**یا در سیستم‌های دبیان:**

```bash
tail -f /var/log/syslog
```

---

## Init (فرآیند راه‌اندازی)

وقتی راه‌اندازی کرنل تمام می‌شود، زمان اجرای برنامه‌های دیگر است. برای این کار، کرنل فرآیند **Initialization Daemon** را اجرا می‌کند که مسئول راه‌اندازی سایر سرویس‌ها، daemon ها و زیرسیستم‌هاست.

با استفاده از سیستم init می‌توان گفت: "ابتدا سرویس A سپس B را اجرا کن. سپس C، D و E را اجرا کن اما D را تا زمانی که A و B در حال اجرا نیستند، شروع نکن".

---

## انواع سیستم Init

### SysVinit

- مبتنی بر Unix System V
- دیگر زیاد استفاده نمی‌شود اما محبوب بود چون از اصول یونیکس پیروی می‌کرد
- ممکن است در سیستم‌های قدیمی یا حتی برخی نصب‌های جدید ببینید

### Upstart

- جایگزین event-based برای init سنتی توسط Canonical (سازندگان اوبونتو)
- هدف: جایگزینی SysV هنگام انتشار در 2007
- پروژه متوقف شد به دلیل پذیرش گسترده Systemd
- حتی اوبونتو امروزه از Systemd استفاده می‌کند
- هنوز در ChromeOS گوگل یافت می‌شود

### Systemd

- جایگزین جدید و پرکاربرد
- توسط برخی به دلیل عدم پیروی از اصول یونیکس انتقاد می‌شود
- به طور گسترده توسط توزیع‌های اصلی پذیرفته شده
- می‌تواند سرویس‌ها را به صورت موازی راه‌اندازی کند
- امکانات پیشرفته زیادی دارد

---

## شناسایی سیستم Init

فرآیند init همیشه شناسه **PID 1** دارد:

```bash
which init
```

**خروجی:**

```
/sbin/init
```

**بررسی نوع init:**

```bash
readlink -f /sbin/init
```

**خروجی در systemd:**

```
/usr/lib/systemd/systemd
```

**مشاهده فرآیند شماره 1:**

```bash
ps -p 1
```

**خروجی:**

```
PID TTY TIME     CMD
1   ?   00:00:06 systemd
```

**مشاهده درخت فرآیندها:**

```bash
pstree
```

---

## Systemd

Systemd جدید، دوست‌داشتنی و نفرت‌انگیز است. ایده‌های جدید زیادی دارد اما برخی اصول محبوب یونیکس را دنبال نمی‌کند (مثلاً لاگ‌ها را در فایل متنی ذخیره نمی‌کند).

**امکانات:**
- اجرای سرویس‌ها هنگام اتصال سخت‌افزار
- اجرای سرویس‌ها در بازه‌های زمانی
- اجرای سرویس‌ها وقتی سرویس دیگری شروع شود
- و...

### واحدها (Units)

Systemd حول **واحدها (units)** ساخته شده. یک واحد می‌تواند یک سرویس، گروهی از سرویس‌ها یا یک عملیات باشد.

واحدها دارای نام، نوع و فایل پیکربندی هستند.

**12 نوع واحد:**
`automount`, `device`, `mount`, `path`, `scope`, `service`, `slice`, `snapshot`, `socket`, `swap`, `target`, `timer`

### systemctl

**لیست تمام واحدها:**

```bash
systemctl list-units
```

**لیست فقط targetها:**

```bash
systemctl list-units --type=target
```

**مشاهده target پیش‌فرض:**

```bash
systemctl get-default
```

!!! note "توضیح"
    گروه‌های سرویس‌ها از طریق فایل‌های واحد target راه‌اندازی می‌شوند.

### محل قرارگیری واحدها

واحدها در این مسیرها قرار دارند (به ترتیب اولویت):

1. `/etc/systemd/system/`
2. `/run/systemd/system/`
3. `/usr/lib/systemd/system/`

**لیست تمام فایل‌های واحد:**

```bash
systemctl list-unit-files
```

**مشاهده محتوای یک واحد:**

```bash
systemctl cat sshd.service
```

**مشاهده target گرافیکی:**

```bash
systemctl cat graphical.target
```

### مدیریت سرویس‌ها

**توقف سرویس:**

```bash
systemctl stop sshd
```

**راه‌اندازی سرویس:**

```bash
systemctl start sshd
```

**وضعیت سرویس:**

```bash
systemctl status sshd
```

**بررسی فعال بودن:**

```bash
systemctl is-active sshd
```

**بررسی خطا:**

```bash
systemctl is-failed sshd
```

**راه‌اندازی مجدد:**

```bash
systemctl restart sshd
```

**بارگذاری مجدد تنظیمات سرویس:**

```bash
systemctl reload sshd
```

**بارگذاری مجدد تنظیمات systemd:**

```bash
systemctl daemon-reload
```

**فعال‌سازی خودکار در بوت:**

```bash
systemctl enable sshd
```

**غیرفعال‌سازی در بوت:**

```bash
systemctl disable sshd
```

### دستورات اضافی

**بررسی وضعیت کلی سیستم:**

```bash
systemctl is-system-running
```

**خروجی احتمالی:** `running`, `degraded`, `maintenance`, `initializing`, `starting`, `stopping`

**مشاهده سرویس‌های با خطا:**

```bash
systemctl --failed
```

---

## journalctl (بررسی لاگ‌ها)

**مشاهده تمام لاگ‌ها:**

```bash
journalctl
```

**بدون استفاده از less:**

```bash
journalctl --no-pager
```

**فقط 10 خط آخر:**

```bash
journalctl -n 10
```

**لاگ‌های 24 ساعت اخیر:**

```bash
journalctl -S -1d
```

**لاگ‌های اخیر با جزئیات:**

```bash
journalctl -xe
```

**لاگ‌های یک سرویس خاص:**

```bash
journalctl -u sshd
```

**لاگ‌های یک فرآیند خاص:**

```bash
journalctl _PID=1234
```

**لاگ‌های بوت فعلی:**

```bash
journalctl -b
```

**لاگ‌های بوت قبلی:**

```bash
journalctl -b -1
```

**لاگ‌های کرنل:**

```bash
journalctl -k
```

**پیگیری لاگ‌ها به صورت زنده:**

```bash
journalctl -f
```

---

## SysV Init

سیستم init قدیمی که هنوز در بسیاری از سیستم‌ها قابل استفاده است.

فایل‌های کنترل در `/etc/init.d/` قرار دارند و شبیه اسکریپت‌های bash معمولی هستند.

**مشاهده وضعیت:**

```bash
/etc/init.d/sshd status
```

**توقف سرویس:**

```bash
/etc/init.d/sshd stop
```

**راه‌اندازی سرویس:**

```bash
/etc/init.d/sshd start
```

**راه‌اندازی مجدد:**

```bash
/etc/init.d/sshd restart
```

**یا استفاده از دستور service:**

```bash
service sshd status
service sshd start
service sshd stop
service sshd restart
```

!!! tip "نکته"
    در فصل 101.3 بیشتر درباره runlevel ها صحبت خواهیم کرد.

---

## تمرین‌های عملی

### تمرین 1: بررسی لاگ‌های بوت

```bash
dmesg | less
journalctl -b
cat /var/log/boot.log
```

### تمرین 2: بررسی سیستم init

```bash
ps -p 1
systemctl --version
```

### تمرین 3: کار با systemd

```bash
systemctl list-units --type=service
systemctl status NetworkManager
systemctl is-enabled sshd
```

### تمرین 4: بررسی خطاها

```bash
systemctl --failed
journalctl -p err -b
```

### تمرین 5: مدیریت سرویس

```bash
systemctl stop cups
systemctl status cups
systemctl start cups
systemctl restart cups
```

---

## خلاصه

در این فصل یاد گرفتیم:

- مراحل فرآیند بوت از BIOS/UEFI تا init
- تفاوت BIOS و UEFI در فرآیند بوت
- نقش bootloader، kernel و initramfs
- بررسی لاگ‌های بوت با `dmesg` و `journalctl`
- تفاوت SysVinit، Upstart و systemd
- کار با `systemctl` برای مدیریت سرویس‌ها
- بررسی لاگ‌ها با `journalctl`
- مدیریت سرویس‌ها در SysV

!!! example "نکات کلیدی برای آزمون"
    - ترتیب مراحل بوت
    - تفاوت `/var/log/messages` و `dmesg`
    - دستورات `systemctl` برای مدیریت سرویس‌ها
    - گزینه‌های `journalctl` برای فیلتر لاگ‌ها
    - محل فایل‌های واحد systemd
    - PID فرآیند init همیشه 1 است
