import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

def load_data():
    data = pd.read_csv('./dashboard/main_data.csv') 
    return data

ecom_df = load_data()   
ecom_df['order_purchase_timestamp'] = pd.to_datetime(ecom_df['order_purchase_timestamp'], errors='coerce')

def seller_by_states(df):
    ecom_states_df = df.groupby(by="seller_state").seller_id.nunique().reset_index()
    ecom_states_df.rename(columns={
        "seller_id": "seller_state_count"
    }, inplace=True)
    
    return ecom_states_df

def seller_by_city(df):
    ecom_city_df = df.groupby(by="seller_city").seller_id.nunique().reset_index()
    ecom_city_df.rename(columns={
        "seller_id": "seller_city_count"
    }, inplace=True)
    
    return ecom_states_df

def seller_by_city(df):
    ecom_city_df = df.groupby(by="seller_city").seller_id.nunique().reset_index()
    ecom_city_df.rename(columns={
        "seller_id": "seller_city_count"
    }, inplace=True)
    
    return ecom_city_df

def cat_by_states(df):
    impor = df[df['customer_state'] != df['seller_state']]
    impor['year'] = impor['order_purchase_timestamp'].dt.year

    total_sales_import = (
        impor[impor['year'] == 2017]  # Filter untuk tahun 2017
        .groupby(['product_category_name_english'])['order_id']
        .count()
        .reset_index()
    )
    total_sales_import.rename(columns={'order_id': 'total_sales'}, inplace=True)    
    return total_sales_import


def create_rfm_df(df):
    rfm_df = df.groupby(by="customer_state", as_index=False).agg({
        "order_purchase_timestamp": "max",
        "order_id": "nunique",
        "price": "sum"
    })

    rfm_df.columns = ["customer_state", "last_purchase_date", "frequency", "monetary"]
    rfm_df["last_purchase_date"] = pd.to_datetime(rfm_df["last_purchase_date"]).dt.date

    recent_date = df["order_purchase_timestamp"].dt.date.max()
    rfm_df["recency"] = rfm_df["last_purchase_date"].apply(lambda x: (recent_date - x).days)

    rfm_df.drop("last_purchase_date", axis=1, inplace=True)
    return rfm_df

min_date = ecom_df["order_purchase_timestamp"].min()
max_date = ecom_df["order_purchase_timestamp"].max()

with st.sidebar:
    st.caption("@Copyright : ID Dicoding " + str("m320b4kx2039"))

    st.image("https://upload.wikimedia.org/wikipedia/commons/0/05/Flag_of_Brazil.svg")
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    main_df = ecom_df[(ecom_df["order_purchase_timestamp"] >= str(start_date)) & 
                      (ecom_df["order_purchase_timestamp"] <= str(end_date))]
    
    ecom_states_df = seller_by_states(main_df)
    ecom_city_df = seller_by_city(main_df)
    rfm_df = create_rfm_df(main_df)
    total_sales_import = cat_by_states(ecom_df)

st.header('Proyek Analisis Data: E-Commerce Public Dataset')
st.caption('Brazilian E-Commerce Public Dataset by Olist')

tab1, tab2, tab3 = st.tabs(["Teknik Analisis Lanjutan", "Pertanyaan 1", "Pertanyaan 2"])
 
with tab1:    
    st.subheader("Best States Based on RFM Parameters")
    st.write("Period : ", start_date, " - ", end_date)
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))
    colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]
    
    sns.barplot(y="recency", x="customer_state", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
    ax[0].set_ylabel(None)
    ax[0].set_xlabel("Customer state", fontsize=30)
    ax[0].set_title("By Recency (days)", loc="center", fontsize=50)
    ax[0].tick_params(axis='y', labelsize=30)
    ax[0].tick_params(axis='x', labelsize=35)
    
    sns.barplot(y="frequency", x="customer_state", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
    ax[1].set_ylabel(None)
    ax[1].set_xlabel("Customer state", fontsize=30)
    ax[1].set_title("By Frequency", loc="center", fontsize=50)
    ax[1].tick_params(axis='y', labelsize=30)
    ax[1].tick_params(axis='x', labelsize=35)
    
    sns.barplot(y="monetary", x="customer_state", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
    ax[2].set_ylabel(None)
    ax[2].set_xlabel("Customer state", fontsize=30)
    ax[2].set_title("By Monetary", loc="center", fontsize=50)
    ax[2].tick_params(axis='y', labelsize=30)
    ax[2].tick_params(axis='x', labelsize=35)
    
    st.pyplot(fig)
 
with tab2:
    st.caption("How is the distribution of customers from each country and city?")
    st.header("Sellers Demographic")
    st.write("Period : ", start_date, " - ", end_date)
    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots(figsize=(20, 10))
        colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
        sns.barplot(
            y="seller_state", 
            x="seller_state_count",
            data=ecom_states_df.sort_values(by="seller_state_count", ascending=False).head(5),
            palette=colors,
            ax=ax
        )
        ax.set_title("Number of Sellers by State", loc="center", fontsize=50)
        ax.set_ylabel(None)
        ax.set_xlabel(None)
        ax.tick_params(axis='x', labelsize=35)
        ax.tick_params(axis='y', labelsize=30)
        st.pyplot(fig)
    
    with col2:
        fig, ax = plt.subplots(figsize=(20, 10))
        
        colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    
        sns.barplot(
            y="seller_city", 
            x="seller_city_count",
            data=ecom_city_df.sort_values(by="seller_city_count", ascending=False).head(5),
            palette=colors,
            ax=ax
        )
        ax.set_title("Number of Sellers by City", loc="center", fontsize=50)
        ax.set_ylabel(None)
        ax.set_xlabel(None)
        ax.tick_params(axis='x', labelsize=35)
        ax.tick_params(axis='y', labelsize=30)
        st.pyplot(fig)

with tab3:
    st.caption("How do product categories contribute to the total imports of the countries in 2017?")
    st.header("Top 5 Import Product Categories in 2017")

    total_sales_import = total_sales_import.sort_values(by='total_sales', ascending=False).head(5)
    fig, ax = plt.subplots(figsize=(16, 8))

    ax.bar(
        total_sales_import["product_category_name_english"],
        total_sales_import["total_sales"],
        color="#90CAF9"
    )

    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)

    ax.set_xlabel("Product Category", fontsize=20)

    st.pyplot(fig)

