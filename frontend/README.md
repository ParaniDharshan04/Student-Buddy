# Student Learning Buddy - Frontend

React TypeScript frontend for the Student Learning Buddy application.

## Features

- **React 18** with TypeScript for type safety
- **Vite** for fast development and building
- **Tailwind CSS** for styling and responsive design
- **React Router** for client-side navigation
- **React Query** for API state management
- **Axios** for HTTP requests

## Getting Started

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Build for production:
```bash
npm run build
```

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Header.tsx
│   ├── Sidebar.tsx
│   └── Layout.tsx
├── pages/              # Page components
│   ├── HomePage.tsx
│   ├── QuestionPage.tsx
│   ├── QuizPage.tsx
│   ├── NotesPage.tsx
│   └── ProfilePage.tsx
├── lib/                # Utilities and configurations
│   └── api.ts
├── types/              # TypeScript type definitions
│   └── index.ts
├── App.tsx             # Main app component
├── main.tsx           # App entry point
└── index.css          # Global styles
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run test` - Run tests with Vitest

## API Integration

The frontend is configured to proxy API requests to the FastAPI backend running on `http://localhost:8000`. All API calls are made through the `/api` prefix.