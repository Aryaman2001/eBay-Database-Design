-- Find the number of users who are both sellers and bidders.
DROP VIEW IF EXISTS all_sellers;
CREATE VIEW all_sellers AS
SELECT DISTINCT(U.UserID)
FROM Item I, User U
WHERE I.SellerID = U.UserID;

SELECT COUNT(DISTINCT(B.BuyerID))
FROM all_sellers A, Bid B
WHERE A.UserID = B.BuyerID;