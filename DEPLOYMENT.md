# Deployment Guide

## Prerequisites

### Backend Requirements
- Python 3.9+
- pip or conda
- Virtual environment tool
- Google Gemini API key

### Frontend Requirements
- Node.js 18+
- npm or yarn

### Production Requirements
- PostgreSQL database (recommended)
- Nginx or Apache (reverse proxy)
- SSL certificate
- Domain name

## Local Development Setup

### Backend Setup

1. **Create virtual environment**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env and add your Gemini API key
```

4. **Initialize database**
```bash
python -c "from app.database import init_db; init_db()"
```

5. **Run development server**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. **Install dependencies**
```bash
cd frontend
npm install
```

2. **Configure environment**
```bash
cp .env.example .env
# Edit .env if needed
```

3. **Run development server**
```bash
npm run dev
```

4. **Access application**
```
http://localhost:3000
```

## Production Deployment

### Option 1: Traditional Server Deployment

#### Backend Deployment

1. **Prepare server**
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx postgresql
```

2. **Setup application**
```bash
cd /var/www/student-buddy
git clone <repository-url> .
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Configure PostgreSQL**
```bash
sudo -u postgres psql
CREATE DATABASE student_buddy;
CREATE USER buddy_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE student_buddy TO buddy_user;
\q
```

4. **Update .env for production**
```env
DATABASE_URL=postgresql://buddy_user:secure_password@localhost/student_buddy
DEBUG=False
SECRET_KEY=<generate-strong-secret-key>
GEMINI_API_KEY=<your-api-key>
```

5. **Setup systemd service**
```bash
sudo nano /etc/systemd/system/student-buddy.service
```

```ini
[Unit]
Description=Student Learning Buddy API
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/student-buddy/backend
Environment="PATH=/var/www/student-buddy/backend/venv/bin"
ExecStart=/var/www/student-buddy/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
```

6. **Start service**
```bash
sudo systemctl daemon-reload
sudo systemctl start student-buddy
sudo systemctl enable student-buddy
```

#### Frontend Deployment

1. **Build frontend**
```bash
cd frontend
npm run build
```

2. **Configure Nginx**
```bash
sudo nano /etc/nginx/sites-available/student-buddy
```

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # Frontend
    location / {
        root /var/www/student-buddy/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

3. **Enable site**
```bash
sudo ln -s /etc/nginx/sites-available/student-buddy /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

4. **Setup SSL with Let's Encrypt**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

### Option 2: Docker Deployment

1. **Create Dockerfile for backend**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. **Create Dockerfile for frontend**
```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
```

3. **Create docker-compose.yml**
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/student_buddy
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=student_buddy
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

4. **Deploy with Docker**
```bash
docker-compose up -d
```

### Option 3: Cloud Platform Deployment

#### Heroku

1. **Backend**
```bash
cd backend
heroku create student-buddy-api
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set GEMINI_API_KEY=your-key
git push heroku main
```

2. **Frontend**
```bash
cd frontend
# Update VITE_API_URL to Heroku backend URL
npm run build
# Deploy to Netlify, Vercel, or similar
```

#### AWS

1. **Backend on Elastic Beanstalk**
- Create application
- Upload zipped backend code
- Configure environment variables
- Setup RDS PostgreSQL

2. **Frontend on S3 + CloudFront**
- Build frontend
- Upload to S3 bucket
- Configure CloudFront distribution
- Setup custom domain

#### Google Cloud Platform

1. **Backend on Cloud Run**
```bash
gcloud run deploy student-buddy-api \
  --source ./backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

2. **Frontend on Firebase Hosting**
```bash
cd frontend
npm run build
firebase init hosting
firebase deploy
```

## Database Migration

### SQLite to PostgreSQL

1. **Export SQLite data**
```bash
sqlite3 student_buddy.db .dump > backup.sql
```

2. **Modify dump for PostgreSQL**
```bash
# Remove SQLite-specific syntax
sed -i 's/AUTOINCREMENT/SERIAL/g' backup.sql
```

3. **Import to PostgreSQL**
```bash
psql -U buddy_user -d student_buddy < backup.sql
```

4. **Update DATABASE_URL in .env**

## Monitoring & Maintenance

### Logging

1. **Backend logs**
```bash
sudo journalctl -u student-buddy -f
```

2. **Nginx logs**
```bash
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Backup Strategy

1. **Database backup**
```bash
pg_dump -U buddy_user student_buddy > backup_$(date +%Y%m%d).sql
```

2. **Automated backups**
```bash
# Add to crontab
0 2 * * * pg_dump -U buddy_user student_buddy > /backups/backup_$(date +\%Y\%m\%d).sql
```

### Performance Optimization

1. **Enable gzip compression in Nginx**
2. **Setup Redis for caching**
3. **Use CDN for static assets**
4. **Implement database connection pooling**
5. **Add rate limiting**

## Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Use strong database passwords
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Implement rate limiting
- [ ] Regular security updates
- [ ] Backup encryption
- [ ] Environment variable protection
- [ ] SQL injection prevention (ORM)
- [ ] XSS prevention (React)
- [ ] CSRF protection
- [ ] Input validation
- [ ] API authentication
- [ ] Secure file uploads

## Scaling Considerations

### Horizontal Scaling
- Load balancer (Nginx, HAProxy)
- Multiple backend instances
- Session management (Redis)
- Database read replicas

### Vertical Scaling
- Increase server resources
- Optimize database queries
- Implement caching
- CDN for static content

### Microservices Migration
- Separate AI service
- File processing service
- Analytics service
- Message queue (RabbitMQ, Celery)
