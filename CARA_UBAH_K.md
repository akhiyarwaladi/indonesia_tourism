# 🎯 CARA MENGUBAH K DAN VISUALISASI HASIL

## Pilihan 1: Menggunakan Script Sederhana (`clustering_custom.py`)

### ⭐ PALING MUDAH - RECOMMENDED!

File: `clustering_custom.py` (1 script, all-in-one)

### Langkah-langkah:

1. **Buka file `clustering_custom.py`**

2. **Cari baris 59-65** (bagian STEP 2: SET PARAMETERS):

```python
# ⭐⭐⭐ UBAH NILAI INI UNTUK MENGUBAH JUMLAH CLUSTER! ⭐⭐⭐
K = 5  # Coba ubah ke 2, 3, 4, 5, 6, 7, dst.

# ⭐⭐⭐ UBAH METODE CLUSTERING ⭐⭐⭐
METHOD = 'kmeans'  # Pilihan: 'kmeans' atau 'hierarchical'

# ⭐⭐⭐ UNTUK HIERARCHICAL, UBAH LINKAGE METHOD ⭐⭐⭐
LINKAGE = 'ward'  # Pilihan: 'ward', 'complete', 'average', 'single'
```

3. **Ubah nilai K** (contoh menjadi 4):
```python
K = 4
```

4. **Jalankan script:**
```bash
python clustering_custom.py
```

5. **Output yang dihasilkan:**
   - Visualisasi lengkap: `clustering_k4_kmeans.png`
   - Data dengan label: `clustering_results_k4_kmeans.csv`
   - Summary metrics: `clustering_summary_k4_kmeans.csv`
   - Print karakteristik setiap cluster di terminal

### Contoh: Coba K berbeda

**Untuk K=3:**
```python
K = 3
METHOD = 'kmeans'
```

**Untuk K=5 dengan Hierarchical:**
```python
K = 5
METHOD = 'hierarchical'
LINKAGE = 'ward'
```

**Untuk K=4 dengan Hierarchical Average:**
```python
K = 4
METHOD = 'hierarchical'
LINKAGE = 'average'
```

---

## Pilihan 2: Menggunakan Script Interactive (`clustering_interactive.py`)

### 🔧 LEBIH ADVANCED - Multiple Examples

File: `clustering_interactive.py` (sudah ada 5 contoh built-in)

### Cara pakai:

1. **Langsung jalankan** untuk lihat semua contoh:
```bash
python clustering_interactive.py
```

Output otomatis:
- K=3 K-Means
- K=4 K-Means
- K=3 Hierarchical
- Comparison K=2 sampai K=7
- Test semua linkage methods

2. **Untuk custom K**, edit bagian CONTOH di bawah `if __name__ == "__main__":`

Misalnya tambahkan contoh baru:
```python
# CONTOH BARU: K=6
k = 6
labels, metrics = perform_clustering(data_scaled, k, method='kmeans')
visualize_clustering(data_scaled, labels, k, 'K-Means', metrics,
                    save_filename=f'clustering_k{k}_kmeans.png')
show_cluster_characteristics(tourism_merged, clustering_data, labels, k)
```

3. **Jalankan:**
```bash
python clustering_interactive.py
```

---

## Pilihan 3: Modifikasi Script Tutorial Utama

### 📚 Untuk Pembelajaran Step-by-Step

File: `clustering_tutorial.py` (script tutorial lengkap)

### Cara ubah K:

1. **Cari baris yang ada `optimal_k`** (sekitar baris 227):

```python
optimal_k = K_range[optimal_k_idx]
optimal_k = K_range[np.argmax(silhouette_scores)]
```

2. **Ubah menjadi fixed value:**

```python
# optimal_k = K_range[np.argmax(silhouette_scores)]  # comment ini
optimal_k = 4  # ← UBAH NILAI INI!
```

3. **Atau ubah `K_range` untuk test range berbeda** (baris 212):

```python
K_range = range(2, 11)  # Default: 2-10
# Ubah menjadi:
K_range = range(2, 8)   # Test 2-7 saja
```

4. **Jalankan:**
```bash
python clustering_tutorial.py
```

---

## 📊 Perbandingan 3 Pilihan

| Aspek | custom | interactive | tutorial |
|-------|--------|-------------|----------|
| **Kemudahan** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Kecepatan** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Output Detail** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Cocok untuk** | Quick test | Eksplorasi | Tutorial |
| **Waktu run** | ~5 detik | ~30 detik | ~60 detik |

### Rekomendasi:

- **Untuk presentasi/demo cepat:** Gunakan `clustering_custom.py` ⭐
- **Untuk eksplorasi mendalam:** Gunakan `clustering_interactive.py`
- **Untuk belajar/tutorial:** Gunakan `clustering_tutorial.py`

---

## 🎨 Visualisasi yang Dihasilkan

### `clustering_custom.py` menghasilkan 1 file comprehensive:

```
clustering_k4_kmeans.png (large, 20x12 inches)
├─ Main scatter plot (PCA 2D)
├─ Cluster sizes (bar chart)
├─ Price distribution per cluster (boxplot)
├─ Rating distribution per cluster (boxplot)
├─ Time distribution per cluster (boxplot)
└─ Average metrics comparison (grouped bar)
```

### `clustering_interactive.py` menghasilkan multiple files:

```
clustering_k3_kmeans.png
clustering_k4_kmeans.png
clustering_k3_hierarchical.png
comparison_k_values_kmeans.png
comparison_linkage_methods.png
```

---

## 💡 Tips & Tricks

### 1. Bandingkan Beberapa K Sekaligus

Edit `clustering_custom.py`, jalankan 3x dengan K berbeda:

```bash
# Edit K=3, jalankan
python clustering_custom.py

# Edit K=4, jalankan
python clustering_custom.py

# Edit K=5, jalankan
python clustering_custom.py
```

Hasilnya:
```
clustering_k3_kmeans.png
clustering_k4_kmeans.png
clustering_k5_kmeans.png
```

Buka 3 file ini bersamaan untuk compare!

### 2. Quick Command untuk Google Colab

```python
# Di Colab, buat cell baru:

# Cell 1: Setup
K = 4  # Ubah nilai ini
METHOD = 'kmeans'

# Cell 2: Load data (copy dari clustering_custom.py baris 22-54)
# ... (paste code load data)

# Cell 3: Clustering (copy dari clustering_custom.py baris 62-78)
# ... (paste code clustering)

# Cell 4: Visualize (copy dari clustering_custom.py baris 144-252)
# ... (paste code visualisasi)
```

### 3. Batch Processing - Test K=2 sampai K=8

Buat script baru `batch_clustering.py`:

```python
import subprocess

for k in range(2, 9):
    # Edit file
    with open('clustering_custom.py', 'r') as f:
        content = f.read()

    # Replace K value
    content = content.replace('K = 5', f'K = {k}')

    with open('clustering_custom_temp.py', 'w') as f:
        f.write(content)

    # Run
    print(f"\n{'='*80}")
    print(f"Running K={k}...")
    print(f"{'='*80}")
    subprocess.run(['python', 'clustering_custom_temp.py'])

    # Reset
    content = content.replace(f'K = {k}', 'K = 5')

print("\n✓ Selesai! Cek file clustering_k*_kmeans.png")
```

Jalankan: `python batch_clustering.py`

---

## 🔍 Interpretasi Hasil

### Saat Anda ubah K, perhatikan:

1. **Silhouette Score:**
   - Turun? → K terlalu besar
   - Naik? → K lebih optimal
   - Ideal: 0.2-0.5 (untuk real-world data)

2. **Cluster Sizes:**
   - Seimbang (20-40% tiap cluster)? → Bagus
   - Ada cluster <5%? → K terlalu besar
   - 1 cluster dominan >80%? → K terlalu kecil

3. **Visual PCA Plot:**
   - Cluster terpisah jelas? → Bagus
   - Overlap banyak? → Coba K berbeda atau cek preprocessing

4. **Business Meaning:**
   - Setiap cluster punya karakteristik unik? → Bagus
   - Cluster mirip-mirip? → K terlalu besar

### Contoh Interpretasi:

**K=2:**
```
✓ Silhouette tinggi (0.21)
✓ Simple, mudah dijelaskan
✗ Kurang detail untuk strategi marketing
→ Cocok untuk high-level segmentation
```

**K=3:**
```
✓ Silhouette masih tinggi (0.206)
✓ Business interpretation jelas
✓ Cluster sizes seimbang
→ OPTIMAL untuk tutorial ini
```

**K=6:**
```
✗ Silhouette turun (0.16)
✗ Cluster sizes timpang
✗ Sulit interpretasi bisnis
→ Over-segmentation, NOT recommended
```

---

## ❓ FAQ

**Q: K berapa yang terbaik?**
A: Untuk dataset ini, K=3 paling optimal (balance antara teknis & bisnis)

**Q: Kenapa K=2 score-nya lebih tinggi tapi tidak direkomendasikan?**
A: Karena K=2 terlalu sederhana, insight bisnis kurang. K=3 hanya sedikit lebih rendah (0.206 vs 0.210) tapi jauh lebih informatif.

**Q: Boleh K=10 atau lebih?**
A: Secara teknis boleh, tapi:
   - Silhouette score rendah
   - Cluster sizes sangat timpang
   - Sulit diimplementasikan di bisnis
   - Over-segmentation

**Q: Perbedaan K-Means vs Hierarchical?**
A:
   - K-Means: Cepat, butuh K di awal, cluster spherical
   - Hierarchical: Lambat, bisa lihat dendrogram, fleksibel
   - Untuk dataset ini, K-Means lebih baik

**Q: Kapan harus preprocessing dan kapan tidak?**
A: SELALU preprocessing! Tanpa preprocessing hasil misleading karena outliers dominan.

---

## 📝 Checklist Sebelum Presentasi

Saat Anda ubah K untuk presentasi, pastikan:

- [ ] Jalankan dengan K yang akan dipresentasikan
- [ ] Cek visualisasi tersimpan dengan benar
- [ ] Baca karakteristik setiap cluster
- [ ] Siapkan business interpretation
- [ ] Compare dengan K lain (minimal 2-3 nilai K)
- [ ] Screenshot atau print hasil metrics
- [ ] Siapkan penjelasan "why this K"

---

## 🚀 Quick Reference

```bash
# Test K=3
vim clustering_custom.py  # ubah K=3
python clustering_custom.py

# Test K=4
vim clustering_custom.py  # ubah K=4
python clustering_custom.py

# Test K=5
vim clustering_custom.py  # ubah K=5
python clustering_custom.py

# Lihat semua hasil
ls -lh clustering_k*_kmeans.png

# Buka visualisasi
xdg-open clustering_k3_kmeans.png  # Linux
# atau
open clustering_k3_kmeans.png      # Mac
# atau double-click di Windows Explorer
```

---

**Good luck dengan tutorial dan presentasi! 🎉**