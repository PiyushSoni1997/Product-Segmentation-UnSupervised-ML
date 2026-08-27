import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
import joblib
import plotly.graph_objects as go
import matplotlib.pyplot as plt


#---------Page Config

st.set_page_config(page_title = "Product Segmentation", page_icon="📦", layout="wide", initial_sidebar_state="expanded")


#-------Load the product_df data

@st.cache_data
def load_data():

    df = pd.read_csv("Product_df.csv")

    return df

@st.cache_resource
def load_model():

    scaler = joblib.load("scaler.pkl")
    model = joblib.load("Kmeans.pkl")

    return scaler, model


try:

    df = load_data()
    scaler, model = load_model()

except Exception as e:

    st.error(f"Error loading file {e}")
    st.info("Make Sure above files exists in the Product Segmentation Folder")
    st.stop()




#--------Sidebar Settings

st.sidebar.title("📦 Product Segmentation")

page = st.sidebar.radio("Page Navigation", ["Products Overview", "Product Segmentation", "Return Analysis", "Product Explorer", "Business Recommendations"])


# KPIs from Product table

Gross_Revenue = df["TotalRevenue"].sum()
Total_Products = df["StockCode"].nunique()
Sold_Quantity = df["TotalSalesQuantity"].sum()
Return_Quantity = df["TotalReturnQuantity"].sum()
Return_Rate = df["ReturnRate"].mean()
Net_Revenue = df["TotalNetRevenue"].sum()



#_____________Pag1 Overview

if page == "Products Overview":

    st.title("Product Segmentation and Return Analysis", text_alignment="center")

    st.markdown("Product Segmentation KPIs"   
    )

    col1,col2,col3 = st.columns(3)

    with col1:
        st.metric("Total Products", f"{Total_Products}")

    with col2:
        st.metric("Gross Revenue", f"{Gross_Revenue}")

    with col3:
        st.metric("Net Revenue", f"{Net_Revenue}")


    st.markdown("------")

        

    col1,col2,col3 = st.columns(3)

    with col1:
        st.metric("Units Sold", f"{Sold_Quantity}")

    with col2:
        st.metric("Units Returned", f"{Return_Quantity}")

    with col3:
        st.metric("Return Rate", f"{Return_Rate:.2f}")



    st.divider()
    st.divider()
    

    #####Some_graphs

    col1, col2 = st.columns(2)

    with col1:

        fig,ax = plt.subplots(figsize=(8,6))
        sns.histplot(data = df, x = "ReturnRate", bins = 40, kde=True)
        ax.set_title("ReturnRate Distribution")
        st.pyplot(fig)


    with col2:
        fig,ax = plt.subplots(figsize=(8,6))
        sns.histplot(data = df, x = "TotalRevenue", bins = 30, kde=True)
        ax.set_title("TotalRevenue Distribution")
        st.pyplot(fig)




#----------First Page Done

elif page == "Product Segmentation":

    st.title("Product Segmentation")

    clusters = sorted(df["KMeansClusters"].unique().tolist())

    selected_cluster = st.selectbox("KMeans Clusters", ["ALL"] + clusters)

    if selected_cluster == "ALL":
        cluster_df = df.copy()

    else:
        cluster_df = df[df["KMeansClusters"] == selected_cluster]


#Cluster KPIs

    col1,col2,col3 = st.columns(3)

    with col1:

        st.metric("Products", f"{cluster_df["StockCode"].nunique()}")

    with col2:

        st.metric("Revenue", f"{cluster_df["TotalRevenue"].sum()}")

    with col3:

        st.metric("Net Revenue", f"{cluster_df["TotalNetRevenue"].sum().round(2)}")


    col1,col2,col3 = st.columns(3)

    with col1:

        st.metric("Units Sold", f"{cluster_df["TotalSalesQuantity"].sum()}")

    with col2:

        st.metric("Units Returned", f"{cluster_df["TotalReturnQuantity"].sum()}")

    with col3:

        st.metric("ReturnRate", f"{cluster_df["ReturnRate"].mean().round(2)}")



    st.divider()
    st.divider()


    ###Graphs

    col1= st.columns(1)[0]

    with col1:

        fig = px.bar(cluster_df, x = "TotalMonths", y="TotalSalesQuantity", color = "TotalMonths", color_discrete_sequence=px.colors.qualitative.Pastel, title="Months Vs Quantity")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)


    col1= st.columns(1)[0]


    with col1:

        fig = px.scatter(
            cluster_df,
            x="TotalRevenue",
            y="ReturnRate",
            size="TotalSalesQuantity",
            color="KMeansClusters",
            hover_data=[
                "StockCode",
                "TotalNetRevenue",
                "TotalReturnQuantity"
            ],
            title="Revenue vs Return Rate"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )



    st.subheader("Cluster Table Dataframe")

    st.dataframe(cluster_df)


elif page == "Return Analysis":

    st.title("↩️ Product Return Analysis")

    st.markdown(
        """
        Returns are treated as a separate business signal rather
        than simply deleting negative-quantity transactions.
        """
    )

    st.markdown("---")


    # Return KPIs

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Returned Quantity",
            f"{Return_Quantity:,.0f}"
        )

    with col2:

        st.metric(
            "Return Value",
            f"£{df["TotalReturnValue"].sum():,.0f}"
        )

    with col3:

        st.metric(
            "Average Return Rate",
            f"{Return_Rate:.2f}%"
        )

    with col4:

        high_return_products = (
            df["ReturnRate"] > 0.1
        ).sum()

        st.metric(
            "Products >10% Return Rate",
            f"{high_return_products:,}"
        )



    st.divider()



    #TOP Returned products

    st.subheader("TOP RETURNED PRODUCTS")
    top_returns = df.sort_values("TotalReturnQuantity", ascending = False).head(20)

    st.dataframe(top_returns)

    fig = px.bar(top_returns, x= "Description", y = "TotalReturnQuantity",
        title="Top 20 Returned Products")

    st.plotly_chart(
        fig,
        use_container_width=True
    )   

elif page == "Product Explorer":

    st.title("Product Information")

    product_list = sorted(df["Description"].unique().tolist())

    product_select = st.selectbox("Select Product type", product_list)

    product = df[df["Description"] == product_select]

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Gross Revenue",
            f"£{product['TotalRevenue'].sum():,.2f}"
        )

    with col2:

        st.metric(
            "Net Revenue",
            f"£{product['TotalNetRevenue'].sum():,.2f}"
        )

    with col3:

        st.metric(
            "Quantity Sold",
            f"{product['TotalSalesQuantity'].sum():,.0f}"
        )

    with col4:

        st.metric(
            "Return Rate",
            f"{product['ReturnRate'].sum():.2f}%"
        )


    st.markdown("---")


    col1, col2 = st.columns(2)

    with col1:

        st.write("### Sales Information")

        st.write(
            f"**Orders:** {product['TotalOrders'].sum():,.0f}"
        )

        st.write(
            f"**Customers:** {product['TotalCustomers'].sum():,.0f}"
        )

        st.write(
            f"**Average Price:** £{product['AveragePrice'].sum():,.2f}"
        )

        st.write(
            f"**Sales Velocity:** "
            f"{product['SalesVelocity'].sum():.2f}"
        )


    with col2:

        st.write("### Return Information")

        st.write(
            f"**Returned Quantity:** "
            f"{product['TotalReturnQuantity'].sum():,.0f}"
        )

        st.write(
            f"**Return Rate:** "
            f"{product['ReturnRate'].sum():.2f}%"
        )


    # Cluster

    if "KMeansClusters" in product.columns:

        st.markdown("---")

        st.subheader("🤖 ML Segment")

        st.success(
            f"Cluster: {product['KMeansClusters'].sum()}"
        )


    # Negative revenue warning

    if product["TotalNetRevenue"].sum() < 0:

        st.warning(
            """
            ⚠️ This product has negative Net Revenue.

            This indicates that recorded return/cancellation
            value exceeds recorded positive sales revenue
            for this product in the dataset.
            """
        )


# =========================================================
# BUSINESS RECOMMENDATIONS
# =========================================================

elif page == "Business Recommendations":

    st.title("Business Recommendation")

    clusters = sorted(df["KMeansClusters"].unique().tolist())
    
    selected_cluster = st.selectbox("KMeans Clusters", ["ALL"] + clusters)
    
    if selected_cluster == "ALL":
            cluster_df = df.copy()
    
    else:
            cluster_df = df[df["KMeansClusters"] == selected_cluster]


    st.dataframe(cluster_df)



    if selected_cluster == 0:

        st.write(
            '''🔴 High-Value but High-Return Products

            This is an interesting cluster.

            650 products
            ₹1.28M revenue
            241K units sold
            53,989 orders
            ₹1,968 average revenue/product
            83 average orders/product
            8% return rate
            Sales velocity: 1.47

            The 8% return rate is the highest among all clusters.

            Business insight

            These products generate substantial revenue, but their return behavior is concerning.

            This could indicate:

            Product quality issues
            Customer dissatisfaction
            Incorrect product descriptions
            Product expectations not matching reality
            Packaging/shipping problems
            Business recommendations

            Don't immediately discontinue these products.

            Instead:

            Investigate why customers are returning them.

            Compare these products by:

            Return reason
            Country
            Customer type
            Product category
            Price
            Order size

            This could potentially become a separate return-risk analysis'''
                    )


    elif selected_cluster == 1:

        st.write(
        '''🔴 Low-Value / Slow-Moving Products

        This is your weakest segment.

        1,134 products
        Only ₹147K revenue
        32K units
        7 average orders/product
        ₹129.90 average revenue/product
        Sales velocity = 1.08
        3% return rate

        These products represent a large portion of your product portfolio but contribute relatively little revenue.

        Business insight

        This is potentially an underperforming / long-tail product segment.

        Having 1,134 products generating only ~₹147K suggests that maintaining inventory for all of these products may not be efficient.

        Business recommendations

        Consider:

        Reducing inventory
        Promotions/discounts
        Bundling
        Removing consistently poor performers
        Keeping them only if they serve a strategic purpose
        Investigating whether some are niche products'''
                    )


    elif selected_cluster == 2:

        st.write(
            '''🔴 Fast-Moving / Low-Return Products

            This cluster is particularly interesting.

            1,144 products
            ₹1.06M revenue
            952K units sold
            70,676 orders
            ₹924 average revenue/product
            61.8 average orders/product
            Almost 0% return rate
            Sales velocity = 4.17

            These products sell large quantities but generate less revenue per product than Cluster 3.

            Business insight

            These are your volume drivers.

            Customers buy them frequently and they have very low return rates.

            Business recommendations
            Maintain sufficient inventory.
            Use these products for promotions.
            Bundle them with Cluster 3 products.
            Use them to increase basket size.
            Focus on efficient procurement because margins may depend heavily on volume.

            A useful business strategy would be:

            Cluster 3 drives value, Cluster 2 drives volume.'''
                    )


    else:

        st.write(
            '''🔴 High-Value / High-Velocity Products

            This is clearly your most important cluster.

            988 products
            ₹6.40M revenue
            ~3.94M units sold
            264K orders
            ₹6,482 average revenue/product
            267 average orders/product
            177.5 sales velocity
            Only ~2% return rate
            Business insight

            These are your star products.

            They generate the majority of revenue while maintaining a relatively low return rate. The extremely high sales velocity suggests strong and consistent demand.

            Business recommendations
            Maintain high inventory availability.
            Prioritize these products in forecasting.
            Avoid stockouts.
            Give them prominent placement.
            Consider bundling/cross-selling.
            Monitor inventory turnover closely.
            Investigate whether some can support premium pricing.

            This cluster should receive the highest operational priority.'''
                    )
            