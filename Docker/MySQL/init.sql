CREATE TABLE users (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  username VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


INSERT INTO users(email, password, username) VALUES('a@gmail.com', 'a_pass', 'a');

CREATE TABLE main_categories (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  main_category_name VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

INSERT INTO main_categories(main_category_name) VALUES('インフラ部屋');

CREATE TABLE sub_categories (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uid INT UNSIGNED,
  sub_category_name VARCHAR(255) UNIQUE NOT NULL,
  sub_category_description VARCHAR(255),
  main_category_id INT UNSIGNED,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (uid) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (main_category_id) REFERENCES main_categories(id) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

INSERT INTO sub_categories(uid, sub_category_name, sub_category_description, main_category_id) VALUES(1, 'セキュリティ', '大事です。', 1);

CREATE TABLE messages (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uid INT UNSIGNED,
  sub_category_id INT UNSIGNED,
  message TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (uid) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (sub_category_id) REFERENCES sub_categories(id) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

INSERT INTO messages(uid, sub_category_id, message) VALUES(1, 1, 'セキュリティは難しい。')