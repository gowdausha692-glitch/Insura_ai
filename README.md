# 🛡️ InsuraAI

### AI-Based Health Insurance Planning Application

InsuraAI is an interactive health-insurance planning application designed to help Indian families estimate their potential annual medical expenses and understand their indicative insurance coverage requirements.

The application collects household information such as age, BMI, number of people covered, previous medical expenditure, chronic conditions, smoking status, and annual household income. Based on these inputs, it generates an estimated medical expense, risk band, and indicative insurance coverage range.

---

## 🚀 Features

* 🏠 **Household Risk Assessment**
* 💰 **Annual Medical Expense Estimation**
* 📊 **Risk Band Classification**
* 🛡️ **Indicative Insurance Coverage Recommendation**
* 📈 **Factor Impact Visualization**
* 🔄 **What-If Scenario Analysis**
* 🌙 **Daylight / Midnight Theme**
* 🎨 **Modern Interactive Dashboard**
* ⚡ **Real-Time Prediction Updates**

---

## 🖥️ Application Workflow

```text
User Input
    ↓
Household Information
    ↓
Prediction Logic
    ↓
Estimated Medical Expense
    ↓
Risk Classification
    ↓
Suggested Insurance Coverage
    ↓
Visual Insights & What-If Analysis
```

---

## 📋 Input Parameters

The application uses the following household information:

| Parameter              | Description                                  |
| ---------------------- | -------------------------------------------- |
| Age                    | Age of the main household member             |
| BMI                    | Body Mass Index                              |
| People Covered         | Number of family members                     |
| Previous Medical Spend | Medical expenditure during the previous year |
| Chronic Condition      | Whether a chronic condition is present       |
| Smoking                | Whether someone in the household smokes      |
| Annual Income          | Total household income                       |

---

## 📊 Outputs

After entering the household information, InsuraAI provides:

### Estimated Annual Medical Spend

An estimated amount representing potential annual household medical expenditure.

### Risk Band

The application categorizes the estimated expenditure into:

* **Low**
* **Moderate**
* **High**

### Suggested Sum Insured

An indicative insurance coverage range based on the estimated medical expenditure.

### Factor Analysis

A visual chart shows how different household factors contribute to the estimated expenditure.

### What-If Analysis

Users can explore scenarios such as:

* No chronic condition
* Five years older
* One additional family member

This helps users understand how individual changes can affect the estimate.

---

## 🛠️ Technologies Used

* **Python**
* **Streamlit**
* **Pandas**
* **HTML**
* **CSS**
* **Data Visualization**
* **Prediction Logic**
* **Git & GitHub**

---

## 📂 Project Structure

```text
InsuraAI/
│
├── insuranceai.py
├── README.md
└── requirements.txt
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/InsuraAI.git
```

### 2. Open the project folder

```bash
cd InsuraAI
```

### 3. Install the required libraries

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt` file yet, install them directly:

```bash
pip install streamlit pandas
```

---

## ▶️ Run the Application

Run the following command:

```bash
streamlit run insuranceai.py
```

The application will open in your browser.

---

## 🎨 User Interface

InsuraAI provides a modern dashboard with:

* Clean health-insurance themed design
* Interactive sidebar inputs
* Top-right Daylight/Midnight theme switch
* Prediction cards
* Charts
* Scenario comparisons
* Insurance recommendation section

---

## 🧠 Prediction Approach

The current version uses a **rule-based prediction approach** to demonstrate the application's functionality.

The prediction considers factors such as:

```text
Age
BMI
Family Size
Previous Medical Spending
Chronic Conditions
Smoking
Household Income
```

These factors are combined to generate an estimated annual medical expenditure.

### Future ML Implementation

The rule-based prediction can be replaced with a trained machine-learning model using a synthetic household dataset.

Possible models include:

* Linear Regression
* Random Forest
* Decision Tree
* Gradient Boosting
* XGBoost

The trained model can then be integrated into the Streamlit application to generate data-driven predictions.

---

## 🔮 Future Enhancements

Future versions of InsuraAI can include:

* 🤖 Trained Machine Learning model
* 🗄️ SQL database integration
* 🔌 FastAPI backend
* 👤 User login and registration
* 📄 Insurance policy comparison
* 📥 PDF report generation
* 📊 Advanced analytics dashboard
* ☁️ Cloud deployment
* 🔐 Secure user data management
* 🧾 Personalized insurance recommendations

---

## ⚠️ Disclaimer

InsuraAI is an educational/project demonstration.

The predictions and suggested coverage ranges are **illustrative only** and should not be considered medical advice, financial advice, insurance quotes, or guarantees of actual healthcare expenses.

Actual insurance coverage depends on the specific insurance provider, policy terms, waiting periods, exclusions, room-rent limits, sub-limits, and other conditions.

---

## 👩‍💻 Author

**Usha Gowda**

B.Sc. Data Science
Bunts Sangha S.M. Shetty College of Science, Commerce & Management
Mumbai, India

---

## ⭐ Project Purpose

InsuraAI demonstrates how **Python, data science, predictive analytics, and interactive dashboards** can be combined to create a practical health-insurance planning application for families.

If you find the project useful, consider giving the repository a ⭐ on GitHub.
