#include "mainnet_governor.h"
#include <chrono>
#include <ctime>

MainnetGovernor::MainnetGovernor() : mainnetLaunched_(false) {}

bool MainnetGovernor::auditEcosystemTransactions(const std::vector<std::vector<Transaction>>& ecosystemTxs) {
    bool allCompliant = true;
    for (size_t i = 0; i < ecosystemTxs.size(); ++i) {
        for (const auto& tx : ecosystemTxs[i]) {
            if (!validator_.validate(tx)) {
                allCompliant = false;
                auditLog_.push_back("Non-compliant transaction detected in component " + std::to_string(i));
            }
        }
    }
    auto now = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());
    auditLog_.push_back("Audit completed at " + std::string(std::ctime(&now)) + " Compliance: " + (allCompliant ? "YES" : "NO"));
    return allCompliant;
}

bool MainnetGovernor::launchMainnet(const std::vector<std::vector<Transaction>>& ecosystemTxs) {
    if (mainnetLaunched_) {
        return false; // Already launched
    }
    if (!auditEcosystemTransactions(ecosystemTxs)) {
        return false; // Abort launch
    }
    mainnetLaunched_ = true;
    auditLog_.push_back("Mainnet launched successfully.");
    return true;
}

const std::vector<std::string>& MainnetGovernor::getAuditLog() const {
    return auditLog_;
}
