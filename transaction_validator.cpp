#include "transaction_validator.h"

bool TransactionValidator::validate(const Transaction& tx) const {
    if (tx.value != PiValuePolicy::FIXED_PI_VALUE) {
        return false;
    }
    if (!PiValuePolicy::isSourceAllowed(tx.source)) {
        return false;
    }
    if (!tx.pi_coin.isPure()) {
        return false;
    }
    return true;
}

void TransactionValidator::assignBadge(Transaction& tx) const {
    if (validate(tx)) {
        tx.pi_coin.setBadge(PiValuePolicy::BADGE_SYMBOL);
    }
}
