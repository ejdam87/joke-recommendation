import numpy as np
import pandas as pd

def funk_svd(R, train_mask, valid_mask, num_factors=20, num_epochs=50, lr=0.0001, reg=0.02):
    """
    R: rating matrix (users x items) with np.nan for missing ratings
    num_factors: number of latent factors
    """
    num_users, num_items = R.shape
    losses = [np.inf, np.inf]
    U = np.random.normal(scale=0.1, size=(num_users, num_factors))
    V = np.random.normal(scale=0.1, size=(num_items, num_factors))

    user_item_pairs = np.argwhere(~np.isnan(R))

    for epoch in range(num_epochs):
        np.random.shuffle(user_item_pairs)
        for user, item in user_item_pairs:
            r_ui = R[user, item]
            pred = np.dot(U[user], V[item])
            err = r_ui - pred

            U[user] += lr * (err * V[item] - reg * U[user])
            V[item] += lr * (err * U[user] - reg * V[item])
        
        pred_matrix = np.dot(U, V.T)
        train_loss = np.nanmean((R[train_mask] - pred_matrix[train_mask])**2)
        val_loss = np.nanmean((R[valid_mask] - pred_matrix[valid_mask])**2)
        print(f"Epoch {epoch+1}/{num_epochs} - Train loss: {train_loss:.4f} - Val loss: {val_loss:.4f}")

        if val_loss > losses[-1] and val_loss > losses[-2]:
            print(f"Trained for {epoch + 1} epochs")
            return U, V
        
        losses.append(val_loss)
    
    return U, V


if __name__ == "__main__":

    # Training configuration sample
    ratings_df = pd.read_csv("../data/rating_matrix_clean_uidless.csv")
    R = ratings_df.to_numpy()

    observed = ~np.isnan(R)
    num_obs = np.sum(observed)
    val_fraction = 0.2

    val_indices = np.random.choice(np.where(observed.ravel())[0],
                                size=int(val_fraction * num_obs),
                                replace=False)

    train_mask = observed.copy().ravel()
    train_mask[val_indices] = False
    train_mask = train_mask.reshape(R.shape)

    val_mask = observed & ~train_mask

    print(R.shape)

    for k in [100]:
        U, V = funk_svd(R, train_mask, val_mask, num_factors=k, num_epochs=1)
        np.savetxt(f"../data/U_{k}.csv", U, delimiter=",")
        np.savetxt(f"../data/V_{k}.csv", V, delimiter=",")
        preds = np.dot(U, V.T)
        error = np.nanmean((R[~np.isnan(R)] - preds[~np.isnan(R)])**2)
        print(f"num_factors={k}, RMSE={np.sqrt(error):.4f}")
