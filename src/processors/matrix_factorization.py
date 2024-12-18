# noqa

import numpy as np
from typing import Tuple, List


class RecommendationsProcessor:
    """Процессор рекомендательной системы."""

    def __init__(
        self,
        data: np.ndarray,
        k: int = 5,
        steps: int = 500,
        alpha: float = 1e-4,
        reg_param: float = 0.8,
        verbose: bool = False,
    ) -> None:
        """
        Constructor of the class. Takes the user preferences matrix R
        and parameters for matrix factorization.

        Args:
            R (np.ndarray): The user-item preference matrix (users-questions).
            k (int): The number of latent factors for matrix factorization.
            steps (int): The number of iterations for ALS.
            alpha (float): The learning rate.
            reg_param (float): The regularization parameter.
        """
        self.verbose = verbose
        self.data = data
        self.k = k
        self.steps = steps
        self.alpha = alpha
        self.reg_param = reg_param

        # Perform matrix factorization during initialization
        self.P, self.Q = self.matrix_factorization()

    def initialize_matrices(self) -> Tuple[np.ndarray, np.ndarray]:
        """Initializes the matrices P and Q with random values.

        Returns:
            Tuple[np.ndarray, np.ndarray]: The initialized matrices.
        """
        num_users, num_questions = self.data.shape
        P = np.random.rand(num_users, self.k)
        Q = np.random.rand(num_questions, self.k)
        return P, Q

    def loss_function(self, P: np.ndarray, Q: np.ndarray) -> float:
        """Computes the loss (MSE) with regularization.

        Args:
            P (np.ndarray): User preference matrix.
            Q (np.ndarray): Item (question) feature matrix.

        Returns:
            float: The computed loss value.
        """
        data_hat = np.dot(P, Q.T)
        error = (self.data - data_hat) * (self.data > 0)
        mse = np.sum(np.square(error))
        reg_term = self.reg_param * (
            np.linalg.norm(P) ** 2 + np.linalg.norm(Q) ** 2
        )
        return mse + reg_term

    def matrix_factorization(self) -> Tuple[np.ndarray, np.ndarray]:
        """Performs matrix factorization using Alternating Least Squares (ALS).

        Returns:
            Tuple[np.ndarray, np.ndarray]: The factorized matrices P and Q.
        """
        num_users, num_questions = self.data.shape
        P, Q = self.initialize_matrices()

        mask = self.data > 0
        prev_loss = float("inf")

        for step in range(self.steps):
            R_hat = np.dot(P, Q.T)
            error_matrix = (self.data - R_hat) * mask

            P_grad = -2 * np.dot(error_matrix, Q) + self.reg_param * P
            Q_grad = -2 * np.dot(error_matrix.T, P) + self.reg_param * Q

            P -= self.alpha * P_grad
            Q -= self.alpha * Q_grad

            loss = self.loss_function(P, Q)

            if self.verbose and step % 100 == 0:
                print(f"Step {step}/{self.steps}, loss: {loss:.4f}")

            # assertion for coveraging
            if abs(prev_loss - loss) < 1e-5:
                if self.verbose:
                    print(f"Converged at step {step}, loss: {loss:.4f}")
                break
            prev_loss = loss

        return P, Q

    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculates cosine similarity between two vectors.

        Args:
            vec1 (np.ndarray): The first vector.
            vec2 (np.ndarray): The second vector.

        Returns:
            float: The cosine similarity between the two vectors.
        """
        dot_product = np.dot(vec1, vec2)
        norm_vec1 = np.linalg.norm(vec1)
        norm_vec2 = np.linalg.norm(vec2)
        return (
            0.0
            if norm_vec1 == 0 or norm_vec2 == 0
            else dot_product / (norm_vec1 * norm_vec2)
        )

    def predict(self, user_id: int, top_n: int = 3) -> List[Tuple[int, float]]:
        """
        Recommends top-N users similar to the given user.
        """
        user_vector = self.P[user_id]
        similarities: List[Tuple[int, float]] = [
            (
                other_user_id,
                self.cosine_similarity(user_vector, self.P[other_user_id]),
            )
            for other_user_id in range(self.P.shape[0])
            if other_user_id != user_id
        ]

        similarities.sort(key=lambda x: x[1], reverse=True)
        top_similar_users = similarities[:top_n]

        if self.verbose:
            print(f"Top-{top_n} recommended users for User {user_id + 1}:")
            for idx, (user, similarity) in enumerate(top_similar_users):
                print(
                    f"{idx + 1}: User {user + 1}"
                    f"(Similarity: {similarity:.4f})"
                )

        return top_similar_users
