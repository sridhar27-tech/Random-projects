# 🏭 Rejection Rate Analytics for Small Industries

**An Interactive Data Analytics Model to Reduce Product Rejection Rates in Manufacturing**

---

## 📋 Project Overview

This Python-based interactive application helps small manufacturing industries analyze, predict, and reduce product rejection rates using data analytics and machine learning. The system provides comprehensive insights into manufacturing defects and generates actionable recommendations for quality improvement.

## ✨ Key Features

### 1. **Data Generation & Analysis**
- Generate realistic manufacturing data with 5000+ samples
- Track 12 key manufacturing parameters
- Analyze correlations between factors and rejection rates

### 2. **Interactive Visualizations**
- 12 comprehensive charts and graphs
- Real-time data exploration
- Correlation matrices and trend analysis
- Feature importance visualization

### 3. **Machine Learning Prediction**
- Random Forest Classifier with 88%+ accuracy
- ROC-AUC score of 0.94+
- Predict rejection probability for new batches
- Real-time quality assessment

### 4. **Actionable Recommendations**
- Prioritized improvement suggestions
- Root cause analysis
- Cost-effective solutions
- Implementation roadmap

---

## 🚀 Getting Started

### Prerequisites
```bash
Python 3.8+
pip package manager
```

### Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python rejection_analytics.py
```

---

## 📊 Data Parameters Analyzed

The system analyzes the following manufacturing parameters:

| Parameter | Description | Range |
|-----------|-------------|-------|
| **Machine Temperature** | Operating temperature in °C | 42-114°C |
| **Operator Experience** | Years of experience | 1-20 years |
| **Production Speed** | Units per hour | 80-120 |
| **Raw Material Quality** | Quality score | 60-100% |
| **Maintenance Hours** | Hours since last maintenance | 0-15 hours |
| **Shift** | Work shift | Morning/Afternoon/Night |
| **Humidity** | Environmental humidity | 30-60% |
| **Machine Age** | Equipment age | 1-15 years |
| **Inspection Thoroughness** | Quality check coverage | 50-100% |
| **Supplier Rating** | Vendor quality score | 3-10 |
| **Defect History** | Previous defects count | 0-12 |

---

## 🎯 How It Works

### Step 1: Generate Sample Data
```
Option 1: Generate Sample Manufacturing Data
- Creates 5000 realistic manufacturing records
- Simulates real-world production scenarios
- Includes natural variance and correlations
```

### Step 2: Explore Data
```
Option 2: Explore Data
- Displays comprehensive statistics
- Shows rejection rates by category
- Identifies key correlations
- Provides data quality assessment
```

### Step 3: Visualize Patterns
```
Option 3: Visualize Data
- Creates 12 interactive charts
- Shows rejection patterns by shift, age, etc.
- Displays feature correlations
- Generates high-resolution PNG outputs
```

### Step 4: Train Predictive Model
```
Option 4: Train Predictive Model
- Trains Random Forest Classifier
- Achieves 88%+ accuracy
- Identifies most important features
- Validates with confusion matrix & ROC curve
```

### Step 5: Make Predictions
```
Option 5: Predict Rejection for New Batch
- Enter new batch parameters
- Get real-time rejection probability
- Receive acceptance/rejection prediction
- Understand risk factors
```

### Step 6: Get Recommendations
```
Option 6: Generate Recommendations
- Prioritized action items (HIGH/MEDIUM)
- Specific, measurable improvements
- Cost-effective solutions
- Implementation guidelines
```

---

## 📈 Sample Results

### Model Performance
- **Accuracy**: 88.40%
- **ROC-AUC Score**: 0.9469
- **Precision (Rejected)**: 91%
- **Recall (Rejected)**: 94%

### Top Feature Importance
1. Raw Material Quality: 49.77%
2. Inspection Thoroughness: 13.85%
3. Operator Experience: 6.66%
4. Maintenance Hours: 4.29%
5. Production Speed: 4.20%

### Sample Recommendations
1. **[HIGH] Raw Materials**
   - Set minimum quality threshold at 85%
   - Audit suppliers quarterly

2. **[HIGH] Training**
   - Implement mentorship program
   - Pair new operators with veterans

3. **[HIGH] Maintenance**
   - Schedule preventive maintenance every 200 hours

---

## 📁 Project Structure

```
rejection-analytics/
│
├── rejection_analytics.py    # Main application file
├── requirements.txt           # Python dependencies
├── README.md                  # This file
│
└── outputs/                   # Generated outputs
    ├── rejection_analysis_visualization.png
    ├── model_evaluation.png
    └── recommendations.csv
```

---

## 🎨 Visualizations Generated

1. **Rejection Rate by Shift** - Bar chart showing shift-wise performance
2. **Temperature Distribution** - Histogram comparing accepted vs rejected
3. **Experience vs Rejection** - Line plot showing correlation
4. **Material Quality Impact** - Scatter plot analysis
5. **Speed Distribution** - Violin plot by status
6. **Maintenance Impact** - Hexbin density plot
7. **Machine Age Analysis** - Bar chart by age groups
8. **Humidity Effect** - Line chart showing environmental impact
9. **Supplier Rating Impact** - Horizontal bar chart
10. **Defect History Pattern** - Scatter plot with color coding
11. **Correlation Matrix** - Heatmap of all features
12. **Overall Status** - Pie chart of acceptance/rejection

Plus model evaluation charts:
- Confusion Matrix
- ROC Curve
- Feature Importance Rankings

---

## 💡 Use Cases

### For Small Manufacturing Units
- Identify quality bottlenecks
- Reduce material waste
- Optimize production parameters
- Improve operator training

### For Quality Managers
- Track performance metrics
- Predict potential defects
- Prioritize improvement areas
- Generate compliance reports

### For Operations Teams
- Optimize shift planning
- Schedule maintenance effectively
- Monitor equipment health
- Improve supplier selection

---

## 🔧 Interactive Menu Options

```
MAIN MENU
----------------------------------------------------------------------
1. Generate Sample Manufacturing Data
2. Explore Data (Statistics & Analysis)
3. Visualize Data (Charts & Graphs)
4. Train Predictive Model
5. Predict Rejection for New Batch
6. Generate Recommendations
7. Run Complete Analysis
8. Exit
```

**Option 7** runs the complete pipeline automatically:
- Generates data
- Performs analysis
- Creates visualizations
- Trains model
- Generates recommendations

---

## 📊 Output Files

### 1. rejection_analysis_visualization.png
High-resolution (300 DPI) chart with 12 visualization panels showing:
- Shift analysis
- Temperature patterns
- Experience correlations
- Quality metrics
- And more...

### 2. model_evaluation.png
Model performance visualization including:
- Confusion matrix
- ROC curve with AUC score
- Feature importance rankings

### 3. recommendations.csv
Structured recommendations with:
- Priority level
- Category
- Issue description
- Action items

---

## 🎓 Technical Details

### Machine Learning Approach
- **Algorithm**: Random Forest Classifier
- **Trees**: 200 estimators
- **Max Depth**: 15
- **Features**: 12 (10 numeric + 2 shift encoded)
- **Train/Test Split**: 80/20
- **Validation**: Stratified sampling

### Feature Engineering
- Standard scaling for numeric features
- One-hot encoding for categorical (shift)
- Feature importance calculation
- Correlation analysis

### Performance Metrics
- Accuracy
- Precision & Recall
- F1-Score
- ROC-AUC Score
- Confusion Matrix

---

## 🚀 Advanced Usage

### Custom Data Input
```python
# Predict for custom batch
batch_params = {
    'machine_temperature': 75,
    'operator_experience_years': 10,
    'production_speed': 100,
    'raw_material_quality': 85,
    'maintenance_hours': 5,
    'shift': 'Morning',
    'humidity_percent': 45,
    'machine_age_years': 5,
    'inspection_thoroughness': 80,
    'supplier_rating': 8,
    'defect_history_count': 2
}
```

### Batch Prediction
You can modify the code to predict multiple batches at once by passing a list of parameter dictionaries.

---

## 📝 Best Practices

### Data Collection
1. Ensure consistent measurement units
2. Record data at regular intervals
3. Include all relevant parameters
4. Maintain data quality

### Model Updates
1. Retrain model quarterly
2. Update with new production data
3. Validate performance metrics
4. Adjust thresholds as needed

### Implementation
1. Start with high-priority recommendations
2. Measure impact over 2-3 months
3. Adjust strategies based on results
4. Document all changes

---

## 🎯 Expected Benefits

### Quality Improvement
- 20-30% reduction in rejection rates
- Improved product consistency
- Better supplier relationships
- Enhanced customer satisfaction

### Cost Savings
- Reduced material waste
- Lower rework costs
- Optimized maintenance schedules
- Decreased overtime expenses

### Operational Excellence
- Data-driven decision making
- Predictive quality control
- Continuous improvement culture
- Competitive advantage

---

## 🤝 Support & Contribution

### Future Enhancements
- Real-time data integration
- Multi-product support
- Advanced analytics dashboard
- Mobile app integration
- Cloud deployment
- API for external systems

### Feedback
For questions, suggestions, or issues, please refer to the project documentation or contact your system administrator.

---

## 📜 License

This project is designed for educational and commercial use in small manufacturing industries.

---

## 🏆 Acknowledgments

Built with:
- Python 3.x
- NumPy & Pandas for data processing
- Scikit-learn for machine learning
- Matplotlib & Seaborn for visualizations

---

## 📞 Getting Help

### Common Issues

**Q: Model accuracy seems low?**
A: Ensure you have sufficient training data (5000+ samples recommended)

**Q: Visualizations not displaying?**
A: Check that matplotlib backend is configured correctly

**Q: Predictions seem incorrect?**
A: Verify input parameters are within expected ranges

**Q: How to interpret feature importance?**
A: Higher percentages indicate stronger influence on rejection rates

---

## 🎓 Learning Resources

### Understanding the Model
- Random Forests use ensemble learning
- Multiple decision trees vote on predictions
- Handles non-linear relationships well
- Robust to outliers and noise

### Key Metrics Explained
- **Accuracy**: Overall correct predictions
- **Precision**: Of predicted rejections, how many were correct
- **Recall**: Of actual rejections, how many we caught
- **ROC-AUC**: Model's ability to distinguish classes

---

## ✅ Quick Start Checklist

- [ ] Install Python 3.8+
- [ ] Install required packages
- [ ] Run the application
- [ ] Select Option 7 (Complete Analysis)
- [ ] Review generated visualizations
- [ ] Read recommendations.csv
- [ ] Implement top 3 recommendations
- [ ] Monitor results for 2-3 months
- [ ] Retrain model with new data

---

**Remember**: Data-driven decisions lead to continuous improvement! 🚀

Last Updated: February 2026
Version: 1.0
