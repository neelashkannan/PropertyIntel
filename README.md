# Purva.ai - Property Intelligence Platform

A modern Vue.js frontend with FastAPI backend for professional property intelligence and portfolio management.

## 🏗️ Project Structure

```
PropertyIntel/
├── frontend/               # Vue.js Frontend
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── views/          # Page components
│   │   ├── stores/         # Pinia state management
│   │   ├── services/       # API services
│   │   ├── types/          # TypeScript types
│   │   └── assets/         # Static assets
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
├── backend/                # FastAPI Backend
│   ├── main.py            # FastAPI application
│   ├── models.py          # Database models
│   ├── schemas.py         # Pydantic schemas
│   ├── database.py        # Database configuration
│   ├── auth.py            # Authentication logic
│   └── requirements.txt   # Python dependencies
└── README.md
```

## 🚀 Quick Start

### Prerequisites

1. **Install Node.js** (v18 or higher)
   ```bash
   # macOS with Homebrew
   brew install node
   
   # Or download from https://nodejs.org/
   ```

2. **Install Python** (3.8 or higher)
   ```bash
   # macOS with Homebrew
   brew install python
   ```

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the backend:**
   ```bash
   python main.py
   # or
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   Backend will be available at: http://localhost:8000

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run development server:**
   ```bash
   npm run dev
   ```

   Frontend will be available at: http://localhost:3000

## 🎨 Features

### Professional Design
- **Modern Theme**: Clean, professional design with blue accents
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Minimal Components**: Clean, accessible UI components
- **Professional Typography**: Inter font family

### Core Functionality
- **User Authentication**: Secure JWT-based login/registration
- **Property Management**: Full CRUD operations for properties
- **Portfolio Analytics**: Smart insights and performance metrics
- **Media Upload**: Property images and documents
- **Advanced Search**: Filter and search properties
- **EPC Tracking**: Energy performance monitoring

### Technical Features
- **Vue 3 + TypeScript**: Modern frontend framework
- **FastAPI**: High-performance Python backend
- **SQLAlchemy**: Database ORM with SQLite/PostgreSQL support
- **Pinia**: State management for Vue.js
- **Axios**: HTTP client with interceptors
- **Tailwind CSS**: Utility-first CSS framework

## 🔧 Configuration

### Environment Variables

Create `.env` files for configuration:

**Backend (.env):**
```
DATABASE_URL=sqlite:///./property_intel.db
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Frontend (.env):**
```
VITE_API_BASE_URL=http://localhost:8000/api
```

### Database Migration

For PostgreSQL production setup:

1. **Install PostgreSQL:**
   ```bash
   brew install postgresql
   ```

2. **Update DATABASE_URL:**
   ```
   DATABASE_URL=postgresql://username:password@localhost/property_intel
   ```

3. **Install PostgreSQL adapter:**
   ```bash
   pip install psycopg2-binary
   ```

## 📱 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login

### Properties
- `GET /api/properties` - List user properties
- `POST /api/properties` - Create property
- `GET /api/properties/{id}` - Get property details
- `PUT /api/properties/{id}` - Update property
- `DELETE /api/properties/{id}` - Delete property
- `POST /api/properties/{id}/upload` - Upload media
- `POST /api/properties/analyze` - Analyze portfolio

## 🎯 Key Improvements Over Streamlit

### Performance
- ✅ **No page reloads** - Single Page Application
- ✅ **Real-time updates** - WebSocket support ready
- ✅ **Faster loading** - Optimized bundling with Vite
- ✅ **Concurrent users** - Async FastAPI backend

### User Experience
- ✅ **Modern UI/UX** - Professional property intelligence design
- ✅ **Mobile responsive** - Works on all devices
- ✅ **Persistent state** - Login sessions maintained
- ✅ **Better navigation** - Vue Router with history

### Scalability
- ✅ **Database integration** - SQLAlchemy ORM
- ✅ **API architecture** - RESTful endpoints
- ✅ **Authentication** - JWT-based security
- ✅ **File storage** - Organized media management

### Development
- ✅ **TypeScript** - Type safety and better DX
- ✅ **Component architecture** - Reusable components
- ✅ **State management** - Pinia stores
- ✅ **Testing ready** - Jest/Vitest setup ready

## 🚀 Deployment

### Production Build

**Frontend:**
```bash
npm run build
# Deploy dist/ folder to CDN/static hosting
```

**Backend:**
```bash
# Use Docker or deploy to cloud platforms
pip install gunicorn
gunicorn main:app --host 0.0.0.0 --port 8000
```

### Recommended Hosting
- **Frontend**: Vercel, Netlify, or AWS S3
- **Backend**: Railway, Heroku, or AWS EC2
- **Database**: PostgreSQL on AWS RDS or DigitalOcean

## 📈 Next Steps

1. **Add more views**: Property creation, editing, analytics
2. **Implement WebSockets**: Real-time notifications
3. **Add charts**: Property performance visualizations
4. **Integration**: Property APIs (Rightmove, Zoopla)
5. **Mobile app**: React Native or Flutter
6. **Advanced analytics**: ML-powered insights

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.