from flask import Flask, request, jsonify
from flasgger import Swagger

app = Flask(__name__)

app.config['SWAGGER'] = {
    'openapi': '3.0.0',
    'title': 'Телефонная книга API',
    'description': 'API для управления телефонными контактами',
    'version': '1.0.0'
}

Swagger(app)

# Словарь для хранения контактов
contacts = {}
# Счетчик для ID контакта
current_id = 1


@app.route('/contacts', methods=['POST'])
def create_contact():
    """
    Создание нового контакта
    ---
    tags:
      - Контакты
    description: |
      Этот эндпоинт позволяет создать новый контакт.
      Требуются обязательные поля name и phone.
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - name
              - phone
            properties:
              name:
                type: string
                description: Имя контакта
                example: "Сидр Сидоров"
              phone:
                type: string
                description: Номер телефона
                example: "+79123456789"
    responses:
      201:
        description: Контакт создан
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                  description: Уникальный идентификатор контакта
                name:
                  type: string
                phone:
                  type: string
      400:
        description: Ошибка в данных запроса
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
    """
    global current_id

    try:
        data = request.json

        # Проверка обязательных полей
        if not data or 'name' not in data or 'phone' not in data:
            return jsonify({'error': 'Требуются поля name и phone'}), 400

        # Создание нового контакта
        new_contact = {
            'id': current_id,
            'name': data['name'],
            'phone': data['phone']
        }

        # Сохранение контакта
        contacts[current_id] = new_contact
        current_id += 1

        return jsonify(new_contact), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/contacts/<int:contact_id>', methods=['GET'])
def get_contact(contact_id):
    """
    Получение информации о контакте
    ---
    tags:
      - Контакты
    description: Возвращает полную информацию о контакте по его уникальному идентификатору.
    parameters:
      - name: contact_id
        in: path
        required: true
        description: Уникальный идентификатор контакта
        schema:
          type: integer
          format: int64
        example: 1
    responses:
      200:
        description: Контакт найден
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                phone:
                  type: string
      404:
        description: Контакт не найден
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
    """
    contact = contacts.get(contact_id)

    if not contact:
        return jsonify({'error': 'Контакт не найден'}), 404

    return jsonify(contact), 200


@app.route('/contacts/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    """
    Удаление контакта
    ---
    tags:
      - Контакты
    description: Удаляет контакт из телефонной книги по его уникальному идентификатору.
    parameters:
      - name: contact_id
        in: path
        required: true
        description: Уникальный идентификатор контакта
        schema:
          type: integer
          format: int64
        example: 1
    responses:
      200:
        description: Контакт успешно удален
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                contact:
                  type: object
      404:
        description: Контакт не найден
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
    """
    if contact_id not in contacts:
        return jsonify({'error': 'Контакт не найден'}), 404

    deleted_contact = contacts.pop(contact_id)
    return jsonify({'message': 'Контакт удален', 'contact': deleted_contact}), 200


if __name__ == '__main__':
    app.run()