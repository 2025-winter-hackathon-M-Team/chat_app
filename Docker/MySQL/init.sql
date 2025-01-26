
-- usersテーブル作成
CREATE TABLE users (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  username VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- rootユーザー登録
INSERT INTO users(email, password, username) VALUES('root', 'root', 'root'); 

-- メインカテゴリテーブル作成
CREATE TABLE main_categories (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  main_category_name VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- デフォルトメインカテゴリ登録
INSERT INTO main_categories(main_category_name) 
VALUES('インフラ部屋'),
('バックエンド部屋'),
('フロントエンド部屋'),
('なんでも質問部屋')
;

-- サブカテゴリテーブル作成
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

-- デフォルトサブカテゴリ登録
-- インフラ部屋のサブカテゴリ追加
INSERT INTO sub_categories(uid, sub_category_name, sub_category_description, main_category_id) 
VALUES (1, 'サーバー', 'サーバーについてお話しする部屋です！', 1),
(1, 'ネットワーク', 'ネットワークについてお話しする部屋です！', 1),
(1, 'セキュリティ', 'セキュリティについてお話しする部屋です！', 1),
(1, 'Linux', 'Linuxについてお話しする部屋です！', 1),
(1, 'AWS', 'AWSについてお話しする部屋です！', 1),
(1, 'Google Cloud', 'Google Cloudについてお話しする部屋です！', 1),
(1, 'Microsoft Azure', 'Microsoft Azureについてお話しする部屋です！', 1)
;
-- バックエンド部屋のサブカテゴリ追加
INSERT INTO sub_categories(uid, sub_category_name, sub_category_description, main_category_id) 
VALUES (1, 'Java', 'Javaについてお話しする部屋です！', 2),
(1, 'Ruby', 'Rubyについてお話しする部屋です！', 2),
(1, 'PHP', 'PHPについてお話しする部屋です！', 2),
(1, 'Perl', 'Perlについてお話しする部屋です！', 2),
(1, 'Python', 'Pythonについてお話しする部屋です！', 2),
(1, 'Go', 'Goについてお話しする部屋です！', 2),
(1, 'C言語', 'C言語についてお話しする部屋です！', 2),
(1, 'C++', 'C++についてお話しする部屋です！', 2),
(1, 'C#', 'C#についてお話しする部屋です！', 2)
;
-- フロントエンド部屋のサブカテゴリ追加
INSERT INTO sub_categories(uid, sub_category_name, sub_category_description, main_category_id) 
VALUES (1, 'HTML/CSS', 'HTML/CSSについてお話しする部屋です！', 3),
(1, 'UI/UXデザイン', 'UI/UXデザインについてお話しする部屋です！', 3),
(1, 'JavaScript', 'JavaScriptについてお話しする部屋です！', 3),
(1, 'TypeScript', 'TypeScriptについてお話しする部屋です！', 3),
(1, 'Figma', 'Figmaについてお話しする部屋です！', 3)
;

-- メッセージテーブル作成
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

/*
INSERT INTO messages(uid, sub_category_id, message) VALUES(1, 1, 'セキュリティは難しい。')
*/