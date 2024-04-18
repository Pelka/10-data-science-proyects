CREATE TABLE "user" (
  "id" uuid PRIMARY KEY,
  "id_matrial_status" int NOT NULL,
  "id_ocupation_status" int NOT NULL,
  "id_incomes_status" int NOT NULL,
  "id_education_status" int NOT NULL,
  "id_zip_code" int,
  "age" smallint,
  "family_size" smallint,
  "latitude" float,
  "longitude" float,
  "zip_code" varchar(10),
  "gender" bool,
  "output" bool,
  "feedback" bool
);

CREATE TABLE "matrial_status" (
  "id" serial PRIMARY KEY,
  "status" varchar(32) UNIQUE
);

CREATE TABLE "ocupation_status" (
  "id" serial PRIMARY KEY,
  "status" varchar(16) UNIQUE
);

CREATE TABLE "incomes_status" (
  "id" serial PRIMARY KEY,
  "status" varchar(16) UNIQUE
);

CREATE TABLE "education_status" (
  "id" serial PRIMARY KEY,
  "status" varchar(16) UNIQUE
);

CREATE TABLE "orders" (
  "id" uuid PRIMARY KEY,
  "id_user" uuid,
  "creation_date" timestamp,
  "message" text
);

CREATE TABLE "order_products" (
  "id" uuid PRIMARY KEY,
  "id_order" uuid,
  "id_product" uuid,
  "amount" smallint
);

CREATE TABLE "products" (
  "id" uuid PRIMARY KEY,
  "name" text,
  "description" text
);

CREATE INDEX "status" ON "user" ("id_matrial_status", "id_ocupation_status", "id_incomes_status", "id_education_status");

CREATE UNIQUE INDEX ON "user" ("id");

CREATE UNIQUE INDEX ON "orders" ("id");

CREATE INDEX ON "orders" ("id_user");

CREATE UNIQUE INDEX ON "order_products" ("id");

CREATE INDEX "origin" ON "order_products" ("id_order", "id_product");

CREATE UNIQUE INDEX ON "products" ("id");

CREATE INDEX ON "products" ("name");

ALTER TABLE "user" ADD FOREIGN KEY ("id_matrial_status") REFERENCES "matrial_status" ("id");

ALTER TABLE "user" ADD FOREIGN KEY ("id_ocupation_status") REFERENCES "ocupation_status" ("id");

ALTER TABLE "user" ADD FOREIGN KEY ("id_incomes_status") REFERENCES "incomes_status" ("id");

ALTER TABLE "user" ADD FOREIGN KEY ("id_education_status") REFERENCES "education_status" ("id");

ALTER TABLE "orders" ADD FOREIGN KEY ("id_user") REFERENCES "user" ("id");

ALTER TABLE "order_products" ADD FOREIGN KEY ("id_order") REFERENCES "orders" ("id");

CREATE TABLE "products_order_products" (
  "products_id" uuid,
  "order_products_id_product" uuid,
  PRIMARY KEY ("products_id", "order_products_id_product")
);

ALTER TABLE "products_order_products" ADD FOREIGN KEY ("products_id") REFERENCES "products" ("id");

ALTER TABLE "products_order_products" ADD FOREIGN KEY ("order_products_id_product") REFERENCES "order_products" ("id_product");

