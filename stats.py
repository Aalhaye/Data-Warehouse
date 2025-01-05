import pandas as pd
import numpy as np
from scipy import stats

# دالة لحساب الإحصائيات الأساسية
def calculate_basic_statistics(data):
    """
    دالة لحساب الإحصائيات الأساسية مثل:
    - المتوسط
    - الوسيط
    - الانحراف المعياري
    - التباين
    - القيم الدنيا والعليا
    - عدد العناصر
    """
    statistics = {
        'mean': np.mean(data),           # المتوسط
        'median': np.median(data),       # الوسيط
        'std_dev': np.std(data),         # الانحراف المعياري
        'variance': np.var(data),        # التباين
        'min': np.min(data),             # القيم الصغرى
        'max': np.max(data),             # القيم الكبرى
        'count': len(data)               # عدد العناصر
    }
    return statistics

# دالة لحساب الإحصائيات باستخدام pandas DataFrame
def calculate_dataframe_statistics(df, column):
    """
    دالة لحساب الإحصائيات الأساسية باستخدام pandas على عمود محدد:
    - المتوسط
    - الانحراف المعياري
    - القيم الصغرى والعليا
    """
    statistics = df[column].describe()
    return statistics

# دالة لحساب معامل الارتباط (correlation) بين الأعمدة
def calculate_correlation(df, column1, column2):
    """
    دالة لحساب معامل الارتباط بين عمودين في DataFrame.
    """
    correlation = df[column1].corr(column2)
    return correlation

# دالة لاختبار الفرضيات (مثال باستخدام t-test)
def t_test_sample(data1, data2):
    """
    دالة لاختبار t بين عينتين، للتحقق من وجود فرق ذو دلالة إحصائية.
    """
    t_stat, p_value = stats.ttest_ind(data1, data2)
    return t_stat, p_value

# دالة لقراءة البيانات من الجداول واستخراج التحليلات
def read_and_analyze_data(customers_file, sales_file):
    # قراءة البيانات
    customers_df = pd.read_csv(customers_file)
    sales_df = pd.read_csv(sales_file)

    # إحصائيات على جدول العملاء
    print("Statistics for customers data:")
    print(calculate_dataframe_statistics(customers_df, 'age'))
    
    # إحصائيات على جدول المبيعات
    print("\nStatistics for sales data:")
    print(calculate_dataframe_statistics(sales_df, 'quantity'))

    # حساب معامل الارتباط بين العمر وعدد المبيعات (في حال كان هناك)
    print("\nCorrelation between age and quantity sold:")
    correlation = calculate_correlation(customers_df, 'age', sales_df['quantity'])
    print(f"Correlation: {correlation}")
    
    # اختبار t-test بين أعمار مجموعتين من العملاء (مثال مع تقسيم أعمار العملاء)
    group1 = customers_df[customers_df['age'] < 30]['age']
    group2 = customers_df[customers_df['age'] >= 30]['age']
    
    t_stat, p_value = t_test_sample(group1, group2)
    print(f"\nT-test result between ages under 30 and 30+: t_stat = {t_stat}, p_value = {p_value}")

# استخدام الدالة مع مسارات ملفات البيانات
if __name__ == "__main__":
    # تحديد مسار الملفات كـ نص
    customers_file = 'C:/Users/Ahmed/Desktop/project/dataWH_clean/customersData.csv'
    sales_file = 'C:/Users/Ahmed/Desktop/project/dataWH_clean/salesData.csv'
    
    # استدعاء الدالة وتحليل البيانات
    read_and_analyze_data(customers_file, sales_file)
