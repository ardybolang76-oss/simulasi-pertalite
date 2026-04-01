import streamlit as st

# Konfigurasi Halaman
st.set_page_config(page_title="Kalkulator Subsidi BBM", page_icon="🛢️", layout="wide")

# Header Aplikasi
st.title("🧮 Kalkulator Simulasi Subsidi BBM (Pertalite)")
st.markdown("Dashboard interaktif untuk menganalisis dampak harga minyak mentah global dan nilai tukar Rupiah terhadap beban subsidi pada APBN.")
st.markdown("---")

# Sidebar untuk Input Parameter
st.sidebar.header("⚙️ Parameter Input Dasar")
mops_price = st.sidebar.number_input("Harga Minyak (MOPS/Platts) USD/bbl", value=133.442, step=1.0)
kurs = st.sidebar.number_input("Kurs Rupiah (Rp/USD)", value=17002, step=100)
margin = st.sidebar.number_input("Margin & Distribusi (Rp/liter)", value=1200, step=100, help="Sesuai Perpres 191/2014")
harga_jual = st.sidebar.number_input("Harga Jual Pertalite (Rp/liter)", value=10000, step=500)

st.sidebar.markdown("---")
st.sidebar.header("📊 Parameter Makro (APBN)")
konsumsi_tahunan_juta_kl = st.sidebar.number_input("Konsumsi Tahunan (Juta KL)", value=28.06, step=1.0)
anggaran_subsidi_t = st.sidebar.number_input("Total Anggaran Subsidi (Triliun Rp)", value=382.6, step=10.0)
realisasi_subsidi_t = st.sidebar.number_input("Realisasi Subsidi (Triliun Rp)", value=51.5, step=5.0)

# Perhitungan Logika
# 1 barrel = 159 liter
hip = (mops_price * kurs) / 159
harga_dasar = hip + margin
subsidi_per_liter = harga_dasar - harga_jual

# Perhitungan Beban
konsumsi_harian_liter = (konsumsi_tahunan_juta_kl * 1_000_000 * 1_000) / 365
beban_harian_rp = subsidi_per_liter * konsumsi_harian_liter
beban_bulanan_rp = beban_harian_rp * 30
beban_tahunan_rp = beban_harian_rp * 365

# Perhitungan Kapasitas APBN
sisa_anggaran_t = anggaran_subsidi_t - realisasi_subsidi_t
sisa_bulan = sisa_anggaran_t / (beban_bulanan_rp / 1_000_000_000_000) if beban_bulanan_rp > 0 else 0

# Tampilan UI Utama
st.subheader("1. Harga Keekonomian vs Harga Jual")
col1, col2, col3 = st.columns(3)
col1.metric("Harga Indeks Pasar (HIP)", f"Rp {hip:,.0f} / L")
col2.metric("Harga Dasar (Tanpa Subsidi)", f"Rp {harga_dasar:,.0f} / L")
col3.metric("Subsidi Ditanggung Negara", f"Rp {subsidi_per_liter:,.0f} / L", delta="Selisih Harga", delta_color="inverse")

st.markdown("<br>", unsafe_allow_html=True)
st.subheader("2. Proyeksi Beban Subsidi Negara")
col4, col5, col6 = st.columns(3)
col4.metric("Beban Subsidi per Hari", f"Rp {beban_harian_rp / 1_000_000_000:,.2f} Miliar")
col5.metric("Beban Subsidi per Bulan", f"Rp {beban_bulanan_rp / 1_000_000_000_000:,.2f} Triliun")
col6.metric("Estimasi Beban Setahun", f"Rp {beban_tahunan_rp / 1_000_000_000_000:,.2f} Triliun")

st.markdown("<br>", unsafe_allow_html=True)
st.subheader("3. Kapasitas & Ketahanan APBN")
col7, col8 = st.columns(2)
col7.metric("Sisa Anggaran Subsidi", f"Rp {sisa_anggaran_t:,.2f} Triliun")

# Logika peringatan jika sisa anggaran tidak cukup untuk sisa tahun berjalan
if sisa_bulan >= 10:
    status_apbn = "Aman (Bisa Cover Sisa Tahun)"
    color = "normal"
else:
    status_apbn = "Perlu Geser Anggaran!"
    color = "inverse"

col8.metric("Ketahanan Sisa Anggaran", f"{sisa_bulan:,.1f} Bulan", delta=status_apbn, delta_color=color)

# Footer Persona
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Dibuat oleh <b>Alif Towew</b> | <b>Semua Bisa Dihitung</b></p>", unsafe_allow_html=True)
