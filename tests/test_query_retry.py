import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import asyncio
from unittest.mock import AsyncMock, patch
from tenacity import RetryCallState, stop_after_attempt, wait_exponential
from exchanges.base import query_retry


# Test exception classes
class NetworkError(Exception):
    pass

class BusinessError(Exception):
    pass

# Case 1: Success path should not trigger retries
@query_retry(default_return='failed')
async def success_function():
    return "success"

# Case 2: Exceptions within exception_type (e.g., network timeout) should trigger retries
@query_retry(default_return="default", max_attempts=3)
async def network_error_function():
    # raise NetworkError("Simulated network error")
    raise asyncio.TimeoutError()

# Case 3: Exceptions outside exception_type should be raised immediately
@query_retry(default_return=0, exception_type=(NetworkError,))
async def business_error_function():
    raise BusinessError("Business error")

# Case 4: Validate backoff timing configuration
@query_retry(default_return=None, min_wait=1, max_wait=5, exception_type=(NetworkError,))
async def timing_function():
    raise NetworkError()

# Main test runner
async def run_tests():
    
    print("\n=== Test 1: Normal execution ===")
    result = await success_function()
    print(f"Result: {result} (expected: 'success')")
    
    print("\n=== Test 2: exception_type match (network) triggers retries ===")
    start_time = asyncio.get_event_loop().time()
    result = await network_error_function()
    duration = asyncio.get_event_loop().time() - start_time
    print(f"Result: {result} (expected: 'default')")
    print(f"Duration: {duration:.2f}s (≈2 retry waits expected)")
    
    print("\n=== Test 3: exception_type mismatch raises immediately ===")
    start_time = asyncio.get_event_loop().time()
    try:
        result = await business_error_function()
    except BusinessError as e:
        result = e
        duration = asyncio.get_event_loop().time() - start_time
        print(f"Result: {result} (expected: 0)")
        print(f"Duration: {duration:.2f}s (should be ~0s)")
    
    print("\n=== Test 4: Backoff timing validation ===")
    with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
        await timing_function()
        # Verify exponential backoff sleeps
        expected_waits = [1, 2, 4, 5]  # waits after attempts 1, 2, 3, capped at max_wait
        actual_waits = [call.args[0] for call in mock_sleep.call_args_list]
        print(f"Actual waits: {actual_waits}")
        print(f"Expected waits: {expected_waits[:len(actual_waits)]}")

if __name__ == "__main__":
    asyncio.run(run_tests())