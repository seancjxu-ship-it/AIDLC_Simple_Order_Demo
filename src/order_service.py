"""Tiny order service used by the AIDLC demo. / AIDLC演示使用的极简订单服务。"""


class OrderService:
    """In-memory service with an intentionally incomplete baseline.

    内存订单服务；初始基线故意保留未完成的幂等能力。
    """

    def __init__(self) -> None:
        self.orders = {"ORDER-1001": {"status": "PAID"}}
        self.audit_events: list[dict[str, str]] = []
        self.replay_cache: dict[str, dict[str, str]] = {}

    def cancel_order(self, order_id: str, idempotency_key: str) -> dict[str, str]:
        """Cancel a paid order. / 取消一个已支付订单。"""

        # REQ-KEY: Reject an empty idempotency key before any state change.
        # REQ-KEY：在修改状态之前拒绝空的幂等键。
        if not idempotency_key:
            raise ValueError("IDEMPOTENCY_KEY_REQUIRED")

        # REQ-REPLAY / REQ-AUDIT: Return the cached response for a repeated key
        # without creating a second audit event. This check must precede the
        # CANCELLED-state check so duplicates are replayed, not rejected.
        # REQ-REPLAY / REQ-AUDIT：对重复幂等键返回缓存响应，不产生第二条审计事件。
        # 此检查必须位于CANCELLED状态检查之前，否则重复请求会被拒绝而非重放。
        if idempotency_key in self.replay_cache:
            return self.replay_cache[idempotency_key]

        # REQ-NOT-FOUND: An unknown order returns ORDER_NOT_FOUND.
        # REQ-NOT-FOUND：未知订单返回ORDER_NOT_FOUND。
        order = self.orders.get(order_id)
        if order is None:
            raise ValueError("ORDER_NOT_FOUND")
        if order["status"] == "CANCELLED":
            raise ValueError("ORDER_ALREADY_CANCELLED")

        # REQ-CANCEL: Change PAID to CANCELLED, create one audit event, and
        # cache the response so subsequent replays return the original result.
        # REQ-CANCEL：将PAID改为CANCELLED，生成一条审计事件，并缓存响应以便重放。
        order["status"] = "CANCELLED"
        result = {"order_id": order_id, "status": "CANCELLED"}
        self.audit_events.append({"event": "ORDER_CANCELLED", "order_id": order_id})
        self.replay_cache[idempotency_key] = result
        return result
