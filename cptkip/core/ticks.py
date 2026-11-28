# Allocation-free, wrap-safe millisecond timing.
#
# On CircuitPython time.monotonic_ns() returns values far larger than a small int
# (about +/-2**30 on 32-bit boards), so every call and every add/compare allocates a
# long int on the heap. time.monotonic() returns a 30-bit float whose resolution gets
# worse the longer the board has been running. supervisor.ticks_ms() avoids both: it
# is a millisecond counter that wraps every 2**29 ms (~6.2 days), so it always fits in
# a small int. The helpers below do the wrap-safe arithmetic, following the same
# pattern as the adafruit_ticks library without the dependency.
#
# On a desktop the same wrapping behaviour is emulated so code (and tests) behave the
# same in both environments.
#
# Usage:
#     deadline = ticks_add(ticks_ms(), 500)
#     ...
#     if ticks_less(deadline, ticks_ms()):  # or ticks_diff(ticks_ms(), deadline) >= 0
#         ...
#
import cptkip.core.environment as environment

TICKS_PERIOD = 1 << 29
TICKS_MAX = TICKS_PERIOD - 1
_TICKS_HALF_PERIOD = TICKS_PERIOD // 2

if environment.is_running_on_microcontroller():
    # noinspection PyUnresolvedReferences
    from supervisor import ticks_ms

else:
    from time import monotonic_ns as _monotonic_ns

    def ticks_ms() -> int:
        """
        Returns the current millisecond tick count, wrapping every 2**29 ms, matching
        supervisor.ticks_ms() on CircuitPython.
        """
        return (_monotonic_ns() // 1_000_000) & TICKS_MAX


def ticks_add(ticks: int, delta: int) -> int:
    """
    Returns ticks + delta (milliseconds), wrapped into the tick range. delta must be
    less than half the tick period (~3.1 days) in magnitude.
    """
    return (ticks + delta) & TICKS_MAX


def ticks_diff(ticks1: int, ticks2: int) -> int:
    """
    Returns the signed number of milliseconds from ticks2 to ticks1 (ticks1 - ticks2),
    correctly handling wrap-around. The result is only meaningful when the two values
    are less than half the tick period (~3.1 days) apart.
    """
    diff = (ticks1 - ticks2) & TICKS_MAX
    return ((diff + _TICKS_HALF_PERIOD) & TICKS_MAX) - _TICKS_HALF_PERIOD


def ticks_less(ticks1: int, ticks2: int) -> bool:
    """
    Returns True if ticks1 is before ticks2, correctly handling wrap-around.
    """
    return ticks_diff(ticks1, ticks2) < 0
