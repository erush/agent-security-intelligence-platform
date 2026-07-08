def __post_init__(self) -> None:

    self.patterns = AttackPatternMining(self.analytics)

    self.risk = RiskTrends(self.patterns)

    self.guardrails = GuardrailIntelligence(self.risk)

    self.strategy = StrategyRecommendation(
        self.guardrails
    )