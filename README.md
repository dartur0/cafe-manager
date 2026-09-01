# Left No Crumbs – Technical Documentation & User Manual

**Left No Crumbs** is an extensive 2D real-time arcade-strategy management game built in Python using the Pygame library. The player steps into the role of a restaurant manager serving unique pastries and caffeinated beverages to a demanding, paranormal clientele.

The application features advanced time-management mechanics, a dynamic shop/economic system, an adaptive difficulty curve, and comprehensive unit test coverage for core business logic. The project is fully containerized with Docker and configured to run in headless environments.

## 1. Project Structure

The directory architecture strictly separates data/business logic (Backend) from graphic rendering and UI event handling components (Frontend/UI).

```text
cafe_manager/
├── assets/                      # Multimedia assets used by the game
│   ├── fonts/                   # TrueType fonts (e.g., Pacifico.ttf for stylized GUI)
│   ├── images/                  # Textures for workstations, ingredients, cakes, and coffees
│   ├── music/                   # Level background music tracks
│   └── sounds/                  # Sound effects (clicks, coffee brewing, completion sounds)
├── saves/                       # Directory dedicated to persistent save files
├── src/                         # Application source code organized modularly
│   ├── core/                    # Engine core and pure business logic
│   │   ├── decorators/          # Object modifiers implementation (Decorator Pattern)
│   │   ├── entities/            # Domain entities (Customer, Kitchen, Coffee, Cake, Order)
│   │   ├── states/              # Life-cycle screen management classes (State Pattern)
│   │   ├── systems/             # Peripheral systems (SaveManager, LevelManager, SoundManager)
│   │   └── game.py              # Main Game Loop and subsystem coordination
│   └── ui/                      # Presentation layer, GUI components and screens
│       ├── components/          # Interactive panels (CakePanel, CoffeePanel, Button)
│       └── screens/             # Main menu, shop, and end-of-day summary screens
├── tests/                       # Automated unit tests suite (Pytest)
│   ├── test_customer.py         # Patience mechanics, tip algorithms, and customer types
│   ├── test_decorators.py       # Decorator pattern pricing calculations and naming tests
│   ├── test_kitchen.py          # Resource management, tray limits, and showcase tests
│   ├── test_level.py            # Win conditions, difficulty progression, and star allocation
│   └── test_order.py            # Order validation mechanics (Combo/Single)
├── Dockerfile                   # Build recipe for a lightweight Linux-slim image
├── docker-compose.yml           # Declarations for audio/video environment variables and volumes
├── requirements.txt             # Strict Python package dependencies list
└── save.json                    # Auto-generated serialized game state (Auto-save)

```

## 2. Dependencies and Environmental Requirements

The application is optimized for Python 3.12 and Python 3.14 runtime environments.

### Python Dependencies (`requirements.txt`):

* `pygame==2.6.1` – Handles low-level SDL communications (GUI windowing, 2D surface rendering, audio mixer processing, and system mouse events).
* `pytest==9.1.0` – Used for isolated test assertions in local environments and CI/CD pipelines.

### Native System Requirements:

* **Linux (Ubuntu/Debian)**: Requires development packages for SDL2 installed via `apt`: `libsdl2-dev`, `libsdl2-image-dev`, `libsdl2-mixer-dev`, `libsdl2-ttf-dev`, `libfreetype6-dev`.
* **macOS**: Requires Python 3.12+ and optional support libraries installed via Homebrew.
* **Windows**: Installing Pygame via `pip` automatically delivers precompiled SDL dynamic link libraries (DLLs).

## 3. Architecture & Design Patterns

### A. State Pattern

Manages the Finite State Machine (FSM) of the application. The main `Game` class holds an instance of the current state represented by a polymorphic object inheriting from the `GameState` base class in `base_state.py`. Screen transitions occur without interrupting the main game loop.

* **Implementation**: Every state overrides four key methods: `on_enter()` (initialization and resource allocation), `handle_event()` (user input capturing), `update()` (physics/logic time delta updating), and `draw()` (rendering onto the screen surface).
* **State Classes**:
* `MenuState`: Welcome interface and profile selection.
* `DayState`: Main gameplay phase, handling customer orders and kitchen work.
* `GameoverState`: Loss condition handling, freezing game time, and displaying final metrics.
* `PauseState`: Instant game loop pause without session data loss.
* `SettingsState`: Audio, display, and control configuration menu.
* `ShopState`: Economic phase for purchasing cafe upgrades between levels.
* `TutorialState`: Dedicated tutorial introducing game mechanics to new players.

### B. Decorator Pattern

Used to avoid combinatorial class explosion (deep inheritance trees) when creating complex food products with dynamic properties and pricing.

* **Implementation**: The `BaseCake` class represents a plain sponge base with a pre-defined price. As ingredients are chosen by the player, this object is dynamically wrapped by concrete cake flavor and cream decorators.
* **Architectural Impact**: Calling `get_price()`, `get_name()`, or `get_prep_time()` on the final object recursively traverses the decorator chain, dynamically summing component prices, appending name descriptions, and calculating baking duration based on recipe complexity.

## 4. Setup & Execution Guide

### Option A: Local Execution (Native Environment)

1. Ensure Python 3.12 or higher is installed on your system.
2. Open a terminal in the root directory of `cafe_manager` and install dependencies:
```bash
pip install -r requirements.txt

```

3. Run the application entry point:
```bash
python src/core/game.py

```

### Option B: Docker Container Execution (Isolated / Headless Environment)

The container image is built on a minimal `python:3.12-slim` distribution. To allow the game to run without physical GPU or sound card access (e.g., in CI environments), the container incorporates:

* **Xvfb (X Virtual Framebuffer)**: Virtual X11 server simulating a 1280x720 24-bit depth display in RAM.
* **Environment variable `SDL_AUDIODRIVER=dummy**`: Redirects Pygame mixer calls to a dummy audio driver, preventing `pygame.error: mixer not initialized` crashes.

1. Launch Docker Desktop on your machine.
2. Build the Docker image:
```bash
docker compose build

```

3. Run the service in detached mode (initiates the game loop on a virtual display in the background):
```bash
docker compose up -d

```

4. Stop the container and free system resources:
```bash
docker compose down --remove-orphans

```

## 5. Automated Unit Testing

The application features unit test coverage divided across 5 test modules in the `tests/` directory.

* **Execute tests locally**:
```bash
PYTHONPATH=src pytest tests/

```

* **Execute tests inside Docker**:
```bash
docker compose run game bash -c "PYTHONPATH=src python3 -m pytest tests/"

```


*A successful run returns: `============================= 45 passed in ...s =============================`.*


## 6. User Manual & Controls

### Objective

Survival through consecutive working days at the cafe. Each day sets a primary goal (e.g., *Serve 5 customers*). Speech bubbles over incoming customers indicate their exact orders (coffee type, milk option, cake base, cream topping, or combo sets).

Players must manage raw ingredients, kitchen queues, and response time. If a customer's patience meter drops to zero, they leave, causing financial loss and preventing a 3-star level rating.

### Getting Started

1. **Main Menu Options**:
* **PLAY**: Loads the latest saved state from file and resumes the current day.
* **NEW GAME**: Resets progress, sets initial balance to $0.00, and starts Day 1.
* **TUTORIAL**: Opens an interactive overview explaining UI layout and mechanics.
* **SETTINGS**: Configures music and sound effects volume levels.
* **SHOP**: Direct shortcut to the upgrade store.
* **END**: Safely closes the application and frees memory.


2. Clicking **PLAY** or **NEW GAME** initializes the `DayState`.

### Interface Controls & Operations

#### A. Customers (Counter Station)

* Up to 4 customers can visit the counter simultaneously. Each has an individual patience bar.
* Prepare and serve their orders before their patience meter expires.

#### B. Coffee Station / Coffee Preparation (Left Panel)

1. **Choose Drink Base**: Click **ESP** (Espresso) or **MILK** (Milk-based coffee).
2. **Add Milk** *(Required for MILK option only)*: Select one of three milk cartons below: **REG** (Regular), **LACT_FR** (Lactose-free), or **OAT** (Oat milk). Espresso automatically disables milk selection.
3. **Start Espresso Machine**: Click **BREW**. The drink appears on one of three espresso machine trays with a brewing timer. Completion is signaled by a green **OK** badge and audio cue.
4. **Place on Display**: Click the finished coffee cup marked **OK** to move it to the display showcase.

#### C. Cake Station / Pastry Preparation (Right Panel)

1. **Select Cake Base**: Click a flavor icon in the upper row (**VANILLA**, **CHOC**, **RED** Velvet, **CARROT**).
2. **Select Cream Topping**: Click a topping icon in the second row (**VANILLA**, **CHOC**, **STRAWB**, **BANANA**, **BLUEB**, **PISTACH**).
3. **Start Baking**: Click an open **Kitchen Slot** in the bottom-center panel. A countdown timer displays baking progress. Once finished, a green border and **READY** label appear.
4. **Place on Display**: Click the completed slot with **READY** to transfer the cake to the display showcase.

#### D. Showcase & Order Fulfillment (Center Screen)

* Ready products sit on the display showcase.
* When a showcased item matches a customer's order bubble, click directly on that **Customer**.
* The item is automatically deducted from the showcase, the customer leaves satisfied, and payment plus a dynamic tip is added to your balance.

#### E. Inventory Management (REFILL Button)

* Using coffee beans, cake bases, or cream toppings consumes inventory stock (displayed as `x3` or `Cream: 10/10`).
* If an ingredient runs out, production is blocked.
* Click the **REFILL** button at the bottom of the screen to instantly restock all ingredients to maximum capacity at no cost.

#### F. Level Progression & Shop Phase

* Reaching the daily customer quota completes the day.
* Customer satisfaction affects the star rating awarded (0 to 3 stars).
* Completing a day transitions into the `ShopState`, where earned money buys technical upgrades: extra kitchen slots, increased cream tank capacities, or new recipe unlocks.

## 7. Data Persistence (Save & Load System)

The game includes an automated, transparent auto-save system.

* **Format**: State data is serialized into unified JSON format in `save.json`.
* **Save Triggers**: Saves automatically upon successful day completion and upon exiting the shop menu.
* **Stored Scope**: Tracks current level (`day`), total funds (`money`), array of purchased upgrade IDs (`purchased`), and star history.
* **`SaveManager`** ensures seamless progress recovery in case of unexpected application closure.
