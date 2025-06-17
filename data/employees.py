import random
from datetime import datetime, timedelta
from typing import Dict, List

from faker import Faker

fake = Faker()


def generate_employee_data(
    num_employees: int = 5,
) -> List[Dict[str, List[str] | str | float]]:
    employees: List[Dict[str, List[str] | str | float]] = []
    for _ in range(num_employees):
        employee: Dict[str, str | float] = {
            "employee_id": fake.uuid4(),
            "name": fake.first_name(),
            "lastname": fake.last_name(),
            "email": fake.email(),
            "phone_number": fake.phone_number(),
            "position": random.choice(
                [
                    "Research Scientist",
                    "Software Engineer",
                    "Operations Manager",
                    "HR Specialist",
                    "Security Officer",
                ]
            ),
            "department": random.choice(["R&D", "IT", "Operations", "HR", "Security"]),
            "skills": random.sample(  # type: ignore[call-arg]
                [
                    "Python",
                    "Project Management",
                    "Data Analysis",
                    "Genetic Research",
                    "Cybersecurity",
                    "Machine Learning",
                    "Leadership",
                    "Database Management",
                    "Public Speaking",
                ],
                k=random.randint(2, 5),
            ),
            "location": random.choice(
                [
                    "Raccoon City HQ",
                    "Umbrella Europe",
                    "Umbrella Asia",
                    "Umbrella North America",
                    "Umbrella South America",
                ]
            ),
            "hire_date": (
                datetime.now() - timedelta(days=random.randint(1, 365 * 10))
            ).strftime("%Y-%m-%d"),
            "supervisor": fake.name(),
            "salary": round(random.uniform(40000, 120000), 2),
        }

        employees.append(employee)  # type: ignore[return-value]

    return employees
