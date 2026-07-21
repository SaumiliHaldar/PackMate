# PackMate - Box Selection System
A Django-based system for ecommerce warehouses. Given an order (products + quantities), PackMate intelligently recommends the **cheapest shipping box** that fits everything, complete with a beautiful dark-mode dashboard and built-in authentication.


## Features
- **Smart Box Selection Algorithm**: Considers weight, volume, and sorted dimensions to ensure products fit properly and cost effectively.
- **Premium Dashboard UI**: A fully responsive, modern dark-mode frontend to manage orders, boxes, and products.
- **Authentication System**: Secure login and sign-up functionality using Django's built-in auth system.
- **RESTful API**: Fully functional endpoints to integrate with external systems.
- **Robust Testing**: 25 comprehensive unit and integration tests covering all edge cases.


## Setup & Installation

**1. Clone the repository**
```bash
git clone https://github.com/SaumiliHaldar/PackMate.git
cd PackMate
```

**2. Create and activate a virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run database migrations**
```bash
python manage.py migrate
```

**5. Start the development server**
```bash
python manage.py runserver
```
Navigate to `http://127.0.0.1:8000` to view the application! You will be prompted to create an account or log in to view the dashboard.


## Running Tests

The system comes with 25 tests (10 selector unit tests + 15 API integration tests).

```bash
python manage.py test packing.tests --verbosity=2
```
*Note: Test output has been successfully exported to `TEST_OUTPUT.md`.*


## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET/POST | `/products/` | List or create products |
| GET/POST | `/boxes/` | List or create boxes |
| GET/POST | `/orders/` | List or create orders |
| GET | `/orders/<id>/recommend/` | Get recommended box for an order |

### Example: Create a product
```bash
curl -X POST http://127.0.0.1:8000/products/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Laptop","length":35,"width":25,"height":5,"weight":2.5}'
```

### Example: Get a recommendation
```bash
curl http://127.0.0.1:8000/orders/1/recommend/
```
Returns `404` with `{"detail": "No suitable box found for this order."}` if nothing fits.


## Box Selection Algorithm

PackMate uses a **conservative approximation** to solve the 3D bin-packing problem:
1. **Weight check** — `box.max_weight >= total order weight`
2. **Per-item dimension check** — every product's sorted dimensions must fit within the box's sorted inner dimensions (prevents long items from being placed in square boxes despite passing volume checks).
3. **Volume guard** — `sum of all item volumes <= box inner volume` 

All three checks must pass. From the qualifying boxes, the cheapest one is instantly returned and permanently persisted in the database for the order.


## Project Structure

```
PackMate/
├── packing/
│   ├── models.py       — Product, Box, Order, OrderItem
│   ├── serializers.py  — API validation logic
│   ├── views.py        — API endpoints & Frontend views
│   ├── urls.py         — Routing
│   ├── selector.py     — Core box-selection logic (no Django imports)
│   └── tests/          — Unit and Integration tests
├── templates/
│   ├── packing/        — Dashboard templates
│   └── registration/   — Custom Login & Signup pages
├── static/packing/     — CSS & JS (Custom Dark Mode Theme)
└── PackMate/           — Django project settings
```