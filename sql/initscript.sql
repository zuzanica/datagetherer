CREATE TABLE IF NOT EXISTS image (
    id INT NOT NULL AUTO_INCREMENT primary key,
    name VARCHAR(255) NOT NULL,
    path VARCHAR(255) NOT NULL
)  ENGINE=INNODB;

CREATE TABLE annotation(
   id int not null auto_increment primary key,
   gender decimal,
   age decimal,
   image_id int not null,
   FOREIGN KEY fk_image(image_id)
   REFERENCES image(id)
   ON UPDATE CASCADE
   ON DELETE RESTRICT
)ENGINE=InnoDB;

ALTER TABLE annotation
  ADD user_id int;

ALTER TABLE image
  ADD priority int not null;



INSERT INTO IMAGE(name, path) VALUES ("1.jpg", "static/1005/1.jpg", 1);
INSERT INTO IMAGE(name, path) VALUES ("2.jpg", "test/2.jpg", 100);
INSERT INTO IMAGE(name, path) VALUES ("3.jpg", "test/3.jpg", 50);


INSERT INTO ANNOTATION(gender, age,  image_id, user_id) VALUES (0, 1, 1, 11152);
INSERT INTO ANNOTATION(gender, age,  image_id, user_id) VALUES (0, 1, 1, 98524);

UPDATE image SET path = "1005/1.jpg" where id =1;

INSERT INTO ANNOTATION(gender, age,  image_id, user_id) VALUES (null, 1, 1, 65719);


select * from image i inner join annotation a 
 on image.id = annotation.image_id;  
