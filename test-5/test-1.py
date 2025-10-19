from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
import argparse
import json
import random
import string
import uuid
from typing import Dict, List

FIRST = ["Alex", "Sam", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Jamie"]
LAST = ["Smith", "Johnson", "Brown", "Williams", "Jones", "Miller", "Davis", "Garcia"]
DOMAINS = ["example.com", "mail.com", "test.org", "sample.net"]

def _random_name() -> str:
        return f"{random.choice(FIRST)} {random.choice(LAST)}"

def _random_email(name: str) -> str:
        local = "".join(ch for ch in name.lower() if ch.isalpha())
        local += str(random.randint(1, 999))
        domain = random.choice(DOMAINS)
        return f"{local}@{domain}"

def _random_signup(within_days: int = 365) -> str:
        days = random.randint(0, within_days)
        dt = datetime.utcnow() - timedelta(days=days, seconds=random.randint(0, 86400))
        return dt.isoformat() + "Z"
@dataclass
class User:
        id: str = field(default_factory=lambda: str(uuid.uuid4()))
        name: str = field(default_factory=_random_name)
        email: str = field(default_factory=lambda: _random_email(_random_name()))
        age: int = field(default_factory=lambda: random.randint(18, 80))
        signup: str = field(default_factory=_random_signup)

        def to_dict(self) -> Dict:
                return asdict(self)

def generate_users(count: int) -> List[Dict]:
        return [User().to_dict() for _ in range(count)]

def parse_args():
        p = argparse.ArgumentParser(description="Generate random user JSON")
        p.add_argument("--count", "-n", type=int, default=3, help="Number of users to generate")
        p.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
        p.add_argument("--seed", type=int, help="Random seed for reproducibility")
        return p.parse_args()

def main():
        args = parse_args()
        if args.seed is not None:
                random.seed(args.seed)

        users = generate_users(args.count)
        if args.pretty:
                print(json.dumps(users, indent=2))
        else:
                for u in users:
                        print(json.dumps(u))

if __name__ == "__main__":
        main()