#!/usr/bin/env python3
"""Hitung WR ML: kalkulator win rate Mobile Legends (target WR, WR dari menang/kalah, simulasi).

Hanya memakai standard library (Python 3.8+). Semua hitungan memakai pecahan eksak
(fractions.Fraction) agar bebas galat floating point. Jalankan tanpa argumen untuk mode interaktif.
Karya JoinBareng (https://joinbareng.com), dikelola oleh @redyopa2929. Lisensi MIT.
Tidak berafiliasi dengan Moonton. Mobile Legends: Bang Bang adalah merek dagang Moonton.
"""
from __future__ import annotations

import argparse
import math
import sys
from decimal import ROUND_HALF_UP, Decimal
from fractions import Fraction
from typing import List, Optional, Sequence, Tuple, Union

Angka = Union[int, float, str, Decimal, Fraction]
TARGET_TABEL = (50, 60, 65, 70, 75, 80, 85, 90)
DESIMAL_WR_GAME = 2  # asumsi: WR di profil dibulatkan ke 2 angka desimal (bisa diubah: --desimal)


# ---------------------------------------------------------------- fungsi inti

def pecahan(x: Angka) -> Fraction:
    """Ubah angka/teks ('52,37', '52.37', 0.6) menjadi Fraction eksak."""
    if isinstance(x, Fraction):
        return x
    if isinstance(x, float):
        x = repr(x)
    teks = str(x).strip().replace("%", "").replace(",", ".")
    try:
        return Fraction(teks)
    except (ValueError, ZeroDivisionError):
        raise ValueError(f"'{x}' bukan angka yang valid.") from None


def persen_valid(x: Angka, nama: str = "WR") -> Fraction:
    p = pecahan(x)
    if not 0 <= p <= 100:
        raise ValueError(f"{nama} harus di antara 0 dan 100 persen (diberikan: {x}).")
    return p


def bulat(x: Fraction) -> int:
    """Pembulatan setengah ke atas (0,5 -> 1), bukan banker's rounding."""
    return math.floor(x + Fraction(1, 2))


def _cek_total(total: int) -> None:
    if not isinstance(total, int) or total <= 0:
        raise ValueError("Total match harus bilangan bulat lebih dari 0.")


def _cek_menang(total: int, menang: int) -> None:
    _cek_total(total)
    if not 0 <= menang <= total:
        raise ValueError(f"Jumlah menang harus di antara 0 dan total match ({total}).")


def rekonstruksi_menang(total: int, wr: Angka) -> int:
    """Perkiraan jumlah menang dari total match & WR%: W = round(T x WR / 100)."""
    _cek_total(total)
    return bulat(total * persen_valid(wr) / 100)


def rentang_menang(total: int, wr: Angka, desimal: int = DESIMAL_WR_GAME) -> Tuple[int, int]:
    """Semua jumlah menang yang, bila dibulatkan ke `desimal` angka, menghasilkan WR tersebut."""
    _cek_total(total)
    if desimal < 0:
        raise ValueError("Jumlah desimal tidak boleh negatif.")
    p, setengah = persen_valid(wr), Fraction(1, 2 * 10 ** desimal)
    bawah = math.ceil(total * (p - setengah) / 100)
    atas = math.floor(total * (p + setengah) / 100)
    return max(0, bawah), min(total, atas)


def hitung_wr(menang: int, kalah: int) -> Fraction:
    """WR (%) = menang / (menang + kalah) x 100."""
    if menang < 0 or kalah < 0:
        raise ValueError("Jumlah menang dan kalah tidak boleh negatif.")
    if menang + kalah == 0:
        raise ValueError("Belum ada match: menang dan kalah sama-sama 0.")
    return Fraction(100 * menang, menang + kalah)


def butuh_menang(total: int, menang: int, target: Angka) -> Optional[int]:
    """Menang beruntun minimal agar WR >= target. None = mustahil (target 100% padahal pernah kalah)."""
    _cek_menang(total, menang)
    t = persen_valid(target, "Target WR") / 100
    if Fraction(menang, total) >= t:
        return 0
    if t == 1:
        return None
    return max(0, math.ceil((t * total - menang) / (1 - t)))


def butuh_menang_dari_wr(total: int, wr: Angka, target: Angka) -> Optional[int]:
    """Versi dari WR%: x = ceil((target x T - W) / (1 - target)), dengan W = round(T x WR / 100)."""
    if persen_valid(target, "Target WR") <= persen_valid(wr):
        return 0
    return butuh_menang(total, rekonstruksi_menang(total, wr), target)


def wr_setelah_kalah(total: int, menang: int, n_kalah: int) -> Fraction:
    _cek_menang(total, menang)
    if n_kalah < 0:
        raise ValueError("Jumlah kalah tidak boleh negatif.")
    return Fraction(100 * menang, total + n_kalah)


def kalah_sampai_di_bawah(total: int, menang: int, batas: Angka) -> Optional[int]:
    """Kalah beruntun minimal sampai WR < batas. None = tidak mungkin (batas 0%)."""
    _cek_menang(total, menang)
    b = persen_valid(batas, "Batas WR") / 100
    if Fraction(menang, total) < b:
        return 0
    if b == 0:
        return None
    return math.floor(menang / b - total) + 1


def simulasi_campuran(total: int, menang: int, tambahan: int,
                      wr_tambahan: Angka) -> Tuple[int, int, Fraction]:
    """Tambah `tambahan` match dengan WR p%. Menang tambahan = round(tambahan x p / 100)."""
    _cek_menang(total, menang)
    if tambahan < 0:
        raise ValueError("Jumlah match tambahan tidak boleh negatif.")
    menang_baru = menang + bulat(tambahan * persen_valid(wr_tambahan, "WR tambahan") / 100)
    total_baru = total + tambahan
    return menang_baru, total_baru, Fraction(100 * menang_baru, total_baru)


def match_untuk_target(total: int, menang: int, target: Angka, wr_main: Angka) -> Optional[int]:
    """Perkiraan jumlah match (dengan WR rata-rata wr_main) agar WR mencapai target.
    None bila wr_main <= target sehingga target tidak akan pernah tercapai."""
    _cek_menang(total, menang)
    t = persen_valid(target, "Target WR") / 100
    p = persen_valid(wr_main, "WR rata-rata") / 100
    if Fraction(menang, total) >= t:
        return 0
    if p <= t:
        return None
    return math.ceil((t * total - menang) / (p - t))


def tabel_target(total: int, menang: int,
                 targets: Sequence[Angka] = TARGET_TABEL) -> List[Tuple[Fraction, Optional[int]]]:
    return [(pecahan(t), butuh_menang(total, menang, t)) for t in targets]


# ------------------------------------------------------------- format output

def format_angka(n: int) -> str:
    return f"{n:,}".replace(",", ".")


def format_persen(x: Angka, desimal: int = 2) -> str:
    fr = pecahan(x)
    d = (Decimal(fr.numerator) / Decimal(fr.denominator)).quantize(
        Decimal(1).scaleb(-desimal), rounding=ROUND_HALF_UP)
    return f"{d:,.{desimal}f}".replace(",", "_").replace(".", ",").replace("_", ".") + "%"


def ringkas(total: int, menang: int) -> str:
    return (f"{format_angka(menang)} menang, {format_angka(total - menang)} kalah dari "
            f"{format_angka(total)} match (WR {format_persen(Fraction(100 * menang, total))})")


def laporan_target(total: int, menang: int, target: Angka, dari_wr: Optional[Angka] = None,
                   desimal: int = DESIMAL_WR_GAME) -> str:
    baris = []
    if dari_wr is not None:
        lo, hi = rentang_menang(total, dari_wr, desimal)
        baris.append(f"WR {format_persen(dari_wr)} dari {format_angka(total)} match ≈ "
                     f"{format_angka(menang)} menang.")
        if lo > hi:
            baris.append(f"  Peringatan: tidak ada jumlah menang yang menghasilkan WR persis "
                         f"{format_persen(dari_wr)} dari {format_angka(total)} match. Cek lagi angkanya.")
        elif lo != hi:
            baris.append(f"  Catatan: karena WR dibulatkan, jumlah menang sebenarnya bisa "
                         f"{format_angka(lo)}–{format_angka(hi)}. Pakai --menang untuk hasil pasti.")
    baris.append(f"Posisi sekarang : {ringkas(total, menang)}")
    baris.append(f"Target WR       : {format_persen(target)}")
    x = butuh_menang_dari_wr(total, dari_wr, target) if dari_wr is not None \
        else butuh_menang(total, menang, target)
    if x is None:
        baris.append("Hasil: MUSTAHIL. WR 100% tidak bisa dicapai lagi karena kamu sudah pernah kalah.")
    elif x == 0:
        baris.append("Hasil: target sudah tercapai, tidak perlu tambahan kemenangan.")
    else:
        baris.append(f"Hasil: kamu butuh {format_angka(x)} kemenangan beruntun tanpa kalah.")
        baris.append(f"Setelah itu     : {ringkas(total + x, menang + x)}")
        if dari_wr is not None:
            lo, hi = rentang_menang(total, dari_wr, desimal)
            if lo < hi:
                xs = [butuh_menang(total, w, target) for w in (hi, lo)]
                if None not in xs and xs[0] != xs[1]:
                    baris.append(f"  Kemungkinan kebutuhan: {format_angka(xs[0])}–{format_angka(xs[1])} win, "
                                 "tergantung jumlah menang sebenarnya.")
    return "\n".join(baris)


def laporan_kalah(total: int, menang: int, n_kalah: Optional[int], batas: Optional[Angka]) -> str:
    baris = [f"Posisi sekarang : {ringkas(total, menang)}"]
    langkah = [n_kalah] if n_kalah is not None else [1, 2, 3, 5, 10]
    for n in langkah:
        baris.append(f"Kalah {format_angka(n)}x beruntun -> WR {format_persen(wr_setelah_kalah(total, menang, n))}")
    if batas is not None:
        n = kalah_sampai_di_bawah(total, menang, batas)
        if n is None:
            baris.append("WR tidak mungkin turun di bawah 0%.")
        elif n == 0:
            baris.append(f"WR sekarang sudah di bawah {format_persen(batas)}.")
        else:
            baris.append(f"WR turun di bawah {format_persen(batas)} setelah kalah {format_angka(n)}x "
                         f"beruntun (menjadi {format_persen(wr_setelah_kalah(total, menang, n))}).")
    return "\n".join(baris)


def laporan_campuran(total: int, menang: int, tambahan: int, wr_tambahan: Angka,
                     target: Optional[Angka] = None) -> str:
    m2, t2, _ = simulasi_campuran(total, menang, tambahan, wr_tambahan)
    baris = [f"Posisi sekarang : {ringkas(total, menang)}",
             f"Tambahan        : {format_angka(tambahan)} match dengan WR {format_persen(wr_tambahan)} "
             f"(≈ {format_angka(m2 - menang)} menang)",
             f"Hasil akhir     : {ringkas(t2, m2)}"]
    if target is not None:
        n = match_untuk_target(total, menang, target, wr_tambahan)
        if n is None:
            baris.append(f"Dengan WR {format_persen(wr_tambahan)}, target {format_persen(target)} "
                         "tidak akan pernah tercapai (WR main harus di atas target).")
        elif n == 0:
            baris.append(f"Target {format_persen(target)} sudah tercapai saat ini.")
        else:
            baris.append(f"Perkiraan match dengan WR {format_persen(wr_tambahan)} untuk mencapai "
                         f"{format_persen(target)}: {format_angka(n)} match.")
    return "\n".join(baris)


def laporan_tabel(total: int, menang: int) -> str:
    baris = [f"Posisi sekarang : {ringkas(total, menang)}", "",
             "Target WR | Menang beruntun dibutuhkan", "----------+---------------------------"]
    for t, x in tabel_target(total, menang):
        isi = "mustahil" if x is None else ("sudah tercapai" if x == 0 else f"{format_angka(x)} win")
        baris.append(f"{format_persen(t):>9} | {isi}")
    return "\n".join(baris)


# --------------------------------------------------------------------- CLI

def parse_bulat(teks: Union[str, int], nama: str) -> int:
    """Terima '1.234' atau '1234' sebagai bilangan bulat."""
    t = str(teks).strip().replace(".", "")
    if not t.isdigit():
        raise ValueError(f"{nama} harus bilangan bulat positif (diberikan: {teks}).")
    return int(t)


def buat_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="hitung_wr.py",
                                description="Hitung WR ML: kalkulator win rate Mobile Legends.",
                                epilog="Tanpa argumen, program berjalan dalam mode interaktif.")
    sub = p.add_subparsers(dest="perintah")
    posisi = argparse.ArgumentParser(add_help=False)
    posisi.add_argument("-t", "--total", required=True, help="total match sekarang")
    grup = posisi.add_mutually_exclusive_group(required=True)
    grup.add_argument("-w", "--wr", help="WR sekarang dalam persen, mis. 52,37")
    grup.add_argument("-m", "--menang", help="jumlah menang sekarang (lebih akurat dari --wr)")

    s = sub.add_parser("target", parents=[posisi], help="hitung win beruntun untuk mencapai target WR")
    s.add_argument("-g", "--target", required=True, help="target WR dalam persen")
    s.add_argument("--desimal", type=int, default=DESIMAL_WR_GAME,
                   help="jumlah angka desimal WR di game (default 2)")
    s = sub.add_parser("wr", help="hitung WR dari jumlah menang & kalah")
    s.add_argument("-m", "--menang", required=True)
    g = s.add_mutually_exclusive_group(required=True)
    g.add_argument("-k", "--kalah")
    g.add_argument("-t", "--total")
    s = sub.add_parser("kalah", parents=[posisi], help="simulasi kalah beruntun")
    s.add_argument("-n", "--jumlah", help="jumlah kalah beruntun yang disimulasikan")
    s.add_argument("-b", "--batas", help="cari berapa kali kalah sampai WR di bawah batas ini")
    s = sub.add_parser("campuran", parents=[posisi], help="simulasi tambahan match dengan WR tertentu")
    s.add_argument("-a", "--tambahan", required=True, help="jumlah match tambahan")
    s.add_argument("-p", "--wr-tambahan", required=True, help="WR pada match tambahan (persen)")
    s.add_argument("-g", "--target", help="opsional: perkiraan match untuk mencapai target WR")
    sub.add_parser("tabel", parents=[posisi], help="tabel kebutuhan win untuk target 50–90%%")
    return p


def _posisi(args: argparse.Namespace) -> Tuple[int, int]:
    total = parse_bulat(args.total, "Total match")
    if args.menang is not None:
        menang = parse_bulat(args.menang, "Jumlah menang")
        _cek_menang(total, menang)
        return total, menang
    return total, rekonstruksi_menang(total, args.wr)


def jalankan(args: argparse.Namespace) -> str:
    if args.perintah == "wr":
        menang = parse_bulat(args.menang, "Jumlah menang")
        kalah = (parse_bulat(args.kalah, "Jumlah kalah") if args.kalah is not None
                 else parse_bulat(args.total, "Total match") - menang)
        if kalah < 0:
            raise ValueError("Jumlah menang tidak boleh melebihi total match.")
        hitung_wr(menang, kalah)  # validasi: tidak boleh 0 match
        return ringkas(menang + kalah, menang)
    total, menang = _posisi(args)
    if args.perintah == "target":
        return laporan_target(total, menang, args.target, args.wr if args.menang is None else None,
                              args.desimal)
    if args.perintah == "kalah":
        n = parse_bulat(args.jumlah, "Jumlah kalah") if args.jumlah is not None else None
        return laporan_kalah(total, menang, n, args.batas)
    if args.perintah == "campuran":
        return laporan_campuran(total, menang, parse_bulat(args.tambahan, "Match tambahan"),
                                args.wr_tambahan, args.target)
    return laporan_tabel(total, menang)


MENU = """Pilih menu:
  1. Hitung kebutuhan win untuk target WR
  2. Hitung WR dari jumlah menang & kalah
  3. Simulasi kalah beruntun
  4. Simulasi tambahan match dengan WR tertentu
  5. Tabel kebutuhan win (target 50–90%)
  0. Keluar"""


def _tanya_posisi() -> Tuple[int, int, Optional[str]]:
    total = parse_bulat(input("Total match sekarang: "), "Total match")
    teks = input("WR sekarang (%), atau ketik m untuk isi jumlah menang: ").strip()
    if teks.lower() == "m":
        menang = parse_bulat(input("Jumlah menang: "), "Jumlah menang")
        _cek_menang(total, menang)
        return total, menang, None
    return total, rekonstruksi_menang(total, teks), teks


def mode_interaktif() -> int:
    print("Hitung WR ML (mode interaktif). Tekan Ctrl+C untuk keluar.")
    while True:
        print("\n" + MENU)
        pilih = input("Pilihan (0-5): ").strip()
        if pilih == "0":
            print("Terima kasih sudah memakai Hitung WR ML. Semoga winstreak!")
            return 0
        try:
            if pilih == "2":
                menang = parse_bulat(input("Jumlah menang: "), "Jumlah menang")
                kalah = parse_bulat(input("Jumlah kalah: "), "Jumlah kalah")
                hitung_wr(menang, kalah)
                print(ringkas(menang + kalah, menang))
                continue
            if pilih not in ("1", "3", "4", "5"):
                print("Pilihan tidak dikenal. Ketik angka 0 sampai 5.")
                continue
            total, menang, wr = _tanya_posisi()
            if pilih == "1":
                print(laporan_target(total, menang, input("Target WR (%): "), wr))
            elif pilih == "3":
                n = parse_bulat(input("Berapa kali kalah beruntun? (mis. 5): "), "Jumlah kalah")
                batas = input("Batas WR (%) yang ingin dicek (Enter = lewati): ").strip() or None
                print(laporan_kalah(total, menang, n, batas))
            elif pilih == "4":
                tambahan = parse_bulat(input("Jumlah match tambahan: "), "Match tambahan")
                p = input("WR pada match tambahan (%): ")
                target = input("Target WR (%) (Enter = lewati): ").strip() or None
                print(laporan_campuran(total, menang, tambahan, p, target))
            else:
                print(laporan_tabel(total, menang))
        except ValueError as e:
            print(f"Maaf, {e}")


def main(argv: Optional[Sequence[str]] = None) -> int:
    argv = sys.argv[1:] if argv is None else list(argv)
    try:
        if not argv:
            return mode_interaktif()
        parser = buat_parser()
        args = parser.parse_args(argv)
        if not args.perintah:
            parser.print_help()
            return 2
        print(jalankan(args))
        return 0
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except (KeyboardInterrupt, EOFError):
        print("\nDibatalkan. Sampai jumpa!")
        return 130


if __name__ == "__main__":
    sys.exit(main())
