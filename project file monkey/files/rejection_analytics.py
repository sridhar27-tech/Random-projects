"""
Interactive Data Analytics Model for Reducing Rejection Rates in Small Industries
A comprehensive tool for analyzing, predicting, and reducing product rejection rates
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class RejectionAnalytics:
    """Main class for rejection rate analysis and prediction"""
    
    def __init__(self):
        self.data = None
        self.model = None
        self.scaler = StandardScaler()
        self.feature_importance = None
        
    def generate_sample_data(self, n_samples=5000):
        """Generate realistic manufacturing data"""
        np.random.seed(42)
        
        # Generate features
        data = {
            'batch_id': range(1, n_samples + 1),
            'machine_temperature': np.random.normal(75, 10, n_samples),
            'operator_experience_years': np.random.randint(1, 21, n_samples),
            'production_speed': np.random.normal(100, 15, n_samples),
            'raw_material_quality': np.random.uniform(60, 100, n_samples),
            'maintenance_hours': np.random.exponential(5, n_samples),
            'shift': np.random.choice(['Morning', 'Afternoon', 'Night'], n_samples),
            'humidity_percent': np.random.normal(45, 12, n_samples),
            'machine_age_years': np.random.randint(1, 16, n_samples),
            'inspection_thoroughness': np.random.uniform(50, 100, n_samples),
            'supplier_rating': np.random.uniform(3, 10, n_samples),
            'defect_history_count': np.random.poisson(3, n_samples)
        }
        
        df = pd.DataFrame(data)
        
        # Create target variable based on logical rules
        rejection_score = (
            (df['machine_temperature'] - 75).abs() * 0.3 +
            (20 - df['operator_experience_years']) * 0.5 +
            (df['production_speed'] - 100).abs() * 0.2 +
            (100 - df['raw_material_quality']) * 0.8 +
            (10 - df['maintenance_hours']).clip(0) * 0.4 +
            (df['shift'] == 'Night').astype(int) * 5 +
            (df['humidity_percent'] - 45).abs() * 0.2 +
            df['machine_age_years'] * 0.3 +
            (100 - df['inspection_thoroughness']) * 0.3 +
            (10 - df['supplier_rating']) * 0.5 +
            df['defect_history_count'] * 1.5
        )
        
        # Add some randomness
        rejection_score += np.random.normal(0, 5, n_samples)
        
        # Convert to binary classification (rejected or not)
        df['rejected'] = (rejection_score > rejection_score.quantile(0.25)).astype(int)
        
        self.data = df
        print(f"✓ Generated {n_samples} samples")
        print(f"  Rejection rate: {df['rejected'].mean()*100:.2f}%")
        return df
    
    def explore_data(self):
        """Perform exploratory data analysis"""
        if self.data is None:
            print("⚠ No data available. Generate data first!")
            return
        
        print("\n" + "="*70)
        print("📊 EXPLORATORY DATA ANALYSIS")
        print("="*70)
        
        # Basic statistics
        print("\n1. Dataset Overview:")
        print(f"   Total Batches: {len(self.data)}")
        print(f"   Rejected Batches: {self.data['rejected'].sum()}")
        print(f"   Accepted Batches: {len(self.data) - self.data['rejected'].sum()}")
        print(f"   Rejection Rate: {self.data['rejected'].mean()*100:.2f}%")
        
        # Feature statistics
        print("\n2. Key Feature Statistics:")
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        stats = self.data[numeric_cols].describe().round(2)
        print(stats)
        
        # Correlation with rejection
        print("\n3. Correlation with Rejection:")
        correlations = self.data[numeric_cols].corrwith(self.data['rejected']).sort_values(ascending=False)
        for feat, corr in correlations.items():
            if feat != 'rejected' and feat != 'batch_id':
                print(f"   {feat:30s}: {corr:+.3f}")
        
        return stats
    
    def visualize_data(self):
        """Create comprehensive visualizations"""
        if self.data is None:
            print("⚠ No data available. Generate data first!")
            return
        
        fig = plt.figure(figsize=(20, 12))
        
        # 1. Rejection rate by shift
        plt.subplot(3, 4, 1)
        shift_rejection = self.data.groupby('shift')['rejected'].mean() * 100
        colors = ['#2ecc71', '#f39c12', '#e74c3c']
        bars = plt.bar(shift_rejection.index, shift_rejection.values, color=colors, alpha=0.7)
        plt.title('Rejection Rate by Shift', fontsize=12, fontweight='bold')
        plt.ylabel('Rejection Rate (%)')
        plt.xticks(rotation=45)
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom')
        
        # 2. Temperature distribution
        plt.subplot(3, 4, 2)
        for status in [0, 1]:
            data_subset = self.data[self.data['rejected'] == status]['machine_temperature']
            plt.hist(data_subset, alpha=0.6, bins=30, 
                    label=['Accepted', 'Rejected'][status])
        plt.xlabel('Machine Temperature (°C)')
        plt.ylabel('Frequency')
        plt.title('Temperature Distribution', fontsize=12, fontweight='bold')
        plt.legend()
        
        # 3. Operator experience vs rejection
        plt.subplot(3, 4, 3)
        exp_rejection = self.data.groupby('operator_experience_years')['rejected'].mean() * 100
        plt.plot(exp_rejection.index, exp_rejection.values, marker='o', linewidth=2, markersize=6)
        plt.xlabel('Operator Experience (years)')
        plt.ylabel('Rejection Rate (%)')
        plt.title('Experience vs Rejection Rate', fontsize=12, fontweight='bold')
        plt.grid(True, alpha=0.3)
        
        # 4. Raw material quality impact
        plt.subplot(3, 4, 4)
        plt.scatter(self.data['raw_material_quality'], self.data['rejected'], 
                   alpha=0.3, c=self.data['rejected'], cmap='RdYlGn_r')
        plt.xlabel('Raw Material Quality')
        plt.ylabel('Rejected (0=No, 1=Yes)')
        plt.title('Material Quality Impact', fontsize=12, fontweight='bold')
        
        # 5. Production speed distribution
        plt.subplot(3, 4, 5)
        violin_data = [self.data[self.data['rejected']==0]['production_speed'],
                      self.data[self.data['rejected']==1]['production_speed']]
        parts = plt.violinplot(violin_data, positions=[0, 1], showmeans=True)
        plt.xticks([0, 1], ['Accepted', 'Rejected'])
        plt.ylabel('Production Speed')
        plt.title('Speed Distribution by Status', fontsize=12, fontweight='bold')
        
        # 6. Maintenance hours impact
        plt.subplot(3, 4, 6)
        plt.hexbin(self.data['maintenance_hours'], self.data['rejected'], 
                  gridsize=20, cmap='YlOrRd', mincnt=1)
        plt.xlabel('Maintenance Hours')
        plt.ylabel('Rejected')
        plt.title('Maintenance Impact', fontsize=12, fontweight='bold')
        plt.colorbar(label='Count')
        
        # 7. Machine age analysis
        plt.subplot(3, 4, 7)
        age_groups = pd.cut(self.data['machine_age_years'], bins=[0, 5, 10, 15, 20])
        age_rejection = self.data.groupby(age_groups, observed=True)['rejected'].mean() * 100
        age_labels = [str(interval) for interval in age_rejection.index]
        plt.bar(range(len(age_rejection)), age_rejection.values, 
               color=plt.cm.Reds(np.linspace(0.3, 0.9, len(age_rejection))))
        plt.xticks(range(len(age_rejection)), age_labels, rotation=45, ha='right')
        plt.xlabel('Machine Age (years)')
        plt.ylabel('Rejection Rate (%)')
        plt.title('Machine Age Impact', fontsize=12, fontweight='bold')
        
        # 8. Humidity effect
        plt.subplot(3, 4, 8)
        humidity_bins = pd.cut(self.data['humidity_percent'], bins=10)
        humidity_rejection = self.data.groupby(humidity_bins)['rejected'].mean() * 100
        plt.plot(range(len(humidity_rejection)), humidity_rejection.values, 
                marker='s', linewidth=2, markersize=8, color='#3498db')
        plt.xlabel('Humidity Bins')
        plt.ylabel('Rejection Rate (%)')
        plt.title('Humidity Effect', fontsize=12, fontweight='bold')
        plt.grid(True, alpha=0.3)
        
        # 9. Supplier rating correlation
        plt.subplot(3, 4, 9)
        supplier_bins = pd.cut(self.data['supplier_rating'], bins=5)
        supplier_rejection = self.data.groupby(supplier_bins)['rejected'].mean() * 100
        plt.barh(range(len(supplier_rejection)), supplier_rejection.values, 
                color=plt.cm.RdYlGn(np.linspace(0.2, 0.8, len(supplier_rejection))))
        plt.yticks(range(len(supplier_rejection)), ['Poor', 'Fair', 'Good', 'Very Good', 'Excellent'])
        plt.xlabel('Rejection Rate (%)')
        plt.title('Supplier Rating Impact', fontsize=12, fontweight='bold')
        
        # 10. Defect history
        plt.subplot(3, 4, 10)
        history_rejection = self.data.groupby('defect_history_count')['rejected'].mean() * 100
        plt.scatter(history_rejection.index, history_rejection.values, 
                   s=100, alpha=0.6, c=history_rejection.values, cmap='Reds')
        plt.xlabel('Previous Defect Count')
        plt.ylabel('Rejection Rate (%)')
        plt.title('Defect History Pattern', fontsize=12, fontweight='bold')
        plt.colorbar(label='Rejection %')
        
        # 11. Correlation heatmap
        plt.subplot(3, 4, 11)
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        corr_matrix = self.data[numeric_cols].corr()
        sns.heatmap(corr_matrix, annot=False, cmap='coolwarm', center=0, 
                   square=True, linewidths=0.5)
        plt.title('Feature Correlation Matrix', fontsize=12, fontweight='bold')
        
        # 12. Overall rejection pie chart
        plt.subplot(3, 4, 12)
        rejection_counts = self.data['rejected'].value_counts()
        colors_pie = ['#2ecc71', '#e74c3c']
        plt.pie(rejection_counts.values, labels=['Accepted', 'Rejected'], 
               autopct='%1.1f%%', colors=colors_pie, startangle=90)
        plt.title('Overall Batch Status', fontsize=12, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('/mnt/user-data/outputs/rejection_analysis_visualization.png', 
                   dpi=300, bbox_inches='tight')
        print("✓ Visualizations saved: rejection_analysis_visualization.png")
        plt.close()
    
    def train_model(self):
        """Train machine learning model for rejection prediction"""
        if self.data is None:
            print("⚠ No data available. Generate data first!")
            return
        
        print("\n" + "="*70)
        print("🤖 TRAINING PREDICTIVE MODEL")
        print("="*70)
        
        # Prepare features
        feature_cols = ['machine_temperature', 'operator_experience_years', 
                       'production_speed', 'raw_material_quality', 'maintenance_hours',
                       'humidity_percent', 'machine_age_years', 'inspection_thoroughness',
                       'supplier_rating', 'defect_history_count']
        
        # Encode shift
        shift_encoded = pd.get_dummies(self.data['shift'], prefix='shift', drop_first=True)
        X = pd.concat([self.data[feature_cols], shift_encoded], axis=1)
        y = self.data['rejected']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y)
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train Random Forest
        print("\nTraining Random Forest Classifier...")
        self.model = RandomForestClassifier(
            n_estimators=200, max_depth=15, min_samples_split=10,
            min_samples_leaf=5, random_state=42, n_jobs=-1)
        self.model.fit(X_train_scaled, y_train)
        
        # Predictions
        y_pred = self.model.predict(X_test_scaled)
        y_pred_proba = self.model.predict_proba(X_test_scaled)[:, 1]
        
        # Evaluation
        print("\n📈 Model Performance:")
        print(f"   Accuracy: {self.model.score(X_test_scaled, y_test)*100:.2f}%")
        print(f"   ROC-AUC Score: {roc_auc_score(y_test, y_pred_proba):.4f}")
        
        print("\n📊 Classification Report:")
        print(classification_report(y_test, y_pred, 
                                   target_names=['Accepted', 'Rejected']))
        
        # Feature importance
        self.feature_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\n🎯 Top 10 Most Important Features:")
        for idx, row in self.feature_importance.head(10).iterrows():
            print(f"   {row['feature']:30s}: {row['importance']*100:.2f}%")
        
        # Visualize results
        self._plot_model_results(y_test, y_pred, y_pred_proba, X.columns)
        
        return self.model
    
    def _plot_model_results(self, y_test, y_pred, y_pred_proba, feature_names):
        """Plot model evaluation results"""
        fig = plt.figure(figsize=(18, 6))
        
        # 1. Confusion Matrix
        plt.subplot(1, 3, 1)
        cm = confusion_matrix(y_test, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=['Accepted', 'Rejected'],
                   yticklabels=['Accepted', 'Rejected'])
        plt.title('Confusion Matrix', fontsize=14, fontweight='bold')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        
        # 2. ROC Curve
        plt.subplot(1, 3, 2)
        fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
        auc_score = roc_auc_score(y_test, y_pred_proba)
        plt.plot(fpr, tpr, linewidth=3, label=f'ROC Curve (AUC = {auc_score:.3f})')
        plt.plot([0, 1], [0, 1], 'k--', linewidth=2, label='Random Classifier')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curve', fontsize=14, fontweight='bold')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 3. Feature Importance
        plt.subplot(1, 3, 3)
        top_features = self.feature_importance.head(10)
        colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(top_features)))
        plt.barh(range(len(top_features)), top_features['importance'].values, color=colors)
        plt.yticks(range(len(top_features)), top_features['feature'].values)
        plt.xlabel('Importance Score')
        plt.title('Top 10 Feature Importance', fontsize=14, fontweight='bold')
        plt.gca().invert_yaxis()
        
        plt.tight_layout()
        plt.savefig('/mnt/user-data/outputs/model_evaluation.png', 
                   dpi=300, bbox_inches='tight')
        print("✓ Model evaluation plots saved: model_evaluation.png")
        plt.close()
    
    def predict_rejection(self, batch_params):
        """Predict rejection probability for a new batch"""
        if self.model is None:
            print("⚠ Model not trained yet!")
            return None
        
        # Prepare input
        features = np.array([[
            batch_params['machine_temperature'],
            batch_params['operator_experience_years'],
            batch_params['production_speed'],
            batch_params['raw_material_quality'],
            batch_params['maintenance_hours'],
            batch_params['humidity_percent'],
            batch_params['machine_age_years'],
            batch_params['inspection_thoroughness'],
            batch_params['supplier_rating'],
            batch_params['defect_history_count'],
            1 if batch_params['shift'] == 'Morning' else 0,
            1 if batch_params['shift'] == 'Night' else 0
        ]])
        
        features_scaled = self.scaler.transform(features)
        prediction = self.model.predict(features_scaled)[0]
        probability = self.model.predict_proba(features_scaled)[0]
        
        return {
            'prediction': 'REJECTED' if prediction == 1 else 'ACCEPTED',
            'rejection_probability': probability[1] * 100,
            'acceptance_probability': probability[0] * 100
        }
    
    def generate_recommendations(self):
        """Generate actionable recommendations to reduce rejection rates"""
        if self.data is None or self.feature_importance is None:
            print("⚠ Train the model first!")
            return
        
        print("\n" + "="*70)
        print("💡 RECOMMENDATIONS TO REDUCE REJECTION RATES")
        print("="*70)
        
        # Analyze rejection patterns
        rejected_data = self.data[self.data['rejected'] == 1]
        accepted_data = self.data[self.data['rejected'] == 0]
        
        recommendations = []
        
        # 1. Raw material quality
        if 'raw_material_quality' in self.feature_importance['feature'].values[:5]:
            avg_rejected = rejected_data['raw_material_quality'].mean()
            avg_accepted = accepted_data['raw_material_quality'].mean()
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Raw Materials',
                'issue': f'Rejected batches have {avg_rejected:.1f}% avg quality vs {avg_accepted:.1f}% for accepted',
                'action': 'Set minimum quality threshold at 85% and audit suppliers quarterly'
            })
        
        # 2. Operator experience
        if 'operator_experience_years' in self.feature_importance['feature'].values[:5]:
            avg_exp_rejected = rejected_data['operator_experience_years'].mean()
            avg_exp_accepted = accepted_data['operator_experience_years'].mean()
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Training',
                'issue': f'Operators on rejected batches have {avg_exp_rejected:.1f} years vs {avg_exp_accepted:.1f} years',
                'action': 'Implement mentorship program pairing new operators with veterans (10+ years)'
            })
        
        # 3. Machine temperature
        temp_std_rejected = rejected_data['machine_temperature'].std()
        if temp_std_rejected > 10:
            recommendations.append({
                'priority': 'MEDIUM',
                'category': 'Equipment',
                'issue': f'Temperature variance too high (±{temp_std_rejected:.1f}°C)',
                'action': 'Install automated temperature control systems with ±2°C tolerance'
            })
        
        # 4. Maintenance
        if rejected_data['maintenance_hours'].mean() < accepted_data['maintenance_hours'].mean():
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Maintenance',
                'issue': 'Machines on rejected batches receive less maintenance',
                'action': 'Schedule preventive maintenance every 200 production hours minimum'
            })
        
        # 5. Shift analysis
        night_rejection = self.data[self.data['shift']=='Night']['rejected'].mean()
        if night_rejection > self.data['rejected'].mean() * 1.2:
            recommendations.append({
                'priority': 'MEDIUM',
                'category': 'Operations',
                'issue': f'Night shift has {night_rejection*100:.1f}% rejection rate',
                'action': 'Add quality supervisor for night shift and improve lighting'
            })
        
        # 6. Machine age
        old_machines_rejection = self.data[self.data['machine_age_years'] > 10]['rejected'].mean()
        if old_machines_rejection > self.data['rejected'].mean() * 1.3:
            recommendations.append({
                'priority': 'MEDIUM',
                'category': 'Equipment',
                'issue': f'Machines over 10 years old have {old_machines_rejection*100:.1f}% rejection rate',
                'action': 'Create 3-year equipment replacement plan for machines >12 years old'
            })
        
        # 7. Inspection thoroughness
        if rejected_data['inspection_thoroughness'].mean() < 70:
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Quality Control',
                'issue': 'Inspection thoroughness below optimal level on rejected batches',
                'action': 'Implement checklist-based inspection protocol with minimum 80% coverage'
            })
        
        # Print recommendations
        for i, rec in enumerate(recommendations, 1):
            print(f"\n{i}. [{rec['priority']}] {rec['category']}")
            print(f"   Issue: {rec['issue']}")
            print(f"   Action: {rec['action']}")
        
        # Save to file
        rec_df = pd.DataFrame(recommendations)
        rec_df.to_csv('/mnt/user-data/outputs/recommendations.csv', index=False)
        print("\n✓ Recommendations saved: recommendations.csv")
        
        return recommendations


def interactive_menu():
    """Interactive menu for the application"""
    analytics = RejectionAnalytics()
    
    print("\n" + "="*70)
    print("🏭 REJECTION RATE ANALYTICS FOR SMALL INDUSTRIES")
    print("="*70)
    print("An Interactive Data Analytics Tool to Reduce Manufacturing Defects\n")
    
    while True:
        print("\n" + "-"*70)
        print("MAIN MENU")
        print("-"*70)
        print("1. Generate Sample Manufacturing Data")
        print("2. Explore Data (Statistics & Analysis)")
        print("3. Visualize Data (Charts & Graphs)")
        print("4. Train Predictive Model")
        print("5. Predict Rejection for New Batch")
        print("6. Generate Recommendations")
        print("7. Run Complete Analysis")
        print("8. Exit")
        print("-"*70)
        
        choice = input("Enter your choice (1-8): ").strip()
        
        if choice == '1':
            n_samples = input("Enter number of samples (default 5000): ").strip()
            n_samples = int(n_samples) if n_samples else 5000
            analytics.generate_sample_data(n_samples)
            
        elif choice == '2':
            analytics.explore_data()
            
        elif choice == '3':
            analytics.visualize_data()
            
        elif choice == '4':
            analytics.train_model()
            
        elif choice == '5':
            if analytics.model is None:
                print("⚠ Please train the model first (Option 4)")
                continue
            
            print("\n📝 Enter batch parameters:")
            batch_params = {
                'machine_temperature': float(input("  Machine Temperature (°C) [65-85]: ") or 75),
                'operator_experience_years': int(input("  Operator Experience (years) [1-20]: ") or 10),
                'production_speed': float(input("  Production Speed [80-120]: ") or 100),
                'raw_material_quality': float(input("  Raw Material Quality [60-100]: ") or 85),
                'maintenance_hours': float(input("  Maintenance Hours [0-15]: ") or 5),
                'shift': input("  Shift [Morning/Afternoon/Night]: ") or 'Morning',
                'humidity_percent': float(input("  Humidity (%) [30-60]: ") or 45),
                'machine_age_years': int(input("  Machine Age (years) [1-15]: ") or 5),
                'inspection_thoroughness': float(input("  Inspection Thoroughness [50-100]: ") or 80),
                'supplier_rating': float(input("  Supplier Rating [3-10]: ") or 8),
                'defect_history_count': int(input("  Previous Defects [0-10]: ") or 2)
            }
            
            result = analytics.predict_rejection(batch_params)
            print("\n🎯 PREDICTION RESULT:")
            print(f"   Status: {result['prediction']}")
            print(f"   Rejection Probability: {result['rejection_probability']:.2f}%")
            print(f"   Acceptance Probability: {result['acceptance_probability']:.2f}%")
            
        elif choice == '6':
            analytics.generate_recommendations()
            
        elif choice == '7':
            print("\n🚀 Running complete analysis pipeline...\n")
            analytics.generate_sample_data(5000)
            analytics.explore_data()
            analytics.visualize_data()
            analytics.train_model()
            analytics.generate_recommendations()
            print("\n✅ Complete analysis finished!")
            
        elif choice == '8':
            print("\n👋 Thank you for using Rejection Rate Analytics!")
            print("💾 All results saved to /mnt/user-data/outputs/")
            break
            
        else:
            print("⚠ Invalid choice. Please enter 1-8.")


if __name__ == "__main__":
    interactive_menu()
