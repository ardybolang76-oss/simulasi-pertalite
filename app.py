import streamlit as st
import matplotlib.pyplot as plt

# Konfigurasi Halaman
st.set_page_config(page_title="Kalkulator Subsidi BBM", page_icon="🧮", layout="wide")

# Header Aplikasi
st.title("🧮 Kalkulator Simulasi Subsidi BBM")
st.markdown("Dashboard interaktif untuk menganalisis beban subsidi BBM berdasarkan parameter global dan domestik.")
st.markdown("---")

# ==========================================
# BAGIAN INPUT (Tanpa Sidebar)
# ==========================================
st.markdown("### ⚙️ Parameter Input")
col_in1, col_in2, col_in3 = st.columns(3)

with col_in1:
    mops_price = st.slider("Harga Minyak (MOPS) USD/bbl", min_value=50.0, max_value=200.0, value=133.44)
    kurs = st.number_input("Kurs Rupiah (Rp/USD)", min_value=10000, max_value=20000, value=17002, step=100)

with col_in2:
    margin = st.number_input("Margin & Distribusi (Rp/L)", value=1200, step=100)
    harga_jual = st.number_input("Harga Jual Pertalite (Rp/L)", value=10000, step=500)

with col_in3:
    konsumsi_tahunan_juta_kl = st.slider("Konsumsi Tahunan (Juta KL)", min_value=10.0, max_value=50.0, value=28.06)
    anggaran_subsidi_t = st.number_input("Total Anggaran Subsidi (Triliun Rp)", value=382.6, step=10.0)
    realisasi_subsidi_t = st.number_input("Realisasi Subsidi (Triliun Rp)", value=51.5, step=5.0)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# PERHITUNGAN LOGIKA (Sesuai Catatan Analisis)
# ==========================================
hip = (mops_price * kurs) / 159
harga_dasar = hip + margin
subsidi_per_liter = harga_dasar - harga_jual if harga_dasar > harga_jual else 0

konsumsi_harian_liter = (konsumsi_tahunan_juta_kl * 1_000_000 * 1_000) / 365
beban_harian_rp = subsidi_per_liter * konsumsi_harian_liter
beban_bulanan_rp = beban_harian_rp * 30
beban_tahunan_rp = beban_harian_rp * 365

sisa_anggaran_t = anggaran_subsidi_t - realisasi_subsidi_t
sisa_bulan = sisa_anggaran_t / (beban_bulanan_rp / 1_000_000_000_000) if beban_bulanan_rp > 0 else 0

# ==========================================
# TAMPILAN DASHBOARD (Sesuai Layout Gambar)
# ==========================================
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("**Profil Pengguna Pertalite**")
    # Membuat Pie Chart Statis menggunakan Matplotlib
    fig, ax = plt.subplots(figsize=(6, 4))
    labels = ['Lainnya (>1400cc)', 'Mobil <1400cc', 'Motor']
    sizes = [40, 31.4, 28.6]
    colors = ['#2b5baf', '#85bcf5', '#ea4335']
    
    # Plotting
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, textprops={'fontsize': 10})
    ax.axis('equal') # Agar proporsi bulat sempurna
    fig.patch.set_alpha(0.0) # Background transparan
    
    # Render figure statis di Streamlit
    st.pyplot(fig)

with col2:
    with st.container(border=True):
        st.markdown("#### ⛽ Neraca Harga & Subsidi")
        st.markdown(f"**Harga Indeks Pasar (HIP):** Rp {hip:,.0f} / L")
        st.markdown(f"**Harga Dasar (Keekonomian):** Rp {harga_dasar:,.0f} / L")
        st.divider()
        st.markdown(f"✅ **Harga Jual Saat Ini:** Rp {harga_jual:,.0f} / L")
        st.markdown(f"⚠️ **Beban Subsidi per Liter:** Rp {subsidi_per_liter:,.0f} / L")

st.markdown("<br>", unsafe_allow_html=True)
col3, col4 = st.columns(2)

with col3:
    with st.container(border=True):
        st.markdown("#### 💰 Dampak Ekonomi Nasional")
        st.markdown(f"Beban Subsidi per Hari: **Rp {beban_harian_rp / 1_000_000_000:,.2f} Miliar**")
        st.markdown(f"Beban Subsidi per Bulan: **Rp {beban_bulanan_rp / 1_000_000_000_000:,.2f} Triliun**")
        st.divider()
        st.markdown(f"Estimasi Beban Setahun: **+Rp {beban_tahunan_rp / 1_000_000_000_000:,.2f} Triliun**")

with col4:
    with st.container(border=True):
        st.markdown("#### 🏛️ Kapasitas & Ketahanan APBN")
        st.markdown(f"Sisa Anggaran Subsidi: **Rp {sisa_anggaran_t:,.2f} Triliun**")
        st.divider()
        if sisa_bulan >= 10:
            st.success(f"Ketahanan Sisa Anggaran: {sisa_bulan:,.1f} Bulan")
        else:
            st.error(f"Ketahanan Sisa Anggaran: {sisa_bulan:,.1f} Bulan (Perlu Geser Anggaran!)")

st.markdown("<br>", unsafe_allow_html=True)
with st.expander("💡 Dari Mana Angka Harga Keekonomian Berasal?"):
    st.write("Berdasarkan Perpres 191/2014, **Harga Dasar = (MOPS x Kurs) / 159 + Rp 1.200** (Margin & Biaya Distribusi).")

# ==========================================
# FOOTER
# ==========================================
st.markdown("<br><br><hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 16px; color: #555;'>💡 Semua Bisa Dihitung<br>By Alif Towew</p>", unsafe_allow_html=True)
