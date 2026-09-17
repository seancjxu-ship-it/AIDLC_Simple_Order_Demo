import unittest

from src.order_service import OrderService


class CancelOrderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = OrderService()

    def test_first_cancel_succeeds(self) -> None:
        result = self.service.cancel_order("ORDER-1001", "KEY-001")
        self.assertEqual({"order_id": "ORDER-1001", "status": "CANCELLED"}, result)
        self.assertEqual(1, len(self.service.audit_events))

    def test_duplicate_key_replays_same_result_without_duplicate_audit(self) -> None:
        first = self.service.cancel_order("ORDER-1001", "KEY-001")
        second = self.service.cancel_order("ORDER-1001", "KEY-001")
        self.assertEqual(first, second)
        self.assertEqual(1, len(self.service.audit_events))

    def test_missing_idempotency_key_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "IDEMPOTENCY_KEY_REQUIRED"):
            self.service.cancel_order("ORDER-1001", "")

    def test_unknown_order_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "ORDER_NOT_FOUND"):
            self.service.cancel_order("ORDER-404", "KEY-404")


if __name__ == "__main__":
    unittest.main()

