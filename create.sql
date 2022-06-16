drop table if exists Item;
drop table if exists Bid;
drop table if exists User;
drop table if exists Category;

create table Item ( 
    ItemID int,
    SellerID varchar(225),
    Name varchar(225) NOT NULL,
    Currently float NOT NULL,
    Buy_Price float,
    First_Bid float NOT NULL,
    Number_Of_Bids int NOT NULL,
    Started varchar(225) NOT NULL,
    Ends varchar(225) NOT NULL,
    Description varchar(225),
    primary key(ItemID),
    foreign key(SellerID) references User(UserID)
);
create table Bid ( 
    ItemID int,
    BuyerID varchar(225),
    SellerID varchar(225),
    Amount float NOT NULL,
    Time varchar(225) NOT NULL,
    primary key(ItemID,BuyerID,Time),
    foreign key(ItemID) references Item(ItemID),
    foreign key(BuyerID) references User(UserID),
    foreign key(SellerID) references User(UserID)
);
create table User ( 
    UserID varchar(225),
    Rating int NOT NULL,
    Location varchar(225),
    Country varchar(225),
    primary key(UserID)
);
create table Category ( 
    ItemID int,
    CategoryName varchar(225) NOT NULL,
    primary key(CategoryName,ItemID),
    foreign key(ItemID) references Item(ItemID)
);