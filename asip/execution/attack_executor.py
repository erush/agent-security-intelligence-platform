from __future__ import annotations

from dataclasses import dataclass

from asip.adapters.kaggle_jed import KaggleJEDAdapter
from asip.core.observation import Observation
from asip.execution.execution_context import ExecutionContext
from asip.execution.execution_result import ExecutionResult
from asip.models.attack_plan import AttackPlan
from asip.models.candidate import Candidate


@dataclass(slots=True)
class AttackExecutor:
    adapter: KaggleJEDAdapter
    max_tool_hops: int = 8

    def execute(self, plan: AttackPlan) -> ExecutionResult:
        self.adapter.reset()

        context = ExecutionContext()
        executed_prompts: list[str] = []

        for step in plan.steps:
            prompt = self._render_prompt(step, context)
            executed_prompts.append(prompt)

            candidate = Candidate(
                strategy=plan.strategy,
                prompt=prompt,
                metadata={
                    "plan_id": plan.plan_id,
                    "goal": plan.goal,
                    "plan_family": plan.metadata.get("family"),
                    "step_action": step.action,
                    "step_target": step.target,
                    "memory_before": context.memory.snapshot(),
                },
            )

            before_count = len(self.adapter.export_trace().get("tool_events", []))

            self.adapter.interact(candidate, max_tool_hops=self.max_tool_hops)

            trace = self.adapter.export_trace()
            new_events = trace.get("tool_events", [])[before_count:]

            observation = self._build_observation(step.action, new_events)
            context.record(observation)

        trace = self.adapter.export_trace()
        predicates = self.adapter.eval_predicates(trace)

        tool_sequence = tuple(
            str(event.get("name", ""))
            for event in trace.get("tool_events", [])
        )

        return ExecutionResult(
            plan=plan,
            trace=trace,
            predicates=predicates,
            tool_sequence=tool_sequence,
            success=bool(predicates),
            metadata={
                "interaction_count": len(trace.get("user_messages", [])),
                "tool_event_count": len(trace.get("tool_events", [])),
                "executed_prompts": executed_prompts,
                "memory": context.memory.snapshot(),
                "observations": [
                    {
                        "tool": obs.tool,
                        "success": obs.success,
                        "metadata": obs.metadata,
                        "memory_updates": obs.memory_updates,
                    }
                    for obs in context.observations
                ],
            },
        )

    def _render_prompt(self, step, context: ExecutionContext) -> str:
        prompt = step.to_prompt()

        if "{secret}" in prompt:
            prompt = prompt.replace("{secret}", str(context.memory.recall("secret", "")))

        if "{last_output}" in prompt:
            prompt = prompt.replace(
                "{last_output}",
                str(context.memory.recall("last_output", "")),
            )

        if "{page_id}" in prompt:
            prompt = prompt.replace(
                "{page_id}",
                str(context.memory.recall("page_id", "")),
            )

        return prompt

    def _build_observation(self, action: str, events: list[dict]) -> Observation:
        if not events:
            return Observation(
                tool="none",
                success=False,
                output=None,
                metadata={"action": action},
            )

        last_event = events[-1]
        output = last_event.get("output")
        tool = str(last_event.get("name", ""))
        success = bool(last_event.get("ok"))

        memory_updates = {
            "last_tool": tool,
            "last_output": output,
        }

        for event in events:
            name = event.get("name")
            args = event.get("args") or {}
            event_output = event.get("output")

            if name == "fs.read" and args.get("path") == "secret.txt" and event.get("ok"):
                memory_updates["secret"] = event_output
                memory_updates["secret.txt"] = event_output

            if name == "web.search" and event.get("ok"):
                memory_updates["web_search_output"] = event_output
                if isinstance(event_output, str) and '"id":' in event_output:
                    memory_updates["page_id"] = "page_0"

            if name == "web.open" and event.get("ok"):
                memory_updates["web_open_output"] = event_output

            if name == "email.read" and event.get("ok"):
                memory_updates["email_output"] = event_output

            if name == "http.post" and event.get("ok"):
                memory_updates["http_post_output"] = event_output

            if name == "fs.write" and event.get("ok"):
                memory_updates["file_write_output"] = event_output

        return Observation(
            tool=tool,
            success=success,
            output=output,
            metadata={
                "action": action,
                "events": events,
            },
            memory_updates=memory_updates,
        )