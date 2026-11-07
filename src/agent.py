from typing import Any

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware
from langchain.agents.structured_output import ProviderStrategy

from config.config import MAX_MODEL_CALLS_PER_RUN, hitl_enabled
from llm.factory import build_chat_model
from middlewares import AuditMiddleWare, HITLMiddleware, ProtectionMiddleware
from prompts import build_system_prompt
from schema import TurnSummary
from tools import ALL_TOOLS


def build_middleware(
    *,
    enable_hitl: bool
) -> list[Any]:
    """
    Harness layers, outermost first.
    
    1. model-call cap
    2. Audit log
    3. payload guarding
    4. HITL on write/edit/run
    """

    layers: list[Any] = [
        ModelCallLimitMiddleware(
            run_limit=MAX_MODEL_CALLS_PER_RUN,
            exit_behaviour="end"
        ),
        AuditMiddleWare(),
        ProtectionMiddleware()
    ]
    if enable_hitl:
        layers.append(HITLMiddleware())
    
    return layers


def build_agent(
    *,
    enable_hitl: bool | None = None,
    extra_guidance: str = "",
) -> Any:
    model, provider = build_chat_model()
    use_hitl = enable_hitl if enable_hitl is not None else hitl_enabled()
    
    return create_agent(
        model=model,
        tools=ALL_TOOLS,
        system_prompt=build_system_prompt(extra_guidance=extra_guidance),
        middleware=build_middleware(enable_hitl=use_hitl),
        response_format=ProviderStrategy(TurnSummary),
        name="Toffee"
    )