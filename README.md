# The Insight Vault

A modern, full-stack "Smart Bookmark" manager designed to help you master the Python/DevOps/AI ecosystem. This project evolves from a simple API to a containerized, AI-powered knowledge engine.

## The Idea

Your personal digital brain. 🧠

Stop losing valuable content in 50 open tabs or chaotic bookmark folders. The Insight Vault is a private web app that saves your links, generates AI summaries, and makes everything searchable—so you can actually find what you saved.

## How It Works

### The User Journey

**Step 1: Save**  
You discover a Python tutorial on Flask decorators. Paste the URL into your app.

**Step 2: Process (The Magic)**  
Behind the scenes, Redis queues a background worker to scrape the website and extract all text content.

**Step 3: Summarize (The AI)**  
Ollama/LangChain analyzes the content and generates a concise 3-sentence summary: *"This tutorial explains how to use decorators in Flask to create reusable route logic and reduce code duplication."*

**Step 4: Search**  
A month later, you can't remember the link. You search "How do I fix Flask routes?" and your app uses semantic search to surface that exact tutorial—even though "route" wasn't in the original title.

### The Tech Stack

| Technology         | Role               | Why It Matters                                                                                  |
| ------------------ | ------------------ | ----------------------------------------------------------------------------------------------- |
| **Python/Flask**   | Application server | Handles HTTP requests, orchestrates workflows, and manages database operations                  |
| **PostgreSQL**     | Persistent storage | Stores links, summaries, user data, and metadata with relational integrity                      |
| **Redis**          | Task queue & cache | Processes slow operations (web scraping, AI inference) asynchronously to keep the UI responsive |
| **Docker**         | Containerization   | Creates reproducible environments—no manual Postgres/Redis setup on each machine                |
| **GitHub Actions** | CI/CD pipeline     | Automatically tests code and deploys updates to production                                      |
| **Ollama**         | Local AI inference | Provides free, private AI summaries without API costs or data leaving your infrastructure       |

## Getting Started

### Prerequisites

Before you begin, make sure you have:

- **Docker Desktop** installed ([Download here](https://www.docker.com/products/docker-desktop))
- **Git** for cloning the repository
- **Ollama** installed locally ([Download here](https://ollama.ai))

### Installation & Setup

**1. Clone the Repository**

```bash
git clone https://github.com/yourusername/insight-vault.git
cd insight-vault
```

**2. Set Up Environment Variables**

```bash
cp .env.example .env
```
Edit `.env` and configure:

```bash
DATABASE_URL=postgresql://postgres:password@db:5432/insight_vault
REDIS_URL=redis://redis:6379/0
OLLAMA_HOST=http://host.docker.internal:11434
SECRET_KEY=your-secret-key-here
```

**3. Pull the AI Model**

```bash
ollama pull llama2
```

**4. Start the Application**

```bash
docker-compose up -d
```

This command:

- Spins up PostgreSQL, Redis, Flask app, and background workers
- Creates the database schema automatically
- Starts the web server on `http://localhost:5000`

**5. Verify Everything Works**

```bash
docker-compose ps
```

You should see all containers running:

- `insight-vault-web`
- `insight-vault-worker`
- `insight-vault-db`
- `insight-vault-redis`

**6. Access the App**

Open your browser and go to: `http://localhost:5000`

Create an account and start saving links!

### Common Commands

**View logs:**

```bash
docker-compose logs -f web
```

**Stop the application:**

```bash
docker-compose down
```

**Reset the database (WARNING: deletes all data):**

```bash
docker-compose down -v
docker-compose up -d
```

**Run tests:**
```bash
docker-compose exec web pytest
```

**Update AI model:**
```bash
ollama pull llama2:latest
docker-compose restart worker
```

### Troubleshooting

**Problem: Ollama connection refused**  

- Make sure Ollama is running: `ollama serve`
- Check if the model is downloaded: `ollama list`

**Problem: Port 5000 already in use**  

- Change the port in `docker-compose.yml` under `web.ports`: `"8000:5000"`

**Problem: Slow summarization**  

- First run downloads the AI model (1-2 GB)
- Subsequent summaries should take 5-10 seconds

## Development Workflow

### Making Changes

1. Edit your code in the project directory
2. Rebuild the container:

   ```bash
      docker-compose up -d --build
   ```

3. Check logs for errors:

   ```bash
      docker-compose logs -f
   ```

### Running Migrations

```bash
docker-compose exec web flask db migrate -m "Description of changes"
docker-compose exec web flask db upgrade
```

### Adding New Dependencies

1. Add package to `requirements.txt`
2. Rebuild:

   ```bash
      docker-compose up -d --build
   ```

## What You'll Actually Learn

This isn't just a coding exercise—it's a **production engineering bootcamp**:

- **Deployment**: Move your app from localhost to a real server accessible anywhere
- **Maintenance**: Update AI models, swap dependencies, and refactor code without breaking existing data
- **Rollback**: Use version control and containerization to revert to stable releases when things break
- **Async Processing**: Understand how background jobs prevent slow operations from blocking users
- **Semantic Search**: Implement vector embeddings to find content by meaning, not just keywords

## Why This Matters

You're building the infrastructure that powers real SaaS products—job queues, AI pipelines, automated testing, and zero-downtime deployments. When you finish, you won't just have a cool project. You'll understand how production systems actually work.

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

MIT License - feel free to use this project for learning.