CREATE TABLE IF NOT EXISTS "offer" (
  "id" UUID PRIMARY KEY,
  "platformId" VARCHAR,
  "countryCode" CHAR(2),
  "platformSellerId" VARCHAR,
  "platformOfferId" VARCHAR,
  "platformProductId" VARCHAR,
  "isOversizeDelivery" BOOLEAN,
  "isDeliveryFeeByQuantity" BOOLEAN,
  "unitWeightGram" BOOLEAN,
  "isFreeMarketplaceDelivery" BOOLEAN
);

CREATE TABLE "attribute" (
  "offerId" UUID,
  "name" VARCHAR,
  "value" VARCHAR,
  PRIMARY KEY ("offerId", "name")
);

ALTER TABLE "attribute" ADD FOREIGN KEY ("offerId") REFERENCES "offer" ("id");
