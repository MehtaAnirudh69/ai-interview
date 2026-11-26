QUESTION_BANK = [
    # ------------------------------------------------------------------ Python
    {
        "topic": "Python",
        "difficulty": "Beginner",
        "text": "What are Python lists?",
        "reference_answer": (
            "A Python list is an ordered, mutable collection that can store "
            "multiple elements of different data types. Elements are accessed "
            "by index, and lists support adding, removing and changing items."
        ),
        "concepts": ["Ordered", "Mutable", "Indexing", "Mixed data types"],
    },
    {
        "topic": "Python",
        "difficulty": "Beginner",
        "text": "What is the difference between a list and a tuple? Explain mutability.",
        "reference_answer": (
            "Lists are mutable, so their elements can be changed after creation. "
            "Tuples are immutable, so they cannot be modified once created. "
            "Because of this, tuples are hashable (if their items are) and can be "
            "used as dictionary keys, and they are slightly faster and safer for fixed data."
        ),
        "concepts": ["Mutable", "Immutable", "Hashable", "Dictionary keys", "Performance"],
    },
    {
        "topic": "Python",
        "difficulty": "Beginner",
        "text": "Explain Python dictionaries and how to retrieve a value safely.",
        "reference_answer": (
            "A dictionary stores key-value pairs with fast average O(1) lookup using "
            "hashing. Keys must be unique and hashable. You can read a value with "
            "d[key], which raises KeyError if missing, or d.get(key, default), "
            "which returns a default instead."
        ),
        "concepts": ["Key-value pairs", "Hashing", "Unique keys", "get() method", "KeyError"],
    },
    {
        "topic": "Python",
        "difficulty": "Beginner",
        "text": "What is a set in Python and when would you use it?",
        "reference_answer": (
            "A set is an unordered collection of unique, hashable elements. It is "
            "used to remove duplicates and for fast membership tests, and it "
            "supports operations like union, intersection and difference."
        ),
        "concepts": ["Unique elements", "Unordered", "Membership test", "Union", "Intersection"],
    },
    {
        "topic": "Python",
        "difficulty": "Beginner",
        "text": "What is the difference between '==' and 'is' in Python?",
        "reference_answer": (
            "'==' compares values for equality, calling __eq__. 'is' compares "
            "object identity, meaning whether both names point to the exact same "
            "object in memory. Use 'is' for None checks, e.g. 'x is None'."
        ),
        "concepts": ["Equality", "Identity", "__eq__", "Memory reference", "None check"],
    },
    {
        "topic": "Python",
        "difficulty": "Intermediate",
        "text": "Explain list comprehensions and when you should avoid them.",
        "reference_answer": (
            "A list comprehension builds a list in a single concise expression, "
            "such as [x*x for x in nums if x > 0]. They are readable and usually "
            "faster than manual loops for simple transforms. Avoid them when the "
            "logic is complex or nested, or when you only need to iterate once, "
            "where a generator expression saves memory."
        ),
        "concepts": ["Concise syntax", "Filtering", "Readability", "Generator expression", "Memory"],
    },
    {
        "topic": "Python",
        "difficulty": "Intermediate",
        "text": "Explain decorators in Python and describe a practical use case.",
        "reference_answer": (
            "A decorator is a function that takes another function and returns a "
            "new function that adds behavior without changing the original code. "
            "It relies on functions being first-class objects and closures. "
            "Practical uses include logging, timing, caching, access control and "
            "FastAPI route registration. functools.wraps preserves metadata."
        ),
        "concepts": ["Higher-order function", "Closure", "functools.wraps", "Logging", "Authorization"],
    },
    {
        "topic": "Python",
        "difficulty": "Intermediate",
        "text": "What are generators and how does the 'yield' keyword work?",
        "reference_answer": (
            "A generator is a function that uses yield to produce values lazily, "
            "one at a time, pausing and resuming its state between calls. This "
            "saves memory for large or infinite sequences because values are not "
            "stored all at once."
        ),
        "concepts": ["Lazy evaluation", "yield", "Iterator", "Memory efficiency", "State preservation"],
    },
    {
        "topic": "Python",
        "difficulty": "Intermediate",
        "text": "What do *args and **kwargs do?",
        "reference_answer": (
            "*args collects extra positional arguments into a tuple, and **kwargs "
            "collects extra keyword arguments into a dictionary. They let a "
            "function accept a flexible number of arguments and are often used to "
            "forward arguments to another function."
        ),
        "concepts": ["Positional arguments", "Keyword arguments", "Tuple", "Dictionary", "Unpacking"],
    },
    {
        "topic": "Python",
        "difficulty": "Intermediate",
        "text": "How does exception handling work in Python?",
        "reference_answer": (
            "Code that may fail goes in a try block, and specific errors are "
            "caught in except blocks. else runs if no exception occurred, and "
            "finally always runs for cleanup. You can raise custom exceptions "
            "with raise. Catch specific exceptions rather than a bare except."
        ),
        "concepts": ["try/except", "else", "finally", "raise", "Custom exceptions"],
    },
    {
        "topic": "Python",
        "difficulty": "Intermediate",
        "text": "Why is using a mutable default argument, like def f(x=[]), a problem?",
        "reference_answer": (
            "Default argument values are evaluated once when the function is "
            "defined, not on each call. A mutable default such as a list is "
            "therefore shared across calls and keeps accumulating changes. The "
            "fix is to default to None and create a new object inside the function."
        ),
        "concepts": ["Evaluated once", "Shared state", "Mutable default", "None sentinel"],
    },
    {
        "topic": "Python",
        "difficulty": "Intermediate",
        "text": "What is a context manager and what does the 'with' statement do?",
        "reference_answer": (
            "A context manager defines setup and cleanup logic through __enter__ "
            "and __exit__, or through contextlib.contextmanager. The with "
            "statement guarantees cleanup even if an exception occurs, for "
            "example closing files or releasing database connections and locks."
        ),
        "concepts": ["__enter__", "__exit__", "Resource cleanup", "contextlib", "File handling"],
    },
    {
        "topic": "Python",
        "difficulty": "Advanced",
        "text": "What is the Global Interpreter Lock (GIL) and how does it affect concurrency?",
        "reference_answer": (
            "The GIL is a mutex in CPython that lets only one thread execute "
            "Python bytecode at a time. It limits CPU-bound multithreading, so "
            "use multiprocessing for CPU-bound work. Threads and asyncio still "
            "work well for I/O-bound tasks because the GIL is released while waiting."
        ),
        "concepts": ["CPython", "Mutex", "CPU-bound", "I/O-bound", "Multiprocessing", "Threading"],
    },
    {
        "topic": "Python",
        "difficulty": "Advanced",
        "text": "How does Python manage memory and garbage collection?",
        "reference_answer": (
            "CPython uses reference counting: an object is freed when its count "
            "reaches zero. A cyclic garbage collector handles reference cycles "
            "that counting alone cannot free. Memory is managed in a private "
            "heap with an allocator for small objects."
        ),
        "concepts": ["Reference counting", "Cyclic GC", "Private heap", "Memory leaks", "Weak references"],
    },

    # --------------------------------------------------------------------- OOP
    {
        "topic": "OOP",
        "difficulty": "Beginner",
        "text": "Explain classes, objects, constructors and instance attributes in Python.",
        "reference_answer": (
            "A class is a blueprint and an object is an instance of it. The "
            "constructor, __init__, runs when an object is created and sets up "
            "instance attributes through self. Each object has its own attribute "
            "values, while class attributes are shared by all instances."
        ),
        "concepts": ["Class", "Object", "__init__", "self", "Instance vs class attributes"],
    },
    {
        "topic": "OOP",
        "difficulty": "Beginner",
        "text": "What are the four pillars of OOP?",
        "reference_answer": (
            "Encapsulation bundles data with methods and restricts direct access. "
            "Abstraction hides complexity behind a simple interface. Inheritance "
            "lets a class reuse another class's behavior. Polymorphism lets "
            "different classes respond to the same method call in their own way."
        ),
        "concepts": ["Encapsulation", "Abstraction", "Inheritance", "Polymorphism"],
    },
    {
        "topic": "OOP",
        "difficulty": "Intermediate",
        "text": "What is the difference between @classmethod, @staticmethod and an instance method?",
        "reference_answer": (
            "An instance method receives self and works with instance state. A "
            "classmethod receives cls and works with class-level state, often as "
            "an alternative constructor. A staticmethod receives neither and is a "
            "utility function that just lives in the class namespace."
        ),
        "concepts": ["self", "cls", "Alternative constructor", "Utility function", "Namespace"],
    },
    {
        "topic": "OOP",
        "difficulty": "Intermediate",
        "text": "Compare inheritance and composition. When do you prefer composition?",
        "reference_answer": (
            "Inheritance models an 'is-a' relationship, while composition models "
            "'has-a' by holding other objects. Prefer composition when behavior "
            "needs to be flexible or swappable, because inheritance creates tight "
            "coupling and deep hierarchies that are hard to change."
        ),
        "concepts": ["Is-a", "Has-a", "Coupling", "Flexibility", "Code reuse"],
    },
    {
        "topic": "OOP",
        "difficulty": "Intermediate",
        "text": "What are magic (dunder) methods? Give examples.",
        "reference_answer": (
            "Dunder methods are special methods surrounded by double underscores "
            "that let objects work with Python syntax and built-ins. Examples are "
            "__init__ for construction, __str__ and __repr__ for display, __len__ "
            "for len(), and __eq__ for ==."
        ),
        "concepts": ["__init__", "__str__", "__repr__", "__len__", "Operator overloading"],
    },
    {
        "topic": "OOP",
        "difficulty": "Advanced",
        "text": "What are abstract base classes and how do you create them in Python?",
        "reference_answer": (
            "An abstract base class defines an interface that subclasses must "
            "implement. In Python, inherit from abc.ABC and mark methods with "
            "@abstractmethod. The class cannot be instantiated directly, and "
            "subclasses that do not implement every abstract method raise TypeError."
        ),
        "concepts": ["abc.ABC", "@abstractmethod", "Interface", "Cannot instantiate", "Contract"],
    },

    # ----------------------------------------------------------------- FastAPI
    {
        "topic": "FastAPI",
        "difficulty": "Beginner",
        "text": "What is FastAPI and how do you create a GET and a POST endpoint?",
        "reference_answer": (
            "FastAPI is a modern, high-performance Python web framework built on "
            "Starlette and Pydantic, with automatic OpenAPI docs. Create an app "
            "with FastAPI(), then use @app.get('/path') and @app.post('/path') "
            "decorators on functions. POST endpoints typically take a Pydantic "
            "model as the request body."
        ),
        "concepts": ["Starlette", "Pydantic", "Decorators", "Automatic docs", "Request body"],
    },
    {
        "topic": "FastAPI",
        "difficulty": "Beginner",
        "text": "What is the difference between path parameters and query parameters in FastAPI?",
        "reference_answer": (
            "Path parameters are part of the URL path, like /users/{user_id}, and "
            "identify a specific resource. Query parameters come after '?', like "
            "/users?limit=10, and are used for filtering, sorting and pagination. "
            "FastAPI infers each from the function signature and validates types."
        ),
        "concepts": ["Path parameter", "Query parameter", "Type hints", "Filtering", "Validation"],
    },
    {
        "topic": "FastAPI",
        "difficulty": "Intermediate",
        "text": "How does Pydantic validate request data in FastAPI?",
        "reference_answer": (
            "You define a BaseModel with typed fields. FastAPI parses the request "
            "body into it, validating types and constraints (such as Field limits "
            "or EmailStr). Invalid data automatically returns a 422 error with "
            "details. Models can also define response_model to filter output."
        ),
        "concepts": ["BaseModel", "Type validation", "422 error", "Field constraints", "response_model"],
    },
    {
        "topic": "FastAPI",
        "difficulty": "Intermediate",
        "text": "What is dependency injection in FastAPI and why is it useful?",
        "reference_answer": (
            "Depends() lets you declare reusable dependencies, such as a database "
            "session or the current user, that FastAPI resolves and passes into "
            "endpoints. It reduces duplicated code, makes authentication and "
            "database access reusable, and makes testing easier through "
            "dependency overrides."
        ),
        "concepts": ["Depends", "Reusability", "Database session", "Authentication", "Testing overrides"],
    },
    {
        "topic": "FastAPI",
        "difficulty": "Intermediate",
        "text": "When should you use 'async def' versus 'def' for FastAPI endpoints?",
        "reference_answer": (
            "Use async def when the endpoint awaits non-blocking I/O such as async "
            "database drivers or HTTP clients. Use plain def for blocking code, "
            "which FastAPI runs in a thread pool. Calling blocking code inside "
            "async def blocks the event loop and hurts performance."
        ),
        "concepts": ["Event loop", "Blocking vs non-blocking", "Thread pool", "await", "Performance"],
    },
    {
        "topic": "FastAPI",
        "difficulty": "Intermediate",
        "text": "How do you handle errors and return custom status codes in FastAPI?",
        "reference_answer": (
            "Raise HTTPException(status_code=..., detail=...) to return an error "
            "response. Set status_code in the decorator for success codes like "
            "201. Use @app.exception_handler for custom global handlers, and "
            "keep error responses consistent."
        ),
        "concepts": ["HTTPException", "Status codes", "Exception handler", "Consistent errors"],
    },
    {
        "topic": "FastAPI",
        "difficulty": "Intermediate",
        "text": "What is CORS and how do you configure it in FastAPI?",
        "reference_answer": (
            "CORS is a browser security rule that blocks requests from a "
            "different origin unless the server allows it through response "
            "headers. In FastAPI, add CORSMiddleware with allowed origins, "
            "methods and headers. Avoid allowing all origins in production, "
            "especially with credentials."
        ),
        "concepts": ["Same-origin policy", "CORSMiddleware", "Allowed origins", "Preflight", "Security"],
    },
    {
        "topic": "FastAPI",
        "difficulty": "Advanced",
        "text": "How would you structure a large FastAPI project?",
        "reference_answer": (
            "Split code into routers (APIRouter) per feature, with separate "
            "layers for schemas (Pydantic), models (ORM), services or business "
            "logic, and database setup. Keep configuration in environment-based "
            "settings, use dependencies for shared logic, and add tests, "
            "migrations and logging."
        ),
        "concepts": ["APIRouter", "Layered architecture", "Schemas vs models", "Settings", "Migrations"],
    },

    # ---------------------------------------------------------------- REST API
    {
        "topic": "REST API",
        "difficulty": "Beginner",
        "text": "Explain REST APIs and the difference between GET, POST, PUT and DELETE.",
        "reference_answer": (
            "REST is an architectural style where resources are identified by "
            "URLs and manipulated through standard HTTP methods over a stateless "
            "protocol. GET reads, POST creates, PUT replaces or updates a "
            "resource, and DELETE removes it."
        ),
        "concepts": ["Resources", "Stateless", "HTTP methods", "CRUD", "URLs"],
    },
    {
        "topic": "REST API",
        "difficulty": "Beginner",
        "text": "What do the common HTTP status codes 200, 201, 400, 401, 403, 404 and 500 mean?",
        "reference_answer": (
            "200 OK is success, 201 Created means a resource was created, 400 is "
            "a bad request from the client, 401 means unauthenticated, 403 means "
            "authenticated but forbidden, 404 means not found, and 500 is an "
            "internal server error."
        ),
        "concepts": ["2xx success", "4xx client error", "5xx server error", "401 vs 403"],
    },
    {
        "topic": "REST API",
        "difficulty": "Intermediate",
        "text": "What does idempotency mean, and which HTTP methods are idempotent?",
        "reference_answer": (
            "An operation is idempotent if repeating it has the same effect as "
            "doing it once. GET, PUT and DELETE are idempotent, while POST "
            "normally is not. Idempotency makes retries safe after network failures."
        ),
        "concepts": ["Repeatable", "PUT", "DELETE", "POST not idempotent", "Safe retries"],
    },
    {
        "topic": "REST API",
        "difficulty": "Intermediate",
        "text": "How do you implement pagination in a REST API?",
        "reference_answer": (
            "Offset pagination uses limit and offset (or page and page_size) and "
            "is simple but slows down on large tables and can skip items when "
            "data changes. Cursor-based pagination uses a pointer to the last "
            "item and is more efficient and stable. Responses should include "
            "total or next-page information."
        ),
        "concepts": ["Limit/offset", "Cursor-based", "Performance", "Consistency", "Next page link"],
    },
    {
        "topic": "REST API",
        "difficulty": "Intermediate",
        "text": "How would you version a REST API?",
        "reference_answer": (
            "Common approaches are URL versioning (/v1/users), header-based "
            "versioning, or media-type versioning. URL versioning is the most "
            "visible and simple. Avoid breaking changes within a version, and "
            "deprecate old versions with notice."
        ),
        "concepts": ["URL versioning", "Header versioning", "Backward compatibility", "Deprecation"],
    },

    # ---------------------------------------------------------- Authentication
    {
        "topic": "Authentication",
        "difficulty": "Beginner",
        "text": "What is the difference between authentication and authorization?",
        "reference_answer": (
            "Authentication verifies who a user is, for example with a password. "
            "Authorization decides what that authenticated user is allowed to "
            "do, such as access to certain resources or admin actions."
        ),
        "concepts": ["Identity", "Permissions", "Login", "Roles", "401 vs 403"],
    },
    {
        "topic": "Authentication",
        "difficulty": "Intermediate",
        "text": "How does JWT-based authentication work?",
        "reference_answer": (
            "After login, the server issues a signed JSON Web Token containing "
            "claims such as user id and expiry. It has three parts: header, "
            "payload and signature. The client sends it in the Authorization: "
            "Bearer header, and the server verifies the signature and expiry "
            "without storing a session. The payload is encoded, not encrypted, "
            "so never put secrets in it."
        ),
        "concepts": ["Header.Payload.Signature", "Claims", "Expiry", "Bearer token", "Stateless", "Not encrypted"],
    },
    {
        "topic": "Authentication",
        "difficulty": "Intermediate",
        "text": "How should passwords be stored in a database?",
        "reference_answer": (
            "Never store plain text. Hash passwords with a slow, salted "
            "algorithm designed for passwords such as bcrypt, scrypt or Argon2. "
            "Verify by hashing the login attempt and comparing. A unique salt "
            "per password defeats rainbow tables."
        ),
        "concepts": ["Hashing", "Salt", "bcrypt/Argon2", "Slow hash", "No plain text"],
    },
    {
        "topic": "Authentication",
        "difficulty": "Advanced",
        "text": "Explain access tokens versus refresh tokens and how OAuth2 uses them.",
        "reference_answer": (
            "An access token is short-lived and used to call APIs. A refresh "
            "token is long-lived and used only to get new access tokens, which "
            "limits damage if an access token leaks. OAuth2 is an authorization "
            "framework where a client obtains tokens from an authorization "
            "server with the user's consent, using flows such as Authorization "
            "Code with PKCE."
        ),
        "concepts": ["Short-lived access token", "Refresh token", "OAuth2 flows", "PKCE", "Token revocation"],
    },

    # --------------------------------------------------------------------- SQL
    {
        "topic": "SQL",
        "difficulty": "Beginner",
        "text": "Explain primary keys, foreign keys and database relationships.",
        "reference_answer": (
            "A primary key uniquely identifies each row in a table and cannot be "
            "null. A foreign key is a column that references another table's "
            "primary key, enforcing referential integrity. Relationships can be "
            "one-to-one, one-to-many or many-to-many (using a join table)."
        ),
        "concepts": ["Unique identifier", "Referential integrity", "One-to-many", "Many-to-many", "Join table"],
    },
    {
        "topic": "SQL",
        "difficulty": "Beginner",
        "text": "What is the difference between WHERE and HAVING?",
        "reference_answer": (
            "WHERE filters individual rows before grouping and cannot use "
            "aggregate functions. HAVING filters groups after GROUP BY and can "
            "use aggregates such as COUNT or SUM."
        ),
        "concepts": ["Row filter", "Group filter", "GROUP BY", "Aggregate functions"],
    },
    {
        "topic": "SQL",
        "difficulty": "Intermediate",
        "text": "Explain SQL joins and the difference between INNER JOIN and LEFT JOIN.",
        "reference_answer": (
            "INNER JOIN returns only rows with matches in both tables. LEFT JOIN "
            "returns all rows from the left table and matching rows from the "
            "right, filling with NULL where there is no match. RIGHT JOIN is the "
            "mirror, and FULL OUTER JOIN returns all rows from both."
        ),
        "concepts": ["INNER JOIN", "LEFT JOIN", "NULL for no match", "RIGHT JOIN", "FULL OUTER JOIN"],
    },
    {
        "topic": "SQL",
        "difficulty": "Intermediate",
        "text": "What is an index and what are the trade-offs of using one?",
        "reference_answer": (
            "An index is a data structure, usually a B-tree, that speeds up "
            "lookups, filters and sorts on a column. The trade-offs are extra "
            "storage and slower INSERT, UPDATE and DELETE because the index "
            "must be maintained. Index columns used often in WHERE, JOIN and "
            "ORDER BY clauses."
        ),
        "concepts": ["B-tree", "Faster reads", "Slower writes", "Storage cost", "Composite index"],
    },
    {
        "topic": "SQL",
        "difficulty": "Intermediate",
        "text": "What are ACID properties and database transactions?",
        "reference_answer": (
            "A transaction groups operations into one unit. ACID stands for "
            "Atomicity (all or nothing), Consistency (valid state to valid "
            "state), Isolation (concurrent transactions do not interfere) and "
            "Durability (committed data survives crashes). COMMIT saves changes "
            "and ROLLBACK undoes them."
        ),
        "concepts": ["Atomicity", "Consistency", "Isolation", "Durability", "COMMIT/ROLLBACK"],
    },
    {
        "topic": "SQL",
        "difficulty": "Advanced",
        "text": "What are CTEs and window functions, and when are they useful?",
        "reference_answer": (
            "A CTE (WITH clause) defines a named temporary result that makes "
            "complex queries readable and allows recursion. Window functions "
            "such as ROW_NUMBER, RANK and SUM() OVER (PARTITION BY ...) compute "
            "values across related rows without collapsing them like GROUP BY. "
            "They are useful for rankings, running totals and top-N per group."
        ),
        "concepts": ["WITH clause", "Recursive CTE", "OVER / PARTITION BY", "ROW_NUMBER", "Running total"],
    },

    # --------------------------------------------------------------- Databases
    {
        "topic": "Databases",
        "difficulty": "Intermediate",
        "text": "What is database normalization and why is it useful?",
        "reference_answer": (
            "Normalization organizes data into separate related tables to reduce "
            "redundancy and avoid insert, update and delete anomalies. 1NF "
            "requires atomic values, 2NF removes partial dependencies, and 3NF "
            "removes transitive dependencies. Sometimes denormalization is used "
            "deliberately for read performance."
        ),
        "concepts": ["Redundancy", "1NF/2NF/3NF", "Anomalies", "Data integrity", "Denormalization"],
    },
    {
        "topic": "Databases",
        "difficulty": "Intermediate",
        "text": "Compare SQL and NoSQL databases. How do you choose between them?",
        "reference_answer": (
            "SQL databases are relational with fixed schemas, joins and strong "
            "ACID guarantees, which suits structured data and complex queries. "
            "NoSQL databases (document, key-value, column, graph) offer flexible "
            "schemas and easier horizontal scaling, which suits large or "
            "changing data. Choose based on data shape, consistency needs and "
            "scale."
        ),
        "concepts": ["Relational", "Schema flexibility", "ACID", "Horizontal scaling", "Use cases"],
    },
    {
        "topic": "Databases",
        "difficulty": "Intermediate",
        "text": "What is an ORM like SQLAlchemy and what is the N+1 query problem?",
        "reference_answer": (
            "An ORM maps database tables to Python classes so you work with "
            "objects instead of raw SQL. The N+1 problem happens when loading a "
            "list of N parent objects triggers one extra query per object to "
            "fetch related data. Fix it with eager loading, such as joinedload "
            "or selectinload."
        ),
        "concepts": ["Object mapping", "Lazy loading", "N+1 problem", "Eager loading", "Query performance"],
    },

    # ----------------------------------------------------------------- Backend
    {
        "topic": "Backend",
        "difficulty": "Intermediate",
        "text": "How would you design a backend API for creating and tracking interview sessions?",
        "reference_answer": (
            "Define entities such as User, Interview, Question and Answer with "
            "relationships between them. Expose REST endpoints to create an "
            "interview, fetch questions, submit answers and view results, with "
            "status tracking (created, in progress, completed). Add "
            "authentication, input validation with Pydantic, a relational "
            "database with migrations, pagination, error handling and logging."
        ),
        "concepts": ["Data model", "REST endpoints", "Status tracking", "Authentication", "Validation", "Database"],
    },
    {
        "topic": "Backend",
        "difficulty": "Intermediate",
        "text": "What is caching and where would you use it in a backend?",
        "reference_answer": (
            "Caching stores frequently used results in fast storage, such as "
            "memory or Redis, to reduce latency and database load. Use it for "
            "expensive queries, rarely changing data and external API "
            "responses. Key concerns are expiry (TTL) and invalidation so "
            "users do not see stale data."
        ),
        "concepts": ["Redis", "TTL", "Cache invalidation", "Latency", "Stale data"],
    },
    {
        "topic": "Backend",
        "difficulty": "Advanced",
        "text": "How do you make a backend resilient when it depends on an unreliable external API?",
        "reference_answer": (
            "Set timeouts, retry transient failures with exponential backoff and "
            "jitter, and use a circuit breaker to stop calling a failing "
            "service. Add fallbacks such as alternative providers or cached "
            "responses, and return clear errors to the client. Log and monitor "
            "failure rates."
        ),
        "concepts": ["Timeouts", "Exponential backoff", "Circuit breaker", "Fallback", "Monitoring"],
    },
    {
        "topic": "Backend",
        "difficulty": "Advanced",
        "text": "What is rate limiting and how would you implement it?",
        "reference_answer": (
            "Rate limiting restricts how many requests a client can make in a "
            "time window to prevent abuse and protect resources. Common "
            "algorithms are fixed window, sliding window and token bucket. It "
            "is typically implemented with a shared store like Redis, keyed by "
            "user or IP, and returns 429 Too Many Requests."
        ),
        "concepts": ["Token bucket", "Sliding window", "Redis", "429 status", "Abuse prevention"],
    },

    # ----------------------------------------------------------------- Testing
    {
        "topic": "Testing",
        "difficulty": "Beginner",
        "text": "What is the difference between unit tests and integration tests?",
        "reference_answer": (
            "Unit tests check a small piece of code, like one function, in "
            "isolation and run fast. Integration tests check that several "
            "components, such as the API, database and services, work together. "
            "A healthy suite has many unit tests and fewer integration tests."
        ),
        "concepts": ["Isolation", "Components together", "Speed", "Test pyramid"],
    },
    {
        "topic": "Testing",
        "difficulty": "Intermediate",
        "text": "How would you test a REST API and handle invalid input or server errors?",
        "reference_answer": (
            "Use pytest with FastAPI's TestClient to call endpoints and assert "
            "on status codes and response bodies. Cover the happy path, invalid "
            "input (expect 422 or 400), missing authentication (401), missing "
            "resources (404) and simulated server failures (500) using mocks. "
            "Use a separate test database and fixtures for setup and cleanup."
        ),
        "concepts": ["pytest", "TestClient", "Edge cases", "Status code assertions", "Fixtures", "Test database"],
    },
    {
        "topic": "Testing",
        "difficulty": "Intermediate",
        "text": "What is mocking and when should you use it?",
        "reference_answer": (
            "Mocking replaces real dependencies, like external APIs, databases "
            "or the clock, with controlled fakes so tests are fast, "
            "deterministic and isolated. Use unittest.mock or pytest-mock, for "
            "example to simulate an AI provider returning a 503. Avoid "
            "over-mocking, which can hide real integration bugs."
        ),
        "concepts": ["Test doubles", "unittest.mock", "Isolation", "Deterministic", "Over-mocking"],
    },

    # --------------------------------------------------------------------- Git
    {
        "topic": "Git",
        "difficulty": "Beginner",
        "text": "What is the difference between git merge and git rebase?",
        "reference_answer": (
            "Merge combines branches by creating a merge commit, preserving the "
            "full history. Rebase replays your commits on top of another branch "
            "to produce a linear history, but it rewrites commits, so avoid "
            "rebasing branches that others share."
        ),
        "concepts": ["Merge commit", "Linear history", "Rewriting history", "Shared branches"],
    },
]