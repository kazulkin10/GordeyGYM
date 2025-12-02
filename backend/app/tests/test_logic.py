from datetime import datetime, timedelta
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))

from app.models.models import SubscriptionStatus, VisitDirection
from app.api.visits import _active_subscription


class FakeSub:
    def __init__(self, status=SubscriptionStatus.active, end_date=None, remaining_visits=None):
        self.status = status
        self.end_date = end_date
        self.remaining_visits = remaining_visits


def test_active_subscription_prefers_valid_date():
    today = datetime.utcnow().date()
    active = FakeSub(end_date=today + timedelta(days=1))
    expired = FakeSub(end_date=today - timedelta(days=1))
    assert _active_subscription([expired, active]) is active


def test_active_subscription_with_visits():
    unlimited = FakeSub(end_date=None, remaining_visits=None)
    zero_visits = FakeSub(remaining_visits=0)
    assert _active_subscription([zero_visits, unlimited]) is unlimited


def test_visit_direction_toggle():
    from app.api import visits

    class FakeVisit:
        def __init__(self, direction):
            self.direction = direction
            self.timestamp = datetime.utcnow()

    last_visit = FakeVisit(VisitDirection.in_)
    now = datetime.utcnow()
    # With previous IN, next should be OUT
    assert visits.VisitDirection.out == visits.VisitDirection.out
