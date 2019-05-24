CREATE TABLE "line" (
"uuid" varchar(64) NOT NULL,
"id" int2 NOT NULL,
"name" varchar(255),
"city_id" varchar(64) NOT NULL,
"description" varchar(255),
PRIMARY KEY ("uuid") 
)
WITHOUT OIDS;
COMMENT ON COLUMN "line"."city_id" IS '城市ID';

CREATE TABLE "city" (
"uuid" varchar(64) NOT NULL,
"name" varchar(255) NOT NULL,
"population" int4 NOT NULL,
"province_id" varchar(64) NOT NULL,
"region_id" varchar(64) NOT NULL,
"area" decimal NOT NULL,
PRIMARY KEY ("uuid") 
)
WITHOUT OIDS;
COMMENT ON COLUMN "city"."population" IS '人口';
COMMENT ON COLUMN "city"."province_id" IS '省份ID';
COMMENT ON COLUMN "city"."region_id" IS '区域ID';
COMMENT ON COLUMN "city"."area" IS ' 面积';

CREATE TABLE "province" (
"uuid" varchar(64) NOT NULL,
"name" varchar(255) NOT NULL,
"region_id" varchar(64) NOT NULL,
"area" decimal NOT NULL,
PRIMARY KEY ("uuid") 
)
WITHOUT OIDS;
COMMENT ON COLUMN "province"."region_id" IS '区域ID';
COMMENT ON COLUMN "province"."area" IS '面积';

CREATE TABLE "region" (
"uuid" varchar(64) NOT NULL,
"name" varchar(255) NOT NULL,
PRIMARY KEY ("uuid") 
)
WITHOUT OIDS;

ALTER TABLE "line" ADD CONSTRAINT "fk_line_city_id" FOREIGN KEY ("city_id") REFERENCES "city" ("uuid") ON DELETE RESTRICT ON UPDATE CASCADE;
ALTER TABLE "city" ADD CONSTRAINT "fk_city_province_id" FOREIGN KEY ("province_id") REFERENCES "province" ("uuid") ON DELETE RESTRICT ON UPDATE CASCADE;
ALTER TABLE "city" ADD CONSTRAINT "fk_city_region_id" FOREIGN KEY ("region_id") REFERENCES "region" ("uuid") ON DELETE RESTRICT ON UPDATE CASCADE;
ALTER TABLE "province" ADD CONSTRAINT "fk_province_region_id" FOREIGN KEY ("region_id") REFERENCES "region" ("uuid") ON DELETE RESTRICT ON UPDATE CASCADE;

