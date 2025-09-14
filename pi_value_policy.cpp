#include "pi_value_policy.h"

const std::unordered_set<std::string> PiValuePolicy::ALLOWED_SOURCES = {
    "mining", "p2p", "contribution", "marketplace", "app"
};

const std::unordered_set<std::string> PiValuePolicy::BLACKLISTED_SOURCES = {
    "exchange"
};

const std::string PiValuePolicy::BADGE_SYMBOL = "🌟";

bool PiValuePolicy::isSourceAllowed(const std::string& source) {
    return ALLOWED_SOURCES.count(source) > 0 && BLACKLISTED_SOURCES.count(source) == 0;
}
