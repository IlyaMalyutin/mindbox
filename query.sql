-- В базе данных MS SQL Server есть продукты и категории.
-- Одному продукту может соответствовать много категорий, в одной категории может быть много продуктов.
-- Напишите SQL запрос для выбора всех пар «Имя продукта – Имя категории».
-- Если у продукта нет категорий, то его имя все равно должно выводиться.

-- если я правильно понял задание, то отношение между таблицами many-to-many
-- и LEFT JOIN вернет нам все что нужно

SELECT p.product_name, c.category_name FROM products AS p
LEFT JOIN category as c ON c.id = p.category_id;