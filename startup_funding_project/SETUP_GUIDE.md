# 🚀 Setup Guide: Indian Startup Funding Analysis Project

**Project:** Predictive Analysis of Indian Startup Funding (2015-2020)  
**Environment:** Python 3.10+ | Windows PowerShell  
**Time Required:** 5-10 minutes

---

## 📋 Prerequisites

Before starting, ensure you have:
- ✅ Python 3.10 or higher installed ([Download here](https://www.python.org/downloads/))
- ✅ Windows PowerShell (comes with Windows)
- ✅ Internet connection (for downloading packages)

**Verify Python installation:**
```powershell
python --version
```
Expected output: `Python 3.10.x` or higher

---

## 🛠️ Step 1: Navigate to Project Directory

Open PowerShell and navigate to the project folder:

```powershell
cd "d:\ENGR\DE&VL_Project\startup_funding_project"
```

Verify you're in the correct directory:
```powershell
Get-Location
```
Should show: `d:\ENGR\DE&VL_Project\startup_funding_project`

---

## 🐍 Step 2: Create Virtual Environment

Create a new virtual environment named `.venv`:

```powershell
python -m venv .venv
```

**Wait for completion** (takes 30-60 seconds). You should see a new `.venv` folder appear.

**Troubleshooting:**
- If `python` command not found, try: `python3 -m venv .venv` or `py -m venv .venv`
- If you get "ExecutionPolicy" error, see Step 3 below

---

## 🔓 Step 3: Set Execution Policy (If Needed)

If you encounter an error like:
```
.venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled...
```

Run this command **once** (as Administrator or with your user account):

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Type `Y` and press Enter to confirm.

**What this does:** Allows locally created scripts to run while still requiring downloaded scripts to be signed.

---

## ✅ Step 4: Activate Virtual Environment

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

**Success indicator:** Your prompt should change to show `(.venv)` at the beginning:
```
(.venv) PS D:\ENGR\DE&VL_Project\startup_funding_project>
```

**Troubleshooting:**
- If you still get execution policy error, see Step 3
- Alternative activation (if above fails):
  ```powershell
  & .\.venv\Scripts\Activate.ps1
  ```

---

## 📦 Step 5: Upgrade pip (Recommended)

Before installing packages, upgrade pip to the latest version:

```powershell
python -m pip install --upgrade pip
```

---

## 📥 Step 6: Install Project Dependencies

Install all required packages from `requirements.txt`:

```powershell

```

**This will install:**
- `pandas` - Data manipulation
- `numpy` - Numerical operations
- `matplotlib` - Plotting
- `seaborn` - Statistical visualizations
- `plotly` - Interactive charts
- `scikit-learn` - Machine learning
- `xgboost` - Gradient boosting
- `shap` - Model explainability
- `jupyter` - Notebook interface
- `notebook` - Jupyter notebook server
- `tqdm` - Progress bars

**Installation time:** 3-5 minutes (depends on internet speed)

**Troubleshooting:**
- If installation fails for a specific package, try installing it separately:
  ```powershell
  pip install <package-name>
  ```
- For `shap` installation issues on Windows, you may need Visual C++ Build Tools

---

## 🔍 Step 7: Verify Installation

Check that all packages are installed correctly:

```powershell
pip list
```

You should see all the packages listed above with their version numbers.

**Quick test:**
```powershell
python -c "import pandas, numpy, sklearn, xgboost, shap; print('All packages imported successfully!')"
```

Expected output: `All packages imported successfully!`

---

## 📓 Step 8: Launch Jupyter Notebook

Start Jupyter Notebook server:

```powershell
jupyter notebook
```

**What happens:**
- Jupyter server starts in the terminal
- Your default browser opens automatically
- You'll see the project folder structure
- Navigate to `notebooks/` to access analysis notebooks

**To stop Jupyter:**
Press `Ctrl + C` in the terminal, then type `y` and press Enter

---

## 🔄 Step 9: Deactivating Virtual Environment

When you're done working, deactivate the virtual environment:

```powershell
deactivate
```

Your prompt will return to normal (without `(.venv)` prefix).

---

## 🔁 Daily Workflow

**Every time you work on the project:**

1. Open PowerShell
2. Navigate to project:
   ```powershell
   cd "d:\ENGR\DE&VL_Project\startup_funding_project"
   ```
3. Activate virtual environment:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
4. Start Jupyter:
   ```powershell
   jupyter notebook
   ```
5. Work on notebooks
6. When done, press `Ctrl + C` to stop Jupyter
7. Deactivate:
   ```powershell
   deactivate
   ```

---

## 🚨 Common Issues & Solutions

### Issue 1: "python not found"
**Solution:** Add Python to PATH or use full path:
```powershell
C:\Users\<YourUsername>\AppData\Local\Programs\Python\Python310\python.exe -m venv .venv
```

### Issue 2: "Cannot activate .venv"
**Solution:** 
- Check execution policy (Step 3)
- Verify `.venv` folder exists
- Try alternative activation method:
  ```powershell
  & .\.venv\Scripts\Activate.ps1
  ```

### Issue 3: "Package installation failed"
**Solution:**
- Upgrade pip: `python -m pip install --upgrade pip`
- Install packages one by one
- Check internet connection
- Try with `--no-cache-dir` flag:
  ```powershell
  pip install --no-cache-dir -r requirements.txt
  ```

### Issue 4: "Jupyter notebook won't open"
**Solution:**
- Check if port 8888 is already in use
- Try specifying a different port:
  ```powershell
  jupyter notebook --port 8889
  ```
- Manually open browser and go to: `http://localhost:8888`

### Issue 5: "SHAP installation fails on Windows"
**Solution:**
- Install Microsoft C++ Build Tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/
- Or try: `pip install shap --no-build-isolation`

---

## 📂 Project Structure After Setup

```
startup_funding_project/
├── .venv/                    # Virtual environment (created in Step 2)
├── data/
│   └── raw/
│       └── startup_funding.csv
├── notebooks/                # Your Jupyter notebooks will be here
│   └── README.md
├── scripts/
│   ├── setup_env.ps1        # Alternative setup script
│   └── data_profiling.py    # Data profiling utility
├── models/                   # Saved models (created later)
├── visuals/                  # Generated plots (created later)
├── reports/                  # Final reports (created later)
├── docs/
│   ├── STAGE_DEFINITIONS.md
│   └── NOTES.md
├── requirements.txt
├── .gitignore
├── README.md
└── SETUP_GUIDE.md           # This file
```

---

## ✅ Setup Checklist

- [ ] Python 3.10+ installed and verified
- [ ] Navigated to `startup_funding_project/` directory
- [ ] Created `.venv` virtual environment
- [ ] Set execution policy (if needed)
- [ ] Activated virtual environment (prompt shows `.venv`)
- [ ] Upgraded pip
- [ ] Installed all requirements from `requirements.txt`
- [ ] Verified installation with `pip list` and import test
- [ ] Successfully launched Jupyter Notebook
- [ ] Can access notebooks in browser

---

## 🎯 Next Steps After Setup

Once setup is complete, proceed with the analysis pipeline:

1. **Data Loading** (`notebooks/1_data_loading.ipynb`)
2. **Data Cleaning** (`notebooks/2_data_cleaning.ipynb`)
3. **Exploratory Data Analysis** (`notebooks/3_eda.ipynb`)
4. **Feature Engineering** (`notebooks/4_feature_engineering.ipynb`)
5. **Modeling** (`notebooks/5_modeling.ipynb`)
6. **Explainability** (`notebooks/6_explainability.ipynb`)
7. **Final Report** (`reports/final_report.ipynb`)

---

## 📞 Need Help?

If you encounter issues not covered here:
1. Check Python version compatibility
2. Ensure you have a stable internet connection
3. Try creating a fresh virtual environment
4. Search for specific error messages online
5. Check package documentation for known Windows issues

---

**🎉 Setup Complete!** You're ready to start analyzing Indian startup funding data.

**Author:** Rohit & Team  
**Department:** Computer Engineering, PCCOE  
**Last Updated:** November 2025
