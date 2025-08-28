import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def load_data(file_path):
    df = pd.read_csv(file_path)
    return df


def calculate_total_sales(df):
    if 'Total Sales' not in df.columns:
        df['Total Sales'] = df['Quantity'] * df['Price per Unit']
    return df


def calculate_category_sales(df):
    cat_sales = df.groupby('Product Category')['Total Sales'].sum().reset_index()
    cat_sales['Sales_Percentage'] = (cat_sales['Total Sales'] / cat_sales['Total Sales'].sum()) * 100
    return cat_sales.sort_values(by='Total Sales', ascending=False)


def calculate_monthly_sales(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.to_period('M')
    monthly_sales = df.groupby('Month')['Total Sales'].sum().reset_index()
    monthly_sales['Total Sales'] = monthly_sales['Total Sales'].astype(float)
    monthly_sales['Pct_Change'] = monthly_sales['Total Sales'].pct_change() * 100
    monthly_sales['Month'] = monthly_sales['Month'].dt.to_timestamp()
    return monthly_sales


def plot_category_sales(cat_sales):
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(data=cat_sales, x='Product Category', y='Total Sales')
    plt.title('Total sales by product category')
    for p in ax.patches:
        ax.annotate(f'{p.get_height():,.0f}', (p.get_x() + p.get_width() / 2, p.get_height()), ha='center', va='bottom')
    plt.tight_layout()
    plt.show()


def plot_monthly_sales(monthly_sales):
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=monthly_sales, x=monthly_sales['Month'].astype(str), y='Total Sales')
    plt.xticks(rotation=45)
    plt.title('Monthly Sales Percentage Change')
    plt.xlabel('Month')
    plt.ylabel('Percentage Change (%)')
    plt.tight_layout()
    plt.show()


def plot_gender_sales(df):
    gender = df.groupby('Gender')['Total Sales'].sum().reset_index()
    plt.figure(figsize=(6, 4))
    ax = sns.barplot(data=gender, x='Gender', y='Total Sales')
    plt.title('Sales by Gender')
    plt.ylabel('Total Sales')
    for p in ax.patches:
        ax.annotate(f'{p.get_height():,.0f}', (p.get_x() + p.get_width() / 2, p.get_height()), ha='center', va='bottom')
    plt.tight_layout()
    plt.show()


def plot_price_sales(df):
    price_bins = [0, 50, 100, 300, 500, 1000]
    price_labels = ['0-50', '51-100', '101-300', '301-500', '500+']
    df['Price_Range'] = pd.cut(df['Price per Unit'], bins=price_bins, labels=price_labels)
    price_sales = df.groupby('Price_Range', observed=True)['Total Sales'].sum().reset_index()
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(data=price_sales, x='Price_Range', y='Total Sales')
    plt.title('Sales by Price Per Unit Range')
    plt.xlabel('Price Range')
    plt.ylabel('Total Sales')
    for p in ax.patches:
        ax.annotate(f'{p.get_height():,.0f}', (p.get_x() + p.get_width() / 2, p.get_height()), ha='center', va='bottom')
    plt.tight_layout()
    plt.show()


def plot_corr_heatmap(df, ax=None):
    corr = df[['Quantity', 'Price per Unit', 'Total Sales', 'Age']].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", center=0, square=True, ax=ax)
    if ax:
        ax.set_title('Correlation Heatmap', fontsize=10)


def main():
    file_path = '/Users/shreya/Desktop/SalesAnalytics/Dataset/Retail_sales_DS_Clean.csv'
    df = load_data(file_path)

    print("Data Summary : ")
    print(df.info())

    print("\nFirst 5 Rows : ")
    print(df.head())

    df = calculate_total_sales(df)
    cat_sales = calculate_category_sales(df)
    print("\nSales by Product Category with Percentage Contribution:")
    print(cat_sales)

    monthly_sales = calculate_monthly_sales(df)
    print("\nMonthly sales with percentage change: ")
    print(monthly_sales[['Month', 'Total Sales', 'Pct_Change']])

    plot_category_sales(cat_sales)
    plot_monthly_sales(monthly_sales)
    plot_gender_sales(df)
    plot_price_sales(df)

    fig, axs = plt.subplots(2, 3, figsize=(15, 15), gridspec_kw={'wspace': 0.4, 'hspace': 0.5})
    axs = axs.flatten()

    sns.barplot(data=cat_sales, x='Product Category', y='Total Sales', ax=axs[0])
    axs[0].set_title('Total Sales by Product Category', fontsize=10)
    for p in axs[0].patches:
        axs[0].annotate(f'{p.get_height():,.0f}', (p.get_x() + p.get_width() / 2, p.get_height()), ha='center', va='bottom',
                       fontsize=8)
    axs[0].tick_params(axis='x', rotation=45, labelsize=8)
    axs[0].tick_params(axis='y', labelsize=8)
    axs[0].set_ylim(0, axs[0].get_ylim()[1] * 1.1)

    sns.lineplot(data=monthly_sales, x='Month', y='Total Sales', marker='o', ax=axs[1])
    axs[1].set_title('Monthly Sales Trend', fontsize=10)
    axs[1].tick_params(axis='x', rotation=45, labelsize=8)
    axs[1].tick_params(axis='y', labelsize=7)
    axs[1].set_ylim(0, axs[1].get_ylim()[1] * 1.1)

    gender = df.groupby('Gender')['Total Sales'].sum().reset_index()
    sns.barplot(data=gender, x='Gender', y='Total Sales', ax=axs[2])
    axs[2].set_title('Sales by Gender', fontsize=10)
    for p in axs[2].patches:
        axs[2].annotate(f'{p.get_height():,.0f}', (p.get_x() + p.get_width() / 2, p.get_height()), ha='center', va='bottom')
    axs[2].tick_params(axis='x', rotation=45, labelsize=8)
    axs[2].tick_params(axis='y', labelsize=7)
    axs[2].set_ylim(0, axs[2].get_ylim()[1] * 1.1)

    price_bins = [0, 50, 100, 300, 500, 1000]
    price_labels = ['0-50', '51-100', '101-300', '301-500', '500+']
    df['Price_Range'] = pd.cut(df['Price per Unit'], bins=price_bins, labels=price_labels)
    price_sales = df.groupby('Price_Range', observed=True)['Total Sales'].sum().reset_index()
    sns.barplot(data=price_sales, x='Price_Range', y='Total Sales', ax=axs[3])
    axs[3].set_title('Sales by Price Range', fontsize=10)
    for p in axs[3].patches:
        axs[3].annotate(f'{p.get_height():,.0f}', (p.get_x() + p.get_width() / 2, p.get_height()), ha='center', va='bottom')
    axs[3].tick_params(axis='x', rotation=45, labelsize=8)
    axs[3].tick_params(axis='y', labelsize=7)
    axs[3].set_ylim(0, axs[3].get_ylim()[1] * 1.1)

    plot_corr_heatmap(df, ax=axs[4])

    fig.delaxes(axs[5])  # remove unused plot
    fig.tight_layout(pad=2.0, w_pad=20.0, h_pad=10.0)
    plt.show()


if __name__ == '__main__':
    main()





#previous code before modularization
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns

# #Loading the CSV file
# def load_data():
#     df = pd.read_csv('/Users/shreya/Desktop/SalesAnalytics/Dataset/Retail_sales_DS_Clean.csv')
#     return df
# #Basic info
# df = load_data()
# print("Data Summary : ")
# print(df.info())

# #Preview Data
# print("\nFirst 5 Rows : ")
# print(df.head())

# #Ensuring total sales column exists
# if 'Total Sales' not in df.columns:
#     df['Total Sales'] = df['Quantity']* df['Price per Unit']

# #Aggregating sales by product Category
# cat_sales = df.groupby('Product Category')['Total Sales'].sum().reset_index()


# #Calculate sales percentagee contribution by category
# cat_sales['Sales_Percentage']=(cat_sales['Total Sales']/
#                                cat_sales['Total Sales'].sum())*100
# cat_sales=cat_sales.sort_values(by='Total Sales', ascending = False)
# print("\nSales by Product Category with Percentage Contribution:")
# print(cat_sales)

# #converting date column to datetime type
# df['Date']=pd.to_datetime(df['Date'])


# #aggregating sales by month
# df['Month'] = df['Date'].dt.to_period('M')
# monthly_sales = df.groupby('Month')['Total Sales'].sum().reset_index()

# #calculating month-over-month percentage change in sales
# monthly_sales['Total Sales'] = monthly_sales['Total Sales'].astype(float)
# monthly_sales['Pct_Change'] = monthly_sales['Total Sales'].pct_change() * 100
# monthly_sales['Month']= monthly_sales['Month'].dt.to_timestamp()

# print("\nMonthly sales with percentage change: ")
# print(monthly_sales[['Month','Total Sales','Pct_Change']])


# #Visualization : Sales by Product Category
# plt.figure(figsize=(10,6))
# ax=sns.barplot(data=cat_sales, x='Product Category',y='Total Sales')
# plt.title('Total sales by product category')
# #Adding values on top of bars

# for p in ax.patches:
#     ax.annotate(f'{p.get_height():,.0f}',(p.get_x() + p.get_width()/2, p.get_height()), ha = 'center',va='bottom')
# plt.tight_layout()
# plt.show()

# #Visualization : Monthly sales trend
# plt.figure(figsize=(12,6))
# sns.lineplot(data=monthly_sales, x=monthly_sales['Month'].astype(str), y='Total Sales')
# plt.xticks(rotation=45)
# plt.title('Monthly Sales Percentage Change')
# plt.xlabel('Month')
# plt.ylabel('Percetage Change (%)')
# plt.tight_layout()
# plt.show()

# #customer Demographics: Sales By Gender
# gender = df.groupby('Gender')['Total Sales'].sum().reset_index()
# plt.figure(figsize=(6,4))
# ax = sns.barplot(data=gender,x='Gender', y='Total Sales')
# plt.title('Sales by Gender')
# plt.ylabel('Total Sales')
# for p in ax.patches:
#     ax.annotate(f"{p.get_height():,.0f}",(p.get_x()+ p.get_width()/2,p.get_height()),ha='center',va='bottom')
# plt.tight_layout()
# plt.show()

# # price per unit analysis : Bin prices and analyse sales distribution
# price_bins = [0,50,100,300,500,1000]
# price_labels = ['0-50','51-100','101-300','301-500','500+']
# df['Price_Range'] = pd.cut(df['Price per Unit'], bins=price_bins,labels=price_labels)
# price_sales=df.groupby('Price_Range',observed=True)['Total Sales'].sum().reset_index()
# plt.figure(figsize=(10,6))
# ax=sns.barplot(data=price_sales,x='Price_Range',y='Total Sales')
# plt.title('Sales by Price Per Unit Range')
# plt.xlabel('Price Range')
# plt.ylabel('Total Sales')
# for p in ax.patches:
#     ax.annotate(f"{p.get_height():,.0f}", (p.get_x() + p.get_width()/2,p.get_height()), ha='center',va='bottom')
# plt.tight_layout()
# plt.show()

# # Correlation Heatmap among numerical Variables

# corr=df[['Quantity','Price per Unit','Total Sales','Age']].corr()
# plt.figure(figsize=(10,8))
# sns.heatmap(corr,annot=True,cmap='coolwarm',fmt=".2f")
# plt.title('Correlation Heatmap')
# plt.tight_layout()
# plt.show()


# # Assuming these DataFrames are already prepared from your analysis:
# # category_sales, monthly_sales, gender_sales, age_group_sales, price_sales

# corr_matrix=df[['Quantity','Price per Unit','Total Sales','Age']].corr()

# #define function to plot correlation heatmap on given axes
# def plot_corr_heatmap(ax=None):
#     sns.heatmap(corr_matrix,annot=True,cmap='coolwarm',center=0,square=True,ax=ax)
#     if ax:
#         ax.set_title('Correlation Heatmap',fontsize=10)

# fig, axs = plt.subplots(2,3, figsize=(15,15) ,gridspec_kw={'wspace':0.4,'hspace':0.5}) #creating 3 rows, 2column grid
# fig.subplots_adjust(wspace = 15,hspace=10) #increase the value to addd more vertical space

# axs = axs.flatten() #flattening to 1D array for easier indexing 


# #1. Sales by product category
# sns.barplot(data=cat_sales,x='Product Category',y='Total Sales', ax=axs[0])
# axs[0].set_title('Total Sales by Product Category',fontsize=10)
# for p in axs[0].patches:
#     axs[0].annotate(f'{p.get_height():,.0f}'
#     ,(p.get_x()+ p.get_width()/2,p.get_height()),
#     ha='center',
#     va='bottom',fontsize=8)
# axs[0].tick_params(axis='x',rotation=45,labelsize=8)
# axs[0].tick_params(axis='y',labelsize=8)
# top_limit = axs[0].get_ylim()[1]
# axs[0].set_ylim(0, top_limit * 1.1)

# #2. Monthly Sales Trend
# sns.lineplot(data=monthly_sales,x='Month',y='Total Sales',marker='o',ax=axs[1])
# axs[1].set_title('Monthy Sales Trend',fontsize=10)
# axs[1].tick_params(axis='x',rotation=45,labelsize=8)
# axs[1].tick_params(axis='y',labelsize=7)
# top_limit = axs[1].get_ylim()[1]
# axs[1].set_ylim(0, top_limit * 1.1)

# #3. Sales by Gender
# sns.barplot(data=gender,x='Gender',y='Total Sales',ax=axs[2])
# axs[2].set_title('Sales by Gender',fontsize=10)
# for p in axs[2].patches:
#     axs[2].annotate(f'{p.get_height():,.0f}',(p.get_x()+p.get_width()/2,p.get_height()),ha='center',va='bottom')
# axs[2].tick_params(axis='x',rotation=45,labelsize=8)
# axs[2].tick_params(axis='y',labelsize=7)
# top_limit = axs[2].get_ylim()[1]
# axs[2].set_ylim(0, top_limit * 1.1)

# #4. Sales by Price Range
# sns.barplot(data=price_sales,x='Price_Range',y='Total Sales',ax=axs[3])
# axs[3].set_title('Sales by Price Range',fontsize=10)
# for p in axs[3].patches:
#     axs[3].annotate(f'{p.get_height():,.0f}',(p.get_x()+p.get_width()/2,p.get_height()),ha='center',va='bottom')
# axs[3].tick_params(axis='x',rotation=45,labelsize=8)
# axs[3].tick_params(axis='y',labelsize=7)
# top_limit = axs[3].get_ylim()[1]
# axs[3].set_ylim(0, top_limit * 1.1)


# #5. Correlation Heatmap
# plot_corr_heatmap(ax=axs[4])

# #6. remove the unused 6th subplot (optional)

# fig.delaxes(axs[5])
# '''
# fig.delaxes(axs[6])
# fig.delaxes(axs[7])
# fig.delaxes(axs[8])
# #fig.delaxes(axs[9])
# '''

# fig.tight_layout(pad=2.0,w_pad=20.0,h_pad=10.0)
# plt.show()