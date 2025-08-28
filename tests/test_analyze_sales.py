import unittest
import pandas as pd
import pandas.testing as pdt
from analyzeSales import (
    load_data,
    calculate_total_sales,
    calculate_category_sales,
    calculate_monthly_sales,
    plot_corr_heatmap
)
import matplotlib.pyplot as plt


class TestAnalyzeSales(unittest.TestCase):
    def setUp(self):
        # Sample data mimicking sales data structure
        data = {
            'Product Category': ['A', 'B', 'A'],
            'Quantity': [10, 5, 2],
            'Price per Unit': [20, 30, 20],
            'Date': pd.to_datetime(['2025-01-01', '2025-01-02', '2025-01-03']),
            'Gender': ['Male', 'Female', 'Female'],
            'Age': [25, 30, 35]
        }
        self.df = pd.DataFrame(data)

    def test_calculate_total_sales(self):
        df = calculate_total_sales(self.df.copy())  # copy to avoid test pollution
        calculated = self.df['Quantity'] * self.df['Price per Unit']
        calculated.name = 'Total Sales'  # match column for assert
        pdt.assert_series_equal(df['Total Sales'], calculated)

    def test_calculate_category_sales(self):
        df_with_sales = calculate_total_sales(self.df.copy())
        expected = pd.DataFrame({
            'Product Category': ['A', 'B'],
            'Total Sales': [240, 150]
        }).sort_values(by='Total Sales', ascending=False).reset_index(drop=True)

        result = calculate_category_sales(df_with_sales).reset_index(drop=True)
        pdt.assert_frame_equal(result[['Product Category', 'Total Sales']], expected)

    def test_calculate_monthly_sales(self):
        df_with_sales = calculate_total_sales(self.df.copy())
        monthly_sales = calculate_monthly_sales(df_with_sales)
        self.assertIn('Pct_Change', monthly_sales.columns)
        self.assertIn('Month', monthly_sales.columns)
        self.assertIn('Total Sales', monthly_sales.columns)
        self.assertEqual(len(monthly_sales), len(self.df['Date'].dt.to_period('M').unique()))

    def test_plot_corr_heatmap_runs(self):
        df_with_sales = calculate_total_sales(self.df.copy())
        fig, ax = plt.subplots()
        try:
            plot_corr_heatmap(df_with_sales, ax=ax)
        except Exception as e:
            self.fail(f"plot_corr_heatmap raised an exception: {e}")

if __name__ == '__main__':
    unittest.main()


# import unittest
# import pandas as pd
# import pandas.testing as pdt
# from analyzeSales import plot_corr_heatmap, cat_sales, monthly_sales 

# class TestAnalyzeSales(unittest.TestCase):
#     def setUp(self):
#         #Creating sample dataFrame mimicing sales data structure
#         data = {
#             'Product Category': ['A','B','A'],
#             'Quantity': [10, 5, 2],
#             'Price per Unit':[20,30,20],
#             'Total Sales':[200,150,40],
#             'Date' : pd.to_datetime(['2025-01-01', '2025-01-02', '2025-01-03']),
#             'Gender':['Male', 'Female', 'Female'],
#             'Age':[25,30,35]

#         }
#         self.df = pd.DataFrame(data)
#         self.df['Total Sales'] = self.df['Quantity'] * self.df['Price per Unit']

#     def test_total_sales_calculation(self):
#         self.df['Calculated Total Sales'] = self.df['Quantity'] * self.df['Price per Unit']
#         pdt.assert_series_equal(self.df['Total Sales'], self.df['Calculated Total Sales'])

#     def test_cat_sales_aggregation(self):
#        # cat_sales = self.df.groupby('Product')['Total Sales'].sum().reset_index()
#         expected = pd.DataFrame({
#             'Product Category': ['A', 'B'],
#             'Total Sales': [240, 150]
#         }).sort_values(by='Total Sales', ascending=False).reset_index(drop=True)

#         result = calculate_category_sales(self.df).reset_index(drop=True)
#         pdt.assert_frame_equal(result[['Product Category', 'Total Sales']], expected)
#         #pdt.assert_frame_equal(cat_sales, expected)

#     def test_plot_corr_heatmap_runs(self):
#         # ensuring the plotting function does not raise error
#         import matplotlib.pyplot as plt
#         fig,ax = plt.subplots()
#         try:
#             plot_corr_heatmap(ax=ax)
#         except Exception as e:
#             self.fail(f"plot_corr_heatmap raised an exception: {e}")
        
# if __name__ == '__main__':
#     unittest.main()