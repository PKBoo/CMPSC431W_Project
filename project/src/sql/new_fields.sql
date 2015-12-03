

ALTER TABLE Transactions ADD (
	card_number int NOT NULL,
    card_name varchar(200) NOT NULL,
    card_expiration DATE NOT NULL,
    card_cvc int NOT NULL
);

ALTER TABLE Items ADD (
    description varchar(5000) NULL
);

ALTER TABLE Services ADD (
	ended INT DEFAULT 0
);