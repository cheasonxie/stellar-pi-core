#[cfg(test)]
mod test_pi_stablecoin_manager {
    use soroban_sdk::testutils::Env;
    use crate::pi_stablecoin_manager::PiStablecoinManager;
    use crate::ahi_ai_core::AhiAiCore;
    use soroban_sdk::Symbol;

    #[test]
    fn test_create_pi_transaction() {
        let env = Env::default();
        let ahi_ai = AhiAiCore::init(env.clone());
        let pi_manager = PiStablecoinManager::init(env.clone(), ahi_ai);
        let result = PiStablecoinManager::create_pi_transaction(env, Symbol::new(&env, "recipient"), 100, Symbol::new(&env, "mining"));
        assert!(result, "Should create valid PI transaction");
    }

    #[test]
    fn test_get_balance() {
        let env = Env::default();
        let ahi_ai = AhiAiCore::init(env.clone());
        let pi_manager = PiStablecoinManager::init(env.clone(), ahi_ai);
        let balance = PiStablecoinManager::get_balance(env);
        assert_eq!(balance, 1000, "Balance should be 1000");
    }
}
