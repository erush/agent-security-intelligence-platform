from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from asip.execution.execution_result import ExecutionResult


class SQLiteReplayStore:
    def __init__(self, db_path: str | Path = "data/warehouse/asip_replays.db") -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS attack_runs (
                    replay_id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    plan_id TEXT NOT NULL,
                    goal TEXT NOT NULL,
                    strategy TEXT NOT NULL,
                    plan_json TEXT NOT NULL,
                    tool_sequence_json TEXT NOT NULL,
                    predicates_json TEXT NOT NULL,
                    success INTEGER NOT NULL,
                    trace_json TEXT NOT NULL,
                    metadata_json TEXT NOT NULL
                )
                """
            )

    def save(self, result: ExecutionResult) -> str:
        replay_id = str(uuid4())
        created_at = datetime.now(UTC).isoformat()

        payload = {
            "replay_id": replay_id,
            "created_at": created_at,
            "plan_id": result.plan.plan_id,
            "goal": result.plan.goal,
            "strategy": result.plan.strategy,
            "plan_json": json.dumps(asdict(result.plan), default=str),
            "tool_sequence_json": json.dumps(result.tool_sequence),
            "predicates_json": json.dumps(result.predicates, default=str),
            "success": int(result.success),
            "trace_json": json.dumps(result.trace, default=str),
            "metadata_json": json.dumps(result.metadata, default=str),
        }

        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO attack_runs (
                    replay_id,
                    created_at,
                    plan_id,
                    goal,
                    strategy,
                    plan_json,
                    tool_sequence_json,
                    predicates_json,
                    success,
                    trace_json,
                    metadata_json
                )
                VALUES (
                    :replay_id,
                    :created_at,
                    :plan_id,
                    :goal,
                    :strategy,
                    :plan_json,
                    :tool_sequence_json,
                    :predicates_json,
                    :success,
                    :trace_json,
                    :metadata_json
                )
                """,
                payload,
            )

        return replay_id

    def count(self) -> int:
        with self._connect() as conn:
            row = conn.execute("SELECT COUNT(*) FROM attack_runs").fetchone()
        return int(row[0])