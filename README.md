# Customer Support Analytics

An end-to-end analytics platform for customer support call data, designed to aggregate operational KPIs and generate actionable insights through a FastAPI backend and an interactive dashboard. The system supports rule-based insights today and is architected to seamlessly integrate AI/LLM-powered analysis in the future.

##  Features

- **Call Management**: View and manage customer support calls with detailed transcripts
- **Analytics Dashboard**: Real-time visualization of operational KPIs metrics including:
  - Total, resolved, and unresolved calls
  - Average call duration and frustration scores
  - Sentiment distribution charts
  - Tone analysis visualization
  - Issue type breakdown
- **AI-Powered Insights**: Optional OpenAI integration for intelligent call analysis:
  - Risk level assessment
  - Automated recommendations
  - Smart summaries
- **Call Details**: In-depth view of individual calls with:
  - Transcript analysis
  - Sentiment and tone classification
  - Frustration scoring
  - Resolution status tracking
  - Actionable insights

## Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **Supabase** - PostgreSQL database with real-time capabilities
- **OpenAI API** - AI-powered insights generation (optional)
- **Uvicorn** - ASGI server for running FastAPI
- **Python 3.9+** - Backend programming language

### Frontend
- **React 19** - UI library
- **TypeScript** - Type-safe JavaScript
- **Vite** - Fast build tool and dev server
- **Recharts** - Composable charting library
- **Axios** - HTTP client for API requests

---

##  Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9+** ([Download](https://www.python.org/downloads/))
- **Node.js 18+** and **npm** ([Download](https://nodejs.org/))
- **Supabase Account** - For database hosting ([Sign up](https://supabase.com/))
- **OpenAI API Key** (Optional) - For AI-powered insights ([Get API Key](https://platform.openai.com/api-keys))

---

##  Installation

### 1. Clone the Repository

git clone <repository-url>
cd Customer_support_analytics


### 2. Backend Setup

1. Create a virtual environment:
python -m venv venv


2. Activate the virtual environment:
   - **Windows (PowerShell):**
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

3. Install Python dependencies:
pip install -r requirements.txt


### 3. Frontend Setup

1. Navigate to the frontend directory:
cd frontend

2. Install dependencies:
npm install


3. Return to the root directory:
cd ..


### 4. Environment Configuration

Create a `.env` file in the root directory with the following variables:

# Supabase Configuration
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key

# OpenAI Configuration (Optional)
OPENAI_API_KEY=your_openai_api_key
USE_AI=true


**Note:** If you don't have an OpenAI API key, set `USE_AI=false` to use rule-based insights instead.

---
## Database Setup

1. Create a new Supabase project at [supabase.com](https://supabase.com)
2. In your Supabase dashboard, go to SQL Editor and create the `support_calls` table:
3. Copy your Supabase URL and anon key from Project Settings → API

---
## Running the Application

### Start the Backend Server

1. Activate your virtual environment (if not already activated)
2. From the root directory, run:
uvicorn Backend.main:app --reload


The API will be available at `http://127.0.0.1:8000`

- API Documentation: `http://127.0.0.1:8000/docs` (Swagger UI)

### Start the Frontend Development Server

1. Open a new terminal window
2. Navigate to the frontend directory:
cd frontend

3. Start the development server:
npm run dev

The frontend will be available at `http://localhost:5173` (or the port shown in the terminal)

## Generating Sample Data

To populate your database with sample customer support calls, use the data generator:
cd Data_Generator
python generate_calls.py --count 20


This will create sample calls with various sentiments, tones, and issue types for testing and demonstration purposes.

## 📡 API Endpoints

### Calls
- `GET /calls/` - List all calls (supports `limit` and `offset` query parameters)
- `GET /calls/{call_id}` - Get details of a specific call

### Statistics
- `GET /stats/summary` - Get summary statistics (total calls, resolved/unresolved, averages)
- `GET /stats/sentiment` - Get sentiment distribution
- `GET /stats/tone` - Get tone distribution
- `GET /stats/issues` - Get issue type distribution (sorted by count)

### Insights
- `GET /insights/{call_id}` - Get AI-powered insights for a specific call including:
  - Risk level assessment
  - Recommended actions
  - Short summary

---

## 🚀 Deployment to Vercel

This project is configured for deployment on Vercel, which hosts both the frontend and backend as serverless functions.

### Prerequisites

- A [Vercel account](https://vercel.com/signup)
- Your repository pushed to GitHub, GitLab, or Bitbucket
- Environment variables configured (see below)

### Deployment Steps

1. **Install Vercel CLI** (optional, for local testing):
   ```bash
   npm install -g vercel
   ```

2. **Deploy via Vercel Dashboard**:
   - Go to [vercel.com](https://vercel.com)
   - Click "Add New Project"
   - Import your repository
   - Vercel will automatically detect the configuration

3. **Configure Environment Variables**:
   In your Vercel project settings, add the following environment variables:
   - `SUPABASE_URL` - Your Supabase project URL
   - `SUPABASE_KEY` - Your Supabase anon key
   - `OPENAI_API_KEY` (Optional) - Your OpenAI API key
   - `USE_AI` (Optional) - Set to `true` or `false`

4. **Deploy**:
   - Vercel will automatically build and deploy your application
   - The frontend will be served from the root URL
   - API endpoints will be available at `/api/*`

### Project Structure for Vercel

- **Backend**: Deployed as serverless functions via `api/index.py`
- **Frontend**: Built with Vite and served as static files
- **Routing**: Configured in `vercel.json` to route `/api/*` to backend and everything else to frontend

### Important Notes

- The API base URL is automatically configured in production to use `/api` prefix
- For local development, the frontend still connects to `http://127.0.0.1:8000`
- Make sure your Supabase database is accessible from Vercel's IP addresses (usually enabled by default)
- Cold starts may occur with serverless functions but are typically under 1 second

### Troubleshooting Vercel Deployment

- **Build failures**: Check build logs in Vercel dashboard
- **API errors**: Verify environment variables are set correctly
- **CORS issues**: The backend CORS middleware allows all origins, which should work for Vercel
- **Import errors**: Ensure all Python dependencies are in `requirements.txt`

---
### AI Integration (Optional)

The platform is designed to support AI-generated transcripts and insights.

To enable AI later:
USE_AI=true
OPENAI_API_KEY=your_key_here


Restart the backend — no frontend changes required.