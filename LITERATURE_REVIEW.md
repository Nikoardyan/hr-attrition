# Literature Review: Employee Attrition Prediction using Deep Learning

## 1. Background

Employee attrition is a critical concern in human resource management. The cost of replacing an employee ranges from 50% to 200% of their annual salary, depending on role complexity and tenure (SHRM, 2017). Traditional HR analytics relied on descriptive statistics and demographic profiling, but recent advances in machine learning — particularly deep learning — have enabled predictive approaches that allow proactive intervention.

This literature review summarizes key prior work that informed the methodology of this project.

---

## 2. Reviewed Studies

### 2.1 Classical Machine Learning Approaches

**Frye et al. (2018) — "Employee Attrition: What Makes an Employee Quit?"**
*SMU Data Science Review, Vol. 1, No. 1*

The authors applied logistic regression, decision trees, and random forests to the IBM HR Attrition dataset. Random forest achieved the best baseline performance with ROC-AUC of 0.81. The study identified **OverTime**, **MonthlyIncome**, and **YearsAtCompany** as the strongest predictors. This work established a benchmark for subsequent deep learning comparisons.

**Relevance to this project:** Confirmed the feature importance ranking we observed in our EDA, and provided a baseline metric (ROC-AUC ≥ 0.80) to target.

---

### 2.2 Deep Neural Networks for Tabular HR Data

**Yedida et al. (2018) — "Employee Attrition Prediction"**
*arXiv:1806.10480*

Proposed a deep neural network (DNN) with three hidden layers for the IBM dataset. Key findings:
- DNN outperformed shallow models when paired with proper regularization (dropout 0.3-0.5)
- Class imbalance handling improved recall on the minority (Leave) class by 18%
- Hyperparameter tuning was critical — random search over learning rate and layer width yielded ~5% AUC improvement

**Relevance to this project:** Directly informed our architecture choice (DNN with batch normalization + dropout) and the decision to use Keras Tuner for hyperparameter search.

---

### 2.3 Handling Class Imbalance

**Chawla et al. (2002) — "SMOTE: Synthetic Minority Over-sampling Technique"**
*Journal of Artificial Intelligence Research, Vol. 16*

The seminal paper introducing SMOTE. Demonstrated that generating synthetic minority class samples in feature space produces better generalization than naive oversampling or undersampling. Critical insight: **SMOTE should only be applied to training data**, never to validation or test sets, to avoid information leakage.

**Relevance to this project:** Our dataset has ~16% positive class. SMOTE was applied to the training fold after train/test split, preserving test set integrity for honest evaluation.

---

### 2.4 Modern HR Analytics Pipelines

**Fallucchi et al. (2020) — "Predicting Employee Attrition Using Machine Learning Techniques"**
*Computers, Vol. 9, No. 4, 86*

Surveyed multiple ML techniques on the IBM dataset. Reported that ensemble methods and DNNs both reach 85-87% accuracy, but DNNs offer better recall for the high-risk (Leave) class — which is the operationally important class for HR teams. The study emphasized that **F1-score and recall on the positive class** are more informative than overall accuracy in this imbalanced setting.

**Relevance to this project:** Justified our metric selection (F1, ROC-AUC, recall on Leave class) over raw accuracy.

---

### 2.5 Model Deployment Best Practices

**Sculley et al. (2015) — "Hidden Technical Debt in Machine Learning Systems"**
*NeurIPS 2015*

Google paper that became the de-facto reference for ML in production. Emphasizes:
- Serving infrastructure (REST API) decoupled from training code
- Logging predictions for model monitoring and drift detection
- CI/CD pipelines to ensure reproducibility

**Relevance to this project:** Informed the deployment architecture — FastAPI for serving, SQLite for prediction logging, GitHub Actions for CI/CD.

---

## 3. Methodological Synthesis

Drawing from the studies above, this project adopts the following pipeline:

| Stage | Approach | Justification (Source) |
|---|---|---|
| Preprocessing | StandardScaler + OneHotEncoder | Standard practice (Fallucchi et al., 2020) |
| Imbalance handling | SMOTE on training set only | Chawla et al. (2002) |
| Model architecture | DNN with BatchNorm + Dropout | Yedida et al. (2018) |
| Hyperparameter tuning | Random search (Keras Tuner) | Yedida et al. (2018) |
| Primary metric | ROC-AUC + F1 on Leave class | Fallucchi et al. (2020) |
| Deployment | REST API + prediction logging | Sculley et al. (2015) |

This combination is well-established in the literature and represents a defensible, reproducible approach to the problem.

---

## 4. Gap Addressed by This Project

While prior work focused on model accuracy in isolation, **few studies present an end-to-end deployable system** with API integration, prediction logging, and an HR-friendly UI. This project closes that gap by integrating the proven modeling techniques above into a production-style stack (FastAPI + SQLite + Streamlit + CI/CD), making the predictions actionable for non-technical HR users.

---

## References

1. Chawla, N. V., Bowyer, K. W., Hall, L. O., & Kegelmeyer, W. P. (2002). SMOTE: Synthetic Minority Over-sampling Technique. *Journal of Artificial Intelligence Research*, 16, 321–357.

2. Fallucchi, F., Coladangelo, M., Giuliano, R., & De Luca, E. W. (2020). Predicting Employee Attrition Using Machine Learning Techniques. *Computers*, 9(4), 86.

3. Frye, A., Boomhower, C., Smith, M., Vitovsky, L., & Fabricant, S. (2018). Employee Attrition: What Makes an Employee Quit? *SMU Data Science Review*, 1(1), Article 9.

4. Sculley, D., Holt, G., Golovin, D., Davydov, E., Phillips, T., Ebner, D., ... & Dennison, D. (2015). Hidden Technical Debt in Machine Learning Systems. *Advances in Neural Information Processing Systems* (NeurIPS), 28.

5. Society for Human Resource Management (SHRM). (2017). *Retaining Talent: A Guide to Analyzing and Managing Employee Turnover.*

6. Yedida, R., Reddy, R., Vahi, R., Jana, R., Gv, A., & Kulkarni, D. (2018). Employee Attrition Prediction. *arXiv preprint* arXiv:1806.10480.
