# LLM-Based Text Segmentation for NLDB 2025

This repository contains the research code for **"LLM-Based Context Segmentation"**, submitted to NLDB 2025. The project investigates the effectiveness of Large Language Models in determining topic boundaries within text documents through various segmentation approaches.

## 🎯 Project Overview

Text segmentation is a fundamental NLP task that involves identifying topic boundaries in documents. This research explores how modern LLMs can be leveraged for this task using different methodologies:

1. **Direct LLM-based segmentation**: Using prompts to determine if consecutive sentences belong to the same topic
2. **RAG-enhanced segmentation**: Incorporating retrieval-augmented generation for context-aware decisions
3. **Multi-model comparison**: Evaluating performance across different LLMs (Mistral, GPT-4o, OpenAI o1, DeepSeek)

## 📊 Datasets

The project evaluates segmentation performance on multiple benchmark datasets:

- **Choi Dataset**: Standard text segmentation benchmark with different configurations (3-5, 3-11, 6-8, 9-11 segments)
- **WikiSection**: Wikipedia article sections for topic boundary detection
- **Meeting Transcripts**: Dialogue segmentation in meeting contexts
- **Clinical Text**: Medical document segmentation
- **Academic Papers**: Scientific article section boundaries

## 🛠 Installation

### Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai/) (for local LLM inference)
- OpenAI API key (optional, for GPT models)

### Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/llm-context-ts.git
   cd llm-context-ts
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Install Ollama models** (if using local models):

   ```bash
   ollama pull mistral
   ollama pull deepseek-r1:8b
   ```

4. **Configure API keys** (optional):
   Create a `.env` file in the root directory:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## 🚀 Usage

### Quick Start

1. **Basic text segmentation** using the Determinor class:

   ```python
   from src.determinor import Determinor

   # Initialize with different models
   determinor = Determinor()  # Default: Mistral
   determinor_gpt = Determinor(openai_4o=True)  # GPT-4o-mini
   determinor_deepseek = Determinor(deepseek=True)  # DeepSeek

   # Segment a list of sentences
   sentences = ["First sentence.", "Second sentence.", "Third sentence."]
   predictions = determinor.query_batch_data(sentences)
   ```

2. **RAG-based segmentation**:

   ```python
   from src.rag import RAG

   rag = RAG()
   result = rag.query_data("Are these sentences about the same topic?")
   ```

### Running Experiments

The project includes several Jupyter notebooks for different experiments:

- `notebooks/1.0-context-ts-testing.ipynb`: Basic segmentation testing
- `notebooks/1.0-context-ts-testing-choi.ipynb`: Choi dataset evaluation
- `notebooks/1.0-context-ts-testing-wikisection.ipynb`: Wikipedia section segmentation
- `notebooks/1.0-context-ts-testing-meeting.ipynb`: Meeting transcript segmentation
- `notebooks/1.1-context-ts-evaluation.ipynb`: Comprehensive evaluation with metrics

### Evaluation Metrics

The project uses standard text segmentation evaluation metrics:

- **Pk (Probabilistic Error Metric)**: Measures segmentation accuracy
- **WindowDiff**: Penalizes near-miss errors differently than distant errors

## 📁 Project Structure

```
llm-context-ts/
├── src/                          # Source code
│   ├── determinor.py            # Main segmentation logic
│   ├── rag.py                   # RAG-based segmentation
│   ├── populate_database.py     # Database setup utilities
│   ├── query_data.py           # Data querying utilities
│   └── dataset/                # Dataset handling utilities
├── notebooks/                   # Jupyter notebooks for experiments
├── db/                         # Database utilities and schemas
├── data/                       # Dataset storage (excluded from git)
├── requirements.txt            # Python dependencies
└── README.md                  # This file
```

## 🔧 Configuration Options

### Model Selection

The `Determinor` class supports multiple LLM backends:

```python
# Local models (via Ollama)
determinor = Determinor()                    # Mistral (default)
determinor = Determinor(deepseek=True)       # DeepSeek R1

# OpenAI models
determinor = Determinor(openai_4o=True)      # GPT-4o-mini
determinor = Determinor(openai_o1=True)      # o1-mini
```

### Context Window

Adjust the context window size for segmentation decisions:

```python
determinor = Determinor(max_context_window=10)  # Use last 10 sentences
```

### Dataset-Specific Prompts

Enable meeting-specific prompts for dialogue segmentation:

```python
determinor = Determinor(meeting_dataset=True)
```

## 📈 Results

Preliminary results on the Choi dataset show:

| Model   | Dataset   | Pk (k=2) | WindowDiff (k=2) |
| ------- | --------- | -------- | ---------------- |
| Mistral | Choi 3-5  | 0.245    | 0.408            |
| Mistral | Choi 3-11 | 0.265    | 0.337            |

_Full results and analysis available in the paper and evaluation notebooks._

## 🤝 Contributing

This is a research project for NLDB 2025. If you're interested in collaborating or have suggestions:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request with detailed description

## 📄 Citation

If you use this code in your research, please cite:

```bibtex
@inproceedings{llm-context-segmentation-2025,
  title={LLM-Based Context Segmentation},
  author={[Your Name]},
  booktitle={Proceedings of NLDB 2025},
  year={2025}
}
```

## 🔒 Security Note

**Important**: This repository excludes API keys and large database files. You'll need to:

- Add your own OpenAI API key to `.env` file
- Download/generate the dataset files as needed
- The original tutorial reference: https://www.youtube.com/watch?v=2TJxpyO3ei4

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built upon concepts from the RAG tutorial: https://www.youtube.com/watch?v=2TJxpyO3ei4
- Uses the Choi dataset for text segmentation evaluation
- Powered by various LLM providers (Ollama, OpenAI)
