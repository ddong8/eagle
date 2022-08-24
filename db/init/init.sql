CREATE TABLE "line" ("uuid" VARCHAR (64) NOT NULL,"id" int2 NOT NULL,"name" VARCHAR (255),"city_id" VARCHAR (64) NOT NULL,"description" VARCHAR (255),PRIMARY KEY ("uuid")) WITHOUT OIDS; COMMENT ON COLUMN "line"."city_id" IS '城市ID'; 
CREATE TABLE "city" ("uuid" VARCHAR (64) NOT NULL,"name" VARCHAR (255) NOT NULL,"population" int4 NOT NULL,"province_id" VARCHAR (64) NOT NULL,"region_id" VARCHAR (64) NOT NULL,"area" DECIMAL NOT NULL,PRIMARY KEY ("uuid")) WITHOUT OIDS; COMMENT ON COLUMN "city"."population" IS '人口'; COMMENT ON COLUMN "city"."province_id" IS '省份ID'; COMMENT ON COLUMN "city"."region_id" IS '区域ID'; COMMENT ON COLUMN "city"."area" IS ' 面积'; 
CREATE TABLE "province" ("uuid" VARCHAR (64) NOT NULL,"name" VARCHAR (255) NOT NULL,"region_id" VARCHAR (64) NOT NULL,"area" DECIMAL NOT NULL,PRIMARY KEY ("uuid")) WITHOUT OIDS; COMMENT ON COLUMN "province"."region_id" IS '区域ID'; COMMENT ON COLUMN "province"."area" IS '面积'; 
CREATE TABLE "region" ("uuid" VARCHAR (64) NOT NULL,"name" VARCHAR (255) NOT NULL,PRIMARY KEY ("uuid")) WITHOUT OIDS; 
ALTER TABLE "line" ADD CONSTRAINT "fk_line_city_id" FOREIGN KEY ("city_id") REFERENCES "city" ("uuid") ON 
DELETE RESTRICT ON 
UPDATE CASCADE; 
ALTER TABLE "city" ADD CONSTRAINT "fk_city_province_id" FOREIGN KEY ("province_id") REFERENCES "province" ("uuid") ON 
DELETE RESTRICT ON 
UPDATE CASCADE; 
ALTER TABLE "city" ADD CONSTRAINT "fk_city_region_id" FOREIGN KEY ("region_id") REFERENCES "region" ("uuid") ON 
DELETE RESTRICT ON 
UPDATE CASCADE; 
ALTER TABLE "province" ADD CONSTRAINT "fk_province_region_id" FOREIGN KEY ("region_id") REFERENCES "region" ("uuid") ON 
DELETE RESTRICT ON 
UPDATE CASCADE; 
DROP TABLE IF EXISTS "public"."stock"; 
CREATE TABLE "public"."stock" ("id" TEXT COLLATE "pg_catalog"."default","code" TEXT COLLATE "pg_catalog"."default","name" TEXT COLLATE "pg_catalog"."default","trade_date" TEXT COLLATE "pg_catalog"."default","change_rate" float8,"close_price" float8,"buy_amt" float8,"net_buy_amt" float8,"accum_amount" int8,"market" TEXT COLLATE "pg_catalog"."default","explanation" TEXT COLLATE "pg_catalog"."default"); 
ALTER TABLE "public"."stock" OWNER TO "postgres";