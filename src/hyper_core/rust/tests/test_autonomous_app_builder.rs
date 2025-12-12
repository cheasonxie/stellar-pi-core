#[cfg(test)]
mod test_autonomous_app_builder {
    use soroban_sdk::testutils::Env;
    use crate::autonomous_app_builder::AutonomousAppBuilder;
    use crate::ahi_ai_core::AhiAiCore;
    use crate::pi_stablecoin_manager::PiStablecoinManager;
    use soroban_sdk::{Symbol, Map};

    #[test]
    fn test_generate_app_no_gambling() {
        let env = Env::default();
        let ahi_ai = AhiAiCore::init(env.clone());
        let pi_manager = PiStablecoinManager::init(env.clone(), ahi_ai.clone());
        let app_builder = AutonomousAppBuilder::init(env.clone(), ahi_ai, pi_manager);
        let app_spec = Map::new(&env);
        app_spec.set(Symbol::new(&env, "description"), Symbol::new(&env, "gambling app"));
        let result = AutonomousAppBuilder::generate_app(env, app_spec);
        assert!(result.is_none(), "Should reject gambling app");
    }

    #[test]
    fn test_generate_app_valid() {
        let env = Env::default();
        let ahi_ai = AhiAiCore::init(env.clone());
        let pi_manager = PiStablecoinManager::init(env.clone(), ahi_ai.clone());
        let app_builder = AutonomousAppBuilder::init(env.clone(), ahi_ai, pi_manager);
        let app_spec = Map::new(&env);
        app_spec.set(Symbol::new(&env, "description"), Symbol::new(&env, "PI wallet app"));
        let result = AutonomousAppBuilder::generate_app(env, app_spec);
        assert!(result.is_some(), "Should generate valid app");
    }
}
