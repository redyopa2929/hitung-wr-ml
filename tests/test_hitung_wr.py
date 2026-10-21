"""Unit test Hitung WR ML. Jalankan: python3 -m unittest discover -s tests -v"""
import io
import os
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from fractions import Fraction

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import hitung_wr as hw  # noqa: E402


class TestTargetWR(unittest.TestCase):
    def test_contoh_manual_100_match_50_ke_60(self):
        # (50 + x) / (100 + x) = 0,6  ->  x = (60 - 50) / 0,4 = 25
        self.assertEqual(hw.butuh_menang_dari_wr(100, 50, 60), 25)
        self.assertEqual(hw.butuh_menang(100, 50, 60), 25)

    def test_contoh_readme_250_match(self):
        # W = round(250 x 0,524) = 131 ; x = ceil((150 - 131) / 0,4) = ceil(47,5) = 48
        self.assertEqual(hw.rekonstruksi_menang(250, "52,4"), 131)
        self.assertEqual(hw.butuh_menang_dari_wr(250, "52,4", 60), 48)
        self.assertGreaterEqual(Fraction(131 + 48, 250 + 48), Fraction(60, 100))
        self.assertLess(Fraction(131 + 47, 250 + 47), Fraction(60, 100))

    def test_target_tidak_lebih_dari_wr_sekarang(self):
        self.assertEqual(hw.butuh_menang_dari_wr(100, 50, 50), 0)
        self.assertEqual(hw.butuh_menang_dari_wr(100, 50, 40), 0)
        self.assertEqual(hw.butuh_menang(10, 7, 70), 0)

    def test_target_100_persen(self):
        self.assertIsNone(hw.butuh_menang_dari_wr(100, 99, 100))  # pernah kalah -> mustahil
        self.assertEqual(hw.butuh_menang_dari_wr(20, 100, 100), 0)  # belum pernah kalah
        teks = hw.laporan_target(100, 99, 100)
        self.assertIn("MUSTAHIL", teks)

    def test_wr_nol_persen(self):
        self.assertEqual(hw.butuh_menang_dari_wr(10, 0, 50), 10)
        self.assertEqual(hw.hitung_wr(0, 25), 0)
        self.assertEqual(hw.butuh_menang(10, 0, 90), 90)

    def test_bebas_galat_floating_point(self):
        # Versi float: (0.8*30 - 20) / (1 - 0.8) = 20.000000000000004 -> ceil = 21 (salah).
        self.assertEqual(hw.butuh_menang(30, 20, 80), 20)
        self.assertEqual(hw.butuh_menang(30, 20, 0.8 * 100), 20)
        self.assertEqual(hw.butuh_menang(10, 6, 70), 4)

    def test_hasil_minimal_dan_cukup(self):
        for total, menang, target in [(57, 23, 65), (1234, 600, 55), (9, 4, 85), (500, 251, 75)]:
            x = hw.butuh_menang(total, menang, target)
            t = Fraction(target, 100)
            self.assertGreaterEqual(Fraction(menang + x, total + x), t)
            self.assertLess(Fraction(menang + x - 1, total + x - 1), t)


class TestHitungWR(unittest.TestCase):
    def test_wr_dari_menang_kalah(self):
        self.assertEqual(hw.hitung_wr(120, 80), 60)
        self.assertEqual(hw.format_persen(hw.hitung_wr(2, 1)), "66,67%")
        self.assertEqual(hw.format_persen(hw.hitung_wr(1, 2)), "33,33%")

    def test_input_tidak_valid(self):
        with self.assertRaises(ValueError):
            hw.hitung_wr(0, 0)
        with self.assertRaises(ValueError):
            hw.hitung_wr(-1, 5)
        for wr in ("abc", "101", "-5", ""):
            with self.assertRaises(ValueError, msg=wr):
                hw.persen_valid(wr)
        with self.assertRaises(ValueError):
            hw.butuh_menang(0, 0, 50)
        with self.assertRaises(ValueError):
            hw.butuh_menang(10, 11, 50)


class TestSimulasi(unittest.TestCase):
    def test_simulasi_kalah_beruntun(self):
        self.assertEqual(hw.wr_setelah_kalah(100, 50, 10), Fraction(500, 11))
        self.assertEqual(hw.format_persen(hw.wr_setelah_kalah(100, 50, 10)), "45,45%")

    def test_kalah_sampai_di_bawah_batas(self):
        self.assertEqual(hw.kalah_sampai_di_bawah(100, 50, 45), 12)   # 50/112 = 44,64%
        self.assertEqual(hw.kalah_sampai_di_bawah(90, 45, 45), 11)    # 45/100 = 45% belum di bawah
        self.assertEqual(hw.kalah_sampai_di_bawah(100, 40, 50), 0)    # sudah di bawah
        self.assertIsNone(hw.kalah_sampai_di_bawah(100, 40, 0))       # tidak mungkin < 0%

    def test_simulasi_campuran(self):
        self.assertEqual(hw.simulasi_campuran(100, 50, 100, 60), (110, 200, 55))
        self.assertEqual(hw.match_untuk_target(100, 50, 55, 60), 100)
        self.assertIsNone(hw.match_untuk_target(100, 50, 55, 55))

    def test_tabel_target(self):
        tabel = hw.tabel_target(100, 50)
        self.assertEqual([int(t) for t, _ in tabel], [50, 60, 65, 70, 75, 80, 85, 90])
        self.assertEqual([x for _, x in tabel], [0, 25, 43, 67, 100, 150, 234, 400])


class TestPembulatan(unittest.TestCase):
    def test_rekonstruksi_dan_rentang(self):
        self.assertEqual(hw.rekonstruksi_menang(3, "66,67"), 2)
        self.assertEqual(hw.rentang_menang(3, "66,67"), (2, 2))
        self.assertEqual(hw.rentang_menang(10000, "52,37"), (5237, 5237))
        self.assertEqual(hw.rentang_menang(20000, "50,00"), (9999, 10001))
        self.assertEqual(hw.rentang_menang(1000, "52", desimal=0), (515, 525))

    def test_pembulatan_setengah_ke_atas(self):
        self.assertEqual(hw.bulat(Fraction(5, 2)), 3)  # round() Python memberi 2
        self.assertEqual(hw.format_persen(Fraction(1, 8) * 100), "12,50%")
        self.assertEqual(hw.format_persen("52.345"), "52,35%")

    def test_format_indonesia(self):
        self.assertEqual(hw.format_angka(12345), "12.345")
        self.assertEqual(hw.parse_bulat("1.234", "x"), 1234)
        self.assertEqual(hw.pecahan("52,37"), Fraction(5237, 100))


class TestCLI(unittest.TestCase):
    def jalankan(self, argv):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            kode = hw.main(argv)
        return kode, out.getvalue(), err.getvalue()

    def test_cli_target(self):
        kode, out, _ = self.jalankan(["target", "--total", "100", "--wr", "50", "--target", "60"])
        self.assertEqual(kode, 0)
        self.assertIn("25 kemenangan beruntun", out)

    def test_cli_input_salah(self):
        kode, _, err = self.jalankan(["target", "--total", "100", "--wr", "150", "--target", "60"])
        self.assertNotEqual(kode, 0)
        self.assertIn("Error", err)


if __name__ == "__main__":
    unittest.main()
