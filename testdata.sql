USE webauction;
INSERT INTO User (username, phone, email, passwdHash, firstName, lastName, houseFlatNo, street, city, pincode, dateJoined, isVerified)
VALUES
('john_doe', '1234567890', 'john.doe@example.com', 'hashed_password1', 'John', 'Doe', '12A', 'Baker Street', 'London', '123456', '2023-01-01 10:00:00', TRUE),
('jane_smith', '0987654321', 'jane.smith@example.com', 'hashed_password2', 'Jane', 'Smith', '34B', 'Fleet Street', 'London', '654321', '2023-01-02 11:00:00', TRUE),
('alice_jones', '1231231234', 'alice.jones@example.com', 'hashed_password3', 'Alice', 'Jones', '56C', 'Oxford Street', 'Oxford', '111222', '2023-01-03 12:00:00', TRUE),
('bob_brown', '3213213210', 'bob.brown@example.com', 'hashed_password4', 'Bob', 'Brown', '78D', 'King\'s Road', 'London', '333444', '2023-01-04 13:00:00', TRUE),
('charlie_miller', '4564564567', 'charlie.miller@example.com', 'hashed_password5', 'Charlie', 'Miller', '90E', 'Queen\'s Road', 'London', '555666', '2023-01-05 14:00:00', TRUE),
('david_wilson', '6546546543', 'david.wilson@example.com', 'hashed_password6', 'David', 'Wilson', '12F', 'High Street', 'London', '777888', '2023-01-06 15:00:00', TRUE),
('emily_davis', '7897897896', 'emily.davis@example.com', 'hashed_password7', 'Emily', 'Davis', '34G', 'Main Street', 'Oxford', '999000', '2023-01-07 16:00:00', TRUE),
('frank_clark', '9879879871', 'frank.clark@example.com', 'hashed_password8', 'Frank', 'Clark', '56H', 'Elm Street', 'London', '101010', '2023-01-08 17:00:00', TRUE),
('grace_evans', '1122334455', 'grace.evans@example.com', 'hashed_password9', 'Grace', 'Evans', '78I', 'Cedar Street', 'Oxford', '202020', '2023-01-09 18:00:00', TRUE),
('harry_white', '5566778899', 'harry.white@example.com', 'hashed_password10', 'Harry', 'White', '90J', 'Maple Street', 'London', '303030', '2023-01-10 19:00:00', TRUE);

INSERT INTO Category (categoryName)
VALUES
('Electronics'),
('Books'),
('Clothing'),
('Home & Kitchen'),
('Sports & Outdoors'),
('Beauty & Personal Care'),
('Toys & Games'),
('Automotive'),
('Health & Wellness'),
('Office Supplies');

INSERT INTO Product (title, `description`, `condition`, initialBid, currentBidPrice, `status`, startTime, endTime, userId)
VALUES
('Smartphone', 'A brand new smartphone with 128GB storage.', 'new', 299.99, 350.00, 'active', '2023-09-01 10:00:00', '2023-09-10 10:00:00', 1),
('Laptop', 'Used laptop in good condition, 8GB RAM, 256GB SSD.', 'used', 499.99, 550.00, 'active', '2023-09-02 11:00:00', '2023-09-12 11:00:00', 2),
('Gaming Console', 'Refurbished gaming console with 1TB storage.', 'refurbished', 199.99, 220.00, 'sold', '2023-09-03 12:00:00', '2023-09-13 12:00:00', 3),
('Headphones', 'Brand new wireless headphones with noise cancellation.', 'new', 99.99, 120.00, 'expired', '2023-09-04 13:00:00', '2023-09-14 13:00:00', 4),
('Bookshelf', 'Used wooden bookshelf, 5 shelves.', 'used', 59.99, 70.00, 'active', '2023-09-05 14:00:00', '2023-09-15 14:00:00', 5),
('Digital Camera', 'Refurbished digital camera with 24MP resolution.', 'refurbished', 299.99, 320.00, 'sold', '2023-09-06 15:00:00', '2023-09-16 15:00:00', 6),
('Coffee Maker', 'New coffee maker with programmable settings.', 'new', 49.99, 60.00, 'expired', '2023-09-07 16:00:00', '2023-09-17 16:00:00', 7),
('Bicycle', 'Used mountain bike in good condition.', 'used', 149.99, 170.00, 'active', '2023-09-08 17:00:00', '2023-09-18 17:00:00', 8),
('Smartwatch', 'Refurbished smartwatch with heart rate monitor.', 'refurbished', 129.99, 150.00, 'sold', '2023-09-09 18:00:00', '2023-09-19 18:00:00', 9),
('Office Chair', 'New ergonomic office chair with lumbar support.', 'new', 89.99, 110.00, 'active', '2023-09-10 19:00:00', '2023-09-20 19:00:00', 10);

INSERT INTO Bid (bidAmount, bidTime, isWinningBid, userId, productId)
VALUES
(305.00, '2023-09-01 12:00:00', FALSE, 1, 1),
(360.00, '2023-09-01 14:00:00', TRUE, 2, 1),
(510.00, '2023-09-02 12:30:00', FALSE, 3, 2),
(580.00, '2023-09-02 15:00:00', TRUE, 4, 2),
(215.00, '2023-09-03 13:00:00', FALSE, 5, 3),
(230.00, '2023-09-03 16:00:00', TRUE, 6, 3),
(115.00, '2023-09-04 11:30:00', FALSE, 7, 4),
(125.00, '2023-09-04 14:30:00', TRUE, 8, 4),
(65.00, '2023-09-05 10:00:00', FALSE, 9, 5),
(75.00, '2023-09-05 13:00:00', TRUE, 10, 5),
(305.00, '2023-09-06 12:00:00', FALSE, 1, 6),
(320.00, '2023-09-06 14:30:00', TRUE, 2, 6),
(55.00, '2023-09-07 12:00:00', FALSE, 3, 7),
(65.00, '2023-09-07 15:00:00', TRUE, 4, 7),
(160.00, '2023-09-08 10:00:00', FALSE, 5, 8),
(175.00, '2023-09-08 13:00:00', TRUE, 6, 8),
(140.00, '2023-09-09 14:00:00', FALSE, 7, 9),
(155.00, '2023-09-09 16:00:00', TRUE, 8, 9),
(100.00, '2023-09-10 10:30:00', FALSE, 9, 10),
(115.00, '2023-09-10 12:30:00', TRUE, 10, 10),
(315.00, '2023-09-01 15:00:00', FALSE, 1, 1),
(370.00, '2023-09-01 17:00:00', FALSE, 2, 1),
(525.00, '2023-09-02 13:30:00', FALSE, 3, 2),
(595.00, '2023-09-02 16:30:00', FALSE, 4, 2),
(220.00, '2023-09-03 14:00:00', FALSE, 5, 3),
(235.00, '2023-09-03 17:00:00', FALSE, 6, 3),
(120.00, '2023-09-04 12:00:00', FALSE, 7, 4),
(130.00, '2023-09-04 15:00:00', FALSE, 8, 4),
(70.00, '2023-09-05 11:00:00', FALSE, 9, 5),
(80.00, '2023-09-05 14:00:00', FALSE, 10, 5);
