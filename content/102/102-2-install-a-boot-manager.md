# 102.2 - نصب Boot Manager

## اهداف یادگیری

در این فصل با موارد زیر آشنا می‌شوید:

- انتخاب، نصب و پیکربندی Boot Manager  
- فراهم کردن گزینه‌های بوت جایگزین و پشتیبان  
- نصب و پیکربندی Boot Loader مانند GRUB Legacy  
- انجام تغییرات پیکربندی پایه در GRUB2  
- تعامل با Boot Loader  

## کلیدواژه‌ها

`menu.lst`, `grub.cfg`, `grub.conf`, `grub-install`, `grub-mkconfig`, `MBR`, `chainloader`

---

## مرور فرآیند بوت

- در سیستم‌های **BIOS**:  
  - اجرای تست POST (Power-On Self-Test)  
  - انتقال کنترل به اولین سکتور دیسک (MBR)  
  - MBR فقط 512 بایت است، بنابراین نیاز به Bootloader هوشمند داریم (مانند LILO، GRUB، GRUB2)  

- در سیستم‌های **UEFI**:  
  - مراحل امنیتی و سپس جستجوی EFI System Partition (ESP)  
  - ESP یک پارتیشن FAT32 است که فایل‌های اجرایی PE را نگه می‌دارد  

!!! note "نکته"
    Chain Loading زمانی است که یک Bootloader، Bootloader دیگری را اجرا می‌کند. مثال: بوت لینوکس که ویندوز را chainload می‌کند.

---

## GRUB

**GRUB (GRand Unified Bootloader)** جایگزین LILO شد.  
- **Grub Legacy (نسخه 1)**: شروع از 1999  
- **Grub2 (نسخه 2)**: بازنویسی کامل در 2005  

ویژگی‌ها:  
- منوی انتخاب کرنل یا chainloader  
- امکان ویرایش منوها در لحظه  
- خط فرمان داخلی برای اجرای دستورات  

---

## Grub Legacy

- مسیر نصب: `/boot/grub/`  
- فایل پیکربندی: `menu.lst` یا `grub.conf`  

### تنظیمات عمومی

| گزینه | توضیح |
|-------|-------|
| `color` | رنگ متن و پس‌زمینه |
| `default` | آیتم پیش‌فرض بوت |
| `fallback` | آیتم جایگزین در صورت شکست بوت |
| `hiddenmenu` | مخفی کردن منو |
| `splashimage` | تصویر پس‌زمینه |
| `timeout` | زمان انتظار قبل از بوت پیش‌فرض |
| `password` | رمز عبور برای امنیت |
| `savedefault` | ذخیره آخرین آیتم بوت شده |

### تنظیمات بخش کرنل/Chainloader

| گزینه | توضیح |
|-------|-------|
| `title` | نام بخش |
| `root` | دیسک و پارتیشن `/boot` |
| `kernel` | فایل کرنل در `/boot` |
| `initrd` | فایل initramfs |
| `rootnoverify` | پارتیشن غیر لینوکسی |
| `chainloader` | اجرای Bootloader دیگر (مثلاً ویندوز) |

### نصب GRUB Legacy

```bash
grub-install /dev/sda
grub-install '(fd0)'
```

!!! warning "هشدار"
    اگر GRUB را خارج از MBR نصب کنید، باید از chainloader برای اشاره به آن استفاده کنید.

### تعامل با GRUB Legacy

- کلید `e`: ویرایش آیتم انتخابی  
- کلید `c`: ورود به خط فرمان GRUB  
- دستورات: `root`, `kernel`, `initrd`, `boot`  

---

## GRUB2

- مسیر نصب:  
  - BIOS: `/boot/grub/` یا `/boot/grub2/`  
  - UEFI: `/boot/efi/EFI/<distro>/`  

- فایل پیکربندی: `grub.cfg`  

### نمونه ساده grub.cfg

```bash
set default="0"
menuentry "Fedora" {
  set root=(hd0,1)
  linux /boot/vmlinuz-5.10.0-9-arm64 ro quiet
  initrd /boot/initrd.img-5.10.0-9-arm64
}
menuentry "Windows" {
  chainloader (hd1,msdos2)+1
}
```

### گزینه‌های مهم

| گزینه | توضیح |
|-------|-------|
| `menuentry` | تعریف آیتم منو |
| `set root` | محل `/boot` |
| `linux`, `linux16` | کرنل لینوکس در BIOS |
| `linuxefi` | کرنل لینوکس در UEFI |
| `initrd`, `initrdefi` | فایل initramfs |

### نصب و پیکربندی GRUB2

```bash
grub-install /dev/sda
grub2-mkconfig -o /boot/grub2/grub.cfg
```

یا:

```bash
update-grub
```

!!! info "نکته"
    `update-grub` در واقع یک frontend برای `grub-mkconfig` است.

### تعامل با GRUB2

- کلید `c`: ورود به خط فرمان GRUB  
- دستورات مشابه GRUB Legacy (`root`, `linux`, `initrd`, `boot`)  

---

## پارامترهای کرنل

نمونه:

```bash
linux /boot/vmlinuz-5.10.0-9-arm64 root=/dev/sda1 ro quiet
```

گزینه‌های رایج:

| گزینه | توضیح |
|-------|-------|
| `console=` | تعیین کنسول |
| `debug` | حالت اشکال‌زدایی |
| `init=` | اجرای برنامه خاص به جای init پیش‌فرض |
| `ro` | mount ریشه به صورت read-only |
| `rw` | mount ریشه به صورت read-write |
| `root=` | تعیین فایل‌سیستم ریشه |
| `selinux` | غیرفعال کردن SELinux |
| `single` یا `S` یا `1` | بوت در حالت تک‌کاربره |
| `systemd.unit=` | بوت در target مشخص systemd |

---

## تمرین‌های عملی

### تمرین 1: نصب GRUB Legacy
```bash
grub-install /dev/sda
```

### تمرین 2: بررسی فایل پیکربندی GRUB Legacy
```bash
cat /boot/grub/menu.lst
```

### تمرین 3: نصب GRUB2
```bash
grub-install /dev/sda
grub2-mkconfig -o /boot/grub2/grub.cfg
```

### تمرین 4: تغییر پارامترهای کرنل
```bash
linux /boot/vmlinuz root=/dev/sda1 ro single
```

---

## خلاصه

در این فصل یاد گرفتیم:

- تفاوت فرآیند بوت در BIOS و UEFI  
- نقش MBR و ESP در بوت  
- ساختار و تنظیمات GRUB Legacy (`menu.lst`, `grub.conf`)  
- نصب و پیکربندی GRUB2 (`grub.cfg`)  
- تعامل با Bootloader از طریق منو و خط فرمان  
- ارسال پارامترهای کرنل در زمان بوت  

!!! example "نکات کلیدی برای آزمون"
    - تفاوت GRUB Legacy و GRUB2  
    - مسیرهای نصب در BIOS و UEFI  
    - دستورات `grub-install`, `grub-mkconfig`, `update-grub`  
    - پارامترهای کرنل مانند `ro`, `rw`, `single`  
    - مفهوم chainloader برای بوت ویندوز  
