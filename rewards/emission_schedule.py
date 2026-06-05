# XGold Emission Schedule & Harvesting Integration

# This module defines how XGold is emitted over time
# and how harvesting claims from XGoldNet translate into minted rewards.

class XGoldEmission:
    def __init__(self):
        self.base_daily_emission = 100_000  # Base daily XGold emission
        self.halving_cycle_days = 365 * 2   # Example: halving every 2 years
        self.days_since_launch = 0

    def get_current_daily_emission(self):
        halvings = self.days_since_launch // self.halving_cycle_days
        return self.base_daily_emission / (2 ** halvings)

    def calculate_harvest_reward(self, claim: dict, node_reputation: float):
        """
        Calculate reward for a harvesting claim.
        This would be called after Nexus validates a claim from XGoldNet.
        """
        base_reward = claim.get('bandwidth_gb', 0) * 0.7
        reputation_bonus = node_reputation * 0.3
        special_task_bonus = claim.get('special_tasks', 0) * 25

        total_reward = base_reward + reputation_bonus + special_task_bonus
        return round(total_reward, 2)

    def process_validated_claim(self, node_id: str, claim: dict, reputation: float):
        """Main entry point from XGoldNet / Nexus when a claim is approved."""
        reward = self.calculate_harvest_reward(claim, reputation)
        # In real system: call minting function here
        print(f"[Emission] Node {node_id} earned {reward} XGold from harvesting")
        return {
            "node_id": node_id,
            "reward": reward,
            "claim_period": claim.get('period')
        }