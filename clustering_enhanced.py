"""
===============================================================================
CLUSTERING TOURISM DESTINATIONS - K-MEANS WITH VISUALIZATIONS
===============================================================================

Script ini melakukan clustering destinasi wisata Indonesia menggunakan K-Means
dan menghasilkan 2 visualisasi:
1. Pairwise scatter plot (PNG)
2. Interactive map dengan OpenStreetMap (HTML)

Fitur yang digunakan:
- Price, Rating, Time_Minutes (business features)
- Lat, Long (geographic features)
- Avg_Rating, Rating_Count, Rating_Std (user review aggregation)

===============================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from matplotlib.patches import Ellipse
import itertools
import folium
from folium import plugins
import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-whitegrid')

# ============================================================================
# STEP 1: LOAD DATA
# ============================================================================
print("="*80)
print("STEP 1: LOADING DATA")
print("="*80)

tourism = pd.read_csv('tourism_with_id.csv')
ratings = pd.read_csv('tourism_rating.csv')

print(f"✓ Tourism data: {len(tourism)} destinations")
print(f"✓ Ratings data: {len(ratings)} user ratings\n")


# ============================================================================
# STEP 2: AGGREGATE USER RATINGS
# ============================================================================
print("="*80)
print("STEP 2: AGGREGATE USER RATINGS")
print("="*80)

# Hitung rata-rata, jumlah, dan std untuk setiap destinasi
ratings_agg = ratings.groupby('Place_Id').agg({
    'Place_Ratings': ['mean', 'count', 'std']
}).reset_index()

ratings_agg.columns = ['Place_Id', 'Avg_Rating', 'Rating_Count', 'Rating_Std']
ratings_agg['Rating_Std'] = ratings_agg['Rating_Std'].fillna(0)

print(f"✓ Aggregated ratings for {len(ratings_agg)} places\n")


# ============================================================================
# STEP 3: MERGE DATA
# ============================================================================
print("="*80)
print("STEP 3: MERGE TOURISM + RATINGS")
print("="*80)

tourism_merged = tourism.merge(ratings_agg, on='Place_Id', how='left')

print(f"✓ Merged data: {len(tourism_merged)} destinations")
print(f"  Columns: {list(tourism_merged.columns)}\n")


# ============================================================================
# STEP 4: SELECT FEATURES FOR CLUSTERING
# ============================================================================
print("="*80)
print("STEP 4: SELECT FEATURES")
print("="*80)

features = ['Price', 'Rating', 'Time_Minutes', 'Lat', 'Long',
            'Avg_Rating', 'Rating_Count', 'Rating_Std']

clustering_data = tourism_merged[features].copy()

print(f"✓ Selected {len(features)} features:")
for feat in features:
    print(f"  - {feat}")
print()


# ============================================================================
# STEP 5: HANDLE MISSING VALUES (TIME_MINUTES)
# ============================================================================
print("="*80)
print("STEP 5: HANDLE MISSING VALUES")
print("="*80)

print(f"Missing Time_Minutes: {clustering_data['Time_Minutes'].isna().sum()} "
      f"({100*clustering_data['Time_Minutes'].isna().sum()/len(clustering_data):.1f}%)")

# Impute berdasarkan median per Category (lebih realistis)
time_medians = tourism_merged.groupby('Category')['Time_Minutes'].median()

for idx in clustering_data[clustering_data['Time_Minutes'].isna()].index:
    category = tourism_merged.loc[idx, 'Category']

    if category in time_medians.index and not pd.isna(time_medians[category]):
        clustering_data.loc[idx, 'Time_Minutes'] = time_medians[category]
    else:
        # Fallback ke global median
        clustering_data.loc[idx, 'Time_Minutes'] = tourism_merged['Time_Minutes'].median()

# Tambah jitter kecil untuk menghindari overlap sempurna
np.random.seed(42)
clustering_data['Time_Minutes'] = clustering_data['Time_Minutes'] + np.random.normal(0, 3, len(clustering_data))

print(f"✓ Missing values filled with category-based median + jitter\n")


# ============================================================================
# STEP 6: OUTLIER CAPPING (IQR METHOD)
# ============================================================================
print("="*80)
print("STEP 6: OUTLIER CAPPING")
print("="*80)

for col in clustering_data.columns:
    Q1 = clustering_data[col].quantile(0.25)
    Q3 = clustering_data[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    before = clustering_data[col].copy()
    clustering_data[col] = clustering_data[col].clip(lower=lower, upper=upper)
    n_capped = (before != clustering_data[col]).sum()

    if n_capped > 0:
        print(f"  {col}: {n_capped} values capped")

print(f"✓ Outliers capped using IQR method\n")


# ============================================================================
# STEP 7: SAVE ORIGINAL DATA (BEFORE SCALING)
# ============================================================================
clustering_data_original = clustering_data.copy()


# ============================================================================
# STEP 8: FEATURE SCALING (STANDARDIZATION)
# ============================================================================
print("="*80)
print("STEP 8: FEATURE SCALING")
print("="*80)

scaler = StandardScaler()
data_scaled = scaler.fit_transform(clustering_data)

print(f"✓ Features scaled using StandardScaler")
print(f"  Mean = 0, Std = 1 for all features")
print(f"  Shape: {data_scaled.shape}\n")


# ============================================================================
# STEP 9: SET K VALUE
# ============================================================================
print("="*80)
print("STEP 9: SET K VALUE")
print("="*80)

K = 5  # ← UBAH NILAI K DI SINI JIKA PERLU!

print(f"✓ K = {K} clusters\n")


# ============================================================================
# STEP 10: PERFORM K-MEANS CLUSTERING
# ============================================================================
print("="*80)
print("STEP 10: K-MEANS CLUSTERING")
print("="*80)

kmeans = KMeans(n_clusters=K, random_state=42, n_init=10)
labels = kmeans.fit_predict(data_scaled)

print(f"✓ K-Means completed")
print(f"  Algorithm: Lloyd (default)")
print(f"  n_init: 10 (10 different centroid initializations)\n")


# ============================================================================
# STEP 11: EVALUATE CLUSTERING
# ============================================================================
print("="*80)
print("STEP 11: EVALUATE CLUSTERING")
print("="*80)

silhouette = silhouette_score(data_scaled, labels)

print(f"Silhouette Score: {silhouette:.4f}")
print(f"  Range: [-1, 1]")
print(f"  Higher = better separation\n")

print("Cluster Distribution:")
unique, counts = np.unique(labels, return_counts=True)
for cluster, count in zip(unique, counts):
    pct = 100 * count / len(labels)
    print(f"  Cluster {cluster}: {count:3d} destinations ({pct:5.1f}%)")
print()


# ============================================================================
# STEP 12: PREPARE COLOR PALETTE
# ============================================================================
colors_palette = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F']
colors = colors_palette[:K]


# ============================================================================
# STEP 13: VISUALISASI 1 - PAIRWISE SCATTER PLOT
# ============================================================================
print("="*80)
print("STEP 13: CREATE PAIRWISE SCATTER PLOT")
print("="*80)

# Pilih 4 fitur penting untuk visualisasi
important_features = ['Price', 'Rating', 'Time_Minutes', 'Avg_Rating']
feature_labels = {
    'Price': 'Price (Rp)',
    'Rating': 'Rating (1-5)',
    'Time_Minutes': 'Time (minutes)',
    'Avg_Rating': 'User Rating (1-5)'
}

# Buat semua kombinasi 2 fitur (6 kombinasi dari 4 fitur)
feature_combinations = list(itertools.combinations(important_features, 2))

# Buat figure dengan 2 baris x 3 kolom
fig, axes = plt.subplots(2, 3, figsize=(20, 12))
axes = axes.ravel()

# Plot setiap kombinasi fitur
for idx, (feat1, feat2) in enumerate(feature_combinations):
    ax = axes[idx]

    # Plot setiap cluster
    for cluster in range(K):
        # Ambil data untuk cluster ini
        mask = labels == cluster
        x_data = clustering_data_original.loc[mask, feat1].values
        y_data = clustering_data_original.loc[mask, feat2].values

        # Scatter plot
        ax.scatter(x_data, y_data,
                  c=colors[cluster],
                  label=f'Cluster {cluster} (n={mask.sum()})',
                  alpha=0.7,
                  edgecolors='white',
                  linewidth=1.5,
                  s=120)

        # Hitung dan gambar confidence ellipse
        if len(x_data) >= 3:
            # Hitung covariance matrix
            cov = np.cov(x_data, y_data)
            lambda_, v = np.linalg.eig(cov)
            lambda_ = np.sqrt(lambda_)

            # Gambar ellipse (1 sigma dan 2 sigma)
            for n_std in [1, 2]:
                ell = Ellipse(
                    xy=(np.mean(x_data), np.mean(y_data)),
                    width=lambda_[0]*n_std*2,
                    height=lambda_[1]*n_std*2,
                    angle=np.rad2deg(np.arccos(v[0, 0])),
                    facecolor=colors[cluster],
                    alpha=0.15/(n_std),
                    edgecolor=colors[cluster],
                    linewidth=2,
                    linestyle='--'
                )
                ax.add_patch(ell)

        # Tandai cluster center dengan X
        center_x = x_data.mean()
        center_y = y_data.mean()

        # X hitam besar
        ax.scatter(center_x, center_y,
                  c='black', marker='X', s=400,
                  edgecolors='white', linewidth=3, zorder=10)

        # X warna cluster di tengah
        ax.scatter(center_x, center_y,
                  c=colors[cluster], marker='X', s=250,
                  edgecolors='black', linewidth=2, zorder=11)

    # Set labels dan title
    ax.set_xlabel(feature_labels[feat1], fontsize=13, fontweight='bold')
    ax.set_ylabel(feature_labels[feat2], fontsize=13, fontweight='bold')
    ax.set_title(f'{feature_labels[feat1]} vs {feature_labels[feat2]}',
                fontsize=14, fontweight='bold', pad=10)
    ax.legend(loc='best', fontsize=10, framealpha=0.95, edgecolor='black')
    ax.grid(True, alpha=0.3, linestyle='--')

    # Tambah text box dengan silhouette score
    textstr = f'Silhouette: {silhouette:.3f}'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=10,
           verticalalignment='top', bbox=props)

# Set judul keseluruhan
plt.suptitle(f'K-Means Clustering (K={K}): Pairwise Visualization\n'
             f'Ellipses show cluster spread (1σ and 2σ), X marks show centers',
             fontsize=16, fontweight='bold', y=0.995)
plt.tight_layout()

# Simpan gambar
filename1 = f'enhanced_pairwise_k{K}.png'
plt.savefig(filename1, dpi=150, bbox_inches='tight')
print(f"✓ Saved: {filename1}\n")
plt.close()


# ============================================================================
# STEP 14: VISUALISASI 2 - INTERACTIVE MAP (FOLIUM)
# ============================================================================
print("="*80)
print("STEP 14: CREATE INTERACTIVE MAP")
print("="*80)

# Tambahkan kolom tambahan ke data original
clustering_data_original['Category'] = tourism_merged['Category']
clustering_data_original['City'] = tourism_merged['City']
clustering_data_original['Place_Name'] = tourism_merged['Place_Name']
clustering_data_original['Cluster'] = labels

# Hitung center map (rata-rata koordinat Indonesia)
center_lat = clustering_data_original['Lat'].mean()
center_lon = clustering_data_original['Long'].mean()

print(f"Map center: Lat={center_lat:.4f}, Lon={center_lon:.4f}")

# Buat base map dengan OpenStreetMap
m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=5,
    tiles='OpenStreetMap',
    control_scale=True
)

# Color mapping untuk cluster (sama dengan pairwise plot)
color_map = {
    0: '#FF6B6B',  # Red
    1: '#4ECDC4',  # Teal
    2: '#45B7D1',  # Blue
    3: '#FFA07A',  # Orange
    4: '#98D8C8',  # Green
    5: '#F7DC6F',  # Yellow
}

# Tambahkan marker untuk setiap destinasi
for idx, row in clustering_data_original.iterrows():
    cluster = int(row['Cluster'])

    # Buat HTML popup dengan info destinasi
    popup_html = f"""
    <div style="font-family: Arial; width: 250px;">
        <h4 style="margin: 0 0 10px 0; color: {color_map.get(cluster, '#333')};">
            {row['Place_Name']}
        </h4>
        <table style="width: 100%; font-size: 12px;">
            <tr><td><b>Cluster:</b></td><td>{cluster}</td></tr>
            <tr><td><b>City:</b></td><td>{row['City']}</td></tr>
            <tr><td><b>Category:</b></td><td>{row['Category']}</td></tr>
            <tr><td><b>Price:</b></td><td>Rp {row['Price']:,.0f}</td></tr>
            <tr><td><b>Rating:</b></td><td>{row['Rating']:.1f} / 5.0</td></tr>
            <tr><td><b>Time:</b></td><td>{row['Time_Minutes']:.0f} min</td></tr>
            <tr><td><b>User Rating:</b></td><td>{row['Avg_Rating']:.2f}</td></tr>
        </table>
    </div>
    """

    # Tambahkan CircleMarker
    folium.CircleMarker(
        location=[row['Lat'], row['Long']],
        radius=8,
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=f"{row['Place_Name']} (Cluster {cluster})",
        color='white',
        fillColor=color_map.get(cluster, '#999999'),
        fillOpacity=0.7,
        weight=2
    ).add_to(m)

# Tambahkan marker untuk cluster centers
for cluster in range(K):
    mask = clustering_data_original['Cluster'] == cluster

    if mask.sum() > 0:
        # Hitung center cluster (rata-rata Lat/Long)
        center_lat_cluster = clustering_data_original.loc[mask, 'Lat'].mean()
        center_lon_cluster = clustering_data_original.loc[mask, 'Long'].mean()
        count = mask.sum()

        # Tambahkan star marker untuk cluster center
        folium.Marker(
            location=[center_lat_cluster, center_lon_cluster],
            popup=f"<b>Cluster {cluster} Center</b><br>{count} destinations",
            icon=folium.Icon(color='black', icon='star', prefix='fa'),
            tooltip=f"Cluster {cluster} Center"
        ).add_to(m)

# Tambahkan legend di kanan bawah
legend_html = f"""
<div style="position: fixed;
            bottom: 50px; right: 50px;
            width: 200px; height: auto;
            background-color: white;
            border:2px solid grey;
            z-index:9999;
            font-size:14px;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
            ">
<h4 style="margin: 0 0 10px 0;">K-Means Clusters (K={K})</h4>
"""

for cluster in range(K):
    mask = clustering_data_original['Cluster'] == cluster
    count = mask.sum()
    pct = 100 * count / len(clustering_data_original)

    legend_html += f"""
    <p style="margin: 5px 0;">
        <span style="background-color: {color_map.get(cluster, '#999')};
                     width: 15px; height: 15px;
                     display: inline-block;
                     border: 1px solid #333;
                     margin-right: 5px;">
        </span>
        Cluster {cluster}: {count} ({pct:.1f}%)
    </p>
    """

legend_html += f"""
<hr style="margin: 10px 0;">
<p style="margin: 5px 0; font-size: 12px;">
    <b>Silhouette:</b> {silhouette:.4f}
</p>
<p style="margin: 5px 0; font-size: 11px; color: #666;">
    ⭐ = Cluster center
</p>
</div>
"""

m.get_root().html.add_child(folium.Element(legend_html))

# Tambahkan fullscreen button
plugins.Fullscreen().add_to(m)

# Simpan map sebagai HTML
filename2 = f'enhanced_geographic_map_k{K}.html'
m.save(filename2)

print(f"✓ Saved: {filename2}")
print(f"  → Buka file ini di browser untuk melihat peta Indonesia!")
print(f"  → Klik marker untuk detail destinasi")
print(f"  → Zoom in/out untuk eksplorasi\n")


# ============================================================================
# SUMMARY
# ============================================================================
print("="*80)
print("SUMMARY")
print("="*80)

print(f"\n✓ Total visualizations created: 2 files")
print(f"\nFiles:")
print(f"  1. {filename1} - Pairwise scatter plot (PNG)")
print(f"  2. {filename2} - Interactive OpenStreetMap (HTML)")

print(f"\nClustering Results (K={K}):")
print(f"  Silhouette Score: {silhouette:.4f}")
print(f"  Cluster distribution:")
for cluster, count in zip(unique, counts):
    pct = 100 * count / len(labels)
    print(f"    - Cluster {cluster}: {count} destinations ({pct:.1f}%)")

print(f"\nFeatures used (8 total):")
print(f"  • Price, Rating, Time_Minutes (business)")
print(f"  • Lat, Long (geographic)")
print(f"  • Avg_Rating, Rating_Count, Rating_Std (user reviews)")

print("\n" + "="*80)
print("SELESAI! ✓")
print("="*80)