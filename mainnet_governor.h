#ifndef MAINNET_GOVERNOR_H
#define MAINNET_GOVERNOR_H

#include <vector>
#include "transaction.h"
#include "transaction_validator.h"

class MainnetGovernor {
public:
    MainnetGovernor();

    // Audit semua transaksi dari seluruh komponen ekosistem
    bool auditEcosystemTransactions(const std::vector<std::vector<Transaction>>& ecosystemTxs);

    // Meluncurkan mainnet jika semua patuh
    bool launchMainnet(const std::vector<std::vector<Transaction>>& ecosystemTxs);

    // Mendapatkan log audit
    const std::vector<std::string>& getAuditLog() const;

private:
    TransactionValidator validator_;
    std::vector<std::string> auditLog_;
    bool mainnetLaunched_;
};

#endif // MAINNET_GOVERNOR_H
