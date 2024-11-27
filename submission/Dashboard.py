# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 16:07:08 2024

@author: Alifio Noerifanza
"""

#'import modules'
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

path1 = Path(__file__).parent / "data/day.csv"
path2 = Path(__file__).parent / "data/hour.csv"

#'Gathering data'
df = pd.read_csv(path1) #import data Day
hour_df= pd.read_csv(path2)

#'assessing data'
dupes=df.duplicated().sum()#nyari duplicate
hour_dupes=hour_df.duplicated().sum()
nan=df.isna().sum()
hour_nan=hour_df.isna().sum()
print(hour_dupes)
print(dupes) #print jumlah duplicates
print(nan)
print(hour_nan)  #print jumlah missing value

#'cleaning data'
hour_df.drop_duplicates(inplace=True)
df.drop_duplicates(inplace=True)
df['dteday'] = pd.to_datetime(df['dteday']) #mengubah data tanggal jadi bisa dibaca
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
new_df = df.dropna() #menghilangkan kolom data yang kosong jika ada
hnew_df = hour_df.dropna()

hnew_df['True Temperature'] = hnew_df['temp'] * 41 #menambah data true temp (celcius)
hnew_df['True Humidity'] = hnew_df['hum'] * 100 #menambah data true humidity (persentase kelembapan)
hnew_df['Felt Temperature'] = hnew_df['atemp'] * 50 #menambah data felt temperature (celcius)
hnew_df['True Wind'] = hnew_df['windspeed'] * 67 #data kecepatan angin (Meter per detik)

new_df['True Temperature'] = new_df['temp'] * 41 #menambah data true temp (celcius)
new_df['True Humidity'] = new_df['hum'] * 100 #menambah data true humidity (persentase kelembapan)
new_df['Felt Temperature'] = new_df['atemp'] * 50 #menambah data felt temperature (celcius)
new_df['True Wind'] = new_df['windspeed'] * 67 #data kecepatan angin (Meter per detik)

#'Exploratory data analysis'
df_cuaca = new_df.loc[:, ["mnth","Felt Temperature","True Humidity", "True Wind", "weathersit" ,"casual", "registered"]] #memilih kolom temp dan cnt dan menjadikannya data frame 2 (df2)
df_weekday = new_df.loc[:, ["holiday","weekday","workingday", "casual", "registered"]]
corrcuaca= df_cuaca.corr() #mencari korelasi antar variable. semakin positif maka berbanding positif, jika negatif berbanding terbalik
corrweekday= df_weekday.corr()
described=new_df.describe()
hdescribed=hnew_df.describe()
based_cuaca= new_df.groupby(by="weathersit").max().reset_index()
df_tempdate = new_df.loc[:, ["dteday", "Felt Temperature"]].reset_index()
#untuk dataset hour
based_hday= hnew_df.loc[:, ["weekday","hr","workingday", "casual", "registered"]]
corrday= based_hday.corr()

print(described)

#"Menampilkan data di Streamlit"
st.title('DASHBOARD DATA BISNIS RENTAL SEPEDA')
 
min_date = new_df["dteday"].min()
max_date = new_df["dteday"].max()

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/5320/5320247.png",width=300,)
    
    start_date, end_date = st.date_input(
       label='Rentang Waktu',min_value=min_date,
       max_value=max_date,
       value=[min_date, max_date])
    
    main_df = new_df[(new_df["dteday"] >= str(start_date)) & 
                (new_df["dteday"] <= str(end_date))]
    hmain_df = hnew_df[(new_df["dteday"] >= str(start_date)) & 
                (hnew_df["dteday"] <= str(end_date))]
    
    text = st.text_area('Kotak Saran')
    if st.button('Kirim'):
        st.write('Saran: ', text)
        
    st.write("Bike-rent© 2024, All rights not reserved yet")
    
    
tab1, tab2, tab3= st.tabs(["Efek Cuaca", "Graf Perilaku pelanggan","Tabel Korelasi dan Statistik"])
 
with tab1:
    st.header("Data Cuaca")
    
    col1, col2= st.columns([4, 1])
    with col1:
        st.header("Grafik")
        #"Plot data cuaca"
        fig2, axes = plt.subplots(3, 1, figsize=(20, 20))

        sns.lineplot(x='dteday', y='Felt Temperature', ax=axes[0],data=main_df)
        axes[0].set_title('Temperatur atas tanggal')
        
        sns.lineplot(x='hr', y='Felt Temperature', ax=axes[1],data=hmain_df)
        axes[1].set_title('jam dan rata-rata temperatur dalam rentang tanggal')
        
        sns.lineplot(x='weathersit', y='cnt', ax=axes[2],data=main_df)
        axes[2].set_title("Cuaca dan Customer")
        
        plt.subplots_adjust(left=0.1,
                            bottom=0.1, 
                            right=0.9, 
                            top=0.8, 
                            wspace=0.4, 
                            hspace=1)
        st.pyplot(fig2.get_figure())
     
    with col2:
        st.header("Catatan")
        st.write("nilai weathersit: \n\n 1= cerah/berawan \n\n 2= berkabut/hujan \n\n 3=hujan besar atau badai es")
     

with tab2:
    st.header("Graf Perilaku Pelanggan")
    with st.container():
        st.subheader("Pelanggan Per Jam")
        #'plot data customer
        fig3, axes = plt.subplots(3, figsize=(20, 20))
        sns.lineplot(x="hr", y='cnt', ax=axes[0],data=hmain_df) #untuk hour --> customer
        axes[0].set_title('jam dan customer total')
    
        sns.lineplot(x="hr", y='casual', ax=axes[1],data=hmain_df) #untuk hour --> casual customer
        axes[1].set_title('jam dan customer kasual')
    
        sns.lineplot(x="hr", y='registered', ax=axes[2],data=hmain_df) #untuk hour --> registered customer
        axes[2].set_title('jam dan customer terdaftar')
        plt.subplots_adjust(left=0.1,
                            bottom=0.1, 
                            right=0.9, 
                            top=0.8, 
                            wspace=0.4, 
                            hspace=1)
        st.pyplot(fig3.get_figure())

    with st.container():
        st.subheader("Pelanggan Harian")
        fig4, axes = plt.subplots(3, figsize=(20, 20))
        sns.lineplot(x="weekday", y='casual', ax=axes[0],data=main_df) #untuk weekday --> casual customer
        axes[0].set_title('Hari ke customer kasual, 0= Hari minggu')
    
        sns.lineplot(x="weekday", y='cnt', ax=axes[1],data=main_df) #untuk weekday --> customer
        axes[1].set_title('Hari ke customer total, 0= Hari minggu')
    
        sns.lineplot(x="weekday", y='registered', ax=axes[2],data=main_df) #untuk weekday --> registered customer
        axes[2].set_title('Hari ke customer yang terdaftar, 0= Hari minggu')
        plt.subplots_adjust(left=0.1,
                            bottom=0.1, 
                            right=0.9, 
                            top=0.8, 
                            wspace=0.4, 
                            hspace=1)
        st.pyplot(fig4.get_figure())

    
    
with tab3:
    st.subheader("Tabel Korelasi dan Statistik Data")
    with st.container():
        col1, col2= st.columns([3.5, 1])
        with col1:
            
            #'memvisualisasikan data korelasi
            fig1, axes = plt.subplots(3, figsize=(20, 20))
        
            sns.heatmap(data=corrcuaca, ax=axes [0], annot=True)
            axes[0].set_title('korelasi cuaca dan customer')
        
            sns.heatmap(data=corrweekday, ax=axes[1], annot=True)
            axes[1].set_title('korelasi hari dan customer')
        
            sns.heatmap(data=corrday, ax=axes[2],annot=True) 
            axes[2].set_title('korelasi antara hari, jam dan customer')
            plt.subplots_adjust(left=0.1,
                                bottom=0.1, 
                                right=0.9, 
                                top=0.8, 
                                wspace=0.4, 
                                hspace=1)
            st.pyplot(fig1.get_figure())

        with col2:
            st.header("Catatan")
            st.write("Korelasi Positif= \n\n -Berbanding positif \n\n Korelasi Negatif= \n\n -Berbanding terbalik")
    with st.container():
        st.subheader("Statistik data Harian")
        st.dataframe(described)
        st.write("Count= Total Data, Mean= Rata-Rata data, Min= Nilai terendah, Max= Nilai tertinggi")
    with st.container():
        st.subheader("Statistik data per Jam")
        st.dataframe(hdescribed)
        st.write("Count= Total Data, Mean= Rata-Rata data, Min= Nilai terendah, Max= Nilai tertinggi")

plt.show()
