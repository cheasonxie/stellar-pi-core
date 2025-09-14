#ifndef PI_VALUE_POLICY_H
#define PI_VALUE_POLICY_H

#include <string>
#include <unordered_set>

class PiValuePolicy {
public:
    static constexpr int64_t FIXED_PI_VALUE = 314159; // Fixed Pi Coin value in smallest unit
    static const std::unordered_set<std::string> ALLOWED_SOURCES;
    static const std::unordered_set<std::string> BLACKLISTED_SOURCES;
    static const std::string BADGE_SYMBOL;

    static bool isSourceAllowed(const std::string& source);
};

#endif // PI_VALUE_POLICY_H
