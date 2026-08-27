# Product-Segmentation-UnSupervised-ML

Product segmentation is the process of grouping products with similar sales, revenue, customer demand, and purchasing characteristics. This project uses unsupervised machine learning techniques to identify meaningful product groups and generate actionable business insights. The project analyzes retail transaction data and segments products based on their performance and behavior. Special consideration is given to returns and negative transactions, allowing the analysis to focus on Net Revenue rather than only gross sales.

Retail businesses often manage thousands of products, making it difficult to understand which products are:

* High-performing products
* High-revenue products
* Frequently purchased products
* Low-performing products
* Products with high return rates
* Products requiring promotional attention
* Products suitable for inventory optimization

These segments can help businesses make better decisions regarding:

1. Inventory management
2. Product promotion
3. Pricing strategies
4. Product portfolio optimization
5. Return reduction
6. Revenue growth

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

:/Project Workflow

    Raw Retail Dataset
            │
            ▼
    Data Cleaning
            │
            ▼
    Exploratory Data Analysis
            │
            ▼
    Feature Engineering
            │
            ▼
    Product-Level Aggregation
            │
            ▼
    Feature Scaling
            │
            ▼
    Clustering Models
            │
     ┌──────┼───────────┬───────────┐
     ▼      ▼           ▼           ▼
    K-Means GMM       DBSCAN   Hierarchical
     │
     ▼
    Cluster Evaluation
     │
     ▼
    Product Segment Analysis
     │
     ▼
    Business Recommendations
     │
     ▼
    Streamlit Application

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

:/Data Cleaning

The following steps were performed during data preprocessing:

1. Removed duplicate records.
2. Handled missing values.
3. Converted [InvoiceDate] to datetime format.
4. Removed invalid product records where required.
5. Checked negative quantities and prices.
6. Identified return transactions.
7. Created revenue-related features.
8. Handled extreme values and outliers where necessary.

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
:/ Feature Engineering

Several product-level features were created to understand product performance.

    1. Total Revenue
    
    2. Net Revenue
    
    3. Total Sales Quantity
    
    4. Total Revenue Quantity
    
    5. Total Orders
    
    6. Unique Customers 
    
    7. Average Price
    
    8. Return Rate
    
    9. Sales Velocity
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Machine Learning Models

This project compares multiple clustering algorithms.

1. K-Means Clustering

K-Means groups products based on similarity in numerical features.
The optimal number of clusters was evaluated using metrics such as Inertia, silhouettes score and db score.

2. Gaussian Mixture Model (GMM)

GMM is a probabilistic clustering algorithm that assigns probabilities of belonging to different clusters. Not that useful in this project.

3. DBSCAN

DBSCAN groups products based on density.

4. Hierarchical Clustering

Hierarchical clustering creates a tree-like structure of product similarity.
Useful for understanding relationships between clusters

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

💡 Key Business Insights

Basically the model differentiates the whole data in 4 clusters.
1. High Value but High Return Products
2. High Value and High Velocity Products
3. Fast Moving and Low Return Products
4. Low Value and Slow Moving Products

This project helps answer questions such as:

-Which products generate the highest net revenue?
-Which products are sold most frequently?
-Which products have high customer demand?
-Which products have high return rates?
-Which products contribute negatively to revenue?
-Which products should receive additional marketing?
-Which products may require inventory reduction?
-Which products should be investigated for quality issues?
-Which product segments have the highest growth potential?

