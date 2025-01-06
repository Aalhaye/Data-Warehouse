
-- Question 1: What are the most common payment methods?
SELECT 
    payment_method,
    COUNT(*) AS usage_count
FROM 
    dw.customer_dimension
GROUP BY 
    payment_method
ORDER BY 
    usage_count DESC;
-- ملاحظات
-- تم ترتيب النتائج تنازلي  
-- 


-- Question 2: Which malls had the highest overall sales?
SELECT 
    shopping_mall,
    SUM(quantity * price) AS total_sales
FROM 
    dw.sales_fact
GROUP BY 
    shopping_mall
ORDER BY 
    total_sales DESC;
	
-- ملاحظات
-- تم ترتيب النتائج تنازلي 
-- حساب مجموع قيم المنتجات المباعة لكل مركز تسوق من خلال ضرب الكمية بالسعر للحصول على اجمالي المبيعات ثم يتم جمع هذه القيمعبر جميع السجلات لكل مركز تسوق


-- Question 3: What age group of customers spends the most at each mall?
SELECT 
    c.age,
    s.shopping_mall,
    SUM(s.quantity * s.price) AS total_spent
FROM 
    dw.customer_dimension c
JOIN 
    dw.sales_fact s
ON 
    c.customer_id = s.customer_id
GROUP BY 
    c.age, s.shopping_mall
ORDER BY 
    s.shopping_mall, total_spent DESC;
-- ملاحظات
-- تم ترتيب النتائج تنازلي
-- الاستعلام يقوم بحساب إجمالي الإنفاق لكل عميل وفقًا لعمره و مركز التسوق الذي قام بالشراء منه
--	 


-- Question 4: What are the top-selling product categories in each mall?
SELECT 
    shopping_mall,
    category,
    SUM(quantity * price) AS total_sales
FROM 
    dw.sales_fact

GROUP BY 
    shopping_mall, category
ORDER BY 
    total_sales DESC;
-- ملاحظات
-- تم ترتيب النتائج تنازلي
-- الاستعلام  يقوم بحساب إجمالي المبيعات لكل مركز تسوق
--


-- Question 5: What is the relationship between the age group of customers and the type of products they buy?
SELECT 
    c.age,
    s.category,
    COUNT(s.customer_id) AS purchase_count
FROM 
    dw.customer_dimension c
JOIN 
    dw.sales_fact s
ON 
    c.customer_id = s.customer_id
GROUP BY 
    c.age, s.category
ORDER BY 
    c.age, purchase_count DESC;
-- ملاحظات
-- تم ترتيب النتائج تنازلي
-- الاستعلام  يقوم بحساب عدد عمليات الشراء التي قام بها العملاء بناءً على الفئة التي تم شراؤها و عمر العميل
--
