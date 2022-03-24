from datetime import date

from models.customer import LoyaltyTier

gold_minimum = 50000
silver_minimum = 10000
tier_minimum = {
    LoyaltyTier.gold: 50000,
    LoyaltyTier.silver: 10000,
    LoyaltyTier.bronze: 0,
}


def calculate_tier(total_purchase_in_cents: int) -> LoyaltyTier:
    if total_purchase_in_cents >= tier_minimum[LoyaltyTier.gold]:
        return LoyaltyTier.gold
    elif total_purchase_in_cents >= tier_minimum[LoyaltyTier.silver]:
        return LoyaltyTier.silver

    return LoyaltyTier.bronze


def tier_start_date() -> date:
    return date(date.today().year - 1, 1, 1)


def tier_end_date() -> date:
    return date(date.today().year, 12, 31)


def next_tier(current: LoyaltyTier) -> LoyaltyTier:
    if current == LoyaltyTier.bronze:
        return LoyaltyTier.silver
    return LoyaltyTier.gold
