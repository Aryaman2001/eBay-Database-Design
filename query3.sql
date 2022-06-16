-- Find the number of auctions belonging to exactly four categories
WITH itemDetails as 
(SELECT ItemID, count(ItemID) 
FROM category 
GROUP BY ItemID 
HAVING count(ItemID) = 4)
SELECT COUNT(*) FROM itemDetails;