# Tutorial Clustering - Indonesia Tourism Dataset

Repository untuk tutorial mata kuliah Data Mining tentang clustering (K-Means dan Hierarchical Clustering) menggunakan dataset destinasi wisata Indonesia.

## 📁 Struktur File

```
indonesia_tourism/
├── venv/                                    # Virtual environment
├── clustering_tutorial.py                   # Script utama tutorial (READY TO USE)
├── clustering_tutorial.ipynb                # Jupyter notebook (optional)
├── ANALISIS_CLUSTERING.md                   # Analisis lengkap business implications
├── README.md                                # File ini
│
├── tourism_with_id.csv                      # Dataset utama (437 destinasi)
├── tourism_rating.csv                       # Rating dari user (10,000 ratings)
├── user.csv                                 # Data user (300 users)
├── package_tourism.csv                      # Paket wisata (100 packages)
│
├── tourism_clustered_results.csv            # Hasil clustering dengan label
├── clustering_comparison_results.csv        # Tabel perbandingan metode
│
└── Output Visualizations:
    ├── 01_feature_distributions.png         # Distribusi & boxplot fitur
    ├── 02_correlation_matrix.png            # Heatmap korelasi
    ├── 03_elbow_method.png                  # Elbow curve
    ├── 04_silhouette_analysis.png           # Silhouette score
    ├── 05_kmeans_preprocessing_comparison.png
    ├── 06_kmeans_different_k.png
    ├── 07_dendrograms.png                   # 4 dendrogram
    ├── 08_hierarchical_linkage_methods.png
    ├── 09_hierarchical_different_k.png
    ├── 10_kmeans_visualization.png          # PCA K-Means
    ├── 11_hierarchical_visualization.png    # PCA Hierarchical
    ├── 12_kmeans_vs_hierarchical.png
    └── 13_final_comparison.png              # Summary
```

## 🎯 Tujuan Tutorial

1. **Eksplorasi Data** - Missing values, outliers, data quality
2. **Integrasi Data** - Menggabungkan multiple CSV files
3. **Preprocessing** - Handling missing values, outliers, scaling
4. **Clustering** - K-Means dan Hierarchical dengan berbagai parameter
5. **Perbandingan** - Dengan/tanpa preprocessing, parameter berbeda
6. **Business Implications** - Interpretasi hasil untuk keputusan bisnis

## 🚀 Quick Start

### Setup (Local)

```bash
# 1. Buat virtual environment
python3 -m venv venv

# 2. Aktifkan venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download dataset (jika belum ada)
kaggle datasets download aprabowo/indonesia-tourism-destination
unzip indonesia-tourism-destination.zip

# 5. Run tutorial
python clustering_tutorial.py
```

### Setup (Google Colab)

```python
# 1. Upload kaggle.json untuk credentials
from google.colab import files
files.upload()

# 2. Setup Kaggle
!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

# 3. Download dataset
!kaggle datasets download aprabowo/indonesia-tourism-destination
!unzip indonesia-tourism-destination.zip

# 4. Install dependencies
!pip install scikit-learn pandas numpy matplotlib seaborn scipy

# 5. Copy & paste seluruh isi clustering_tutorial.py
# 6. Run!
```

## 📊 Dataset

**Sumber:** [Kaggle - Indonesia Tourism Destination](https://www.kaggle.com/datasets/aprabowo/indonesia-tourism-destination)

### Files:
- **tourism_with_id.csv** (437 rows, 13 columns)
  - Place_Id, Place_Name, Description, Category, City
  - Price, Rating, Time_Minutes, Lat, Long, etc.

- **tourism_rating.csv** (10,000 rows)
  - User_Id, Place_Id, Place_Ratings

- **user.csv** (300 rows)
  - User_Id, Location, Age

- **package_tourism.csv** (100 rows)
  - Package details

### Features untuk Clustering:
- `Price` - Harga tiket masuk
- `Rating` - Rating tempat wisata (1-5)
- `Time_Minutes` - Durasi kunjungan rata-rata
- `Lat`, `Long` - Koordinat geografis
- `Avg_Rating` - Average rating dari user (aggregated)
- `Rating_Count` - Jumlah rating yang diterima
- `Rating_Std` - Standar deviasi rating

## 🔬 Metodologi

### Pipeline:

```
1. Load Data
   ↓
2. EDA (Missing values, Outliers, Statistics)
   ↓
3. Data Integration (Merge tourism + ratings)
   ↓
4. Feature Selection (8 numerical features)
   ↓
5. Preprocessing
   ├─ Fill missing values (median)
   ├─ Outlier capping (IQR method)
   └─ Feature scaling (StandardScaler)
   ↓
6. K-Means Clustering
   ├─ Elbow method
   ├─ Silhouette analysis
   ├─ Test K=2,3,4,5,6
   └─ With/Without preprocessing
   ↓
7. Hierarchical Clustering
   ├─ Dendrogram (4 linkage methods)
   ├─ Test linkage: ward, complete, average, single
   ├─ Test K=2,3,4,5,6
   └─ With/Without preprocessing
   ↓
8. Visualization (PCA 2D)
   ↓
9. Evaluation & Comparison
   ├─ Silhouette Score
   ├─ Davies-Bouldin Index
   └─ Calinski-Harabasz Index
   ↓
10. Business Interpretation
```

## 📈 Hasil Utama

### K Optimal:
- **Teknis (Silhouette):** K=2 (Score: 0.2102)
- **Bisnis (Rekomendasi):** K=3 (Score: 0.2060)
- **Detail Analysis:** K=4 (Score: 0.1841)

### Segmentasi K=3:

#### Cluster 0: "Budget Cultural Heritage" (46.7%)
- 💰 Harga: ~Rp 6,300
- ⭐ Rating: 4.43
- 📍 Yogyakarta dominant
- 🎯 Target: Budget travelers, students

#### Cluster 1: "Mid-Range City Tourism" (35.0%)
- 💰 Harga: ~Rp 5,900
- ⭐ Rating: 4.47 (TERTINGGI)
- 📍 Bandung/Jakarta
- 🎯 Target: General tourists

#### Cluster 2: "Premium Theme Parks" (18.3%)
- 💰 Harga: ~Rp 107,000 (15-20x lebih mahal!)
- ⭐ Rating: 4.42
- ⏱️ Durasi: 133 menit (longest)
- 🎯 Target: Families, premium segment

### Impact of Preprocessing:

| Metric | With Preprocessing | Without Preprocessing |
|--------|-------------------|----------------------|
| Silhouette Score | 0.2102 | 0.8919 ⚠️ |
| Davies-Bouldin | 1.8295 | 0.4951 |
| Calinski-Harabasz | 118.20 | 653.97 |

**⚠️ Catatan:** Tanpa preprocessing memberikan score "bagus" tapi **misleading** karena didominasi outliers!

### Comparison: K-Means vs Hierarchical

| Method | Silhouette | Davies-Bouldin | Calinski-Harabasz |
|--------|-----------|----------------|-------------------|
| K-Means (preprocessed) | **0.2102** | 1.8295 | **118.20** |
| Hierarchical ward (preprocessed) | 0.1607 | 2.0974 | 85.04 |
| Hierarchical average | **0.2785** | **1.0667** | 4.92 |
| Hierarchical single | 0.2474 | 0.6044 | 2.54 |

**Best:** K-Means dengan preprocessing untuk balanced performance

## 💡 Business Implications

### Actionable Strategies:

**Untuk Cluster 0 (Budget):**
- Promosi via social media edu-content
- Group discount & student discount
- Package: "Yogya Heritage Tour"

**Untuk Cluster 1 (Mid-Range):**
- Instagram marketing, influencer
- Photo contest, Instagram-able spots
- Weekend special offers

**Untuk Cluster 2 (Premium):**
- Family packages & corporate B2B
- Annual membership program
- TV advertising

### Mixed Package Tours:
- **Budget Explorer:** Rp 50,000 (2 dari C0 + 1 dari C1)
- **Complete Experience:** Rp 150,000 (1 dari tiap cluster)
- **Premium All-In:** Rp 500,000+ (focus C2 + extras)

📖 **Lihat `ANALISIS_CLUSTERING.md` untuk detail lengkap!**

## 🎓 Materi Pembelajaran

### Konsep yang Dicakup:

1. **Data Preprocessing**
   - Missing value imputation
   - Outlier detection & treatment (IQR)
   - Feature scaling (StandardScaler)
   - Why preprocessing matters!

2. **Clustering Algorithms**
   - K-Means (partitional clustering)
   - Hierarchical Clustering (agglomerative)
   - Linkage methods: ward, complete, average, single
   - Dendrogram interpretation

3. **Optimal K Selection**
   - Elbow Method
   - Silhouette Analysis
   - Trade-off: simplicity vs insight

4. **Evaluation Metrics**
   - Silhouette Score (higher better, range -1 to 1)
   - Davies-Bouldin Index (lower better)
   - Calinski-Harabasz Index (higher better)

5. **Visualization**
   - PCA for dimensionality reduction
   - 2D scatter plots
   - Dendrogram

6. **Business Translation**
   - Cluster interpretation
   - Target market identification
   - Actionable marketing strategies

## 🔧 Dependencies

```
pandas
numpy
scikit-learn
matplotlib
seaborn
scipy
kaggle (for dataset download)
```

Install via: `pip install -r requirements.txt`

## 📝 Output Files

### Visualizations (13 PNG files):
Semua visualisasi otomatis ter-generate dengan resolusi tinggi (100 DPI), siap untuk presentasi.

### Data Files (2 CSV files):
- `tourism_clustered_results.csv` - Original data + cluster labels
- `clustering_comparison_results.csv` - Metrics comparison table

## ⚠️ Important Notes

1. **Preprocessing is Critical!**
   - Tanpa preprocessing: hasil misleading (outlier dominant)
   - Dengan preprocessing: hasil interpretable & actionable

2. **K Selection:**
   - K=2: Terlalu sederhana
   - K=3: Sweet spot (REKOMENDASI)
   - K>5: Over-segmentation

3. **Algorithm Choice:**
   - K-Means: Cepat, untuk dataset besar
   - Hierarchical: Lebih fleksibel, tapi lambat

4. **Business Context Matters:**
   - Jangan hanya lihat metrics
   - Interpretasi cluster dalam konteks bisnis
   - Actionable > Perfect score

## 🎯 Pertanyaan Diskusi

1. Mengapa K=2 punya Silhouette Score tertinggi tapi kita rekomendasikan K=3?
2. Apa dampak tidak melakukan preprocessing terhadap hasil clustering?
3. Kapan sebaiknya menggunakan K-Means vs Hierarchical Clustering?
4. Bagaimana cara menjelaskan hasil clustering ke non-technical stakeholder?
5. Jika Anda CEO travel agency, strategi marketing apa yang Anda design berdasarkan clustering ini?

## 📚 References

- Dataset: [Kaggle - Indonesia Tourism Destination](https://www.kaggle.com/datasets/aprabowo/indonesia-tourism-destination)
- Scikit-learn Clustering: https://scikit-learn.org/stable/modules/clustering.html
- Silhouette Analysis: https://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_silhouette_analysis.html

## 👨‍🏫 Untuk Dosen/Instruktur

### Skenario Pengajaran:

**Session 1 (90 menit):**
- Teori: Clustering basics, K-Means, Hierarchical
- Demo: Run `clustering_tutorial.py` section by section
- Diskusi: Interpretasi output & visualisasi

**Session 2 (90 menit):**
- Hands-on: Mahasiswa run sendiri di Google Colab
- Exercise: Ubah parameter (K, linkage method)
- Group work: Business interpretation & presentation

**Assignment:**
- Analyze cluster characteristics
- Propose marketing strategy per cluster
- Compare different K values
- Report hasil dengan visualisasi

### Grading Rubric:
- Technical execution (40%): Preprocessing, clustering, metrics
- Analysis (30%): Interpretasi cluster, optimal K selection
- Business translation (20%): Actionable strategies
- Presentation (10%): Clarity, visualizations

## 📞 Support

Untuk pertanyaan atau issues:
1. Baca `ANALISIS_CLUSTERING.md` untuk detail lengkap
2. Check code comments di `clustering_tutorial.py`
3. Review visualizations untuk insights

---

**Happy Clustering! 🎉**

Dibuat untuk tutorial Data Mining - September 2025# indonesia_tourism
