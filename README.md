# Hitung WR ML — Kalkulator Win Rate Mobile Legends (Python)

**Hitung WR ML** adalah kalkulator WR ML gratis untuk menjawab pertanyaan klasik setelah kalah beruntun: "Aku harus menang berapa kali lagi supaya WR naik ke 60%?" Masukkan total match, WR sekarang, dan target WR, lalu program menghitung jumlah kemenangan beruntun yang dibutuhkan. Tool ini juga bisa cek WR dari jumlah menang dan kalah, mensimulasikan lose streak, menghitung WR akhir setelah sejumlah match dengan WR tertentu, dan menampilkan tabel kebutuhan win untuk target 50–90%. Semua dihitung dengan pecahan eksak, jadi hasilnya tidak meleset karena galat pembulatan komputer.

> 🛠️ Tool gratis & open source ini adalah karya **[JoinBareng](https://joinbareng.com)** — platform patungan langganan premium di Indonesia.

## Daftar Isi

- [Apa Itu WR di Mobile Legends](#apa-itu-wr-di-mobile-legends)
- [Fitur Kalkulator WR ML](#fitur-kalkulator-wr-ml)
- [Cara Install dan Menjalankan](#cara-install-dan-menjalankan)
- [Cara Pakai dan Contoh Output](#cara-pakai-dan-contoh-output)
- [Cara Menghitung WR ML Manual](#cara-menghitung-wr-ml-manual)
- [Soal Pembulatan WR di Profil](#soal-pembulatan-wr-di-profil)
- [Tabel Referensi Kebutuhan Win](#tabel-referensi-kebutuhan-win)
- [Tips dan Kesalahan Umum](#tips-dan-kesalahan-umum)
- [FAQ Hitung WR ML](#faq-hitung-wr-ml)
- [Metodologi, Pengujian, dan Sumber](#metodologi-pengujian-dan-sumber)
- [Tentang Pembuat](#tentang-pembuat)
- [Disclaimer](#disclaimer)
- [Kontribusi](#kontribusi)
- [Lisensi](#lisensi)
- [Dukung Proyek Ini](#dukung-proyek-ini)
- [Tools Lainnya dari Seri Ini](#tools-lainnya-dari-seri-ini)

## Apa Itu WR di Mobile Legends

Dalam konteks win rate Mobile Legends, WR (*win rate*) adalah persentase kemenangan dari seluruh pertandingan yang sudah kamu mainkan. Rumusnya sederhana: jumlah menang dibagi total match, lalu dikali 100%. Pemain yang menang 120 kali dari 200 match punya WR 60%.

[Mobile Legends: Bang Bang](https://en.wikipedia.org/wiki/Mobile_Legends:_Bang_Bang) adalah game MOBA 5 lawan 5 buatan Moonton yang dirilis di Android pada Juli 2016. Game ini punya beberapa mode, antara lain Classic, Ranked, dan Brawl. Di profil pemain, total match dan win rate ditampilkan di halaman statistik. Banyak pemain memakai angka ini sebagai "rapor", misalnya untuk syarat masuk tim, turnamen komunitas, atau sekadar gengsi.

Yang membuat WR menarik sekaligus menyebalkan adalah sifatnya yang makin "berat". Semakin banyak total match, semakin sulit WR bergerak. Sepuluh kemenangan beruntun bisa menaikkan WR akun baru belasan persen, tetapi hampir tidak terasa di akun ribuan match. Karena itu, cara menghitung WR ML dengan tepat penting supaya targetmu realistis.

## Fitur Kalkulator WR ML

- **Target WR**: menghitung berapa kemenangan beruntun (tanpa kalah) yang dibutuhkan untuk mencapai target WR.
- **Cek WR**: menghitung WR dari jumlah menang dan kalah, atau dari jumlah menang dan total match.
- **Simulasi lose streak**: WR setelah kalah N kali beruntun, dan berapa kali kalah beruntun sampai WR jatuh di bawah batas tertentu (misalnya 50%).
- **Simulasi campuran**: WR akhir setelah M match tambahan dengan WR rata-rata p%, ditambah perkiraan jumlah match untuk mencapai target bila WR main harianmu di atas target.
- **Tabel target** 50, 60, 65, 70, 75, 80, 85, dan 90% dalam satu perintah.
- **Input jumlah menang langsung** (`--menang`) agar hasil pasti, tanpa perlu menebak dari WR yang sudah dibulatkan.
- **Peringatan pembulatan**: bila WR yang kamu masukkan cocok dengan lebih dari satu jumlah menang, program menampilkan rentangnya dan rentang kebutuhan win.
- **Kasus khusus ditangani**: target 100% saat sudah pernah kalah dinyatakan mustahil, target di bawah WR sekarang menghasilkan 0, dan WR 0% tetap bisa dihitung.
- **Mode interaktif** dengan menu Bahasa Indonesia bila dijalankan tanpa argumen.
- **Format angka Indonesia** (`12.843`, `52,40%`), hanya standard library Python 3.8+, dan berjalan offline.

## Cara Install dan Menjalankan

Kamu cukup punya Python 3.8 atau lebih baru (cek dengan `python3 --version`).

```bash
git clone https://github.com/redyopa2929/hitung-wr-ml.git
cd hitung-wr-ml
python3 hitung_wr.py
```

Tanpa argumen, program membuka menu interaktif. Untuk mode perintah, pakai subcommand `target`, `wr`, `kalah`, `campuran`, atau `tabel`. Bantuan lengkap tersedia lewat `python3 hitung_wr.py --help` atau `python3 hitung_wr.py target --help`. Di Windows, ganti `python3` dengan `python` atau `py` bila perlu.

## Cara Pakai dan Contoh Output

Semua output di bawah ini adalah hasil asli program hitung WR ML ini. Opsi `--wr` menerima koma maupun titik desimal (`52,4` atau `52.4`), dan angka ribuan boleh ditulis dengan titik (`1.523`).

### Menghitung kebutuhan win untuk target WR

```text
$ python3 hitung_wr.py target --total 250 --wr 52,4 --target 60
WR 52,40% dari 250 match ≈ 131 menang.
Posisi sekarang : 131 menang, 119 kalah dari 250 match (WR 52,40%)
Target WR       : 60,00%
Hasil: kamu butuh 48 kemenangan beruntun tanpa kalah.
Setelah itu     : 179 menang, 119 kalah dari 298 match (WR 60,07%)
```

Kalau kamu tahu jumlah menang yang persis, pakai `--menang` sebagai pengganti `--wr`:

```text
$ python3 hitung_wr.py target --total 250 --menang 131 --target 60
Posisi sekarang : 131 menang, 119 kalah dari 250 match (WR 52,40%)
Target WR       : 60,00%
Hasil: kamu butuh 48 kemenangan beruntun tanpa kalah.
Setelah itu     : 179 menang, 119 kalah dari 298 match (WR 60,07%)
```

Target 100% setelah pernah kalah memang tidak mungkin, dan program menyatakannya dengan jelas:

```text
$ python3 hitung_wr.py target --total 100 --wr 99 --target 100
WR 99,00% dari 100 match ≈ 99 menang.
Posisi sekarang : 99 menang, 1 kalah dari 100 match (WR 99,00%)
Target WR       : 100,00%
Hasil: MUSTAHIL. WR 100% tidak bisa dicapai lagi karena kamu sudah pernah kalah.
```

### Cek WR dari jumlah menang dan kalah

```text
$ python3 hitung_wr.py wr --menang 120 --kalah 80
120 menang, 80 kalah dari 200 match (WR 60,00%)
$ python3 hitung_wr.py wr --menang 1.523 --total 2.890
1.523 menang, 1.367 kalah dari 2.890 match (WR 52,70%)
```

### Simulasi lose streak

```text
$ python3 hitung_wr.py kalah --total 250 --menang 131 --batas 50
Posisi sekarang : 131 menang, 119 kalah dari 250 match (WR 52,40%)
Kalah 1x beruntun -> WR 52,19%
Kalah 2x beruntun -> WR 51,98%
Kalah 3x beruntun -> WR 51,78%
Kalah 5x beruntun -> WR 51,37%
Kalah 10x beruntun -> WR 50,38%
WR turun di bawah 50,00% setelah kalah 13x beruntun (menjadi 49,81%).
```

Gunakan `--jumlah 7` untuk mensimulasikan satu angka kekalahan tertentu saja.

### Simulasi tambahan match dengan WR tertentu

Skenario yang lebih realistis daripada menang terus: kamu main 50 match lagi dengan WR 60%.

```text
$ python3 hitung_wr.py campuran --total 250 --menang 131 --tambahan 50 --wr-tambahan 60 --target 55
Posisi sekarang : 131 menang, 119 kalah dari 250 match (WR 52,40%)
Tambahan        : 50 match dengan WR 60,00% (≈ 30 menang)
Hasil akhir     : 161 menang, 139 kalah dari 300 match (WR 53,67%)
Perkiraan match dengan WR 60,00% untuk mencapai 55,00%: 130 match.
```

### Tabel kebutuhan win

```text
$ python3 hitung_wr.py tabel --total 250 --wr 52,4
Posisi sekarang : 131 menang, 119 kalah dari 250 match (WR 52,40%)

Target WR | Menang beruntun dibutuhkan
----------+---------------------------
   50,00% | sudah tercapai
   60,00% | 48 win
   65,00% | 90 win
   70,00% | 147 win
   75,00% | 226 win
   80,00% | 345 win
   85,00% | 544 win
   90,00% | 940 win
```

### Mode interaktif

```text
$ python3 hitung_wr.py
Hitung WR ML (mode interaktif). Tekan Ctrl+C untuk keluar.

Pilih menu:
  1. Hitung kebutuhan win untuk target WR
  2. Hitung WR dari jumlah menang & kalah
  3. Simulasi kalah beruntun
  4. Simulasi tambahan match dengan WR tertentu
  5. Tabel kebutuhan win (target 50–90%)
  0. Keluar
Pilihan (0-5): 1
Total match sekarang: 250
WR sekarang (%), atau ketik m untuk isi jumlah menang: 52,4
Target WR (%): 60
WR 52,40% dari 250 match ≈ 131 menang.
Posisi sekarang : 131 menang, 119 kalah dari 250 match (WR 52,40%)
Target WR       : 60,00%
Hasil: kamu butuh 48 kemenangan beruntun tanpa kalah.
Setelah itu     : 179 menang, 119 kalah dari 298 match (WR 60,07%)
```

### Jika input salah

Input yang tidak masuk akal ditolak dengan pesan yang jelas, dan program keluar dengan kode error 1:

```text
$ python3 hitung_wr.py target --total 100 --wr 150 --target 60
Error: WR harus di antara 0 dan 100 persen (diberikan: 150).
$ python3 hitung_wr.py wr --menang 0 --kalah 0
Error: Belum ada match: menang dan kalah sama-sama 0.
```

## Cara Menghitung WR ML Manual

### Rumus dasar win rate

```text
WR (%) = menang / total match × 100
total match = menang + kalah
```

Inilah cara menghitung WR Mobile Legends yang paling dasar, dan rumus ini juga dipakai panduan seperti [artikel Suara.com](https://www.suara.com/tekno/2023/01/14/071125/cara-menghitung-winrate-mobile-legends-dijamin-akurat): menang 40 dari 100 match berarti WR 40%. Rumus yang sama berlaku untuk winrate hero ML. Cukup masukkan total match dan WR (atau jumlah menang) hero yang ingin kamu naikkan.

### Rumus jumlah win beruntun untuk target WR

Misalkan T = total match, W = jumlah menang, t = target dalam desimal (60% = 0,6), dan x = kemenangan beruntun yang dicari. Setelah x kemenangan, WR menjadi (W + x) / (T + x). Kita ingin nilainya minimal t:

```text
(W + x) / (T + x) ≥ t
W + x ≥ t·T + t·x
x·(1 − t) ≥ t·T − W
x ≥ (t·T − W) / (1 − t)
```

Karena jumlah match harus bilangan bulat, hasilnya dibulatkan ke atas: **x = ⌈(t·T − W) / (1 − t)⌉**. Jika yang kamu tahu hanya WR, jumlah menang diperkirakan dulu dengan W = round(T × WR / 100).

Ada tiga kasus khusus. Kalau target ≤ WR sekarang, hasilnya 0. Kalau target 100% dan kamu pernah kalah, penyebut (1 − t) menjadi nol, artinya target itu mustahil. Kalau WR sekarang 0%, rumusnya tetap berlaku dengan W = 0.

### Contoh perhitungan langkah demi langkah

**Contoh 1: 100 match, WR 50%, target 60%.**

1. W = round(100 × 50 / 100) = 50 menang.
2. t·T − W = 0,6 × 100 − 50 = 10.
3. 1 − t = 0,4.
4. x = 10 / 0,4 = 25, sudah bulat, jadi **butuh 25 win beruntun**.
5. Cek: (50 + 25) / (100 + 25) = 75 / 125 = 60%. Tepat.

**Contoh 2: 250 match, WR 52,4%, target 60%.**

1. W = round(250 × 0,524) = round(131) = 131 menang, berarti 119 kalah.
2. t·T − W = 150 − 131 = 19.
3. x = 19 / 0,4 = 47,5, dibulatkan ke atas menjadi **48 win**.
4. Cek: dengan 48 win, 179 / 298 = 60,07% (tercapai). Dengan 47 win, 178 / 297 = 59,93% (belum).

Kedua hasil sama dengan output program di atas.

### Rumus simulasi kalah beruntun

Setelah kalah n kali, WR = W / (T + n). Untuk mencari berapa kali kalah sampai WR **di bawah** batas b (desimal), dipakai n = ⌊W/b − T⌋ + 1. Contoh: 131 menang dari 250 match dengan batas 50% menghasilkan 131/0,5 − 250 = 12, lalu ⌊12⌋ + 1 = **13 kali**. Saat kalah 12 kali, WR = 131/262 = 50% persis, yang belum "di bawah" 50%.

Untuk simulasi campuran, menang tambahan = round(M × p), dan WR akhir = (W + menang tambahan) / (T + M). Perkiraan jumlah match dengan WR rata-rata p untuk mencapai target t adalah ⌈(t·T − W) / (p − t)⌉. Rumus ini hanya berlaku bila p lebih besar dari t.

### Kenapa memakai pecahan eksak

Komputer menyimpan angka desimal seperti 0,8 dalam bentuk biner yang tidak persis. [Dokumentasi Python](https://docs.python.org/3/tutorial/floatingpoint.html) mencontohkan bahwa `0.1 + 0.1 + 0.1 == 0.3` bernilai `False`. Pada kalkulator WR, galat sekecil ini bisa menggeser hasil. Untuk 30 match, 20 menang, dan target 80%, hitungan float biasa menghasilkan 20,000000000000004 lalu dibulatkan ke atas menjadi 21, padahal jawaban yang benar 20 (40/50 = 80% persis). Karena itu, program ini memakai modul [`fractions`](https://docs.python.org/3/library/fractions.html) untuk semua hitungan, dan kasus tersebut masuk ke unit test.

Pembulatan tampilan memakai "setengah ke atas" (0,5 menjadi 1), bukan fungsi `round()` bawaan Python. Menurut [dokumentasinya](https://docs.python.org/3/library/functions.html#round), `round()` membulatkan nilai tengah ke bilangan genap.

## Soal Pembulatan WR di Profil

WR yang tampil di game adalah angka persen yang sudah dibulatkan, bukan pecahan lengkap. Kami tidak menemukan dokumentasi resmi Moonton tentang berapa angka desimal yang dipakai. Karena itu, **tool ini mengasumsikan dua angka desimal** (misalnya 52,37%), dan asumsi ini bisa kamu ubah dengan opsi `--desimal`.

Akibatnya, rekonstruksi jumlah menang dari WR bisa meleset. Dengan dua desimal, galat WR paling besar ±0,005 poin persen, sehingga galat jumlah menang paling besar T × 0,00005. Untuk total match sampai 10.000, galat ini paling banyak setengah, sehingga jumlah menang terbaca persis. Di atas itu, hasilnya bisa meleset ±1 atau lebih. Program akan memberi tahu bila hal ini terjadi:

```text
$ python3 hitung_wr.py target --total 25000 --wr 51,37 --target 52
WR 51,37% dari 25.000 match ≈ 12.843 menang.
  Catatan: karena WR dibulatkan, jumlah menang sebenarnya bisa 12.842–12.843. Pakai --menang untuk hasil pasti.
Posisi sekarang : 12.843 menang, 12.157 kalah dari 25.000 match (WR 51,37%)
Target WR       : 52,00%
Hasil: kamu butuh 328 kemenangan beruntun tanpa kalah.
Setelah itu     : 13.171 menang, 12.157 kalah dari 25.328 match (WR 52,00%)
  Kemungkinan kebutuhan: 328–330 win, tergantung jumlah menang sebenarnya.
```

Galatnya jauh lebih besar kalau WR diketik tanpa desimal. Contohnya, "52%" dari 1.000 match cocok dengan 515 sampai 525 kemenangan. Saran kami: **salin total match dan WR persis dari profil, lengkap dengan desimalnya**, atau langsung hitung jumlah menang dan pakai `--menang`.

Satu catatan lagi: program mencari WR yang benar-benar ≥ target. Jika game membulatkan tampilannya, angka di profil bisa sudah terlihat mencapai target sedikit lebih awal, misalnya 59,996% tampil sebagai 60,00%.

## Tabel Referensi Kebutuhan Win

Kebutuhan **win beruntun** untuk naik dari WR 50% ke target, berdasarkan total match:

| Total match | 60% | 65% | 70% | 75% | 80% | 85% | 90% |
|---|---|---|---|---|---|---|---|
| 100 | 25 | 43 | 67 | 100 | 150 | 234 | 400 |
| 500 | 125 | 215 | 334 | 500 | 750 | 1.167 | 2.000 |
| 1.000 | 250 | 429 | 667 | 1.000 | 1.500 | 2.334 | 4.000 |
| 2.000 | 500 | 858 | 1.334 | 2.000 | 3.000 | 4.667 | 8.000 |
| 5.000 | 1.250 | 2.143 | 3.334 | 5.000 | 7.500 | 11.667 | 20.000 |

Untuk akun 1.000 match dengan WR awal berbeda:

| WR sekarang | 50% | 60% | 65% | 70% | 75% | 80% | 90% |
|---|---|---|---|---|---|---|---|
| 45% | 100 | 375 | 572 | 834 | 1.200 | 1.750 | 4.500 |
| 50% | 0 | 250 | 429 | 667 | 1.000 | 1.500 | 4.000 |
| 55% | 0 | 125 | 286 | 500 | 800 | 1.250 | 3.500 |
| 60% | 0 | 0 | 143 | 334 | 600 | 1.000 | 3.000 |

Polanya terlihat jelas. Kebutuhan win naik sebanding dengan total match, dan melonjak tajam ketika target mendekati 100%. Semua angka di tabel dihasilkan oleh fungsi yang sama dengan perintah `tabel`.

## Tips dan Kesalahan Umum

- **Jangan memasukkan WR yang dibulatkan sendiri.** "Sekitar 52%" bisa berarti selisih belasan kemenangan pada akun ribuan match.
- **Pastikan angka diambil dari tampilan yang sama.** Statistik bisa dipisah per musim atau per mode, jadi total match dan WR harus berasal dari layar yang sama.
- **Win beruntun hanyalah batas bawah.** Dalam praktik, kamu pasti sesekali kalah. Pakai perintah `campuran` untuk perkiraan yang lebih realistis berdasarkan WR harianmu.
- **Target di bawah WR main harian tidak akan tercapai.** Jika WR harianmu 50%, WR total akan bergerak mendekati 50%, bukan 60%.
- **Akun besar butuh kesabaran.** Pada 5.000 match, naik dari 50% ke 60% butuh 1.250 win beruntun. Menaikkan WR hero tertentu yang match-nya lebih sedikit sering kali lebih realistis.

## FAQ Hitung WR ML

**Bagaimana cara menghitung WR ML?**
Bagi jumlah menang dengan total match, lalu kalikan 100%. Contohnya, 120 menang dari 200 match berarti WR 60%. Untuk cek WR ML secara otomatis, jalankan `python3 hitung_wr.py wr --menang 120 --kalah 80`, atau pakai `--total` sebagai pengganti `--kalah`.

**Berapa win yang dibutuhkan dari 100 match WR 50% ke 60%?**
Dibutuhkan 25 kemenangan beruntun. Hasil 75 menang dari 125 match sama dengan 60%.

**Kenapa penghitung WR ML lain memberi hasil berbeda satu angka?**
Penyebab yang paling mungkin adalah pembulatan: hasil dibulatkan ke bawah alih-alih ke atas, hitungan terkena galat float, atau jumlah menang ditebak dari WR tanpa desimal. Program ini membulatkan ke atas dengan pecahan eksak dan menampilkan rentang bila ada ketidakpastian.

**Apakah WR 100% bisa dicapai lagi?**
Tidak, kalau kamu pernah kalah sekali saja. Sebanyak apa pun kemenangan, WR hanya akan mendekati 100% tanpa pernah sampai.

**Berapa kali kalah beruntun sampai WR di bawah 50%?**
Gunakan `kalah --batas 50`. Contohnya, dari 131 menang dan 250 match, WR jatuh di bawah 50% setelah 13 kekalahan beruntun.

**Apakah tool ini bisa dipakai untuk winrate hero ML?**
Bisa. Rumusnya sama. Masukkan total match dan WR hero tersebut, atau jumlah menangnya dengan `--menang`.

**Apakah kalkulator ini butuh login atau mengakses akun Mobile Legends saya?**
Tidak. Program berjalan offline di komputermu, tidak terhubung ke server game, dan tidak meminta ID atau password. Kamu hanya mengetik angka.

## Metodologi, Pengujian, dan Sumber

**Metodologi.** Semua input persen diubah menjadi `Fraction` sehingga 52,4 tersimpan persis sebagai 262/5. Kebutuhan win memakai rumus ceiling di atas. Rekonstruksi menang memakai pembulatan setengah ke atas. Rentang menang dihitung dari batas ±setengah satuan desimal terakhir. Persen untuk tampilan diformat dengan `Decimal` dan `ROUND_HALF_UP` dari modul [`decimal`](https://docs.python.org/3/library/decimal.html).

**Pengujian.** Hitung WR ML dilengkapi 18 unit test (`python3 -m unittest discover -s tests -v`) dan semuanya lulus. Test tersebut mencakup:

- contoh manual 100 match 50% → 60% = 25 win dan 250 match 52,4% → 60% = 48 win;
- target ≤ WR sekarang, target 100% (mustahil maupun sudah tercapai), dan WR 0%;
- kasus yang gagal bila memakai float (30 match, 20 menang, target 80% = 20 win);
- uji properti bahwa hasil selalu minimal, yaitu x win cukup tetapi x − 1 tidak;
- simulasi kalah (50 dari 100 lalu kalah 10x = 45,45%, dan batas 45% tercapai setelah 12 kekalahan);
- simulasi campuran, tabel target, rentang rekonstruksi menang, pembulatan, format angka, dan CLI untuk input salah.

Semua tabel di README dihasilkan oleh program, lalu beberapa barisnya dicek ulang dengan hitungan tangan.

**Sumber rujukan:**

- [Mobile Legends: Bang Bang — Wikipedia](https://en.wikipedia.org/wiki/Mobile_Legends:_Bang_Bang) dan [Moonton — Wikipedia](https://en.wikipedia.org/wiki/Moonton) untuk pengembang, tahun rilis, dan mode permainan.
- [Situs resmi Mobile Legends: Bang Bang](https://www.mobilelegends.com/).
- [Cara Menghitung Winrate Mobile Legends — Suara.com](https://www.suara.com/tekno/2023/01/14/071125/cara-menghitung-winrate-mobile-legends-dijamin-akurat) untuk rumus dasar WR.
- Dokumentasi Python: [Floating-Point Arithmetic: Issues and Limitations](https://docs.python.org/3/tutorial/floatingpoint.html), [fractions](https://docs.python.org/3/library/fractions.html), [decimal](https://docs.python.org/3/library/decimal.html), dan [round()](https://docs.python.org/3/library/functions.html#round).

## Tentang Pembuat

Proyek ini adalah karya [JoinBareng](https://joinbareng.com), platform patungan langganan premium (Netflix, Spotify, YouTube Premium, ChatGPT, dll.) plus marketplace akun digital yang aman dan transparan. Repositori ini dikelola oleh [@redyopa2929](https://github.com/redyopa2929) sebagai bagian dari seri tools Python sederhana berbahasa Indonesia.

Menemukan bug atau hasil hitung WR yang janggal? Laporkan lewat [halaman Issues](https://github.com/redyopa2929/hitung-wr-ml/issues) beserta perintah dan output yang muncul.

## Disclaimer

Mobile Legends: Bang Bang adalah merek dagang Moonton. Tool ini adalah proyek independen yang **tidak berafiliasi, tidak disponsori, dan tidak didukung** oleh Moonton. Program tidak terhubung ke server game dan tidak membaca data akun. Hasil hitungan adalah matematika murni berdasarkan angka yang kamu masukkan, dengan asumsi pembulatan yang dijelaskan di atas. Tool ini tidak menjamin kenaikan rank, tidak menebak sistem matchmaking, dan disediakan "apa adanya".

## Kontribusi

Kontribusi sangat diterima, misalnya perbaikan bug atau tambahan test. Fork repositori, buat branch baru, pastikan semua test tetap lulus, lalu kirim pull request. Untuk diskusi, buka [Issues](https://github.com/redyopa2929/hitung-wr-ml/issues).

## Lisensi

Dirilis di bawah [Lisensi MIT](LICENSE). Kamu bebas memakai, mengubah, dan membagikan kode ini selama mencantumkan pemberitahuan hak cipta.

## Dukung Proyek Ini

Kalau alat hitung WR ini membantumu menyusun target push rank, beri ⭐ **star** pada repositori ini supaya pemain lain juga menemukannya. Di sela push rank, hemat biaya langganan aplikasi premium seperti Spotify atau YouTube Premium dengan patungan di [JoinBareng](https://joinbareng.com).

## Tools Lainnya dari Seri Ini

- [Kalkulator Jadian](https://github.com/redyopa2929/kalkulator-jadian) — hitung lama hari jadian & anniversary
- [Kalkulator Jasmani Polri](https://github.com/redyopa2929/kalkulator-jasmani-polri) — hitung nilai kesamaptaan jasmani
- [Tasbih Online](https://github.com/redyopa2929/tasbih-online) — tasbih digital penghitung dzikir
- [Kalkulator Selamatan](https://github.com/redyopa2929/kalkulator-selamatan) — hitung selamatan orang meninggal adat Jawa
- [Terbilang Online](https://github.com/redyopa2929/terbilang-online) — ubah angka ke huruf / terbilang rupiah
- [Kalkulator Saham](https://github.com/redyopa2929/kalkulator-saham) — average down, compounding, ARA/ARB
- [Kalkulator Bangunan](https://github.com/redyopa2929/kalkulator-bangunan) — keramik, hebel, kubikasi, besi
- [Konversi Koordinat](https://github.com/redyopa2929/konversi-koordinat) — DMS, desimal, UTM
- [Cek Weton](https://github.com/redyopa2929/cek-weton) — cek weton & neptu dari tanggal lahir

---

Terakhir diperbarui: 21 Oktober 2026
