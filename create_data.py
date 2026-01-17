import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realestate_chatbot.settings')
django.setup()

from chatbot.models import House, Place, HouseDistance

def create_data():
    # Clean up
    House.objects.all().delete()
    Place.objects.all().delete()
    HouseDistance.objects.all().delete()

    print("Creating test data...")

    # Create House
    house = House.objects.create(
        name="Sunny Villa",
        location="123 Example St",
        price="$500,000",
        description="A beautiful 3-bedroom villa."
    )

    # Create Places
    hospital = Place.objects.create(name="City Hospital", category="medical")
    school = Place.objects.create(name="Greenwood High", category="school")
    metro = Place.objects.create(name="Central Metro", category="transportation")

    # Create Distances (NO Mall created, so Shopping will be missing)
    HouseDistance.objects.create(house=house, place=hospital, distance_in_meters=500)
    HouseDistance.objects.create(house=house, place=school, distance_in_meters=1200)
    HouseDistance.objects.create(house=house, place=metro, distance_in_meters=300)

    print(f"Data created. House ID: {house.id}")

if __name__ == "__main__":
    create_data()
