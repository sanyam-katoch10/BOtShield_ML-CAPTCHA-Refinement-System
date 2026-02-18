"""Train a CNN classifier to predict CAPTCHA difficulty (easy / medium / hard)."""

import os

import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers, models
from tensorflow.keras.utils import to_categorical

DATA_DIR = "data_preprocessed"
CLASSES = ["easy", "medium", "hard"]
MODEL_OUTPUT = "models/captcha_model.keras"


def load_dataset(data_dir: str = DATA_DIR) -> tuple[np.ndarray, np.ndarray]:
    """Load preprocessed CAPTCHA images and their labels from disk.

    Returns:
        A tuple of (images_array, one_hot_labels).
    """
    X, y = [], []
    for idx, cls in enumerate(CLASSES):
        folder = os.path.join(data_dir, cls)
        for f in os.listdir(folder):
            X.append(np.load(os.path.join(folder, f)))
            y.append(idx)

    X = np.array(X).reshape(-1, 70, 200, 3).astype("float32")
    y = to_categorical(np.array(y), num_classes=len(CLASSES))
    return X, y


def build_model() -> models.Sequential:
    """Build and compile the CNN difficulty classifier.

    Returns:
        A compiled Keras Sequential model.
    """
    m = models.Sequential([
        layers.Input((70, 200, 3)),
        layers.Conv2D(32, (3, 3), activation="relu"),
        layers.MaxPooling2D(),
        layers.Conv2D(64, (3, 3), activation="relu"),
        layers.MaxPooling2D(),
        layers.Flatten(),
        layers.Dense(128, activation="relu"),
        layers.Dense(len(CLASSES), activation="softmax"),
    ])
    m.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
    return m


def train(epochs: int = 12, batch_size: int = 32) -> None:
    """Load data, train the model, and save the weights."""
    X, y = load_dataset()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = build_model()
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.1)

    os.makedirs("models", exist_ok=True)
    model.save(MODEL_OUTPUT)
    print(f"Model saved to {MODEL_OUTPUT}")


if __name__ == "__main__":
    train()
