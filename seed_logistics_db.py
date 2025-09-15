"""
seed_logistics_db.py
Script to populate demo data into logistics_db for testing and development.
"""
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Import your models here (adjust path as needed)
from app.models import Base, Customer, Warehouse, Route, Driver, Vehicle, Shipment, Tracking, User, Inventory, ShipmentStatusHistory

load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
DB_NAME = "logistics_db"

engine = create_engine(f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{DB_NAME}")
Session = sessionmaker(bind=engine)

if __name__ == "__main__":
    session = Session()
    # Example demo data
    customer = Customer(name="Alice Smith", email="alice@example.com", phone="123-456-7890")
    warehouse = Warehouse(name="Central Warehouse", location="123 Main St")
    route = Route(origin="City A", destination="City B", distance_km=120.5)
    driver = Driver(name="Bob Driver", phone="555-1234", license_number="LIC12345")
    vehicle = Vehicle(plate_number="ABC-123", type="Truck", capacity=1000)
    user = User(username="admin", password="admin", role="admin")
    session.add_all([customer, warehouse, route, driver, vehicle, user])
    session.commit()
    # Add a shipment
    shipment = Shipment(customer_id=customer.id, warehouse_id=warehouse.id, route_id=route.id, driver_id=driver.id, vehicle_id=vehicle.id, status="pending")
    session.add(shipment)
    session.commit()
    print("Demo data seeded into logistics_db.")
    session.close()
