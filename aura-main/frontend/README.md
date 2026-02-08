# AURA Frontend

Modern, responsive web interface for AURA - AI-Powered Code Analysis Platform.

## Features

✨ **Beautiful UI** - Modern gradient design with Tailwind CSS
🚀 **Fast Performance** - Built with Next.js 14 and React 18
📤 **Drag & Drop Upload** - Intuitive file upload experience
🔍 **Advanced Search** - RAG-powered semantic code search
📊 **Real-time Analysis** - Live progress tracking and results
🎨 **Syntax Highlighting** - Beautiful code display with Prism.js
🔐 **TypeScript** - Full type safety throughout the application
📱 **Responsive** - Works on desktop, tablet, and mobile

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Code Highlighting**: React Syntax Highlighter
- **File Upload**: React Dropzone
- **HTTP Client**: Axios

## Prerequisites

- Node.js 18+ (recommended: 20+)
- npm or yarn
- AURA backend running on `http://localhost:8000`

## Quick Start

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

Create a `.env.local` file:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Start Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### 4. Build for Production

```bash
npm run build
npm start
```

## Project Structure

```
frontend/
├── app/                      # Next.js app directory
│   ├── page.tsx             # Home page
│   ├── layout.tsx           # Root layout
│   ├── globals.css          # Global styles
│   ├── upload/              # Upload page
│   │   └── page.tsx
│   ├── projects/            # Projects list
│   │   └── page.tsx
│   ├── dashboard/           # Analysis dashboard
│   │   └── [projectId]/
│   │       └── page.tsx
│   └── search/              # RAG search
│       └── [projectId]/
│           └── page.tsx
├── components/              # Reusable components
│   ├── FindingsTable.tsx   # Findings display
│   └── CodeViewer.tsx      # Code snippet viewer
├── services/               # API client
│   └── api.ts
├── types/                  # TypeScript types
│   └── index.ts
├── public/                 # Static assets
├── package.json
├── tsconfig.json
├── tailwind.config.js
└── next.config.js
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint

## Features Overview

### 1. Home Page
- Hero section with feature highlights
- Four agent cards (Security, Testing, Scalability, Database)
- "How It Works" guide
- Call-to-action buttons

### 2. Upload Page
- Drag & drop ZIP file upload
- File validation (type, size)
- Real-time upload progress
- Detailed extraction results
- Language and framework detection
- Direct navigation to analysis

### 3. Projects Page
- List all uploaded projects
- Search and filter projects
- Project metadata display
- Delete projects
- Navigate to analysis dashboards

### 4. Analysis Dashboard
- Summary cards (Total, Critical, High, Medium, Low)
- Four agent result cards with metrics
- Filterable findings table
- Sort by severity or file
- Search findings
- Code viewer with syntax highlighting
- Export results as JSON

### 5. RAG Search
- Semantic code search
- Multiple search strategies:
  - Standard (basic semantic search)
  - Multi-Query (AI-generated variations)
  - HyDE (hypothetical documents)
- Configurable result count
- Reranking option
- Context inclusion
- Beautiful code display with syntax highlighting

## API Integration

The frontend communicates with the AURA backend through these endpoints:

- `POST /upload/` - Upload code
- `GET /upload/projects` - List projects
- `DELETE /upload/projects/{id}` - Delete project
- `POST /analyze/{id}` - Run analysis
- `GET /analyze/{id}/results` - Get results
- `POST /rag/search` - Search code

See `services/api.ts` for implementation details.

## Configuration

### Backend URL

Update the API URL in `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://your-backend-url:8000
```

### Proxy Configuration

The Next.js config includes a proxy for API requests:

```javascript
// next.config.js
async rewrites() {
  return [
    {
      source: '/api/:path*',
      destination: 'http://localhost:8000/:path*',
    },
  ]
}
```

## Deployment

### Deploy to Vercel

```bash
npm install -g vercel
vercel
```

### Deploy to Netlify

```bash
npm run build
netlify deploy --prod --dir=.next
```

### Docker

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Troubleshooting

### Backend Connection Issues

If you see connection errors:

1. Verify backend is running: `curl http://localhost:8000/`
2. Check `.env.local` has correct `NEXT_PUBLIC_API_URL`
3. Ensure no CORS issues (backend should allow frontend origin)

### Build Errors

```bash
# Clear cache and reinstall
rm -rf .next node_modules package-lock.json
npm install
npm run build
```

### Port Already in Use

```bash
# Use a different port
PORT=3001 npm run dev
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of AURA - AI Code Analysis Platform.

## Support

For issues or questions:
- Open an issue on GitHub
- Check the backend documentation
- Review API docs at `http://localhost:8000/docs`
