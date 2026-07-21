# AI Usage

## 1. AI Tools Used
- Antigravity IDE 

## 2. Prompts Given
- "build a Django-based system that recommends the most suitable box for an order"
- "add a premium dark-mode dashboard UI"
- "add a signup and login system using Django auth"
- "fix the CSS layout on the top stat cards"
- "run tests and generate output"

## 3. Accepted Output
- The core box selection algorithm (weight, dimension, and volume checks) in `selector.py`.
- The Django models (`Product`, `Box`, `Order`, `OrderItem`).
- The REST API endpoints using Django REST Framework.
- The base UI templates, authentication flows, and styling.
- The comprehensive test suite.

## 4. Rejected or Modified Output
- Initial UI layout issues: The AI applied a vertical column flex layout to the top stat cards on the dashboard, which broke the visual alignment. I had to prompt it to fix this.
- The AI initially hardcoded "Medium Box" in the UI instead of dynamically calculating and fetching the actual recommended box from the database for each order. I had to prompt it to persist this data properly.

## 5. Mistakes Found
- The AI caused a CSS bug where the stat card icons were squished into ovals on smaller screens. I had to instruct it to add `flex-shrink: 0` to fix the icon shapes.
- The AI broke the horizontal alignment of the top cards, placing the icon above the text instead of beside it. I had to provide screenshots to force the AI to correct the flex-direction to `row`.

## 6. Verification Steps
- Wrote and executed 25 comprehensive unit and integration tests (`python manage.py test packing.tests --verbosity=2`) covering all algorithm edge cases. All tests passed successfully.
- Manually tested the UI flow: registering a user, logging in, creating products and boxes, and verifying that the dashboard correctly calculates and displays the recommended box.
- Verified API responses to ensure proper JSON serialization and correct HTTP status codes (e.g., ensuring a 404 is returned when no box fits).

---

## 7. What I Learned
This assignment gave me a great opportunity to brush up on my Django knowledge. I have been primarily working with FastAPI recently, so building this project was a good refresher on Django's ORM, routing, and built-in features like the authentication system. I also enjoyed exploring the logic behind box selection algorithms and learning how to effectively guide an AI assistant by clearly defining requirements and verifying its output.
