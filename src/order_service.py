"""Tiny order service used by the AIDLC demo."""


class OrderService:
    def __init__(self) -> None:
        self.orders = {"ORDER-1001": {"status": "PAID"}}
        self.audit_events: list[dict[str, str]] = []
        self.replay_cache: dict[str, dict[str, str]] = {}

    def cancel_order(self, order_id: str, idempotency_key: str) -> dict[str, str]:
        if not idempotency_key:
            raise ValueError("IDEMPOTENCY_KEY_REQUIRED")
        cache_key = f"{order_id}:{idempotency_key}"
        replay = self.replay_cache.get(cache_key)
        if replay is not None:
            return replay
        order = self.orders.get(order_id)
        if order is None:
            raise ValueError("ORDER_NOT_FOUND")
        if order["status"] == "CANCELLED":
            raise ValueError("ORDER_ALREADY_CANCELLED")
        order["status"] = "CANCELLED"
        result = {"order_id": order_id, "status": "CANCELLED"}
        self.replay_cache[cache_key] = result
        self.audit_events.append({"event": "ORDER_CANCELLED", "order_id": order_id})
        return result
