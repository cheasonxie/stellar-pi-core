#[cfg(test)]
mod test_ahi_ai_core {
    use soroban_sdk::testutils::Env;
    use crate::ahi_ai_core::AhiAiCore;
    use soroban_sdk::{Symbol, Map};

    #[test]
    fn test_filter_transaction_anti_gambling() {
        let env = Env::default();
        let ahi_ai = AhiAiCore::init(env.clone());
        let tx_data = Map::new(&env);
        tx_data.set(Symbol::new(&env, "description"), Symbol::new(&env, "gambling app"));
        tx_data.set(Symbol::new(&env, "currency"), Symbol::new(&env, "PI"));
        let result = AhiAiCore::filter_transaction(env, tx_data);
        assert!(!result, "Should reject gambling transaction");
    }

    #[test]
    fn test_filter_transaction_pi_exclusive() {
        let env = Env::default();
        let ahi_ai = AhiAiCore::init(env.clone());
        let tx_data = Map::new(&env);
        tx_data.set(Symbol::new(&env, "currency"), Symbol::new(&env, "PI"));
        tx_data.set(Symbol::new(&env, "source"), Symbol::new(&env, "mining"));
        let result = AhiAiCore::filter_transaction(env, tx_data);
        assert!(result, "Should accept PI-exclusive transaction");
    }
}
