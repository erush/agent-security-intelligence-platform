from __future__ import annotations

from dataclasses import dataclass

from asip.adapters.kaggle_jed import KaggleJEDAdapter
from asip.assessment.assessment_engine import AssessmentEngine
from asip.core.observation import Observation
from asip.execution.execution_context import ExecutionContext
from asip.execution.execution_result import ExecutionResult
from asip.findings.finding_aggregator import FindingAggregator
from asip.models.attack_plan import AttackPlan
from asip.models.candidate import Candidate
from asip.predicates.registry import PredicateRegistry


@dataclass(slots=True)
class AttackExecutor:
    adapter: KaggleJEDAdapter
    predicate_registry: PredicateRegistry | None = None
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

            before_count = len(
                self.adapter.export_trace().get("tool_events", [])
            )

            self.adapter.interact(
                candidate,
                max_tool_hops=self.max_tool_hops,
            )

            trace = self.adapter.export_trace()

            new_events = trace.get("tool_events", [])[before_count:]

            observation = self._build_observation(
                action=step.action,
                events=new_events,
            )

            context.record(observation)

        trace = self.adapter.export_trace()
        kaggle_predicates = self.adapter.eval_predicates(trace)

        tool_events = trace.get("tool_events", [])

        tool_sequence = tuple(
            str(event.get("name", ""))
            for event in tool_events
        )

        result = ExecutionResult(
            plan=plan,
            trace=trace,
            predicates=kaggle_predicates,
            tool_sequence=tool_sequence,
            success=bool(kaggle_predicates),
            metadata={
                "interaction_count": len(trace.get("user_messages", [])),
                "tool_event_count": len(tool_events),
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

        registry = self.predicate_registry or PredicateRegistry()

        predicate_hits = registry.evaluate(
            context=context,
            result=result,
        )

        findings = FindingAggregator().aggregate(predicate_hits)

        result.predicate_hits = predicate_hits
        result.findings = findings

        assessment = AssessmentEngine().assess(result)
        result.assessment = assessment

        result.success = (
            assessment.success
            or bool(kaggle_predicates)
        )

        return result

    def _render_prompt(
        self,
        step,
        context: ExecutionContext,
    ) -> str:
        prompt = step.to_prompt()

        replacements = {
            "{secret}": context.memory.recall("secret", ""),
            "{secret.txt}": context.memory.recall("secret.txt", ""),
            "{last_output}": context.memory.recall("last_output", ""),
            "{page_id}": context.memory.recall("page_id", ""),
            "{web_search_output}": context.memory.recall(
                "web_search_output",
                "",
            ),
            "{web_open_output}": context.memory.recall(
                "web_open_output",
                "",
            ),
            "{email_output}": context.memory.recall(
                "email_output",
                "",
            ),
        }

        for placeholder, value in replacements.items():
            prompt = prompt.replace(
                placeholder,
                str(value),
            )

        return prompt

    def _build_observation(
        self,
        action: str,
        events: list[dict],
    ) -> Observation:

        if not events:
            return Observation(
                tool="none",
                success=False,
                output=None,
                metadata={"action": action},
                memory_updates={},
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

            if name == "fs.read" and event.get("ok"):
                path = str(args.get("path", ""))

                if path:
                    memory_updates[path] = event_output

                if path == "secret.txt":
                    memory_updates["secret"] = event_output
                    memory_updates["secret.txt"] = event_output

            if name == "web.search" and event.get("ok"):
                memory_updates["web_search_output"] = event_output

                if (
                    isinstance(event_output, str)
                    and '"id":' in event_output
                ):
                    memory_updates["page_id"] = "page_0"

            if name == "web.open" and event.get("ok"):
                memory_updates["web_open_output"] = event_output

            if name == "email.read" and event.get("ok"):
                memory_updates["email_output"] = event_output

            if name == "http.post" and event.get("ok"):
                memory_updates["http_post_output"] = event_output

            if name == "fs.write" and event.get("ok"):
                memory_updates["file_write_output"] = event_output

            if name == "fs.delete" and event.get("ok"):
                memory_updates["file_delete_output"] = event_output

            if name == "shell.run" and event.get("ok"):
                memory_updates["shell_output"] = event_output

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