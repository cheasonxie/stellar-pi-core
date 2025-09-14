#include "value_synchronizer.h"
#include "pi_value_policy.h"
#include <iostream>

void ValueSynchronizer::registerComponent(const std::string& name, StateFetcher fetcher) {
    components_[name] = fetcher;
}

bool ValueSynchronizer::synchronizeComponent(const std::string& name, StateFetcher fetcher) {
    int64_t currentValue = fetcher();
    if (currentValue != PiValuePolicy::FIXED_PI_VALUE) {
        // Simulate update call to component
        std::cout << "Synchronizing component " << name << " from value " << currentValue << " to " << PiValuePolicy::FIXED_PI_VALUE << std::endl;
        // Real implementation would update component state here
        return true;
    }
    return true;
}

bool ValueSynchronizer::synchronizeAll() {
    bool allSuccess = true;
    for (const auto& [name, fetcher] : components_) {
        if (!synchronizeComponent(name, fetcher)) {
            allSuccess = false;
        }
    }
    return allSuccess;
}
