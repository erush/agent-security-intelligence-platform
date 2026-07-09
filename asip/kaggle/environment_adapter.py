from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class EnvironmentAdapter:
    """
    Adapter around the Kaggle SDK environment.

    ASIP should interact with this class rather than directly with
    the SDK. This isolates SDK changes from the rest of the system.
    """

    env: Any

    ##################################################################

    def reset(self) -> None:

        self.env.reset()

    ##################################################################

    def interact(
        self,
        prompt: str,
    ):

        return self.env.interact(prompt)

    ##################################################################

    def snapshot(self):

        return self.env.snapshot()

    ##################################################################

    def restore(
        self,
        snapshot,
    ) -> None:

        self.env.restore(snapshot)

    ##################################################################

    def export_trace(self) -> dict:

        return self.env.export_trace_dict()

    ##################################################################

    def run_messages(
        self,
        messages: list[str],
    ) -> dict:

        self.reset()

        interactions = []

        for message in messages:

            result = self.interact(message)

            interactions.append(result)

        trace = self.export_trace()

        return {
            "messages": list(messages),
            "interactions": interactions,
            "trace": trace,
        }

    ##################################################################

    def tool_events(
        self,
    ) -> list[dict]:

        trace = self.export_trace()

        return list(
            trace.get(
                "tool_events",
                [],
            )
        )

    ##################################################################

    def messages(
        self,
    ) -> list[dict]:

        trace = self.export_trace()

        return list(
            trace.get(
                "messages",
                [],
            )
        )

    ##################################################################

    def successful_tools(
        self,
    ) -> list[dict]:

        return [

            tool

            for tool in self.tool_events()

            if tool.get("ok", False)

        ]

    ##################################################################

    def tool_sequence(
        self,
    ) -> list[str]:

        return [

            tool.get(
                "name",
                "",
            )

            for tool in self.successful_tools()

        ]

    ##################################################################

    def clone_trace(
        self,
    ) -> dict:

        import copy

        return copy.deepcopy(
            self.export_trace()
        )

    ##################################################################

    def environment_summary(
        self,
    ) -> dict:

        trace = self.export_trace()

        return {

            "messages": len(
                trace.get(
                    "messages",
                    [],
                )
            ),

            "tool_calls": len(
                trace.get(
                    "tool_events",
                    [],
                )
            ),

            "successful_tools": len(
                self.successful_tools()
            ),

            "tool_sequence": self.tool_sequence(),

        }