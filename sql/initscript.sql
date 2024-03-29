CREATE TABLE IF NOT EXISTS IMAGE (
    id INT NOT NULL AUTO_INCREMENT primary key,
    name VARCHAR(255) NOT NULL,
    path VARCHAR(255) NOT NULL,
    priority int NOT NULL,
    error_img boolean DEFAULT false
)  ENGINE=INNODB;

CREATE TABLE ANNOTATION(
   id int not null auto_increment primary key,
   gender decimal,
   age decimal,
   style decimal,
   description varchar(255),
   image_id int not null,
   user_id int,
   user_nick varchar(255),
   FOREIGN KEY fk_image(image_id)
   REFERENCES IMAGE(id)
   ON UPDATE CASCADE
   ON DELETE RESTRICT
)ENGINE=InnoDB;

ALTER TABLE annotation
  ADD user_id int;

INSERT INTO IMAGE(name, path, priority) VALUES ("1.jpg", "static/1005/1.jpg", 1);

UPDATE image SET priority = 1 where id =1;
UPDATE image SET priority = 100 where id =3;
UPDATE image SET priority = 50 where id =4;

INSERT INTO ANNOTATION(gender, age, style, description, image_id, user_id) VALUES (0, 1, 1, "empty", 1, 11152);
INSERT INTO ANNOTATION(gender, age,  image_id, user_id) VALUES (0, 1, 1, 98524);
INSERT INTO ANNOTATION(gender, age,  image_id, user_id) VALUES (null, 1, 1, 65719);

UPDATE image SET path = "1005/1.jpg" where id =1;

select * from image i inner join annotation a
 on image.id = annotation.image_id;
