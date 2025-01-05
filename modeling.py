import pandas as pd
import psycopg2
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# إعداد الاتصال بقاعدة البيانات

conn = psycopg2.connect(
dbname="project_DB", 
user="postgres", 
password="123", 
host="localhost", 
port="5432"
)


# قراءة البيانات من جدول المبيعات
query = """
SELECT
    c.age,
    c.gender,
    c.payment_method,
    s.quantity,
    s.price,
    s.category,
    s.shopping_mall
FROM
    dw.customer_dimension c
JOIN
    dw.sales_fact s
ON
    c.customer_id = s.customer_id
"""
data = pd.read_sql(query, conn)

# إغلاق الاتصال بقاعدة البيانات
conn.close()

# معالجة البيانات: إنشاء عمود جديد للمبيعات الكلية
data['total_sales'] = data['quantity'] * data['price']

# تحويل الأعمدة النصية إلى قيم رقمية باستخدام الترميز (Encoding)
data = pd.get_dummies(data, columns=['gender', 'payment_method', 'category', 'shopping_mall'], drop_first=True)

# تحديد الميزات (features) والهدف (target)
X = data.drop(columns=['total_sales'])
y = data['total_sales']

# تقسيم البيانات إلى مجموعة تدريب واختبار
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# بناء نموذج الانحدار الخطي
model = LinearRegression()
model.fit(X_train, y_train)

# إجراء التنبؤات
y_pred = model.predict(X_test)

# حساب الأداء
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# طباعة النتائج
print(f'Mean Squared Error: {mse}')
print(f'R-squared: {r2}')

# رسم النتائج
plt.scatter(y_test, y_pred)
plt.xlabel("True Values")
plt.ylabel("Predictions")
plt.title("True vs Predicted Values")
plt.show()
