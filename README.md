# Indonesia Tourism Clustering Analysis

Analisis clustering untuk destinasi wisata Indonesia menggunakan K-Means dengan Exploratory Data Analysis (EDA) lengkap, Elbow Method, dan visualisasi interaktif menggunakan OpenStreetMap.

## 📊 Dataset

**Sumber:** [Kaggle - Indonesia Tourism Destination](https://www.kaggle.com/datasets/aprabowo/indonesia-tourism-destination)

### Data Files:
- **tourism_with_id.csv** (437 destinations)
  - Place_Id, Place_Name, Description, Category, City
  - Price, Rating, Time_Minutes, Lat, Long

- **tourism_rating.csv** (10,000 user ratings)
  - User_Id, Place_Id, Place_Ratings

- **user.csv** (300 users)
  - User_Id, Location, Age

- **package_tourism.csv** (100 tourism packages)

## 🎯 Features

Script ini menggunakan **8 features** untuk clustering:

1. **Price** - Harga tiket masuk (Rp)
2. **Rating** - Rating official (1-5)
3. **Time_Minutes** - Lama kunjungan yang disarankan (menit)
4. **Lat** - Latitude (koordinat geografis)
5. **Long** - Longitude (koordinat geografis)
6. **Avg_Rating** - Average user rating dari reviews (2-4)
7. **Rating_Count** - Jumlah user reviews
8. **Rating_Std** - Standar deviasi dari user ratings

## 🚀 Quick Start

### Setup Environment

```bash
# 1. Clone repository
git clone https://github.com/akhiyarwaladi/indonesia_tourism.git
cd indonesia_tourism

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate  # Windows

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run clustering analysis
python clustering_enhanced.py
```

### Setup for Google Colab

```python
# 1. Upload kaggle.json untuk download dataset
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
!pip install scikit-learn pandas numpy matplotlib seaborn scipy folium

# 5. Upload clustering_enhanced.py dan run!
```

## 📁 Project Structure

```
indonesia_tourism/
├── clustering_enhanced.py          # Main script (19 steps)
├── requirements.txt                # Python dependencies
├── README.md                       # Documentation
│
├── Dataset CSV Files:
│   ├── tourism_with_id.csv
│   ├── tourism_rating.csv
│   ├── user.csv
│   └── package_tourism.csv
│
└── results/                        # Output folder (auto-generated)
    ├── eda_distributions.png       # Feature distributions (EDA)
    ├── eda_correlation.png         # Correlation matrix (EDA)
    ├── eda_outliers.png            # Outlier detection (EDA)
    ├── elbow_method.png            # Elbow analysis for optimal K
    ├── pairwise_k5.png             # Pairwise scatter plots
    └── geographic_map_k5.html      # Interactive OpenStreetMap
```

## 🔬 Analysis Pipeline (19 Steps)

### **Phase 1: Data Loading & Preparation (Steps 1-3)**
1. **Load Data** - Load tourism dan ratings CSV
2. **Aggregate Ratings** - Calculate avg, count, std per destination
3. **Merge Data** - Combine tourism + ratings data

### **Phase 2: Exploratory Data Analysis (Steps 4-7)**
4. **Data Overview** - Dataset info, missing values, descriptive statistics
5. **Feature Distributions** - Histogram dengan mean/median untuk semua fitur
6. **Correlation Analysis** - Correlation heatmap untuk identifikasi multicollinearity
7. **Outlier Detection** - Boxplot dengan IQR method untuk deteksi outliers

**Key Findings:**
- Time_Minutes: 53.1% missing values
- Price & Time_Minutes: Korelasi positif (0.46)
- Price memiliki outliers ekstrem (max: Rp 900,000)

### **Phase 3: Preprocessing (Steps 8-12)**
8. **Select Features** - Pilih 8 numerical features
9. **Handle Missing Values** - Impute Time_Minutes dengan category-based median + jitter
10. **Outlier Capping** - IQR method untuk cap outliers
11. **Save Original Data** - Simpan untuk visualisasi
12. **Feature Scaling** - StandardScaler (mean=0, std=1)

### **Phase 4: Clustering (Steps 13-16)**
13. **Elbow Method** - Test K=2 sampai 10, plot Inertia & Silhouette
14. **Set K Value** - K=5 (dapat diubah di line 438)
15. **K-Means Clustering** - Fit model dengan K clusters
16. **Evaluate** - Silhouette Score & cluster distribution

**Hasil Elbow Method:**
- Best K berdasarkan Silhouette: K=2 (0.1855)
- K=5 dipilih untuk balance antara simplicity & insight

### **Phase 5: Visualization (Steps 17-19)**
17. **Prepare Colors** - Color palette untuk consistency
18. **Pairwise Scatter** - 6 kombinasi dari 4 fitur penting dengan confidence ellipses
19. **Interactive Map** - OpenStreetMap dengan Folium, 437 markers dengan popup info

## 📈 Output Visualizations

### 1. EDA Outputs (3 files)

#### `eda_distributions.png`
- Histogram untuk 8 features
- Mean dan median lines
- Identify skewness dan data distribution

#### `eda_correlation.png`
- Heatmap correlation matrix 8x8
- Values displayed (-1 to 1)
- Identify feature relationships

#### `eda_outliers.png`
- Boxplots untuk semua features
- IQR outlier detection
- Outlier count per feature

### 2. Clustering Outputs (3 files)

#### `elbow_method.png`
- Plot 1: Inertia vs K (elbow curve)
- Plot 2: Silhouette Score vs K
- Best K highlighted dengan green circle
- Range K=2 to 10

#### `pairwise_k5.png`
- 6 scatter plots (2x3 grid)
- Kombinasi: Price, Rating, Time_Minutes, User_Rating
- Confidence ellipses (1σ dan 2σ)
- Cluster centers marked dengan X
- Silhouette score di setiap subplot

#### `geographic_map_k5.html` ⭐
- **Interactive map** Indonesia dengan OpenStreetMap
- 437 CircleMarkers berwarna sesuai cluster
- Click marker untuk detail: Price, Rating, Time, Category, City
- Cluster centers marked dengan star (⭐)
- Legend dengan cluster distribution
- Zoom & pan untuk eksplorasi
- Fullscreen mode available

## 🎨 Visualization Features

### Pairwise Scatter Plot:
- ✅ Confidence ellipses (1σ dan 2σ) untuk cluster spread
- ✅ Cluster centers (X mark hitam + warna)
- ✅ White edges untuk clarity
- ✅ Silhouette score box di setiap plot
- ✅ 6 combinations dari 4 features penting

### Interactive Map:
- ✅ Real OpenStreetMap Indonesia
- ✅ Color-coded markers per cluster
- ✅ Popup HTML dengan 7 informasi
- ✅ Tooltip on hover
- ✅ Cluster centers dengan star icon
- ✅ Legend floating (kanan bawah)
- ✅ Zoom controls & scale
- ✅ Fullscreen button

## 📊 Clustering Results (K=5)

### Cluster Distribution:
- **Cluster 0:** 62 destinations (14.2%)
- **Cluster 1:** 92 destinations (21.1%)
- **Cluster 2:** 113 destinations (25.9%) ← Largest
- **Cluster 3:** 58 destinations (13.3%)
- **Cluster 4:** 112 destinations (25.6%)

### Performance Metrics:
- **Silhouette Score:** 0.1469
- **Range:** -1 (worst) to 1 (best)
- **Interpretation:** Moderate cluster separation

### Recommended K:
- Dari Elbow Method: **K=2** (Silhouette: 0.1855)
- Current setting: **K=5** (balance insight vs simplicity)
- Dapat diubah di `line 438` script

## 🔧 Customization

### Mengubah Nilai K:

Edit file `clustering_enhanced.py` di **line 438**:

```python
K = 5  # ← UBAH NILAI INI! (2-10 recommended)
```

Lalu jalankan ulang:
```bash
python clustering_enhanced.py
```

Output akan generate dengan K baru:
- `results/elbow_method.png` (sama, untuk reference)
- `results/pairwise_k{K}.png`
- `results/geographic_map_k{K}.html`

### Mengubah Features:

Edit **line 88** untuk memilih features berbeda:

```python
features = ['Price', 'Rating', 'Time_Minutes', 'Lat', 'Long',
            'Avg_Rating', 'Rating_Count', 'Rating_Std']
```

## 💡 Key Insights

### 1. Missing Values
- **Time_Minutes:** 53.1% missing
- **Solution:** Category-based median imputation + small jitter
- Lebih realistis dibanding global median

### 2. Outliers
- **Price:** 40 values capped (max Rp 900,000 → premium theme parks)
- **Time_Minutes:** 27 values capped
- **Method:** IQR (Q1 - 1.5×IQR, Q3 + 1.5×IQR)

### 3. Feature Correlation
- **Price ↔ Time_Minutes:** 0.46 (positive correlation)
- Destinasi mahal cenderung butuh waktu lebih lama
- **Rating ↔ Other features:** Korelasi lemah (rating relatif uniform)

### 4. Geographic Distribution
- Clusters menunjukkan pola geografis
- Jakarta, Bandung, Yogyakarta dominant
- Interactive map memudahkan analisis spasial

## 🎓 Learning Objectives

Script ini mencakup konsep:

1. **Data Preprocessing**
   - Missing value imputation (category-based)
   - Outlier detection & capping (IQR)
   - Feature scaling (StandardScaler)
   - Why preprocessing is critical!

2. **Exploratory Data Analysis**
   - Distribution analysis
   - Correlation analysis
   - Outlier detection
   - Visual insights before modeling

3. **Clustering**
   - K-Means algorithm
   - Optimal K selection (Elbow Method)
   - Silhouette Score evaluation
   - Cluster interpretation

4. **Visualization**
   - Static plots (matplotlib/seaborn)
   - Interactive maps (Folium)
   - Confidence ellipses
   - Multi-plot layouts

5. **Code Quality**
   - 19 clear steps (no functions)
   - Extensive comments
   - Easy to understand for students
   - Ready for Google Colab

## 📦 Dependencies

Lihat `requirements.txt`:

```
pandas
numpy
scikit-learn
matplotlib
seaborn
scipy
folium
```

Install semua:
```bash
pip install -r requirements.txt
```

## ⚙️ Technical Details

### Preprocessing Pipeline:
1. Category-based median imputation untuk Time_Minutes
2. Small jitter (σ=3) untuk menghindari overlap
3. IQR outlier capping untuk semua features
4. StandardScaler untuk normalisasi

### K-Means Parameters:
- `n_clusters`: 5 (default, can be changed)
- `random_state`: 42 (reproducibility)
- `n_init`: 10 (10 different centroid initializations)
- `algorithm`: 'lloyd' (default)

### Elbow Method:
- Test range: K=2 to 10
- Metrics: Inertia & Silhouette Score
- Auto-highlight best K

## 🎯 Use Cases

### For Students:
- Learn clustering step-by-step
- Understand preprocessing importance
- Practice data visualization
- Business interpretation skills

### For Instructors:
- Ready-to-use tutorial material
- Clear step-by-step execution
- Discussion-friendly results
- Assignment-ready

### For Data Analysts:
- Template for clustering analysis
- EDA best practices
- Interactive visualization
- Business insights

## 📝 Notes

1. **Script tanpa function** - Semua code sequential, mudah dipahami mahasiswa
2. **19 steps yang jelas** - Setiap step ter-dokumentasi dengan baik
3. **Output ke folder results/** - Organized & clean
4. **Interactive map** - Better insight daripada static plot
5. **K dapat diubah** - Experiment dengan different K values
6. **EDA comprehensive** - Understand data before modeling

## 🚨 Common Issues

### Issue: Folium import error
```bash
pip install folium
```

### Issue: Results folder not created
Script akan auto-create folder `results/` jika belum ada.

### Issue: Memory error dengan K besar
Reduce K atau subsample data untuk testing.

### Issue: Map tidak load di browser
Pastikan file HTML dibuka dari local file system, bukan dari network drive.

## 📚 References

- Dataset: [Kaggle - Indonesia Tourism Destination](https://www.kaggle.com/datasets/aprabowo/indonesia-tourism-destination)
- Scikit-learn: https://scikit-learn.org/stable/modules/clustering.html
- Folium Maps: https://python-visualization.github.io/folium/

## 👨‍💻 Author

Created for Data Mining course tutorial - September 2025

Repository: https://github.com/akhiyarwaladi/indonesia_tourism

## 📄 License

Dataset from Kaggle (CC0: Public Domain)

---

**Happy Clustering! 🎉**

*Explore Indonesia tourism destinations through data science!*
