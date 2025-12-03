# 🎣 Fish It Simulator (RNG & Physics Prototype)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red)
![Status](https://img.shields.io/badge/Status-Prototype-green)

Sebuah simulasi backend logic untuk game memancing bergaya Roblox (seperti *Fish It* atau *Fisch*). Projek ini dibuat untuk mendemonstrasikan bagaimana **Sistem RNG yang seimbang**, **Skala Keberuntungan (Luck Scaling)**, dan **Fisika Tali Pancing** bekerja dalam pengembangan game.

## 🚀 Live Demo
Anda dapat mencoba simulasi ini langsung melalui browser tanpa perlu menginstall apapun:

👉 **[Klik di sini untuk menjalankan Fish It Simulator](https://fish-it-in-nutshell-nzuu9zvd5hgjnwrszo499t.streamlit.app/#fish-it-simulator-prototype)**

---

## 🧠 Fitur Utama & Logika Game

Projek ini bukan sekadar `random.choice` biasa. Kode ini menggunakan pendekatan matematika untuk menjaga ekonomi game tetap stabil.

### 1. Logarithmic Luck Scaling 📉
Dalam banyak game buruk, Luck 1000% berarti peluang naik 10x lipat secara linear, yang merusak game di level tinggi. Di sini, saya menggunakan **Diminishing Returns**:
$$ Multiplier = 1.0 + \log_{10}(1 + TotalLuck) \times 0.95 $$
*   **Luck 100:** Multiplier ~2.9x
*   **Luck 10.000:** Multiplier ~4.8x
*   *Hasil:* Pemain dengan gear level tinggi tetap mendapatkan keuntungan, tapi tidak "merusak" kelangkaan item (Game Balancing).

### 2. Weighted Probability Pool 🎲
Menggunakan sistem bobot dinamis. Ketika Luck meningkat, bobot item langka (Rare/Secret) diperbesar, sementara bobot Common tetap. Ini secara otomatis mengubah persentase drop rate tanpa perlu hardcode if-else yang rumit.

### 3. Physics-based Line Snapping ⚓
Mendapatkan ikan langka bukan jaminan menang!
*   Setiap ikan memiliki variasi berat.
*   Setiap Rod memiliki batas kekuatan (`line_strength`).
*   Jika berat ikan > kekuatan tali, ada probabilitas tali putus berdasarkan seberapa jauh selisih beratnya.

### 4. Anti-Cheat AFK System ⏱️
Simulasi AFK (Auto Farm) yang berjalan di server-side logic mematuhi waktu casting yang sebenarnya (`time.sleep`). Ini mencegah eksploitasi di mana pemain bisa menangkap ribuan ikan dalam satu detik.

---

## 📊 Database Ikan (Sample)

| Tier | Peluang Dasar | Estimasi Berat (Kg) |
| :--- | :--- | :--- |
| **Common** | 70% | 1 - 4 |
| **Uncommon** | 20% | 2 - 7 |
| **Rare** | 8% | 4 - 12 |
| **Epic** | 1.6% | 6 - 18 |
| **Legendary** | 0.8% | 10 - 30 |
| **Mythic** | 0.4% | 20 - 50 |
| **Secret** | 0.2% | 35 - 90 |

*Terdapat juga sistem Mutasi (Shiny, Big, Titanic) yang memberikan multiplier pada berat ikan.*

---

## 🛠️ Instalasi Lokal

Jika Anda ingin menjalankan kode ini di komputer Anda sendiri:

1.  **Clone Repository**
    ```bash
    git clone https://github.com/md-utbh/fish-it-in-nutshell.git
    cd fish-it-in-nutshell
    ```

2.  **Install Requirements**
    ```bash
    pip install streamlit
    ```

3.  **Jalankan Aplikasi**
    ```bash
    streamlit run app.py
    ```

---

## 📝 Catatan Pengembang
Projek ini dibuat sebagai portofolio untuk menunjukkan pemahaman dalam:
*   Python Programming (Logic & Algoritma).
*   Game Development Concepts (RNG, Balancing, Economy).
*   Web Deployment (Streamlit Cloud).

---

*Dibuat dengan ❤️ dan ☕ menggunakan Python.*
