import streamlit as st
import pandas as pd
import numpy as np
import plotly_express as px
#from PIL import Image

# load model 
import joblib

# linear programming
import pulp
from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable

def main():
    """App with Streamlit"""
    
    st.set_page_config(
    page_title="Action Learning Data Analytics Angkatan V Kelompok 4",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    
    )
    st.subheader("Kalkulator Perhitungan Alokasi Belanja Fungsi untuk meningkatkan Indeks Pembangunan Ekonomi Inklusif")
    st.sidebar.title("Pengaturan Constraints")
    p = st.sidebar.number_input(label="Fungsi Pendidikan (dalam %)",value=20,min_value=20, max_value=100, step=1)
    k= st.sidebar.number_input(label="Fungsi Kesehatan (dalam %)",value=10,min_value=10, max_value=100, step=1)
    l = st.sidebar.number_input(label="Fungsi Perumahan dan Fasilitas Umum (dalam %)",value=25,min_value=1, max_value=100, step=1)
        
    df = pd.read_excel('data_sumber.xlsx')
    pemda = st.selectbox('Pilih Pemerintah Daerah', df['Pemda'].unique())
    tahun = st.selectbox('Pilih Tahun', df['Tahun'].unique())
    
    pilihan = df[(df["Pemda"] == pemda) & (df["Tahun"]==tahun)]

    col1, col2 = st.columns(2)
    
    
    with col1:
        st.write(f"Nilai Alokasi Belanja Fungsi {pemda} Tahun {tahun}")
        st.write("")
        st.write("")
        st.write("")
        st.write(f"Alokasi Pendidikan : {pilihan.iloc[0,9]:20,.02f} ") 
        st.write(f"Alokasi Kesehatan : {pilihan.iloc[0,7]:20,.02f} ")
        st.write(f"Alokasi Pelayanan Umum : {pilihan.iloc[0,2]:20,.02f} ") 
        st.write(f"Alokasi Pariwisata : {pilihan.iloc[0,8]:20,.02f} ")
        st.write(f"Alokasi Ketertiban Umum : {pilihan.iloc[0,3]:20,.02f} ") 
        st.write(f"Alokasi Perlindungan Sosial : {pilihan.iloc[0,10]:20,.02f} ") 
        st.write(f"Alokasi Lingkungan Hidup : {pilihan.iloc[0,5]:20,.02f} ") 
        st.write(f"Alokasi Perumahan : {pilihan.iloc[0,6]:20,.02f} ") 
        st.write(f"Alokasi Ekonomi : {pilihan.iloc[0,4]:20,.02f} ") 
        st.write(f"Total Belanja Daerah : {pilihan.iloc[0,11]:20,.02f} ")
        st.write(f"PDRB : {pilihan.iloc[0,13]*1000000:20,.02f} ")
        st.write(f"IPM : {pilihan.iloc[0,20]:.02f} ")
        
        st.write(f"IPEI : {pilihan.iloc[0,24]:.02f} ")


    with col2:
        #Nilai ambil dari nilai realisasi pemda sesuai filter
        didik = pilihan.iloc[0,9]
        sehat = pilihan.iloc[0,7]
        pelayanan = pilihan.iloc[0,1]
        tertib = pilihan.iloc[0,3]
        eko = pilihan.iloc[0,4]
        lh = pilihan.iloc[0,5]
        perum = pilihan.iloc[0,6]
        wisata = pilihan.iloc[0,8]
        linsos = pilihan.iloc[0,10] 
        totalbelanja = pilihan.iloc[0,11]
        pdrb = pilihan.iloc[0,13]
        ipm = pilihan.iloc[0,20]

        # Create the model
        prob = LpProblem(name="IPEI_LP_Problem",sense=1)
        # Initialize the decision variables
        x1 = LpVariable(name="pendidikan", lowBound=0, cat="Continuous")
        x2 = LpVariable(name="kesehatan", lowBound=0, cat="Continuous")
        x3 = LpVariable(name="pelayanan", lowBound=0, cat="Continuous")
        x4 = LpVariable(name="pariwisata", lowBound=0, cat="Continuous")
        x5 = LpVariable(name="ketertiban", lowBound=0, cat="Continuous")
        x6 = LpVariable(name="perlinsos", lowBound=0, cat="Continuous")
        x7 = LpVariable(name="lingkunganhidup", lowBound=0, cat="Continuous")
        x8 = LpVariable(name="perumahan", lowBound=0, cat="Continuous")
        x9 = LpVariable(name="ekonomi", lowBound=0, cat="Continuous")
            
        # Add the constraints to the model
        prob += (x1 >= p*totalbelanja/100, "pendidikan_constraint")
        prob += (x2 >= k*totalbelanja/100, "kesehatan_constraint")
        prob += (x8 >= l*totalbelanja/100, "perumahan_constraint")
        # Tidak boleh turun lebih dari 5% dan naik lebih dari 10% untuk 6 fungsi lainnya
        prob += (x1 >= 0.95*didik,"pendidikan_bawah_constraint")
        prob += (x1 <= 1.1*didik,"pendidikan_atas_constraint")
        prob += (x2 >= 0.95*sehat,"kesehatan_bawah_constraint")
        prob += (x2 <= 1.1*sehat,"kesehatan_atas_constraint")
        prob += (x3 >= 0.95*pelayanan,"pelayanan_bawah_constraint")
        prob += (x3 <= 1.1*pelayanan,"pelayanan_atas_constraint")        
        prob += (x4 >= 0.95*wisata,"wisata_bawah_constraint")
        prob += (x4 <= 1.1*wisata,"wisata_atas_constraint")
        prob += (x5 >= 0.95*tertib,"tertib_bawah_constraint")
        prob += (x5 <= 1.1*tertib,"tertib_atas_constraint")
        prob += (x6 >= 0.95*linsos,"linsos_bawah_constraint")
        prob += (x6 <= 1.1*linsos,"linsos_atas_constraint")
        prob += (x7 >= 0.95*lh,"lh_bawah_constraint")
        prob += (x7 <= 1.1*lh,"lh_atas_constraint")
        prob += (x3 >= 0.95*,"pelayanan_bawah_constraint")
        prob += (x3 <= 1.1*perum,"perum_atas_constraint")
        prob += (x9 >= 0.95*eko,"eko_bawah_constraint")
        prob += (x9 <= 1.1*eko,"eko_atas_constraint")
        #Total belanja 9 fungsi tidak boleh lebih dari total belanja
        prob += (x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8 + x9 <= totalbelanja, "total_constraint")
        
            
        # Add the objective function to the model
        prob += 0.000000000000118*x1 + 0.000000000000158*x2 - 0.000000000000115*x3 + 0.000000000000145*x4 - 0.000000000000348*x5 - 0.000000000000269*x6 -0.000000000000229*x7 - 0.0000000000000477*x8 + 0.000000000000110*x9 +0.0787967*ipm+ 0.000000000502*pdrb - 0.173271
        # Solve the problem
        st.write(" Berapa Alokasi Belanja Fungsi yang diusulkan?")
        
        if st.button("Klik untuk menghitung!"):
                status = prob.solve()
                
                #
                st.write(f"Alokasi Pendidikan: {pulp.value(x1):20,.02f} ")
                st.write(f"Alokasi Kesehatan: {pulp.value(x2):20,.02f} ")
                st.write(f"Alokasi Pelayanan Umum: {pulp.value(x3):20,.02f} ")
                st.write(f"Alokasi Pariwisata: {pulp.value(x4):20,.02f} ")
                st.write(f"Alokasi Ketertiban Umum: {pulp.value(x5):20,.02f} ")
                st.write(f"Alokasi Perlindungan Sosial: {pulp.value(x6):20,.02f} ")
                st.write(f"Alokasi Lingkungan Hidup: {pulp.value(x7):20,.02f} ")
                st.write(f"Alokasi Perumahan: {pulp.value(x8):20,.02f} ")
                st.write(f"Alokasi Ekonomi: {pulp.value(x9):20,.02f} ")
                st.write(f"Prediksi IPEI : {0.000000000000118*pulp.value(x1) + 0.000000000000158*pulp.value(x2) - 0.000000000000115*pulp.value(x3) + 0.000000000000145*pulp.value(x4) - 0.000000000000348*pulp.value(x5) - 0.000000000000269*pulp.value(x6) -0.000000000000229*pulp.value(x7)- 0.0000000000000477*pulp.value(x8) + 0.000000000000110*pulp.value(x9) +0.0787967*ipm+ 0.000000000502*pdrb - 0.173271:20,.02f}" )
        
        
if __name__=='__main__':
    main()
