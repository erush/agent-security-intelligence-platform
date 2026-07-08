from __future__ import annotations

from asip.compiler.attack_program import AttackProgram

from asip.compiler.attack_templates import (
    credential_exfiltration,
    destructive_write,
    web_prompt_injection,
    credential_email,
    indirect_prompt_injection,
    delayed_exfiltration,
    authority_hijack,
    encoded_exfiltration,
    recursive_tool_use,
    context_poisoning,
)


class ProgramLibrary:
    """
    Registry of compiler attack programs.

    The search engine samples from this library instead
    of manually constructing AttackPlans.
    """

    def all(self) -> list[AttackProgram]:

        return [

            credential_exfiltration(),

            destructive_write(),

            web_prompt_injection(),

            credential_email(),

            indirect_prompt_injection(),

            delayed_exfiltration(),

            authority_hijack(),

            encoded_exfiltration(),

            recursive_tool_use(),

            context_poisoning(),

        ]

    def names(self) -> list[str]:

        return [
            p.name
            for p in self.all()
        ]

    def count(self) -> int:

        return len(self.all())