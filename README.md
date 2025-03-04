# DorkRecon


## 🔍 About DorkRecon
DorkRecon is an advanced reconnaissance tool designed for ethical hacking and penetration testing. It automates **Google Dorking**, allowing security professionals to gather information efficiently from publicly indexed web resources. The tool assists in finding sensitive data, exposed directories, and security misconfigurations with precision.

## 🚀 Features
- **Automated Google Dorking**: Generates and executes advanced Google search queries.
- **Customizable Dorks**: Users can add their own dork queries in `dorks.txt`.
- **Logging & JSON Output**: Stores results in structured logs and JSON format.
- **Multi-platform Support**: Works on Windows, Linux, and macOS.
- **Easy Setup**: Install dependencies and run within minutes.
- **Ethical Hacking & Security Research**: Ideal for security audits and penetration testing.

## 📌 Installation Guide

### Prerequisites
Ensure you have the following installed:
- **Python 3.x** (Recommended: Python 3.8+)
- **pip** (Python package manager)
- **Google Search API Key** (Optional, for higher accuracy)

### 🔧 Windows Installation
```bash
# Clone the repository
git clone https://github.com/Priyank-CyberK/DorkRecon.git
cd DorkRecon

# Install dependencies
pip install -r requirements.txt

# Run the tool
python dork_recon.py
```

### 🐧 Linux/macOS Installation
```bash
# Clone the repository
git clone https://github.com/Priyank-CyberK/DorkRecon.git
cd DorkRecon

# Install dependencies
pip3 install -r requirements.txt

# Give execution permissions
chmod +x setup.sh

# Run the tool
./setup.sh
```

## 🎯 Usage
1. Add your dork queries to `dorks.txt`.
2. Run the script to execute dorks against Google.
3. View results in the generated `scan_results.json` file.

### Example Command
```bash
python dork_recon.py --query "site:example.com intitle:index of"
```

## 🛠 Contributing
We welcome contributions! To contribute:
1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to your fork (`git push origin feature-branch`)
5. Open a pull request

## ⚠️ Legal Disclaimer
This tool is meant for **educational and ethical penetration testing** only. Unauthorized use against websites without permission is strictly prohibited and **illegal**.

## 📜 License
DorkRecon is licensed under the **MIT License**. See [LICENSE](LICENSE) for more details.

---
👨‍💻 Developed by [Priyank-CyberK](https://github.com/Priyank-CyberK)

