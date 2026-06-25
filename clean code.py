#!/usr/bin/env python3
"""
Text to Python Conversion
Generated: 2026-06-25T12:37:47.066Z
Total Lines: 185
"""

def process_text():
    """
    Process and analyze text data
    Returns: dictionary with text data and metadata
    """
    text_lines = [
    "import pandas as pd",
    "import numpy as np",
    "file_path = r\"C:\\Users\\11931\\Downloads\\python_cleaning_practice_200_rows.xlsx\"",
    "df = pd.read_excel(file_path, sheet_name=\"dirty_sales_data\", engine=\"openpyxl\")",
    "df_copy = df.copy()",
    "# Clean Order_ID",
    "df_copy['Order_ID'] = (",
    "    df_copy['Order_ID']",
    "    .astype(str)",
    "    .str.strip()",
    "    .str.upper()",
    "    .str.replace('-', '', regex=False)",
    ")",
    "df_copy = df_copy.drop_duplicates(subset='Order_ID', keep='first')",
    "# Clean Customer_Name",
    "df_copy['Customer_Name'] = (",
    "    df_copy['Customer_Name']",
    "    .astype(str)",
    "    .str.strip()",
    "    .str.title()",
    ")",
    "df_copy['Customer_Name'] = df_copy['Customer_Name'].replace('Nan', np.nan)",
    "#Clean Age",
    "df_copy['Age'] = pd.to_numeric(df_copy['Age'], errors='coerce')",
    "df_copy.loc[",
    "    (df_copy['Age'] < 18) | (df_copy['Age'] > 100),",
    "    'Age'",
    "] = np.nan",
    "median_age = df_copy['Age'].median()",
    "df_copy['Age'] = df_copy['Age'].fillna(median_age)",
    "df_copy['Age'] = df_copy['Age'].astype(int)",
    "#Clean email",
    "df_copy['Email'] = df_copy['Email'].astype(str).str.strip().str.lower()",
    "df_copy['Email'] = df_copy['Email'].replace(",
    "    ['nan', 'none', '', 'missing_email'],",
    "    np.nan",
    ")",
    "df_copy.loc[",
    "    ~(",
    "        df_copy['Email'].str.contains('@', na=False) &",
    "        df_copy['Email'].str.contains('.', regex=False, na=False)",
    "    ),",
    "    'Email'",
    "] = np.nan",
    "#Clean phone",
    "df_copy['Phone'] = (",
    "    df_copy['Phone']",
    "    .astype(str)",
    "    .str.strip()",
    "    .str.replace(r'\\D', '', regex=True)",
    ")",
    "df_copy['Phone'] = df_copy['Phone'].str.replace(r'^60', '0', regex=True)",
    "valid_phone = df_copy['Phone'].str.match(r'^01\\d{8,9}$', na=False)",
    "df_copy.loc[~valid_phone, 'Phone'] = np.nan",
    "#Clean city",
    "df_copy['City'] = (",
    "    df_copy['City']",
    "    .astype(str)",
    "    .str.strip()",
    "    .str.lower()",
    "    .str.title()",
    ")",
    "df_copy['City'] = df_copy['City'].replace('Nan', np.nan)",
    "#Clean Order_Date",
    "df_copy['Order_Date'] = pd.to_datetime(",
    "    df_copy['Order_Date'],",
    "    errors='coerce',",
    "    format='mixed'",
    ")",
    "#Clean Product",
    "df_copy['Product'] = (",
    "    df_copy['Product']",
    "    .astype(str)",
    "    .str.strip()",
    "    .str.lower()",
    "    .str.title()",
    ")",
    "df_copy['Product'] = df_copy['Product'].replace('Nan', np.nan)",
    "#Clean Category",
    "df_copy['Category'] = (",
    "    df_copy['Category']",
    "    .astype(str)",
    "    .str.strip()",
    "    .str.lower()",
    "    .str.title()",
    ")",
    "df_copy['Category'] = df_copy['Category'].replace('Nan', np.nan)",
    "# Fix product acronyms / proper product names",
    "product_map = {",
    "    'Usb Cable': 'USB Cable',",
    "    'Ssd': 'SSD'",
    "}",
    "df_copy['Product'] = df_copy['Product'].replace(product_map)",
    "#Clean Quantity",
    "df_copy['Quantity'] = pd.to_numeric(df_copy['Quantity'], errors='coerce')",
    "df_copy.loc[",
    "    (df_copy['Quantity'] <= 0) | (df_copy['Quantity'] > 100),",
    "    'Quantity'",
    "] = np.nan",
    "df_copy['Quantity'] = df_copy['Quantity'].round().astype('Int64')",
    "#Clean Unit_Price",
    "df_copy['Unit_Price'] = (",
    "    df_copy['Unit_Price']",
    "    .astype(str)",
    "    .str.replace('RM', '', regex=False)",
    "    .str.replace(',', '', regex=False)",
    "    .str.strip()",
    ")",
    "df_copy['Unit_Price'] = pd.to_numeric(df_copy['Unit_Price'], errors='coerce')",
    "#Clean Discount",
    "df_copy['Discount_%'] = pd.to_numeric(df_copy['Discount_%'], errors='coerce')",
    "df_copy['Discount_%'] = df_copy['Discount_%'].fillna(0)",
    "# Create Total_Amount only when Quantity, Unit_Price, and Discount_% are valid",
    "df_copy['Total_Amount'] = np.where(",
    "    df_copy[['Quantity', 'Unit_Price', 'Discount_%']].notna().all(axis=1),",
    "    df_copy['Quantity'].astype(float)",
    "    * df_copy['Unit_Price']",
    "    * (1 - df_copy['Discount_%'] / 100),",
    "    np.nan",
    ")",
    "df_copy['Total_Amount'] = pd.to_numeric(df_copy['Total_Amount'], errors='coerce').round(2)",
    "#Clean Payment Method",
    "df_copy['Payment_Method'] = (",
    "    df_copy['Payment_Method']",
    "    .astype(str)",
    "    .str.strip()",
    "    .str.lower()",
    "    .str.title()",
    ")",
    "df_copy['Payment_Method'] = df_copy['Payment_Method'].replace('Nan', np.nan)",
    "#Clean order status",
    "df_copy['Order_Status'] = (",
    "    df_copy['Order_Status']",
    "    .astype(str)",
    "    .str.strip()",
    "    .str.lower()",
    "    .str.title()",
    ")",
    "df_copy['Order_Status'] = df_copy['Order_Status'].replace('Nan', np.nan)",
    "#Clean Customer Rating",
    "df_copy['Customer_Rating'] = pd.to_numeric(",
    "    df_copy['Customer_Rating'],",
    "    errors='coerce'",
    ")",
    "df_copy.loc[",
    "    (df_copy['Customer_Rating'] < 1) | (df_copy['Customer_Rating'] > 5),",
    "    'Customer_Rating'",
    "] = np.nan",
    "# Fill missing ratings with median rating",
    "median_rating = df_copy['Customer_Rating'].median()",
    "df_copy['Customer_Rating'] = df_copy['Customer_Rating'].fillna(median_rating)",
    "# Convert to integer",
    "df_copy['Customer_Rating'] = df_copy['Customer_Rating'].round().astype(int)",
    "#. Clean Notes",
    "df_copy['Notes'] = (",
    "    df_copy['Notes']",
    "    .astype(str)",
    "    .str.strip()",
    "    .str.lower()",
    ")",
    "df_copy['Notes'] = df_copy['Notes'].replace(['nan', 'none', ''], np.nan)",
    "# Add Revenue Valid Flag",
    "df_copy['Revenue_Valid_Flag'] = np.where(",
    "    df_copy[['Quantity', 'Unit_Price', 'Total_Amount']].isna().any(axis=1),",
    "    'Invalid Revenue Row',",
    "    'Valid Revenue Row'",
    ")",
    "# Add Data Quality Flag",
    "df_copy['Data_Quality_Flag'] = np.where(",
    "    df_copy[['Email', 'Phone', 'Order_Date', 'Quantity', 'Unit_Price', 'Total_Amount']].isna().any(axis=1),",
    "    'Issue Found',",
    "    'Clean'",
    ")",
    "# Add Order Month for Power BI",
    "df_copy['Order_Month'] = df_copy['Order_Date'].dt.to_period('M').astype(str)",
    "df_copy['Order_Month'] = df_copy['Order_Month'].replace('NaT', 'Missing Date')",
    "#Chk result",
    "print(df_copy.head())",
    "print(df_copy.isna().sum())",
    "print(df_copy.dtypes)",
    "df_copy.to_excel(",
    "     r\"C:\\Users\\11931\\Downloads\\cleaned_sales_data.xlsx\",",
    "     index=False",
    " )",
    "print(\"File saved successfully\")"
    ]
    
    # Calculate metadata
    metadata = {
        'total_lines': 185,
        'total_characters': 5574,
        'total_words': 440,
        'created_at': '2026-06-25T12:37:47.066Z',
        'version': '1.0'
    }
    
    # Calculate statistics
    line_lengths = [len(line) for line in text_lines]
    statistics = {
        'average_line_length': sum(line_lengths) // len(line_lengths) if line_lengths else 0,
        'longest_line': max(line_lengths) if line_lengths else 0,
        'shortest_line': min(line_lengths) if line_lengths else 0,
        'empty_lines': 77
    }
    
    return {
        'lines': text_lines,
        'metadata': metadata,
        'statistics': statistics
    }

def display_text(data):
    """Display text data with metadata"""
    print("Metadata:")
    for key, value in data['metadata'].items():
        print(f"  {key}: {value}")
    
    print("\nStatistics:")
    for key, value in data['statistics'].items():
        print(f"  {key}: {value}")
    
    print("\nText Lines:")
    for i, line in enumerate(data['lines'], 1):
        print(f"Line {i}: {line}")

if __name__ == "__main__":
    data = process_text()
    display_text(data)