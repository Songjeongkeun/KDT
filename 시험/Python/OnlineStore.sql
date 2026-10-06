/* Online Store Database */

CREATE DATABASE IF NOT EXISTS online_store;

USE online_store;

GRANT ALL ON online_store.* TO 'apple'@'localhost';


CREATE TABLE member (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(200) NOT NULL,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(200) NOT NULL UNIQUE,
    regdate DATETIME NOT NULL DEFAULT now()
);

CREATE TABLE product (
	id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    price INT NOT NULL CHECK (price >= 0),
    stock INT NOT NULL CHECK (stock >= 0),
    created_at DATETIME NOT NULL DEFAULT now()
);

CREATE TABLE order_header (
	id INT AUTO_INCREMENT PRIMARY KEY,
	member_id INT NOT NULL,
    total_price INT,
    status VARCHAR(10) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT now(),
	CONSTRAINT fk_order_member
		FOREIGN KEY (member_id)
        REFERENCES member(id)
);

CREATE TABLE order_item (
	id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity >= 0),
    price INT NOT NULL CHECK (price >= 0),
    CONSTRAINT fk_order_item
		FOREIGN KEY (order_id)
        REFERENCES order_header(id),
	CONSTRAINT fk_item_product
		FOREIGN KEY (product_id)
        REFERENCES product(id)
);

CREATE TABLE payment (
	id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL UNIQUE,
    method VARCHAR(10),
    paid_amount INT NOT NULL,
    paid_at DATETIME DEFAULT now(),
    CONSTRAINT fk_payment_order
		FOREIGN KEY (order_id)
        REFERENCES order_header(id) 
);

SELECT * FROM member;

INSERT INTO product (name, price, stock) VALUES
('무선 마우스', 25000, 10),
('기계식 키보드', 89000, 5),
('USB-C 케이블', 9000, 30),
('노트북 거치대', 32000, 8),
('블루투스 이어폰', 59000, 12),
('휴대용 충전기', 39000, 15),
('웹캠', 45000, 6),
('모니터 받침대', 27000, 9),
('스마트폰 거치대', 12000, 20),
('게이밍 헤드셋', 76000, 0);

SELECT * FROM member;
SELECT * FROM product;
SELECT * FROM order_header;
SELECT * FROM order_item;
SELECT * FROM payment;

-- Error Code: 1364. Field 'created_at' doesn't have a default value
 