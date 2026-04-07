# Titanic Survival Prediction - End to End ML Project
# Author: Complete ML Pipeline for CampusX Assignment

# ============================================
# 1. IMPORT LIBRARIES
# ============================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)

print("=" * 60)
print("TITANIC SURVIVAL PREDICTION - ML PROJECT")
print("=" * 60)

# ============================================
# 2. LOAD DATASET
# ============================================
print("\n[STEP 1] Loading Dataset...")
# Method 1: Using seaborn (easiest)
df = sns.load_dataset('titanic')

# If seaborn doesn't work, use this:
# df = pd.read_csv('train.csv')

print(f"✓ Dataset loaded successfully!")
print(f"  Shape: {df.shape}")
print(f"  Rows: {df.shape[0]}, Columns: {df.shape[1]}")

# ============================================
# 3. EXPLORATORY DATA ANALYSIS (EDA)
# ============================================
print("\n[STEP 2] Exploratory Data Analysis...")

# Basic info
print("\n--- Dataset Info ---")
print(df.info())

print("\n--- First 5 Rows ---")
print(df.head())

print("\n--- Statistical Summary ---")
print(df.describe())

print("\n--- Missing Values ---")
missing = df.isnull().sum()
missing_pct = (missing / len(df)) * 100
missing_df = pd.DataFrame({'Missing': missing, 'Percentage': missing_pct})
print(missing_df[missing_df['Missing'] > 0].sort_values('Missing', ascending=False))

print("\n--- Survival Rate ---")
survival_rate = df['survived'].value_counts(normalize=True) * 100
print(f"Survived: {survival_rate[1]:.2f}%")
print(f"Not Survived: {survival_rate[0]:.2f}%")

# ============================================
# 4. DATA VISUALIZATION
# ============================================
print("\n[STEP 3] Creating Visualizations...")

# Create subplots
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('Titanic Dataset - Exploratory Data Analysis', fontsize=16, fontweight='bold')

# Plot 1: Survival Count
sns.countplot(data=df, x='survived', ax=axes[0, 0], palette='Set2')
axes[0, 0].set_title('Survival Count')
axes[0, 0].set_xlabel('Survived (0=No, 1=Yes)')

# Plot 2: Survival by Gender
sns.countplot(data=df, x='sex', hue='survived', ax=axes[0, 1], palette='Set1')
axes[0, 1].set_title('Survival by Gender')
axes[0, 1].legend(title='Survived', labels=['No', 'Yes'])

# Plot 3: Survival by Pclass
sns.countplot(data=df, x='pclass', hue='survived', ax=axes[0, 2], palette='viridis')
axes[0, 2].set_title('Survival by Passenger Class')
axes[0, 2].legend(title='Survived', labels=['No', 'Yes'])

# Plot 4: Age Distribution
df['age'].hist(bins=30, ax=axes[1, 0], color='skyblue', edgecolor='black')
axes[1, 0].set_title('Age Distribution')
axes[1, 0].set_xlabel('Age')

# Plot 5: Fare Distribution
df['fare'].hist(bins=30, ax=axes[1, 1], color='lightcoral', edgecolor='black')
axes[1, 1].set_title('Fare Distribution')
axes[1, 1].set_xlabel('Fare')

# Plot 6: Correlation Heatmap
numeric_cols = df.select_dtypes(include=[np.number]).columns
corr_matrix = df[numeric_cols].corr()
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', ax=axes[1, 2], cbar_kws={'shrink': 0.8})
axes[1, 2].set_title('Correlation Heatmap')

plt.tight_layout()
plt.savefig('titanic_eda.png', dpi=300, bbox_inches='tight')
print("✓ Visualizations saved as 'titanic_eda.png'")
plt.show()

# ============================================
# 5. DATA CLEANING & PREPROCESSING
# ============================================
print("\n[STEP 4] Data Cleaning & Preprocessing...")

# Create a copy for processing
data = df.copy()

# Handle missing values
print("\n--- Handling Missing Values ---")

# Age: Fill with median
data['age'].fillna(data['age'].median(), inplace=True)
print(f"✓ Age: Filled {df['age'].isnull().sum()} missing values with median")

# Embarked: Fill with mode
if 'embarked' in data.columns:
    data['embarked'].fillna(data['embarked'].mode()[0], inplace=True)
    print(f"✓ Embarked: Filled missing values with mode")

# Deck: Too many missing values, drop it
if 'deck' in data.columns:
    data.drop('deck', axis=1, inplace=True)
    print("✓ Deck: Dropped (too many missing values)")

# Drop rows with remaining missing values in critical columns
data.dropna(subset=['survived', 'pclass', 'sex'], inplace=True)

# Feature Engineering
print("\n--- Feature Engineering ---")

# Family Size
data['family_size'] = data['sibsp'] + data['parch'] + 1
print("✓ Created 'family_size' feature")

# Is Alone
data['is_alone'] = (data['family_size'] == 1).astype(int)
print("✓ Created 'is_alone' feature")

# Age Group
data['age_group'] = pd.cut(data['age'], bins=[0, 12, 18, 35, 60, 100], 
                            labels=['Child', 'Teen', 'Adult', 'Middle', 'Senior'])
print("✓ Created 'age_group' feature")

# Fare Group
data['fare_group'] = pd.qcut(data['fare'], q=4, labels=['Low', 'Medium', 'High', 'Very High'])
print("✓ Created 'fare_group' feature")

# ============================================
# 6. FEATURE SELECTION & ENCODING
# ============================================
print("\n[STEP 5] Feature Selection & Encoding...")

# Select features for modeling
features_to_use = ['pclass', 'sex', 'age', 'sibsp', 'parch', 'fare', 
                   'family_size', 'is_alone']

# Add embarked if available
if 'embarked' in data.columns:
    features_to_use.append('embarked')

# Create feature dataframe
X = data[features_to_use].copy()
y = data['survived']

print(f"\n✓ Selected {len(features_to_use)} features:")
print(f"  {features_to_use}")

# Encode categorical variables
le_sex = LabelEncoder()
X['sex'] = le_sex.fit_transform(X['sex'])

if 'embarked' in X.columns:
    le_embarked = LabelEncoder()
    X['embarked'] = le_embarked.fit_transform(X['embarked'].astype(str))

print("\n✓ Encoded categorical variables")

# Handle any remaining missing values
X = X.fillna(X.median())

# ============================================
# 7. TRAIN-TEST SPLIT
# ============================================
print("\n[STEP 6] Splitting Data...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, 
                                                      random_state=42, stratify=y)
print(f"✓ Train set: {X_train.shape[0]} samples")
print(f"✓ Test set: {X_test.shape[0]} samples")

# Feature Scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print("✓ Features scaled using StandardScaler")

# ============================================
# 8. MODEL TRAINING & EVALUATION
# ============================================
print("\n[STEP 7] Training Multiple ML Models...")
print("=" * 60)

models = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Decision Tree': DecisionTreeClassifier(random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
    'SVM': SVC(kernel='rbf', random_state=42)
}

results = {}

for name, model in models.items():
    print(f"\n--- Training {name} ---")
    
    # Train model
    if name == 'SVM':
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
    else:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
    
    # Calculate accuracy
    train_score = model.score(X_train_scaled if name == 'SVM' else X_train, y_train)
    test_score = accuracy_score(y_test, y_pred)
    
    # Cross-validation
    cv_scores = cross_val_score(model, X_train_scaled if name == 'SVM' else X_train, 
                                y_train, cv=5, scoring='accuracy')
    
    results[name] = {
        'Train Score': train_score,
        'Test Score': test_score,
        'CV Mean': cv_scores.mean(),
        'CV Std': cv_scores.std(),
        'Model': model,
        'Predictions': y_pred
    }
    
    print(f"  Training Accuracy: {train_score:.4f}")
    print(f"  Testing Accuracy: {test_score:.4f}")
    print(f"  CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

# ============================================
# 9. RESULTS COMPARISON
# ============================================
print("\n" + "=" * 60)
print("[STEP 8] MODEL COMPARISON")
print("=" * 60)

results_df = pd.DataFrame({
    'Model': results.keys(),
    'Train Score': [results[m]['Train Score'] for m in results],
    'Test Score': [results[m]['Test Score'] for m in results],
    'CV Mean': [results[m]['CV Mean'] for m in results],
    'CV Std': [results[m]['CV Std'] for m in results]
})

results_df = results_df.sort_values('Test Score', ascending=False)
print("\n", results_df.to_string(index=False))

# Best model
best_model_name = results_df.iloc[0]['Model']
best_model = results[best_model_name]['Model']
best_predictions = results[best_model_name]['Predictions']

print(f"\n🏆 BEST MODEL: {best_model_name}")
print(f"   Test Accuracy: {results_df.iloc[0]['Test Score']:.4f}")

# ============================================
# 10. DETAILED EVALUATION OF BEST MODEL
# ============================================
print("\n[STEP 9] Detailed Evaluation of Best Model")
print("=" * 60)

print("\n--- Classification Report ---")
print(classification_report(y_test, best_predictions, 
                          target_names=['Not Survived', 'Survived']))

print("\n--- Confusion Matrix ---")
cm = confusion_matrix(y_test, best_predictions)
print(cm)

# Visualize confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False,
            xticklabels=['Not Survived', 'Survived'],
            yticklabels=['Not Survived', 'Survived'])
plt.title(f'Confusion Matrix - {best_model_name}')
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
print("\n✓ Confusion matrix saved as 'confusion_matrix.png'")
plt.show()

# Feature Importance (if available)
if hasattr(best_model, 'feature_importances_'):
    print("\n--- Feature Importance ---")
    feature_imp = pd.DataFrame({
        'Feature': features_to_use,
        'Importance': best_model.feature_importances_
    }).sort_values('Importance', ascending=False)
    print(feature_imp.to_string(index=False))
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=feature_imp, x='Importance', y='Feature', palette='viridis')
    plt.title(f'Feature Importance - {best_model_name}')
    plt.tight_layout()
    plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
    print("\n✓ Feature importance plot saved as 'feature_importance.png'")
    plt.show()

# ============================================
# 11. FINAL SUMMARY
# ============================================
print("\n" + "=" * 60)
print("PROJECT COMPLETED SUCCESSFULLY! 🎉")
print("=" * 60)
print(f"\n📊 Dataset: {df.shape[0]} passengers analyzed")
print(f"🎯 Best Model: {best_model_name}")
print(f"✅ Test Accuracy: {results_df.iloc[0]['Test Score']:.2%}")
print(f"\n📁 Output Files Generated:")
print("   1. titanic_eda.png")
print("   2. confusion_matrix.png")
if hasattr(best_model, 'feature_importances_'):
    print("   3. feature_importance.png")
print("\n" + "=" * 60)