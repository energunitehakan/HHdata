# ⚡ Max Demand Calculator

Welcome to the **Max Demand Calculator** — an automation tool designed to streamline the analysis of energy meter data.

---

## 👥 Who Is This For?

This project helps **energy analysts, consultants, and operators** understand energy usage patterns across **multiple meters** over **different time periods**. It is especially useful for:

- Identifying **peak electricity demand** over any 1-hour rolling window
- Understanding **seasonal trends** in consumption
- Simplifying analysis of **30-minute interval data** from CSV or Excel files
- Visualizing and summarizing results via **interactive dashboards**

You don’t need to be a developer to use it — the final output is designed to be clear, visual, and ready for decision-making.

---

## 🧠 What Does It Do?

- 🧾 Ingests energy usage data from **CSV or Excel files**
- 📅 Handles **multiple time periods and seasonal segmentation**
- 🕐 Calculates the **rolling maximum 1-hour demand** per meter
- 🌱 Groups and compares demand by **season (Spring, Summer, Autumn, Winter)**
- 📊 Generates **summary tables and graphs** for each meter
- 💡 Built for **automation and reproducibility**

---

## ⚙️ Features for Developers

- 📦 Poetry-managed Python environment with local virtualenv
- 📊 Integrated support for `pandas`, `openpyxl`, `SQLAlchemy`, `psycopg2`
- 📈 Dash and Streamlit dashboards for interactive data exploration
- 🧪 Unit tests with Pytest
- 🧹 Pre-commit setup: Black (formatting), Ruff (linting), trailing-whitespace fixes
- 🐳 Docker, Kubernetes, and Cloud Run configs for deployment
- 🔄 CI/CD scaffold with GitHub Actions
- ⚙️ `config.py` to manage project paths in a clean, reproducible way
- 📁 Clean, extensible folder structure for analysis pipelines

---

## 🚀 Quick Start (Developers)

```bash
./init_python_project.sh /full/path/to/project
```

This script sets up:
- Local Poetry + pyenv environment
- Standardized project folder layout
- Pre-configured Docker, CI/CD, and Jupyter support

---

## 📂 Project Structure

| Folder/File               | Purpose |
|---------------------------|---------|
| `src/`                    | Main application code |
| `tests/`                  | Unit tests using Pytest |
| `notebooks/`              | Optional Jupyter notebooks for exploration |
| `deploy/docker`           | Docker container setup |
| `deploy/kubernetes`       | K8s deployment config |
| `deploy/cloudrun`         | GCP Cloud Run setup |
| `.github/workflows/`      | GitHub Actions CI config |
| `.env` / `.env.example`   | Environment variable templates |
| `config.py`               | Project path resolution utility |

---

## 🧾 Example Use Case

You receive multiple Excel files from smart meters, each reporting **30-minute electricity usage**. This tool will:

1. Automatically read and combine them
2. Detect the **highest rolling 1-hour demand** (e.g. between 9:00 and 10:00 AM)
3. Show how those peaks vary by **season**
4. Display the data through **intuitive graphs and tables**

---

## 🌍 Deployment Options

This app can be deployed:
- Locally via Streamlit/Dash
- In the cloud with **Docker**, **Kubernetes**, or **Google Cloud Run**

---

## 🧩 Contributors & Notes

Please open issues or submit pull requests if you want to improve the tool, support new formats, or add new analytics modules.

For deployment or integration questions, contact the **Energunite** engineering team.

---

## 📘 License

MIT License — see `LICENSE` file.
