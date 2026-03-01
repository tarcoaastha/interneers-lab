
## Overview

The goal of this week is to decouple the "Business Logic" from the "Web Framework." By separating these concerns, the core logic remains independent of Django's HTTP implementation, making the system easier to test and maintain.

### Features

* **GET /hello/:** A simple API endpoint that greets users.
* **Dynamic Parameters:** Supports a `name` query parameter.
* **Fallback Logic:** Defaults to "World" if no name is provided.
* **JSON Responses:** Returns data in a standard machine-readable format.

##  Architecture & Layering
I have organized the project into three distinct layers to satisfy the "Hexagonal Architecture" requirement:

### 1. The Core (Domain Layer) - `services.py`
This is the "Brain" of the application. It contains the `generate_greetings` function.
* **Key Characteristic:** It is pure Python. It has no imports from Django and doesn't know the internet exists. It only cares about strings and logic.

### 2. The Adapter (Web Layer) - `views.py`
This is the "Translator."
* **Key Characteristic:** It handles the `request` object, extracts parameters using `request.GET.get()`, and calls the Core layer. It then wraps the result in a `JsonResponse`.

### 3. The Entry Point - `urls.py`
This is the "Map" or "Signpost."
* **Key Characteristic:** It routes external URL paths to the specific Adapters in the Web Layer.


##  Developer Guide

### Prerequisites

* Python 3.14+
* Django 5.x+
* Virtual Environment (`venv`)

### Local Setup & Verification

1. **Activate Environment:**
```powershell
# Windows
.\venv\Scripts\activate

```


2. **Start the Server:**
```powershell
python manage.py runserver

```



### Testing the API

You can verify the changes via **Postman** or a browser:

* **Endpoint:** `http://127.0.0.1:8000/hello/`
* **Test Case:** `http://127.0.0.1:8000/hello/?name=Interneer`
* **Expected Result:** `{"Message": "Hello, Interneer!"}`


##  Technical Reflections
 **Separation of Concerns:** By moving the greeting logic to `services.py`, we ensure that if we ever switched from a Web API to a Command Line Tool, the "Greeting Logic" wouldn't need to be rewritten.


### How to save this:

1. Open your `README.md` file in VS Code.
2. Delete the old text and paste this in.
3. Save the file.
4. Run `git add README.md`, `git commit -m "docs: update README with hexagonal architecture and dev guide"`, and `git push`.

## Advance Week1
A way to layer the project and document it
`
backend/
├── django_app/          <-- The "Framework" Folder
│   ├── api/             <-- ADAPTER LAYER (Web/HTTP)
│   │   └── views.py     (Handles Requests/Responses)
│   ├── core/            <-- DOMAIN LAYER (Business Logic)
│   │   └── services.py  (The pure Python logic)
│   ├── urls.py          (The Router)
│   └── settings.py
└── manage.py
`
