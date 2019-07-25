
URL = "https://archive.scryfall.com/json/scryfall-oracle-cards.json"

# 7  = CMC
# 9  = color identity
# 10 = color indicator
# 11 = colors
# 29 = loyalty
# 30 = mana cost
# 38 = oracle text
# 40 = power
# 44 = rarity
# 46 = released at
# 55 = toughness
# 56 = type line


TARGET_COLUMN = 7

from pandas import read_json
import numpy as np
import matplotlib.pyplot as plt

try:
    # [OPTIONAL] Seaborn makes plots nicer
    import seaborn
except ImportError:
    pass



def download_data():

    frame = read_json(
        URL,
        orient='columns',
        dtype='dict'
        )

    #return frame[['color_identity', 'color_indicator', 'colors', 'loyalty', 'mana_cost', 'oracle_text', 'power', 'rarity', 'released_at', 'toughness', 'type_line', 'cmc']]
    return frame[['power', 'toughness', 'cmc','set_type']]


def get_features_and_labels(frame):
    subframe=frame[~frame['power'].isin(['*', '*+1', '1+*', '2+*', '∞', '?', '*²', float('nan')]) & ~frame['toughness'].isin(['*', '*+1', '1+*', '2+*', '∞', '?', '*²', float('nan')])]
    
    arr = np.array(subframe[['power','toughness','cmc']], dtype=np.float)

    from sklearn.preprocessing import StandardScaler, MinMaxScaler
    arr = MinMaxScaler().fit_transform(arr)

    X, y = arr[:, :-1], arr[:, -1]

    from sklearn.model_selection import train_test_split
    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.5)
    X_test, y_test = X, y

    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()

    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    return X_train, X_test, y_train, y_test



def evaluate_learner(X_train, X_test, y_train, y_test):

    # Use a support vector machine for regression
    from sklearn.svm import SVR

    # Train using a radial basis function
    svr = SVR(kernel='rbf', gamma=0.1)
    svr.fit(X_train, y_train)
    y_pred = svr.predict(X_test)
    r_2 = svr.score(X_test, y_test)
    yield 'RBF Model ($R^2={:.3f}$)'.format(r_2), y_test, y_pred

    # Train using a linear kernel
    svr = SVR(kernel='linear')
    svr.fit(X_train, y_train)
    y_pred = svr.predict(X_test)
    r_2 = svr.score(X_test, y_test)
    yield 'Linear Model ($R^2={:.3f}$)'.format(r_2), y_test, y_pred

    # Train using a polynomial kernel
    svr = SVR(kernel='poly', degree=2)
    svr.fit(X_train, y_train)
    y_pred = svr.predict(X_test)
    r_2 = svr.score(X_test, y_test)
    yield 'Polynomial Model ($R^2={:.3f}$)'.format(r_2), y_test, y_pred



def plot(results):

    fig, plts = plt.subplots(nrows=len(results), figsize=(8, 8))
    fig.canvas.set_window_title('Predicting data from ' + URL)

    for subplot, (title, y, y_pred) in zip(plts, results):

        subplot.set_xticklabels(())
        subplot.set_yticklabels(())

        subplot.set_ylabel('converted mana cost')

        subplot.set_title(title)

        subplot.plot(y, 'b', label='actual')
        subplot.plot(y_pred, 'r', label='predicted')

        subplot.fill_between(
            # Generate X values [0, 1, 2, ..., len(y)-2, len(y)-1]
            np.arange(0, len(y), 1),
            y,
            y_pred,
            color='r',
            alpha=0.2
        )

        subplot.axvline(len(y) // 2, linestyle='--', color='0', alpha=0.2)

        subplot.legend()

    fig.tight_layout()

    plt.show()

    plt.close()



if __name__ == '__main__':
    # Download the data set from URL
    print("Downloading data from {}".format(URL))
    frame = download_data()

    # Process data into feature and label arrays
    print("Processing {} samples with {} attributes".format(len(frame.index), len(frame.columns)))
    X_train, X_test, y_train, y_test = get_features_and_labels(frame)

    # Evaluate multiple regression learners on the data
    print("Evaluating regression learners")
    results = list(evaluate_learner(X_train, X_test, y_train, y_test))

    # Display the results
    print("Plotting the results")
    plot(results)