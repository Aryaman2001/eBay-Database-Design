-- Find the number of categories that include at least one item with a bid of more than $100. 
WITH items
AS (SELECT DISTINCT categories.CategoryName FROM Category categories, Bid bids WHERE categories.ItemID = bids.ItemID AND bids.Amount > 100)
SELECT COUNT(*) FROM items;