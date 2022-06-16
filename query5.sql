-- Find the number of sellers whose rating is higher than 1000
SELECT DISTINCT COUNT(DISTINCT SellerID)
AS numSellers
FROM Item items, User users
WHERE items.SellerID = users.UserID 
AND users.Rating > 1000;