"""DNN model architecture for binary attrition classification."""
from tensorflow import keras
from tensorflow.keras import layers


def build_model(
    input_dim,
    hidden_units=[128, 64, 32],
    dropout_rate=0.3,
    learning_rate=1e-3,
):
    """Build a DNN with batch norm + dropout for binary classification."""
    model = keras.Sequential([keras.Input(shape=(input_dim,))])

    for units in hidden_units:
        model.add(layers.Dense(units, activation="relu"))
        model.add(layers.BatchNormalization())
        model.add(layers.Dropout(dropout_rate))

    model.add(layers.Dense(1, activation="sigmoid"))

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
        loss="binary_crossentropy",
        metrics=["accuracy", keras.metrics.AUC(name="auc")],
    )
    return model


def build_tuner_model(hp, input_dim):
    """Hypermodel for Keras Tuner."""
    n_layers = hp.Int("n_layers", 2, 4)
    hidden_units = [
        hp.Int(f"units_{i}", min_value=16, max_value=128, step=16)
        for i in range(n_layers)
    ]
    dropout_rate = hp.Float("dropout", 0.1, 0.5, step=0.1)
    learning_rate = hp.Choice("lr", [1e-2, 1e-3, 1e-4])

    return build_model(
        input_dim=input_dim,
        hidden_units=hidden_units,
        dropout_rate=dropout_rate,
        learning_rate=learning_rate,
    )
