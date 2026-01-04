# LexGraph 🏛️⚖️

An AI-powered chatbot for legal advice that leverages Large Language Models (LLM), Explainable AI (XAI), and Graph Representation to provide intelligent and transparent legal guidance.

## 📋 Overview

LexGraph is designed to democratize access to legal information by combining the power of modern AI with interpretable reasoning. The system uses graph-based knowledge representation to trace legal reasoning paths and provide explainable advice to users seeking legal guidance.

## ✨ Key Features

- **AI-Powered Legal Advice**: Utilizes state-of-the-art Large Language Models to understand and respond to legal queries
- **Explainable AI (XAI)**: Provides transparent reasoning behind legal advice, helping users understand the basis of recommendations
- **Graph Representation**: Visualizes relationships between legal concepts, cases, and statutes
- **Interactive Chat Interface**: User-friendly web interface for seamless interaction
- **Knowledge Ingestion**: Processes and indexes legal documents for accurate information retrieval

## 🏗️ Architecture

The project consists of three main components:

1. **Backend (Python)**: Handles LLM processing, knowledge graph operations, and API endpoints
2. **Frontend (JavaScript/Vite)**: Provides an interactive web-based chat interface
3. **Graph Module**: Manages knowledge graph construction and querying

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Aishwary0402/LexGraph.git
cd LexGraph
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install JavaScript dependencies:
```bash
npm install
```

### Configuration

Create a `.env` file in the root directory and add your API keys and configuration:

```env
# Add your LLM API keys and other configuration here
OPENAI_API_KEY=your_api_key_here
# Add other necessary environment variables
```

### Running the Application

1. Start the backend server:
```bash
python main.py
```

2. In a separate terminal, start the frontend development server:
```bash
npm run dev
```

3. Open your browser and navigate to the URL displayed in the terminal (typically `http://localhost:5173`)

## 📂 Project Structure

```
LexGraph/
├── app/                    # Frontend application code
├── graph/                  # Graph representation and operations
├── src/                    # Source code for core functionality
├── main.py                 # Main backend entry point
├── ingest.py              # Document ingestion and processing
├── index.html             # HTML entry point
├── requirements.txt       # Python dependencies
├── package.json           # Node.js dependencies
└── vite.config.js         # Vite configuration
```

## 🔧 Usage

### Ingesting Legal Documents

To add legal documents to the knowledge base:

```bash
python ingest.py --path /path/to/legal/documents
```

### Asking Legal Questions

1. Open the web interface
2. Type your legal question in the chat input
3. Review the AI-generated response along with the reasoning graph
4. Explore the knowledge graph to understand the connections between legal concepts

## 🛠️ Technologies Used

- **Backend**: Python, FastAPI/Flask (inferred)
- **Frontend**: JavaScript, Vite, HTML, CSS
- **AI/ML**: Large Language Models (OpenAI, Anthropic, or similar)
- **Graph Database**: Neo4j or similar graph technology
- **Vector Storage**: For semantic search and retrieval

## ⚠️ Disclaimer

**IMPORTANT**: LexGraph is an educational and informational tool. It does not provide professional legal advice and should not be relied upon as a substitute for consultation with a qualified attorney. Always consult with a licensed legal professional for specific legal matters.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.


## 🙏 Acknowledgments

- Thanks to the open-source community for the amazing tools and libraries
- Legal datasets and knowledge bases that power this application
- Contributors and testers who help improve LexGraph

## 📧 Contact

For questions, suggestions, or collaboration opportunities, please open an issue on GitHub or reach out through the repository.

---

**Note**: This project is under active development. Features and documentation may change as the project evolves.
