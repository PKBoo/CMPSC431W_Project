CREATE TABLE Users (
	user_id int NOT NULL AUTO_INCREMENT,
	username VARCHAR(40),
	password varchar(500),
	first_name VARCHAR(40),
	last_name VARCHAR(40),
	email VARCHAR(40),
	PRIMARY KEY (user_id)	
);


CREATE TABLE Items (

	item_id INT not null auto_increment,
	user_id int,
	category_id int,
	name varchar(100),
	created_at DATETIME,
	PRIMARY KEY (item_id)
	#FOREIGN KEY (user_id) references Users(user_id)
	#ON DELETE CASCADE,
	#ON UPDATE CASCADE
	#we are switching this to a weak entity
	);

CREATE TABLE Categories (

	category_id int NOT NULL AUTO_INCREMENT,
	name varchar(40),
	parent_id int,
	PRIMARY KEY(category_id)
	);
	
CREATE TABLE Transaction_Items (
	transaction_item_id int NOT NULL AUTO_INCREMENT,
	transaction_id int NOT NULL,
	item_id int NOT NULL,
	PRIMARY KEY(transaction_item_id, transaction_id),
	#FOREIGN KEY (transaction_id) references Transactions(transaction_id) 
	#ON UPDATE CASCADE
	#ON DELETE CASCADE
	FOREIGN KEY (item_id) references Items(item_id)
	ON UPDATE CASCADE
	ON DELETE CASCADE
	);
	