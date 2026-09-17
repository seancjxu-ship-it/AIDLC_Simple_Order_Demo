Feature: Idempotent order cancellation / 幂等取消订单

  Scenario: First cancellation succeeds / 首次取消成功
    Given order ORDER-1001 is PAID
    When it is cancelled with idempotency key KEY-001
    Then the status is CANCELLED
    And one audit event exists

  Scenario: Duplicate request is replayed / 重复请求被重放
    Given KEY-001 already cancelled ORDER-1001
    When the same request is sent again with KEY-001
    Then the original response is returned
    And only one audit event exists

  Scenario: Missing key is rejected / 缺少幂等键时拒绝请求
    Given order ORDER-1001 is PAID
    When cancellation is requested without an idempotency key
    Then the error is IDEMPOTENCY_KEY_REQUIRED

