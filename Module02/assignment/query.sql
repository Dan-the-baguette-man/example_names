-- TODO: Write a query that counts rows by category.
-- Requirements:
--   • Table name: students
--   • Output columns: category, count
--   • Sort results alphabetically by category

-- Complete the following by replacing [FILL_HERE] with the required syntax:
SELECT category, count(*) AS count
FROM students
GROUP BY category
ORDER BY category;
