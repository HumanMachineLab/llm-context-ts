# Contributing to LLM-Based Text Segmentation

Thank you for your interest in contributing to our NLDB 2025 research project! 🎉

## 🔬 Research Context

This is an academic research project investigating LLM-based text segmentation methods. Contributions are welcome in the form of:

- **Experimental improvements**: New models, datasets, or evaluation approaches
- **Code quality**: Bug fixes, performance optimizations, documentation
- **Reproducibility**: Helping others replicate experiments
- **Analysis**: Additional evaluation metrics or comparative studies

## 🚀 Getting Started

### Prerequisites

1. **Python 3.8+**
2. **Ollama** (for local models): https://ollama.ai/
3. **Git** for version control
4. **Jupyter** for running notebooks

### Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork**:
   ```bash
   git clone https://github.com/yourusername/llm-context-ts.git
   cd llm-context-ts
   ```
3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Install pre-commit hooks** (optional but recommended):
   ```bash
   pip install pre-commit
   pre-commit install
   ```

## 🛠 Types of Contributions

### 🧪 Experimental Contributions

- **New Models**: Add support for additional LLMs
- **New Datasets**: Integrate additional text segmentation benchmarks
- **Evaluation Metrics**: Implement additional segmentation evaluation methods
- **Hyperparameter Studies**: Systematic evaluation of different configurations

### 🐛 Code Improvements

- **Bug Fixes**: Fix issues in existing code
- **Performance**: Optimize slow operations
- **Documentation**: Improve code comments and docstrings
- **Testing**: Add unit tests for core functionality

### 📊 Analysis Contributions

- **Comparative Studies**: Compare different approaches
- **Error Analysis**: Investigate model failures
- **Statistical Analysis**: Deeper statistical evaluation of results

## 📝 Contribution Guidelines

### Code Style

- Follow **PEP 8** Python style guidelines
- Use **meaningful variable names** and **clear function documentation**
- Add **type hints** where appropriate
- Include **docstrings** for all public functions

### Experiment Documentation

- **Document your methodology** clearly in notebooks
- **Include random seeds** for reproducibility
- **Report both successes and failures**
- **Provide clear visualizations** of results

### Commit Messages

Use clear, descriptive commit messages:

```bash
# Good examples
git commit -m "Add support for Llama-2 model in Determinor class"
git commit -m "Fix memory leak in ChromaDB vector storage"
git commit -m "Add evaluation metrics for clinical text dataset"

# Avoid
git commit -m "fix stuff"
git commit -m "update"
```

## 🔄 Pull Request Process

1. **Create a feature branch**:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the guidelines above

3. **Test your changes**:

   ```bash
   python -m pytest  # Run tests
   python example.py  # Test basic functionality
   ```

4. **Update documentation** if needed

5. **Submit a pull request** with:
   - Clear description of changes
   - Motivation for the changes
   - Any relevant experimental results
   - Screenshots/outputs if applicable

## 🧪 Running Experiments

### Adding New Models

To add a new LLM model:

1. **Update the `Determinor` class** in `src/determinor.py`
2. **Add initialization parameters** for the new model
3. **Test with a small dataset** first
4. **Document the model's performance** characteristics

### Adding New Datasets

To add a new text segmentation dataset:

1. **Create a data loader** in `src/dataset/`
2. **Follow the existing dataset structure**
3. **Add evaluation notebook** in `notebooks/`
4. **Document dataset characteristics** and licensing

### Evaluation Guidelines

- **Use consistent evaluation metrics** (Pk, WindowDiff)
- **Report confidence intervals** when possible
- **Include baseline comparisons**
- **Test on multiple dataset configurations**

## 🔒 Security and Privacy

- **Never commit API keys** or credentials
- **Use environment variables** for sensitive configuration
- **Respect dataset licensing** and usage terms
- **Anonymize any proprietary data**

## 📚 Documentation

- **Update README.md** for major changes
- **Add docstrings** to new functions
- **Include examples** in documentation
- **Update requirements** if adding dependencies

## 🤝 Code of Conduct

- **Be respectful** in discussions and code reviews
- **Provide constructive feedback**
- **Focus on the research goals**
- **Help others learn and contribute**

## 📞 Getting Help

- **Open an issue** for bugs or feature requests
- **Start a discussion** for research questions
- **Check existing issues** before creating new ones
- **Be specific** in your problem descriptions

## 🎯 Research Goals

Keep in mind our primary research objectives:

- **Advancing text segmentation** using LLMs
- **Comparative evaluation** of different approaches
- **Reproducible research** practices
- **Contributing to NLDB 2025** conference

## 📈 Recognition

Contributors will be acknowledged in:

- **Research paper acknowledgments**
- **GitHub contributor list**
- **Conference presentation** (if applicable)

Thank you for contributing to advancing the field of NLP research! 🚀
