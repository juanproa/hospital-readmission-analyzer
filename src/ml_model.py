import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def prepare_data(df):
    """Prepare data for machine learning"""
    
    # Going with these features for the model based on analysis
    features = ['age', 'chronic_conditions', 'length_of_stay', 
                'num_medications', 'num_procedures']
    
    X = df[features]
    y = df['readmitted_within_30_days'] #Target Column, 0 = readmitted and 1 = admitted
    
    print(f"Features: {features}")
    print(f"Total samples: {len(X)}")
    print(f"Readmitted: {y.sum()} ({y.mean()*100:.1f}%)")
    
    return X, y


def train_model(X, y):
    """Train a Random Forest model"""
    
    # Let's do a split here: 80% training, 20% testing
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"\nTraining set: {len(X_train)} samples")
    print(f"Testing set: {len(X_test)} samples")
    
    # Train Random Forest
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    print("\n✓ Model trained!")
    
    return model, X_train, X_test, y_train, y_test


def evaluate_model(model, X_test, y_test):
    """Evaluate model performance"""
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    
    print("\n" + "="*60)
    print("MODEL EVALUATION")
    print("="*60)
    print(f"\nAccuracy: {accuracy*100:.2f}%")

    
    return accuracy


def show_feature_importance(model, feature_names):
    """Show which features are most important"""
    
    importances = model.feature_importances_
    feature_importance = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances
    }).sort_values('Importance', ascending=False)
    
    print("\n" + "="*60)
    print("FEATURE IMPORTANCE")
    print("="*60)
    print("\n" + feature_importance.to_string(index=False))
    
    return feature_importance


if __name__ == "__main__":
    print("Building Machine Learning Model...")
    print("="*60)
    
    # Load data
    df = pd.read_csv('data/analysis_dataset.csv')
    
    # Prepare data
    X, y = prepare_data(df)
    
    # Train model
    model, X_train, X_test, y_train, y_test = train_model(X, y)
    
    # Evaluate
    accuracy = evaluate_model(model, X_test, y_test)
    
    # Feature importance
    feature_importance = show_feature_importance(model, X.columns)
    
    print("\n" + "="*60)
    print("✓ Model complete!")
    print(f"✓ Achieved {accuracy*100:.1f}% accuracy")