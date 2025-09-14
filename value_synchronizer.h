#ifndef VALUE_SYNCHRONIZER_H
#define VALUE_SYNCHRONIZER_H

#include <string>
#include <functional>
#include <unordered_map>

class ValueSynchronizer {
public:
    using StateFetcher = std::function<int64_t()>;

    void registerComponent(const std::string& name, StateFetcher fetcher);
    bool synchronizeAll();

private:
    std::unordered_map<std::string, StateFetcher> components_;
    bool synchronizeComponent(const std::string& name, StateFetcher fetcher);
};

#endif // VALUE_SYNCHRONIZER_H
