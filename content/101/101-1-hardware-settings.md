# 101.1 - تشخیص و پیکربندی تنظیمات سخت‌افزار

## اهداف یادگیری

در این فصل با موارد زیر آشنا می‌شوید:

- فعال و غیرفعال کردن تجهیزات جانبی یکپارچه
- تشخیص تفاوت انواع دستگاه‌های ذخیره‌سازی
- تعیین منابع سخت‌افزاری برای دستگاه‌ها
- ابزارهای لیست کردن اطلاعات سخت‌افزاری (lsusb، lspci و...)
- ابزارهای مدیریت دستگاه‌های USB
- درک مفهومی sysfs، udev و dbus

## کلیدواژه‌ها

/sys - /proc - /dev - modprobe - lsmod - lspci - lsusb

---

## مفاهیم پایه

### سیستم عامل

سیستم عامل (Operating System) نرم‌افزاری است که:

- سخت‌افزار کامپیوتر را مدیریت می‌کند
- منابع نرم‌افزاری را کنترل می‌کند  
- سرویس‌های مشترک به برنامه‌ها ارائه می‌دهد

سیستم عامل لایه‌ای بین سخت‌افزار و برنامه‌هاست. وقتی برنامه‌های کاربردی به منابعی نیاز دارند، سیستم عامل آن‌ها را مدیریت و تخصیص می‌دهد.

### Firmware (میان‌افزار)

Firmware نرم‌افزاری است که مستقیماً روی سخت‌افزار اجرا می‌شود و می‌توان آن را به عنوان سیستم عامل یا درایور داخلی سخت‌افزار در نظر گرفت. مادربوردها نیز برای کار به firmware نیاز دارند.

---

## انواع Firmware بوت

### BIOS

BIOS (Basic Input/Output System) فناوری قدیمی است که امروزه منسوخ شده:

- رابط کاربری متنی دارد
- کامپیوتر را با خواندن MBR (اولین بخش دیسک) بوت می‌کند
- برای سیستم‌های مدرن کافی نیست
- از دیسک‌های بزرگ‌تر از 2TB پشتیبانی نمی‌کند

### UEFI

UEFI (Unified Extensible Firmware Interface) استاندارد فعلی است:

- سال 1998 توسط Intel با نام EFI معرفی شد
- از پارتیشن مخصوص EFI System Partition (ESP) استفاده می‌کند
- سیستم فایل FAT دارد
- در لینوکس روی /boot/efi قرار می‌گیرد
- فایل‌ها با پسوند .efi ذخیره می‌شوند
- از دیسک‌های بزرگ‌تر از 2TB پشتیبانی می‌کند
- امکانات امنیتی بیشتری دارد

---

## تجهیزات جانبی

### PCI

PCI (Peripheral Component Interconnect) به کاربران اجازه می‌دهد قطعات اضافی به مادربورد متصل کنند. امروزه اکثر سیستم‌ها از PCI Express یا PCIe استفاده می‌کنند.

### انواع هارد دیسک داخلی

- PATA: فناوری قدیمی موازی
- SATA: فناوری سریال که تا 4 دستگاه پشتیبانی می‌کند (نسخه‌های II و III)
- SCSI: رابط موازی که تا 8 دستگاه پشتیبانی می‌کند

### سایر تجهیزات

- هارد دیسک خارجی: Fiber، SSD over USB
- کارت شبکه: RJ-45
- کارت بی‌سیم: IEEE 802.11
- بلوتوث: IEEE 802.15 (برد تا 10 متر)
- کارت گرافیک و صوت

### مقایسه SSD و HDD

SSD سریع‌تر (خواندن 10 برابر، نوشتن 20 برابر)، بی‌صداتر، کوچک‌تر، مقاوم‌تر و کم‌مصرف‌تر است. در مقابل HDD ارزان‌تر و با ظرفیت بیشتر است.

تفاوت اصلی: SSD بدون قطعات متحرک و با حافظه فلش کار می‌کند، اما HDD دارای بازوهای مکانیکی و صفحات چرخان است.

عمر مفید:
- HDD: 3 تا 5 سال
- SSD: بیش از 10 سال (به دلیل مکانیزم Bad-Block-Management)

### کارت شبکه vs کارت بی‌سیم

- NIC (کارت شبکه): اتصال سیمی از طریق پورت RJ45
- کارت بی‌سیم: اتصال بدون سیم از طریق Access Point

### USB

USB (Universal Serial Bus) رابطی سریال با سرعت‌های مختلف:

- USB 1.0: 12 Mbps
- USB 2.0: 480 Mbps  
- USB 3.0: 5 Gbps
- USB 3.1: 10 Gbps
- USB 3.2: 20 Gbps
- USB 4.0: 40 Gbps

انواع کانکتور: Type-A، Type-B، Type-C

### GPIO

GPIO (General Purpose Input/Output) پین‌های ورودی/خروجی عمومی هستند که برای کنترل سخت‌افزارهای خارجی استفاده می‌شوند. مثال‌ها: Arduino، Raspberry Pi

---

## مسیرهای مهم سیستم

### /sys (Sysfs)

Sysfs یک سیستم فایل مجازی است که اطلاعات کرنل، دستگاه‌های سخت‌افزاری و درایورها را در اختیار کاربر قرار می‌دهد.

دستور بررسی:

ls /sys

خروجی شامل:
- block: دستگاه‌های بلوکی
- bus: دستگاه‌های PCI، USB و...
- class: دسته‌بندی دستگاه‌ها
- devices: لیست کلی دستگاه‌ها

نکته: در /sys دستگاه‌ها بر اساس فناوری دسته‌بندی می‌شوند اما /dev انتزاعی است.

### /dev (Device Files)

udev مدیریت‌کننده دستگاه‌ها در لینوکس است که:

- گره‌های دستگاه را در /dev مدیریت می‌کند
- رویدادهای اتصال/قطع دستگاه را کنترل می‌کند
- firmware مورد نیاز را بارگذاری می‌کند
- قوانل سفارشی برای دستگاه‌ها اجرا می‌کند

مثال بررسی پارتیشن‌های هارد:

ls /dev/sda*

خروجی نمونه:

/dev/sda /dev/sda1 /dev/sda2 /dev/sda3

انواع دستگاه‌ها:

- c (character device): دستگاه‌های کاراکتری مانند صفحه کلید
- b (block device): دستگاه‌های بلوکی مانند هارد دیسک

مثال:

ls -lh /dev/ | head

خروجی نمونه:

crw-rw---- 1 root tty 4, 1 Dec 15 2019 tty1
brw-rw---- 1 root disk 8, 0 Dec 15 2019 sda

قابلیت udev: می‌توانید با قوانین سفارشی نام‌گذاری دلخواه انجام دهید. مثلاً فلش مموری همیشه به عنوان /dev/mybackup شناخته شود و هنگام اتصال، اسکریپت پشتیبان‌گیری اجرا شود.

### /proc (Process Information)

دایرکتوری /proc محلی است که کرنل تنظیمات و اطلاعات خود را نگه می‌دارد. این دایرکتوری در RAM ساخته می‌شود.

محتویات اصلی:
- IRQ: درخواست‌های وقفه
- I/O ports: پورت‌های ورودی/خروجی
- DMA: دسترسی مستقیم به حافظه
- اطلاعات پروسس‌ها
- تنظیمات شبکه

بررسی محتوا:

ls /proc/

اعداد نمایش داده شده شناسه پروسس‌ها (PID) هستند.

مثال - مشاهده اطلاعات CPU:

cat /proc/cpuinfo

مثال - مشاهده اطلاعات حافظه:

cat /proc/meminfo

مثال - تغییر حداکثر فایل‌های باز:

cat /proc/sys/fs/file-max
echo 1000000 > /proc/sys/fs/file-max
cat /proc/sys/fs/file-max

نکته مهم: تغییرات در /proc موقتی هستند و پس از ریبوت حذف می‌شوند. برای دائمی کردن باید فایل‌های پیکربندی در /etc را ویرایش کنید.

تمرین: این فایل‌ها را بررسی کنید:

cat /proc/ioports
cat /proc/dma
cat /proc/iomem

### D-Bus

D-Bus سیستم ارتباط بین فرآیندها (IPC) است که:

- ارتباط ساده بین برنامه‌ها فراهم می‌کند
- چرخه حیات فرآیندها را هماهنگ می‌کند
- اجرای برنامه‌ها را در صورت نیاز مدیریت می‌کند

---

## دستورات بررسی سخت‌افزار

### lspci

نمایش دستگاه‌های PCI متصل:

lspci

خروجی نمونه:

00:00.0 Host bridge: Intel Corporation DRAM Controller
00:02.0 VGA compatible controller: Intel Corporation Integrated Graphics
00:19.0 Ethernet controller: Intel Corporation Gigabit Network Connection
00:1a.0 USB controller: Intel Corporation USB Enhanced Host Controller
00:1b.0 Audio device: Intel Corporation High Definition Audio Controller

برای اطلاعات تفصیلی:

lspci -v

### lsusb

نمایش دستگاه‌های USB متصل:

lsusb

خروجی نمونه:

Bus 002 Device 003: ID 1c4f:0026 SiGma Micro Keyboard
Bus 001 Device 005: ID 04f2:b217 Chicony Electronics Co. Camera
Bus 001 Device 004: ID 0a5c:217f Broadcom Corp. Bluetooth

برای جزئیات بیشتر:

lsusb -v

### lsblk

نمایش دستگاه‌های بلوکی (هارد، SSD و...):

lsblk

خروجی نمونه:

sda      8:0    0 500G  0 disk
├─sda1   8:1    0 512M  0 part /boot/efi
├─sda2   8:2    0  50G  0 part /
└─sda3   8:3    0 449G  0 part /home

### lshw

نمایش کامل سخت‌افزار سیستم (نیاز به دسترسی root):

sudo lshw

یا خروجی کوتاه:

sudo lshw -short

---

## مدیریت ماژول‌های کرنل

ماژول‌های کرنل درایورهایی هستند که به صورت پویا قابل بارگذاری و حذف هستند. این روش باعث می‌شود کرنل کوچک‌تر باشد و فقط درایورهای مورد نیاز بارگذاری شوند.

### lsmod

نمایش ماژول‌های بارگذاری شده:

lsmod

خروجی نمونه:

Module                  Size  Used by
bluetooth             446190  22
uvcvideo               81065  0
snd_hda_intel          45273  5

ستون‌ها:
- Module: نام ماژول
- Size: حجم ماژول
- Used by: تعداد استفاده‌کننده و ماژول‌های وابسته

محل ذخیره ماژول‌ها:

ls /lib/modules/$(uname -r)/

### modinfo

نمایش اطلاعات یک ماژول:

modinfo bluetooth

خروجی شامل: نام، نویسنده، توضیحات، وابستگی‌ها

### modprobe

بارگذاری ماژول (به همراه وابستگی‌ها):

sudo modprobe bluetooth

حذف ماژول:

sudo modprobe -r bluetooth

حذف اجباری (خطرناک):

sudo modprobe -rf bluetooth

تفاوت با insmod:
- modprobe وابستگی‌ها را خودکار حل می‌کند
- insmod نیاز به مسیر کامل فایل دارد و وابستگی‌ها را بررسی نمی‌کند

مثال استفاده از insmod (توصیه نمی‌شود):

sudo insmod /lib/modules/$(uname -r)/kernel/drivers/net/wireless/iwlwifi.ko

### بارگذاری خودکار

برای بارگذاری خودکار ماژول در هنگام بوت:

روش اول - افزودن به /etc/modules:

echo "bluetooth" | sudo tee -a /etc/modules

روش دوم - ایجاد فایل در /etc/modprobe.d/:

echo "options bluetooth disable_ertm=1" | sudo tee /etc/modprobe.d/bluetooth.conf

---

## تمرین‌های عملی

تمرین 1 - بررسی CPU:

cat /proc/cpuinfo | grep "model name" | head -1
lscpu

تمرین 2 - لیست دستگاه‌های USB:

lsusb
lsusb -t

تمرین 3 - بررسی هارد دیسک‌ها:

lsblk
sudo fdisk -l

تمرین 4 - مدیریت ماژول بلوتوث:

lsmod | grep bluetooth
sudo modprobe -r bluetooth
lsmod | grep bluetooth
sudo modprobe bluetooth
lsmod | grep bluetooth

تمرین 5 - بررسی شبکه:

lspci | grep -i network
ip link show

---

## خلاصه

در این فصل یاد گرفتیم:

- تفاوت BIOS و UEFI
- انواع رابط‌های سخت‌افزاری (PCI، USB، SATA و...)
- تفاوت SSD و HDD
- نقش و کاربرد /sys، /proc و /dev
- دستورات lspci، lsusb، lsblk، lshw
- مدیریت ماژول‌های کرنل با lsmod و modprobe
- نقش udev در مدیریت دستگاه‌ها

نکات کلیدی برای آزمون:
- تفاوت character و block device
- تفاوت modprobe و insmod
- موقتی بودن تغییرات در /proc
- محل قرارگیری ماژول‌ها در /lib/modules
