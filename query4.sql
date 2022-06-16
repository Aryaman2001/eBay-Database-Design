-- Find the IDs of auction(s) with the highest current price
WITH maxPrice (maxValue) AS
(SELECT MAX(Currently)
FROM Item)
SELECT ItemID FROM item, maxPrice
WHERE item.Currently = maxPrice.maxValue;