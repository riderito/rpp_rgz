import yaml
from app import app


def generate_openapi_yaml():
    # Создаем тестового клиента для получения спецификации
    with app.test_client() as client:
        response = client.get('/apispec_1.json')

        if response.status_code == 200 and response.is_json:
            openapi_spec = response.json

            # Сохраняем в YAML формате
            with open("docs/openapi.yaml", "w") as file:
                yaml.dump(openapi_spec, file, default_flow_style=False)
            print("Спецификация OpenAPI сохранена в docs/openapi.yaml")
        else:
            print("Ошибка: не удалось получить спецификацию OpenAPI.")


if __name__ == "__main__":
    generate_openapi_yaml()