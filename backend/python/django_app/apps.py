import os
import json
from django.apps import AppConfig

class DjangoAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_app'

    def ready(self):
        # Avoid double-seeding
        if os.environ.get('RUN_MAIN') == 'true':
            self.seed_categories()

    def seed_categories(self):
        # Avoid circular import errors
        try:
            from django_app.models.models import ProductCategory
            
            base_dir = os.path.dirname(os.path.abspath(__file__))
            json_path = os.path.join(base_dir, 'data', 'categories.json')

            if os.path.exists(json_path):
                with open(json_path, 'r') as f:
                    data = json.load(f)
                
                for item in data:
                    # Get or Create logic for MongoEngine
                    if not ProductCategory.objects(title=item['title']).first():
                        ProductCategory(
                            title=item['title'],
                            description=item.get('description', '')
                        ).save()
                        print(f"🌱 Seeded: {item['title']}")
            else:
                print("🟡 Seed file not found, skipping.")

        except Exception as e:
            # This ensures the server still starts even if seeding fails
            print(f"⚠️ Startup seed failed: {e}")