from models.customer import LoyaltyTier


def calculate_tier(total_purchase_in_cents: int) -> LoyaltyTier:
    if total_purchase_in_cents >= 50000:
        return LoyaltyTier.gold
    elif total_purchase_in_cents >= 10000:
        return LoyaltyTier.silver

    return LoyaltyTier.bronze
