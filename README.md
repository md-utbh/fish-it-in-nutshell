# 🎣 Fish It Simulator - Python Backend Prototype

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Status](https://img.shields.io/badge/Status-Prototype-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

**Fish It Simulator** adalah prototipe backend logic untuk game memancing berbasis RNG (Random Number Generation), terinspirasi oleh mekanisme game populer di Roblox (*Fish It* / *Fisch*).

Proyek ini dibuat untuk mensimulasikan dan memecahkan masalah umum dalam desain game ekonomi, seperti inflasi "Luck", eksploitasi kecepatan (speed hack), dan keseimbangan probabilitas item langka.

---

## 🌟 Fitur Utama

### 1. 🧮 Logarithmic Luck Scaling
Berbeda dengan sistem RNG linear yang sering "rusak" saat angka Luck menjadi terlalu tinggi, simulator ini menggunakan skala logaritmik.
*   **Masalah:** Pada sistem linear, Luck 10.000% akan membuat item langka menjadi item sampah (terlalu mudah didapat).
*   **Solusi:** Menggunakan rumus $Multiplier = 1.0 + \log_{10}(1 + TotalLuck) \times Factor$.
*   **Hasil:** Game tetap menantang bagi pemain level tinggi, namun tetap memberikan *reward* yang terasa adil.

### 2. ⚖️ Weighted Pool System
Menggunakan sistem **Dynamic Weighted Probability**.
*   Probabilitas item *Common* tidak dikurangi secara manual.
*   Sebaliknya, bobot (weight) item langka dikalikan dengan *Luck Multiplier*.
*   Secara otomatis, persentase relatif item *Common* akan mengecil seiring meningkatnya Luck pemain, tanpa pernah mencapai angka 0 (selalu ada kemungkinan gagal).

### 3. 🛡️ Anti-Cheat AFK Logic
Mencegah eksploitasi "Speed Hack" pada mode Auto-Farm (AFK).
*   Validasi waktu tunggu (`cast_time`) dilakukan di sisi backend (server-side logic) menggunakan `time.sleep()` yang terikat pada stats Rod.
*   Memastikan 1 menit AFK benar-benar berjalan selama 60 detik waktu nyata, bukan dipercepat oleh manipulasi klien.

### 4. 🎣 Physics-Based Catching
Mekanisme penangkapan ikan yang realistis:
*   **Mutasi Fisik:** Mutasi (seperti *Huge* atau *Titanic*) meningkatkan berat ikan secara drastis.
*   **Line Snap Probability:** Berat ikan dikomparasi dengan kekuatan tali (Rod Line Strength).
    *   Rumus: `Chance = max(0, (FishWeight - LineStrength) * 3)`
    *   Artinya: Jika ikan lebih berat 10kg dari batas, ada peluang 30% tali putus.

---

## 🛠️ Instalasi & Cara Menjalankan

### Cara 1: Menjalankan via Terminal (CLI)
Pastikan Anda sudah menginstal Python di komputer Anda.

1.  **Clone Repository:**
    ```bash
    git clone https://github.com/username-anda/fish-it-simulator.git
    cd fish-it-simulator
    ```

2.  **Jalankan Program:**
    ```bash
    python main.py
    ```

### Cara 2: Menjalankan via Web (Streamlit)
Jika Anda ingin tampilan visual interaktif tanpa coding.

1.  **Install Library:**
    ```bash
    pip install streamlit
    ```

2.  **Jalankan Aplikasi:**
    ```bash
    streamlit run app.py
    ```

---

## 🧬 Struktur Kode

Logika program terbagi menjadi beberapa modul fungsi untuk memudahkan pengembangan:

*   `scaled_luck(rod, bait)`: Menghitung multiplier keberuntungan dengan aman.
*   `roll_rarity(multiplier)`: Algoritma inti penentuan kelangkaan ikan.
*   `check_line_snap(weight, limit)`: Logika fisika penentu keberhasilan menarik ikan.
*   `afk_true(seconds)`: Loop simulasi otomatis yang aman dari manipulasi waktu.

---

## 📊 Contoh Output Statistik

Berikut adalah contoh hasil simulasi AFK selama 1 menit menggunakan **Element Rod** (+1111 Luck) & **Singularity Bait**:

```text
=== HASIL AFK 1 MENIT ===
Total Casts: 28
-------------------------
Common:    3  (10.7%)
Uncommon:  20 (71.4%)
Rare:      4  (14.2%)
Epic:      1  (3.5%)
-------------------------
Catatan: Luck tinggi berhasil menekan drastis jumlah ikan Common.
