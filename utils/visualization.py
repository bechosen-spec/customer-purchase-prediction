import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_confusion_matrix(cm, class_names, title="Confusion Matrix"):
    """
    Plots a confusion matrix with annotations.

    Args:
        cm (ndarray): Confusion matrix values.
        class_names (list): List of class labels.
        title (str): Title of the plot.
    """
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
    plt.title(title)
    plt.xlabel("Predicted Labels")
    plt.ylabel("True Labels")
    plt.show()

def plot_roc_curves(y_test, y_probs, class_names):
    """
    Plots ROC curves for multi-class classification.

    Args:
        y_test (ndarray): True labels, binarized for multi-class ROC.
        y_probs (ndarray): Predicted probabilities.
        class_names (list): List of class labels.
    """
    from sklearn.metrics import roc_curve, auc
    from sklearn.preprocessing import label_binarize

    y_test_binarized = label_binarize(y_test, classes=list(range(len(class_names))))
    plt.figure(figsize=(10, 8))

    for i, class_label in enumerate(class_names):
        fpr, tpr, _ = roc_curve(y_test_binarized[:, i], y_probs[:, i])
        auc_score = auc(fpr, tpr)
        plt.plot(fpr, tpr, label=f"{class_label} (AUC = {auc_score:.2f})")

    plt.plot([0, 1], [0, 1], 'k--')
    plt.title("ROC Curves")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.legend(loc="lower right")
    plt.show()

def plot_prediction_distribution(predictions, title="Prediction Distribution"):
    """
    Plots the distribution of predicted classes.

    Args:
        predictions (list or ndarray): Predicted class labels.
        title (str): Title of the plot.
    """
    plt.figure(figsize=(8, 6))
    sns.countplot(x=predictions, palette="viridis")
    plt.title(title)
    plt.xlabel("Predicted Classes")
    plt.ylabel("Count")
    plt.show()

def plot_feature_importance(feature_names, importances, title="Feature Importance"):
    """
    Plots feature importance for the trained model.

    Args:
        feature_names (list): List of feature names.
        importances (list or ndarray): Importance scores for each feature.
        title (str): Title of the plot.
    """
    feature_importance_df = pd.DataFrame({"Feature": feature_names, "Importance": importances})
    feature_importance_df = feature_importance_df.sort_values(by="Importance", ascending=False)

    plt.figure(figsize=(10, 8))
    sns.barplot(x="Importance", y="Feature", data=feature_importance_df, palette="viridis")
    plt.title(title)
    plt.xlabel("Importance")
    plt.ylabel("Feature")
    plt.show()
