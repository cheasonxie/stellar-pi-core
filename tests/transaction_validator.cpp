#include "transaction_validator.h"
#include "gtest/gtest.h"

TEST(TransactionValidatorTest, ValidTransaction) {
    PiCoin coin(true, "");
    Transaction tx{"mining", 314159, coin};
    TransactionValidator validator;
    EXPECT_TRUE(validator.validate(tx));
}

TEST(TransactionValidatorTest, InvalidValue) {
    PiCoin coin(true, "");
    Transaction tx{"mining", 1000, coin};
    TransactionValidator validator;
    EXPECT_FALSE(validator.validate(tx));
}

TEST(TransactionValidatorTest, BlacklistedSource) {
    PiCoin coin(true, "");
    Transaction tx{"exchange", 314159, coin};
    TransactionValidator validator;
    EXPECT_FALSE(validator.validate(tx));
}

TEST(TransactionValidatorTest, ImpurePiCoin) {
    PiCoin coin(false, "");
    Transaction tx{"mining", 314159, coin};
    TransactionValidator validator;
    EXPECT_FALSE(validator.validate(tx));
}
