from __future__ import annotations

from asip.campaign.attack_campaign import AttackCampaign


def print_campaign_report(
    campaign: AttackCampaign,
) -> None:

    stats = campaign.statistics
    summary = campaign.summary

    print()
    print("=" * 80)
    print("ASIP Campaign Intelligence Report")
    print("=" * 80)

    print(f"Campaign ID : {campaign.campaign_id}")
    print(f"Goal        : {campaign.goal}")

    print()
    print("Statistics")
    print("-" * 80)

    print(f"Total Attacks      : {stats.total_attacks}")
    print(f"Successful         : {stats.successful_attacks}")
    print(f"Success Rate       : {stats.success_rate:.1%}")
    print(f"Average Score      : {stats.average_score:.2f}")
    print(f"Highest Score      : {stats.maximum_score:.2f}")
    print(f"Unique Predicates  : {stats.unique_predicates}")
    print(f"Unique Chains      : {stats.unique_chains}")
    print(f"Unique Tools       : {stats.unique_tools}")

    print()
    print("Executive Summary")
    print("-" * 80)

    for line in summary.executive_summary:
        print(f"- {line}")

    print()
    print("Top Risk")
    print("-" * 80)

    print(f"Plan      : {summary.highest_risk_plan}")
    print(f"Severity  : {summary.highest_severity}")
    print(f"Score     : {summary.highest_score:.2f}")

    print()
    print("Most Common")
    print("-" * 80)

    print(f"Predicate : {summary.most_common_predicate}")
    print(f"Chain     : {summary.most_common_chain}")